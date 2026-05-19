# codex-ppt · Image-first PowerPoint Decks

![GitHub stars](https://img.shields.io/github/stars/Scott-Du/codex-ppt?style=flat-square)
![License](https://img.shields.io/github/license/Scott-Du/codex-ppt?style=flat-square)
![Skill](https://img.shields.io/badge/Skill-Codex-111111?style=flat-square)
![PPTX](https://img.shields.io/badge/Output-PPTX-D24726?style=flat-square)
![Image First](https://img.shields.io/badge/Image--First-Slides-0A7CFF?style=flat-square)

> 中文版: [README.md](./README.md) · If you are an AI Agent, read: [README.agent.md](./README.agent.md)

`codex-ppt` is a Codex skill for creating image-first PowerPoint decks. Codex generates each slide as a full-page image with the built-in `image_gen`, then mechanically assembles those images into a `.pptx`.

The key tradeoff is simple: **the design lives in images; PowerPoint is the delivery container**. This works well for polished delivery decks, not for decks that require long-term editing of every text box, shape, and animation.

## Quick Start

If you are a human, ask Codex directly:

```text
Install codex-ppt for me. Install it from https://github.com/Scott-Du/codex-ppt into my Codex skills directory, then verify that SKILL.md and scripts/assemble_image_ppt.py exist.
```

If it is already installed:

```text
Update codex-ppt for me. Go to the codex-ppt skill directory, run git pull, and tell me the latest commit.
```

Then trigger it with:

```text
Use codex-ppt to create a 10-slide image-first deck from this outline.
Turn this project application material into an 8-slide pitch deck with codex-ppt.
Redo slide 04, archive the old image, keep the new image named 04.png, then reassemble the PPTX.
```

If you are an AI Agent, read: [README.agent.md](./README.agent.md).

## When To Use It

Use it for:

- Pitch decks, project application decks, demo day decks
- Product stories, startup narratives, visual presentations
- Decks where visual quality and style consistency matter more than editable PowerPoint objects

Avoid it for:

- Dense table-heavy documents or text-heavy training decks
- Decks that require native editable text boxes, shapes, and animations

## Workflow

1. Confirm title, slide count, audience, scenario, aspect ratio, and output format.
2. Generate `style-preview.png` to lock the visual direction.
3. Write `outline.md` as the single source of truth.
4. Generate slide images one by one as `images/01.png`, `images/02.png`, and so on.
5. Assemble the images into a `.pptx` with `scripts/assemble_image_ppt.py`.
6. For a single-slide redo, archive the old image under `images/archive/`, regenerate the same page number, then reassemble.

During outline writing, the skill favors outward-facing, positive wording and keeps only what the slide needs to show.

## Artifacts

A run usually creates:

```text
<DeckTitle>-YYYYMMDD-HHMM/
├── outline.md
├── style-preview.png
├── <DeckTitle>.pptx
└── images/
    ├── 01.png
    ├── 02.png
    └── archive/
```

Repository structure:

```text
codex-ppt/
├── SKILL.md
├── README.md
├── README.en.md
├── LICENSE
├── CONTRIBUTING.md
└── scripts/
    └── assemble_image_ppt.py
```

## Assemble Existing Images

If finished slide images already exist under `images/`, run:

```bash
python3 scripts/assemble_image_ppt.py \
  --workdir /absolute/path/to/workdir \
  --title "Deck Title" \
  --expected-pages 10 \
  --ratio 16:9
```

The script only inserts one full-slide image per PowerPoint page. It does not design, render, or edit slide content.

## License

MIT
