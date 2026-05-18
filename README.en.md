# codex-ppt · Image-first PowerPoint Decks

![GitHub stars](https://img.shields.io/github/stars/Scott-Du/codex-ppt?style=flat-square)
![License](https://img.shields.io/github/license/Scott-Du/codex-ppt?style=flat-square)
![Skill](https://img.shields.io/badge/Skill-Codex-111111?style=flat-square)
![PPTX](https://img.shields.io/badge/Output-PPTX-D24726?style=flat-square)
![Image First](https://img.shields.io/badge/Image--First-Slides-0A7CFF?style=flat-square)

> 中文版: [README.md](./README.md)

`codex-ppt` is a Codex skill for creating image-first PowerPoint decks. Each final slide is generated as a full-page image with Codex's built-in `image_gen`, then mechanically assembled into a `.pptx`.

The design lives in the generated slide images. PowerPoint is used as the delivery container.

## 30-second Start

If your environment supports the `skills` CLI:

```bash
npx skills add https://github.com/Scott-Du/codex-ppt --skill codex-ppt
```

Or paste this into a Codex / AI agent with shell access:

```text
Install codex-ppt for me. Clone https://github.com/Scott-Du/codex-ppt into $CODEX_HOME/skills/codex-ppt, then verify that SKILL.md and scripts/assemble_image_ppt.py exist.
```

Then ask Codex:

```text
Use codex-ppt to create a 10-slide image-first pitch deck from this outline.
```

## What It Does

- Generates each final slide as a full-page image.
- Saves final slide images as `images/01.png`, `images/02.png`, and so on.
- Keeps `outline.md` as the single source of truth.
- Generates `style-preview.png` before full production.
- Assembles the slide images into a `.pptx` with `scripts/assemble_image_ppt.py`.
- Supports single-slide redo by archiving the old image and regenerating the selected page.

## Fits / Doesn't Fit

**Fits**

- Pitch decks, project application decks, demo day decks
- Product stories, startup narratives, visual presentations
- Decks where visual quality matters more than editable PowerPoint objects

**Doesn't fit**

- Dense table-heavy documents
- Training decks that need lots of editable text
- Long-term collaborative editing inside PowerPoint
- Native editable text boxes, shapes, and animations

## Why Image-first PPT

- Full-slide image generation is more stable for visual design.
- Style consistency is easier when each slide is generated as one composed image.
- The output is still a `.pptx`, which fits many pitch, review, and application workflows.
- Edits are explicit: update `outline.md`, regenerate the affected slide, then reassemble.

## Workflow

The skill guides the agent through:

1. Confirm deck metadata.
2. Generate and confirm a style preview.
3. Write and confirm `outline.md`.
4. Generate slide images one page at a time.
5. Assemble the final `.pptx`.
6. Return the work folder, PPTX path, outline path, and images folder.

## Install

### Option 1: skills CLI

```bash
npx skills add https://github.com/Scott-Du/codex-ppt --skill codex-ppt
```

### Option 2: manual Codex install

```bash
mkdir -p "$CODEX_HOME/skills"
git clone https://github.com/Scott-Du/codex-ppt.git "$CODEX_HOME/skills/codex-ppt"
```

If `CODEX_HOME` is not set:

```bash
git clone https://github.com/Scott-Du/codex-ppt.git ~/.codex/skills/codex-ppt
```

Restart Codex or reload skills after installation.

## Trigger Phrases

- "Use codex-ppt to make slides"
- "Create an image-first PowerPoint deck"
- "Turn this outline into a 10-slide pitch deck"
- "调用 codex-ppt skill 做 PPT"
- "把这个大纲做成 10 页幻灯片"

## Assemble Existing Slide Images

If finished slide images already exist under `images/`, run:

```bash
python3 scripts/assemble_image_ppt.py \
  --workdir /absolute/path/to/workdir \
  --title "Deck Title" \
  --expected-pages 10 \
  --ratio 16:9
```

The script only inserts one full-slide image per PowerPoint page. It does not design, render, or edit slide content.

## Directory

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

## Tradeoffs

- The output is image-first, not editable-shape-first.
- To change slide text or layout, update `outline.md` and regenerate that slide.
- This skill is optimized for visually polished delivery decks rather than collaborative PowerPoint editing.

## License

MIT
