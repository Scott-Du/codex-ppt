# Contributing

谢谢你愿意改进 `codex-ppt`。

这个项目是一个面向 Codex 的 PPT 生成 skill。最有价值的贡献，是能让"整页图片生成 + PPTX 机械装配"这条链路更稳定、更清楚、更容易复用。

## 提 Issue 前

请尽量说明问题属于哪一类：

- 安装问题：skill 无法被 Codex 发现或触发。
- 图像生成流程：逐页保存、命名、归档、重做流程不清楚。
- PPTX 装配：页数、比例、图片插入、PowerPoint 打开异常。
- 文档问题：README、触发方式、安装方式、使用边界不清楚。
- 工作流建议：风格样张、大纲确认、正向口径检查、交付清单等流程优化。

如果可以，请附上：

- 你的 prompt 或大纲。
- 生成的 `outline.md`。
- `images/` 中对应页面图。
- 报错日志或截图。
- 操作系统、Python 版本、Pillow 版本。

## Pull Request 建议

- PR 尽量小而清楚，一次解决一个问题。
- 如果改了 `SKILL.md`，请说明它会如何改变 Codex 的行为。
- 如果改了 `assemble_image_ppt.py`，请至少用 2 张测试图片跑一次装配。
- 不要把生成出来的 `.pptx`、`.png`、`.jpg` 提交进仓库。

## 脚本检查

提交前建议运行：

```bash
python3 -m py_compile scripts/assemble_image_ppt.py
```

如果你有一组测试图片，也可以运行：

```bash
python3 scripts/assemble_image_ppt.py \
  --workdir /absolute/path/to/workdir \
  --title "Test Deck" \
  --expected-pages 2 \
  --ratio 16:9
```

## 设计原则

- 保持 image-first：正式页面必须来自图像生成工具。
- 保持 PPTX 机械装配：脚本只负责插图，不负责设计页面。
- 保持工作流清晰：`outline.md` 是内容源，`images/` 是页面图，`.pptx` 是交付容器。
- 保持中文主导：这个 skill 的主要使用者以中文协作为主，英文文档作为辅助入口。
