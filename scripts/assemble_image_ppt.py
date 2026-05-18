#!/usr/bin/env python3
"""Assemble generated slide images into a PPTX.

This script is intentionally mechanical. It does not design, render, or edit
slide content; each input image must already be a finished generated slide.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import zipfile
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path


SLIDE_SIZES = {
    "16:9": (12192000, 6858000),
    "4:3": (9144000, 6858000),
}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
PPT_IMAGE_CONTENT_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Assemble generated full-slide images into a PPTX."
    )
    parser.add_argument(
        "--workdir",
        required=True,
        type=Path,
        help="Run folder containing images/, outline.md, and final outputs.",
    )
    parser.add_argument(
        "--title",
        required=True,
        help="Base filename for the output PPTX.",
    )
    parser.add_argument(
        "--expected-pages",
        type=int,
        help="Fail if the number of images does not match this value.",
    )
    parser.add_argument(
        "--ratio",
        choices=("16:9", "4:3"),
        default="16:9",
        help="PowerPoint slide ratio. Defaults to 16:9.",
    )
    parser.add_argument(
        "--images-dir",
        default="images",
        help="Image subfolder name inside workdir. Defaults to images.",
    )
    return parser.parse_args()


def safe_filename(name: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*]', "-", name)
    cleaned = "".join("-" if ord(ch) < 32 else ch for ch in cleaned)
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip(" .-")
    return cleaned or "slides"


def sorted_images(images_dir: Path) -> list[Path]:
    if not images_dir.exists():
        raise FileNotFoundError(f"Missing image directory: {images_dir}")

    images = [
        path
        for path in images_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    ]
    return sorted(images, key=lambda path: path.name.lower())


def assert_pillow() -> object:
    try:
        from PIL import Image
    except ImportError as exc:
        raise SystemExit(
            "Missing dependency: Pillow. Install Pillow before running this "
            "mechanical assembly script."
        ) from exc

    return Image


def validate_images(Image: object, images: list[Path], ratio: str) -> None:
    target_ratio = 16 / 9 if ratio == "16:9" else 4 / 3
    tolerance = 0.08

    for image_path in images:
        with Image.open(image_path) as img:
            width, height = img.size
        if width <= 0 or height <= 0:
            raise ValueError(f"Invalid image dimensions: {image_path}")
        actual_ratio = width / height
        if abs(actual_ratio - target_ratio) > tolerance:
            print(
                "warning: image ratio differs from requested "
                f"{ratio}: {image_path.name} ({width}x{height})",
                file=sys.stderr,
            )


def image_payload(Image: object, image_path: Path) -> tuple[str, str, bytes]:
    suffix = image_path.suffix.lower()
    if suffix in PPT_IMAGE_CONTENT_TYPES:
        return suffix, PPT_IMAGE_CONTENT_TYPES[suffix], image_path.read_bytes()

    with Image.open(image_path) as img:
        img = img.convert("RGB")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
    return ".png", "image/png", buffer.getvalue()


def xml_escape(value: str) -> str:
    return html.escape(value, quote=True)


def content_types_xml(slide_count: int, media_types: list[tuple[str, str]]) -> str:
    defaults = {
        "rels": "application/vnd.openxmlformats-package.relationships+xml",
        "xml": "application/xml",
    }
    for suffix, content_type in media_types:
        defaults[suffix.lstrip(".")] = content_type

    default_xml = "\n".join(
        f'  <Default Extension="{ext}" ContentType="{ctype}"/>'
        for ext, ctype in sorted(defaults.items())
    )
    slide_overrides = "\n".join(
        "  <Override "
        f'PartName="/ppt/slides/slide{idx}.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for idx in range(1, slide_count + 1)
    )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
{default_xml}
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
{slide_overrides}
</Types>
'''


def package_rels_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
'''


def core_xml(title: str) -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    safe_title = xml_escape(title)
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>{safe_title}</dc:title>
  <dc:creator>Codex codex-ppt</dc:creator>
  <cp:lastModifiedBy>Codex codex-ppt</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>
'''


def app_xml(slide_count: int) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex codex-ppt</Application>
  <PresentationFormat>On-screen Show</PresentationFormat>
  <Slides>{slide_count}</Slides>
</Properties>
'''


def presentation_xml(slide_count: int, ratio: str) -> str:
    cx, cy = SLIDE_SIZES[ratio]
    slide_ids = "\n".join(
        f'    <p:sldId id="{255 + idx}" r:id="rId{idx + 1}"/>'
        for idx in range(1, slide_count + 1)
    )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst>
    <p:sldMasterId id="2147483648" r:id="rId1"/>
  </p:sldMasterIdLst>
  <p:sldIdLst>
{slide_ids}
  </p:sldIdLst>
  <p:sldSz cx="{cx}" cy="{cy}" type="screen{ratio.replace(':', 'x')}"/>
  <p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>
'''


def presentation_rels_xml(slide_count: int) -> str:
    rels = [
        '  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>'
    ]
    for idx in range(1, slide_count + 1):
        rels.append(
            f'  <Relationship Id="rId{idx + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{idx}.xml"/>'
        )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
{chr(10).join(rels)}
</Relationships>
'''


def slide_master_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr/>
    </p:spTree>
  </p:cSld>
  <p:clrMap accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" bg1="lt1" bg2="lt2" folHlink="folHlink" hlink="hlink" tx1="dk1" tx2="dk2"/>
  <p:sldLayoutIdLst>
    <p:sldLayoutId id="2147483649" r:id="rId1"/>
  </p:sldLayoutIdLst>
  <p:txStyles/>
</p:sldMaster>
'''


def slide_master_rels_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
</Relationships>
'''


def slide_layout_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1">
  <p:cSld name="Blank">
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr/>
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>
'''


def slide_layout_rels_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>
'''


def theme_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Codex Theme">
  <a:themeElements>
    <a:clrScheme name="Codex">
      <a:dk1><a:sysClr val="windowText" lastClr="000000"/></a:dk1>
      <a:lt1><a:sysClr val="window" lastClr="FFFFFF"/></a:lt1>
      <a:dk2><a:srgbClr val="1F1F1F"/></a:dk2>
      <a:lt2><a:srgbClr val="F7F7F7"/></a:lt2>
      <a:accent1><a:srgbClr val="4472C4"/></a:accent1>
      <a:accent2><a:srgbClr val="ED7D31"/></a:accent2>
      <a:accent3><a:srgbClr val="A5A5A5"/></a:accent3>
      <a:accent4><a:srgbClr val="FFC000"/></a:accent4>
      <a:accent5><a:srgbClr val="5B9BD5"/></a:accent5>
      <a:accent6><a:srgbClr val="70AD47"/></a:accent6>
      <a:hlink><a:srgbClr val="0563C1"/></a:hlink>
      <a:folHlink><a:srgbClr val="954F72"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="Codex"><a:majorFont/><a:minorFont/></a:fontScheme>
    <a:fmtScheme name="Codex"><a:fillStyleLst/><a:lnStyleLst/><a:effectStyleLst/><a:bgFillStyleLst/></a:fmtScheme>
  </a:themeElements>
</a:theme>
'''


def slide_xml(idx: int, ratio: str) -> str:
    cx, cy = SLIDE_SIZES[ratio]
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr/>
      <p:pic>
        <p:nvPicPr>
          <p:cNvPr id="{idx + 1}" name="Slide image {idx}"/>
          <p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr>
          <p:nvPr/>
        </p:nvPicPr>
        <p:blipFill>
          <a:blip r:embed="rId1"/>
          <a:stretch><a:fillRect/></a:stretch>
        </p:blipFill>
        <p:spPr>
          <a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
        </p:spPr>
      </p:pic>
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>
'''


def slide_rels_xml(media_name: str) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/{media_name}"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>
'''


def write_pptx(
    Image: object,
    images: list[Path],
    output_pptx: Path,
    title: str,
    ratio: str,
) -> None:
    media = []
    media_types = []
    for idx, image_path in enumerate(images, start=1):
        suffix, content_type, payload = image_payload(Image, image_path)
        media_name = f"image{idx}{'.jpg' if suffix == '.jpeg' else suffix}"
        media.append((media_name, payload))
        media_types.append((Path(media_name).suffix.lower(), content_type))

    with zipfile.ZipFile(output_pptx, "w", compression=zipfile.ZIP_DEFLATED) as pptx:
        pptx.writestr("[Content_Types].xml", content_types_xml(len(images), media_types))
        pptx.writestr("_rels/.rels", package_rels_xml())
        pptx.writestr("docProps/core.xml", core_xml(title))
        pptx.writestr("docProps/app.xml", app_xml(len(images)))
        pptx.writestr("ppt/presentation.xml", presentation_xml(len(images), ratio))
        pptx.writestr("ppt/_rels/presentation.xml.rels", presentation_rels_xml(len(images)))
        pptx.writestr("ppt/slideMasters/slideMaster1.xml", slide_master_xml())
        pptx.writestr(
            "ppt/slideMasters/_rels/slideMaster1.xml.rels", slide_master_rels_xml()
        )
        pptx.writestr("ppt/slideLayouts/slideLayout1.xml", slide_layout_xml())
        pptx.writestr(
            "ppt/slideLayouts/_rels/slideLayout1.xml.rels", slide_layout_rels_xml()
        )
        pptx.writestr("ppt/theme/theme1.xml", theme_xml())

        for idx, (media_name, payload) in enumerate(media, start=1):
            pptx.writestr(f"ppt/media/{media_name}", payload)
            pptx.writestr(f"ppt/slides/slide{idx}.xml", slide_xml(idx, ratio))
            pptx.writestr(
                f"ppt/slides/_rels/slide{idx}.xml.rels", slide_rels_xml(media_name)
            )


def main() -> int:
    args = parse_args()
    workdir = args.workdir.expanduser().resolve()
    images_dir = workdir / args.images_dir
    output_pptx = workdir / f"{safe_filename(args.title)}.pptx"

    Image = assert_pillow()

    images = sorted_images(images_dir)
    if not images:
        raise SystemExit(f"No slide images found in {images_dir}")
    if args.expected_pages is not None and len(images) != args.expected_pages:
        raise SystemExit(
            f"Expected {args.expected_pages} images, found {len(images)} in {images_dir}"
        )

    validate_images(Image, images, args.ratio)
    write_pptx(Image, images, output_pptx, args.title, args.ratio)

    print(f"pptx={output_pptx}")
    print(f"pages={len(images)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
