# codex-ppt

Codex skill for making image-first PowerPoint decks.

`codex-ppt` turns each slide into a full-page image generated with Codex's built-in `image_gen` tool, then mechanically assembles those images into a `.pptx`. The design stays in the generated slide images; the PowerPoint file is only a delivery container.

## What It Does

- Creates a dedicated work folder for each deck.
- Keeps `outline.md` as the single source of truth.
- Generates a `style-preview.png` before full production.
- Generates each final slide as `images/01.png`, `images/02.png`, and so on.
- Assembles the slide images into a PowerPoint file with `scripts/assemble_image_ppt.py`.
- Supports single-slide redo by archiving the old slide image and regenerating the selected page.

## Requirements

- Codex environment with the built-in `image_gen` tool available.
- Python 3.
- Pillow for the assembly script:

```bash
pip install Pillow
```

## Install

Copy this folder into your Codex skills directory:

```bash
cp -R codex-ppt "$CODEX_HOME/skills/codex-ppt"
```

Then restart Codex or reload skills if your environment supports skill reload.

## Usage

Ask Codex to use `codex-ppt` when you want to make a PPT:

```text
调用 codex-ppt skill，帮我基于这个 outline 做一份 10 页 PPT
```

The skill will guide the process:

1. Confirm deck metadata.
2. Generate a style preview.
3. Write and confirm `outline.md`.
4. Generate slides one page at a time.
5. Assemble the final `.pptx`.

## Assemble Existing Slide Images

If you already have finished slide images in `images/`, run:

```bash
python3 scripts/assemble_image_ppt.py \
  --workdir /absolute/path/to/workdir \
  --title "Deck Title" \
  --expected-pages 10 \
  --ratio 16:9
```

The script inserts one full-slide image per PowerPoint page. It does not design, render, or edit slide content.

## License

MIT
