---
name: anthropic-visual-studio
description: "制作或修改 Anthropic / Claude 视觉风格的网页、交互原型与动效，支持一句话设计需求和指定参考复刻。包含可运行模板、原创 SVG 示例及本地素材导入；不要因项目使用 Claude API 就自动套用此视觉风格。"
---

# Anthropic 视觉设计工作室 · 开源版

将简短需求落实为可运行的页面。先理解用途、核心操作、视觉隐喻和动效强度；已有项目沿用框架。新独立原型默认原生 HTML/CSS/JS。设计、实现和验证是工作阶段，不代表自动启动多个代理。

## 选材与设计

先读 [视觉语言](references/visual-language.md)，涉及动态时读 [动效](references/motion.md)。区分风格演绎与指定参考复刻：复刻先实际查看参考并建立同尺寸对照，不能将风格相似说成精确还原。

公开库自带六份原创 MIT 具象 SVG：思考、书写、生长、灵感、阅读、对话，不含官方插画和专有字体。可按 [本地素材说明](references/assets.md) 导入用户自有资源；按实际检索结果使用，不能声称公开版包含私有档案。

先看 [应用版式](references/page-patterns.md)，再选与用途匹配的页面起点。`examples/index.html` 提供六张主题海报和三种真实网页的总览；论文、文章、互动应用需要各自的信息结构与核心操作。具体人物、手、书页、鸟或植物承担主要隐喻，圆点连线不作为默认主视觉。

```text
python <skill-root>/scripts/catalog.py --theme thinking --editable --limit 6
python <skill-root>/scripts/catalog.py --id STUDIO-growth
```

实际查看候选素材。保留出处、文件哈希、授权与派生身份；预览不是可编辑矢量。模板默认系统字体，导入已持有的三份字体后可使用本地字体；中文保留系统回退。

## 实现

```text
python <skill-root>/scripts/scaffold.py --out <new-output-folder> --title "让研究更进一步" --asset STUDIO-thought --motion gentle
```

脚本只创建新目录，提供海报工作台：六幅插画、配色、标题与副标题编辑、缩放、纸纹与辅助线、暂停、来源说明、插画与整张海报 SVG 导出。它适合视觉实验，不是所有产品的最终页面。论文、文章与互动网站优先从 `examples/paper/`、`examples/article/`、`examples/garden/` 选取结构，并复制其 `examples/shared/` 依赖。按产品改写信息结构和核心流程。按钮连接真实状态；联网能力未实现时明确标记演示。复制本次需要的素材，不携带整个库。持续动画提供暂停和 reduced-motion，触屏不能依赖 hover。

## 验证与交付

读 [验证要点](references/verification.md)，运行真实浏览器检查：

```text
python <skill-root>/scripts/verify_page.py <output-folder>/index.html --out <qa-folder> --starter --channel msedge
```

验证器需要 Playwright；无 Edge 可用 `--channel chromium` 配合已安装的 Playwright Chromium。`--starter` 仅用于保留模板控件的页面；改成业务页面后补实际主流程测试。至少检查运行错误、资源、移动端溢出、键盘、运动与暂停、减少动态效果和实际导出。截图不代替交互测试。

交付可打开的文件，说明所用素材和未核验部分。不要保证任意参考或任意复杂动效都能自动精确复刻。仅按用户明确授权上传或发布；MIT 不覆盖导入的第三方素材与字体。
