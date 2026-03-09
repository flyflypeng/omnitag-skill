# OmniTag 标签推荐技能

[English](./README_en.md)

---

### 📖 简介

**OmniTag 标签推荐技能** 是一个专为个人知识管理设计的智能标签助手。它根据您的 **个性化标签配置文件** 和 **PARA 方法论**，自动为您输入的笔记、文章或思考内容生成标准化、层级清晰的标签组合。

本技能采用经典的 **"PARA + Topic + Type + Meta" (3+1)** 结构，帮助您构建有序的个人知识库。

### 📦 快速安装 (Quick Start)

目前支持通过 `npx skills` 直接从 GitHub 仓库安装：

```bash
npx skills add https://github.com/flyflypeng/omnitag-skill --skill omnitag-recommendation -g -y
```

> ⏳ **Coming Soon**: 等待上架 Clawhub 后将支持更便捷的安装方式。

### ✨ 功能特性

- **标准化标签生成**：严格遵循 `PARA + Topic + Type + Meta` 结构。
- **个性化配置**：完全适配您在 `~/.omnitag/omni-tags.yaml` 中定义的标签体系。
- **智能内容分析**：
  - 直接分析纯文本内容。
  - 自动提取 URL 链接的正文（去除广告/导航），支持 `markdown.new` 和 `Jina Reader` 双引擎。
  - 针对微信公众号文章提供专用处理方案（需配合 `wechat-article-to-markdown` 技能）。
- **标签动态生长**：提供配套脚本，将 AI 推荐的新标签自动同步回您的配置文件，实现知识库的自我进化。

### ⚙️ 环境配置 (Setup)

**⚠️ 重要前提**：本技能依赖用户的自定义标签配置文件运行。使用前请务必完成以下初始化配置：

1.  **创建 Python 环境 (推荐使用 `uv`)**：
    为了避免依赖冲突，建议使用 `uv` 创建独立的虚拟环境。
    ```bash
    # 1. 创建虚拟环境 (建议在 ~/.omnitag 目录下)
    uv venv
    
    # 2. 激活虚拟环境
    source .venv/bin/activate
    
    # 3. 安装依赖
    uv pip install pyyaml
    ```

2.  **准备配置文件**：确保本地存在标签配置文件 `~/.omnitag/omni-tags.yaml`。
    - 如果文件不存在，请参考 [YAML 模板](SKILL.md#配置文件模板-omnitagomni-tagsyaml) 手动创建。
    - **注意**：如果未检测到此文件，技能将无法加载您的个性化标签体系。

### 🚀 使用指南

#### 1. 标签推荐
直接输入您需要打标签的内容或 URL 链接。技能将分析核心主旨并推荐最合适的标签组合。

#### 2. 网页内容提取
对于 URL 链接，技能会调用配套脚本提取正文：
```bash
python scripts/url_to_markdown.py "https://example.com/article"
```
- **主引擎**：[markdown.new](https://markdown.new/)
- **备用引擎**：[Jina Reader](https://jina.ai/reader/)

#### 3. 标签动态更新
如果推荐结果中包含了新标签（如新项目或新领域），使用更新脚本将其同步到配置中：
```bash
python scripts/update_tags.py "#PARA/Project/新项目" "#Topic/新主题"
```

### 🏷️ 核心规则 (3+1 结构)

| 维度      | 描述                                           | 约束             | 示例                             |
| :-------- | :--------------------------------------------- | :--------------- | :------------------------------- |
| **PARA**  | 核心分类 (Project/Area/Resource/Archive/Inbox) | **必选且唯一**   | `#PARA/Project`, `#Inbox`        |
| **Topic** | 内容主题 (所属领域)                            | **必选 (1-4个)** | `#Topic/Agent`, `#Topic/LLM`     |
| **Type**  | 笔记类型 (内容形态)                            | **必选 (1-3个)** | `#Type/Note`, `#Type/Insight`    |
| **Meta**  | 元数据 (属性/状态)                             | 可选             | `#Meta/Daily`, `#Meta/Important` |
