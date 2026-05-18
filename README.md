# codex-ppt · 整页图片生成 PPT

![GitHub stars](https://img.shields.io/github/stars/Scott-Du/codex-ppt?style=flat-square)
![License](https://img.shields.io/github/license/Scott-Du/codex-ppt?style=flat-square)
![Skill](https://img.shields.io/badge/Skill-Codex-111111?style=flat-square)
![PPTX](https://img.shields.io/badge/Output-PPTX-D24726?style=flat-square)
![Image First](https://img.shields.io/badge/Image--First-Slides-0A7CFF?style=flat-square)

> 🌏 **English version: [README.en.md](./README.en.md)**

一个面向 Codex 的 PPT 制作 skill：每一页正式幻灯片都由 Codex 内置 `image_gen` 生成成完整图片，最后再把这些页面图机械装配成 `.pptx`。

它适合你想让 AI 做一份**视觉完整、风格统一、能直接交付的 PPT**，而不是让 AI 在 PowerPoint 里堆文本框和形状。

## 30 秒开始

如果你使用支持 `skills` CLI 的环境，可以尝试：

```bash
npx skills add https://github.com/Scott-Du/codex-ppt --skill codex-ppt
```

也可以直接把这段话发给有 shell 权限的 Codex / AI Agent：

```text
帮我安装 codex-ppt。请把 https://github.com/Scott-Du/codex-ppt 克隆到 $CODEX_HOME/skills/codex-ppt，并检查 SKILL.md 和 scripts/assemble_image_ppt.py 是否存在。
```

已经安装过的话，用这段话更新：

```text
帮我更新 codex-ppt。请进入 $CODEX_HOME/skills/codex-ppt 执行 git pull，然后告诉我当前最新 commit。
```

安装后直接对 Codex 说：

```text
调用 codex-ppt skill，帮我基于这个大纲做一份 10 页 PPT。
```

也可以试这些请求：

```text
用 codex-ppt 把这份项目申报材料做成一份 8 页路演 PPT。
基于这个 outline 生成一份 image-first pitch deck。
重做第 04 页，旧图归档，新图继续叫 04.png，然后重新装配 PPTX。
```

## 它做什么

- **整页图片生成**：每页正式幻灯片 = 一张 `image_gen` 生成的完整图片。
- **PPTX 机械装配**：PPTX 只负责承载页面图，不负责页面设计。
- **风格样张确认**：先生成 `style-preview.png`，确认视觉方向后再逐页生产。
- **大纲单一来源**：`outline.md` 是分页大纲和后续重做页面的唯一内容源。
- **逐页流式展示**：每生成一页，保存为 `images/01.png`、`images/02.png` 等，并立即展示进度。
- **单页可重做**：旧图归档到 `images/archive/`，新图保持原页码文件名，再重新装配。
- **正向口径检查**：写大纲时只保留 PPT 需要展示的内容，优先使用正向、对外可读表达。

## 适合 / 不适合

**适合**

- 路演 PPT / 项目申报 PPT / Demo Day PPT
- 创业项目介绍、产品方案、观点分享
- 需要整体视觉风格统一、但不强调逐字可编辑的演示文稿
- 想让 Codex 逐页生成、逐页确认、最后交付 `.pptx`

**不适合**

- 需要多人在 PowerPoint 里长期协作编辑的材料
- 大量表格、密集文字、逐字可编辑的培训课件
- 对每个文本框、形状、动画都要求 PowerPoint 原生可编辑的场景

## 为什么是 Image-first PPT

- **更适合图像生成模型**：整页作为视觉作品生成，比让模型拆成 PowerPoint 形状更稳定。
- **更容易保持风格一致**：色彩、版式、图标、信息图都在同一张页面图里一次性完成。
- **交付形态仍是 PPTX**：评审、路演、申报场景通常需要 `.pptx`，这个 skill 会把图片装进 PowerPoint。
- **修改路径清楚**：改文案或版式时，先改 `outline.md`，再重做对应页。

## 工作流

Skill 会按结构化流程推进：

1. **确认 PPT 元信息**：标题、语言、页数、受众、使用场景、比例、输出形式。
2. **确认视觉风格**：生成正文第一页风格样张 `style-preview.png`。
3. **确认分页大纲**：写入 `outline.md`，每页包含标题、内容和页面设计说明。
4. **逐页生成图片**：调用 Codex 内置 `image_gen`，每页保存为 `images/NN.png`。
5. **机械装配 PPTX**：运行 `scripts/assemble_image_ppt.py`，将图片逐页铺满。
6. **交付路径**：给出工作文件夹、最终 PPTX、`outline.md` 和 `images/` 位置。

## 安装

### 方式一：skills CLI

```bash
npx skills add https://github.com/Scott-Du/codex-ppt --skill codex-ppt
```

### 方式二：手动安装到 Codex

```bash
mkdir -p "$CODEX_HOME/skills"
git clone https://github.com/Scott-Du/codex-ppt.git "$CODEX_HOME/skills/codex-ppt"
```

如果你的环境没有设置 `CODEX_HOME`，通常可以用：

```bash
git clone https://github.com/Scott-Du/codex-ppt.git ~/.codex/skills/codex-ppt
```

然后重启 Codex，或使用当前环境支持的 skill reload 方式。

## 触发方式

安装后，可以用这些说法触发：

- "调用 codex-ppt skill 做 PPT"
- "帮我做一份 image-first PPT"
- "用 Codex PPT 流程做一份路演 deck"
- "把这个大纲做成 10 页幻灯片"
- "Create an image-first PowerPoint deck"
- "Use codex-ppt to make slides from this outline"

## 手动装配已有页面图

如果你已经有完成的页面图，放在某个工作目录的 `images/` 下，可以直接运行：

```bash
python3 scripts/assemble_image_ppt.py \
  --workdir /absolute/path/to/workdir \
  --title "Deck Title" \
  --expected-pages 10 \
  --ratio 16:9
```

脚本只做机械装配：每一页插入一张整页图片。它不会设计、渲染或修改页面内容。

## 目录结构

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

## 设计取舍

- 生成出的 PPTX 是 **image-first**，不是传统的"可编辑文本框 + 形状"。
- 图片页更适合路演、申报、演讲等视觉交付场景。
- 改某一页时，推荐先改 `outline.md`，再重做对应页面图。
- 不生成总览图，不额外维护预览拼图；逐页图片和 PPTX 就是交付物。

## License

MIT
