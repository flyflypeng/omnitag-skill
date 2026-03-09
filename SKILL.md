---
name: omnitag-recommendation
description: 自动为笔记、文章或思考内容生成标准化的 OmniTag 标签组合。当用户需要分类、打标签、整理知识库，或提及 PARA、OmniTag、标签推荐时，请务必触发此技能。
version: 0.2.0
license: MIT
author: flyflypeng <flyflyflypeng@gmail.com>
tags: [tag, omnitag, knowledge, PARA]
---

# OmniTag Recommendation Skill

## 📖 简介

本技能根据用户输入的内容（文本或 URL）和 **个性化标签配置文件**，智能生成标准化、层级清晰的标签组合。采用经典的 **"PARA + Topic + Type + Meta" (3+1)** 结构，帮助用户构建有序的个人知识库。

## ⚙️ 环境配置 (Setup)

**⚠️ 重要前提**：本技能依赖用户的自定义标签配置文件运行。使用前请务必完成以下初始化配置：

1.  **创建 Python 环境 (推荐使用 uv)**：
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
    - 如果文件不存在，请参考下方的 **YAML 模板** 手动创建。
    - **注意**：如果未检测到此文件，技能将无法加载您的个性化标签体系，推荐结果可能不符合预期。

### 配置文件模板 (`~/.omnitag/omni-tags.yaml`)

```yaml
groups:
  - tag-name: PARA
    tag-usage: "PARA核心分类（必选其一）"
    prefix: "#PARA/"
    items:
      - tag-name: Project
        tag-usage: "当前进行的项目"
        children:
          - tag-name: "OmniTag-20260415"
      - tag-name: Area
        tag-usage: "长期维护的领域"
        children:
          - tag-name: "Agent系统"
          - tag-name: "云原生"
      - tag-name: Resource
        tag-usage: "感兴趣的资源"
        children:
          - tag-name: "AI前沿"
          - tag-name: "编程语言"
      - tag-name: Archive
        tag-usage: "已归档的内容"

  - tag-name: Topic
    tag-usage: "内容主题（多选）"
    prefix: "#Topic/"
    items:
      - tag-name: Agent
        tag-usage: "AI Agent全栈"
        children:
          - tag-name: "运行时框架"
          - tag-name: "沙箱"
      - tag-name: LLM
        tag-usage: "大模型技术"
        children:
          - tag-name: "强化学习"
          - tag-name: "Transformer"

  - tag-name: Type
    tag-usage: "笔记类型（必选，描述笔记形态）"
    prefix: "#Type/"
    items:
      - tag-name: Note
        tag-usage: "原始笔记/摘录；flomo快速记录、会议记录"
      - tag-name: Insight
        tag-usage: "洞察/思考；技术分析、观点输出"
      - tag-name: Paper
        tag-usage: "论文相关；论文阅读、论文分析"

  - tag-name: Meta
    tag-usage: "元标签（系统级，可选）"
    prefix: "#Meta/"
    items:
      - tag-name: Daily
        tag-usage: "每日记录"
      - tag-name: Important
        tag-usage: "重要标记"
```

## 🏷️ 核心规则

标签生成遵循以下 **"3+1"** 结构原则：

| 维度      | 描述                                           | 约束             | 示例                             |
| :-------- | :--------------------------------------------- | :--------------- | :------------------------------- |
| **PARA**  | 核心分类 (Project/Area/Resource/Archive/Inbox) | **必选且唯一**   | `#PARA/Project`, `#Inbox`        |
| **Topic** | 内容主题 (所属领域)                            | **必选 (1-4个)** | `#Topic/Agent`, `#Topic/LLM`     |
| **Type**  | 笔记类型 (内容形态)                            | **必选 (1-2个)** | `#Type/Note`, `#Type/Insight`    |
| **Meta**  | 元数据 (属性/状态)                             | 可选             | `#Meta/Daily`, `#Meta/Important` |

**详细说明：**
*   **PARA (唯一归属)**：每条内容只能属于一个 PARA 类别。若无法明确归类，请使用 `#Inbox`。
*   **Topic (多维描述)**：鼓励组合使用不同领域的标签（如 `#Topic/Agent/沙箱` + `#Topic/CloudNative/安全容器`）。若现有配置中无合适标签，允许根据内容主旨生成新的 Topic 标签。
*   **Type (形态定义)**：描述内容的“形式”而非“内容”（如是“论文”还是“思考”）。
*   **配置优先**：生成标签时，**优先匹配** `omni-tags.yaml` 中已定义的标签层级。

## 🧠 执行流程

1.  **输入解析 (Input Analysis)**:
    *   **纯文本**: 直接进行语义分析。
    *   **URL 链接**: **必须**先调用配套脚本提取正文。
        > **命令**: `python scripts/url_to_markdown.py "<URL>"`
        > **注意**: 微信公众号文章 (`mp.weixin.qq.com`) 需使用 `wechat-article-to-markdown` 技能。
2.  **配置加载 (Context Loading)**:
    *   读取 `~/.omnitag/omni-tags.yaml`，构建当前的标签树。
3.  **语义匹配与生成 (Tagging)**:
    *   **PARA 匹配**: 确定最符合的生命周期阶段。
    *   **Topic 提取**: 在配置树中查找匹配节点；若无精确匹配，则基于父节点语义生成新标签。
    *   **Type/Meta 确定**: 根据内容形式匹配对应的 Type 和 Meta 标签。
4.  **动态生长 (Tag Growth)**:
    *   如果生成了 **新标签**，**必须** 提示用户或自动调用脚本同步。
        > **命令**: `python scripts/update_tags.py "#New/Tag/Path"`
5.  **格式化输出 (Formatting)**:
    *   严格按照规定的 Markdown 格式输出推荐结果和理由。

## 📋 输出格式

ALWAYS use this exact template:

```markdown
推荐 Tag 列表：
#PARA/<Category> #Topic/<Tag1> #Topic/<Tag2> #Type/<Type1> #Meta/<Meta1>

推荐理由：
<简短说明推荐理由，不超过 200 字>
```

## 💡 示例 (Few-Shot)

### 示例 1: 学术研究
**Input**:
> 论文标题：A CPU-Centric Perspective on Agentic AI
> 关键结论：Agentic AI 工作负载的吞吐量受 CPU 因素（缓存一致性、同步）或 GPU 因素（显存容量）限制。

**Output**:
```markdown
推荐 Tag 列表：
#PARA/Area/Agent系统 #Topic/CPU #Topic/Workload #Topic/Agent #Type/Paper

推荐理由：
内容涉及 Agentic AI 的硬件瓶颈分析（CPU/GPU），属于 Agent 系统领域的深度研究，适合归类为 Area 下的长期关注点。
```

### 示例 2: 工具资源
**Input**:
> Banana-Slides 开源 AI PPT 生成工具。支持调用 Google Nano Banana 模型生成 Slide，支持本地容器化部署。

**Output**:
```markdown
推荐 Tag 列表：
#PARA/Resource/效能工具 #Topic/AI-Infra/模型服务 #Type/Resource #Meta/Quick

推荐理由：
这是一个具体的 AI 工具资源，支持本地部署（Infra），适合作为效能工具收藏，并标记为 Quick 以便后续快速查看。
```
