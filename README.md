# codex-ppt · 整页图片生成 PPT

![GitHub stars](https://img.shields.io/github/stars/Scott-Du/codex-ppt?style=flat-square)
![License](https://img.shields.io/github/license/Scott-Du/codex-ppt?style=flat-square)
![Skill](https://img.shields.io/badge/Skill-Codex-111111?style=flat-square)
![PPTX](https://img.shields.io/badge/Output-PPTX-D24726?style=flat-square)
![Image First](https://img.shields.io/badge/Image--First-Slides-0A7CFF?style=flat-square)

> English: [README.en.md](./README.en.md) · 如果你是 AI Agent，请阅读：[README.agent.md](./README.agent.md)

`codex-ppt` 是一个面向 Codex 的 PPT 制作 Skill。它让 Codex 调用内置 `image_gen` 逐页生成完整幻灯片图片，再把这些图片机械装配成 `.pptx`。

核心取舍很简单：**设计在图片里，PPTX 是交付容器**。这适合追求整体视觉效果、风格统一和快速交付的演示文稿；如果你需要长期编辑每个文本框、形状和动画，它不是最佳路线。

## 快速开始

如果你是人类，直接在 Codex 里说：

```text
帮我安装 codex-ppt。请从 https://github.com/Scott-Du/codex-ppt 安装到我的 Codex skills 目录，安装后检查 SKILL.md 和 scripts/assemble_image_ppt.py 是否存在。
```

已经安装过的话，可以说：

```text
帮我更新 codex-ppt。请进入 codex-ppt skill 目录执行 git pull，然后告诉我当前最新 commit。
```

安装后触发：

```text
调用 codex-ppt skill，基于这个大纲做一份 10 页 PPT。
用 codex-ppt 把这份项目申报材料做成 8 页路演 PPT。
重做第 04 页，旧图归档，新图继续叫 04.png，然后重新装配 PPTX。
```

如果你是 AI Agent，请阅读：[README.agent.md](./README.agent.md)。

## 适用场景

适合：

- 路演 PPT、项目申报 PPT、Demo Day deck
- 创业项目介绍、产品方案、观点分享
- 需要视觉完整、风格统一、但不强调逐字可编辑的材料

不适合：

- 大量表格、密集文字、长期协作编辑的课件
- 需要 PowerPoint 原生文本框、形状、动画全部可编辑的材料

## 工作流

1. 确认标题、页数、受众、场景、比例等元信息。
2. 生成 `style-preview.png`，先定视觉方向。
3. 写入 `outline.md`，作为分页大纲和后续改单页的唯一内容源。
4. 逐页调用 `image_gen`，保存为 `images/01.png`、`images/02.png` 等。
5. 用 `scripts/assemble_image_ppt.py` 把页面图装配成 `.pptx`。
6. 如需重做单页，先归档旧图到 `images/archive/`，新图保持原页码文件名，再重新装配。

写大纲时，Skill 会优先使用正向、对外可读表达，只保留 PPT 页面需要展示的内容。

## 产物

一次任务的工作文件夹通常包含：

```text
<PPT名>-YYYYMMDD-HHMM/
├── outline.md
├── style-preview.png
├── <PPT名>.pptx
└── images/
    ├── 01.png
    ├── 02.png
    └── archive/
```

仓库结构：

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

## 手动装配

如果你已经有完成的页面图，并且它们位于某个工作目录的 `images/` 下，可以直接运行：

```bash
python3 scripts/assemble_image_ppt.py \
  --workdir /absolute/path/to/workdir \
  --title "Deck Title" \
  --expected-pages 10 \
  --ratio 16:9
```

脚本只做机械装配：每一页插入一张整页图片。它不会设计、渲染或修改页面内容。

## License

MIT
