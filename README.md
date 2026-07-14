# heisen-skills

个人 AI Agent Skill 合集，收录各类实用技能，用于增强 Claude Code / OpenCode / Cursor / VS Code 等 AI 编程助手的多模态处理与内容生成能力。

所有 Skill 均遵循 [Agent Skills 开放标准](https://agentskills.io)，可跨平台使用。

## Skill 列表

| Skill | 简介 | 版本 | 状态 |
|-------|------|------|------|
| [mm2map](./mm2map/) | 多模态内容（图片/视频/音频/PPT/PDF/URL）→ 思维导图（Mermaid + XMind） | v1.0 | ✅ 可用 |
| [wewrite](./wewrite/) | 微信公众号内容全流程助手：热点→选题→框架→写作→SEO→配图→排版→推草稿箱 | v1.0 | ✅ 可用 |

## 安装方式

将所需 skill 目录复制到 Agent 的 skills 目录下即可：

```bash
# 克隆仓库
git clone https://github.com/heisen-li/heisen-skills.git

# 复制单个 skill 到 skills 目录
# Windows (Claude Code / OpenCode)
xcopy /E /I heisen-skills\mm2map %USERPROFILE%\.claude\skills\mm2map
xcopy /E /I heisen-skills\wewrite %USERPROFILE%\.claude\skills\wewrite

# macOS/Linux (Claude Code / OpenCode)
cp -r heisen-skills/mm2map ~/.claude/skills/mm2map
cp -r heisen-skills/wewrite ~/.claude/skills/wewrite

# Cursor — 复制到项目级 .cursor/skills/ 下
cp -r heisen-skills/mm2map .cursor/skills/mm2map

# VS Code Copilot — 复制到项目级 .github/copilot/skills/ 下
cp -r heisen-skills/mm2map .github/copilot/skills/mm2map
```

---

## mm2map — 多模态转思维导图

将图片、视频、语音、PPT、PDF 以及视频 URL（YouTube/Bilibili 等）转换为详尽的思维导图，输出 Markdown + XMind 双格式文件。

### 功能特性

- **6种输入类型**：图片、视频、音频、PPT、PDF、视频URL
- **详尽导图输出**：不精简不遗漏，每个节点包含定义、分类、步骤、意义、数据、案例等完整信息
- **双格式文件输出**：`.md`（Markdown，Typora/Obsidian可渲染）+ `.xmind`（XMind可直接打开编辑）
- **本地转录无需API Key**：使用 faster-whisper 本地运行，完全免费离线
- **API转录可选**：有 OpenAI Key 时自动切换到 Whisper API（更快更准）
- **多文件合并**：多张关联图片可合并为一个统一导图
- **视频URL下载**：支持 YouTube、Bilibili、Twitter/X 等 1000+ 平台

### 支持的输入格式

| 类型 | 扩展名 |
|------|--------|
| 图片 | .jpg .jpeg .png .gif .bmp .webp .svg |
| 视频 | .mp4 .avi .mkv .mov .wmv .flv .webm |
| 音频 | .mp3 .wav .ogg .flac .aac .m4a .wma |
| PPT | .pptx .ppt |
| PDF | .pdf |
| URL | YouTube / Bilibili / Twitter / Vimeo 等 |

### 依赖安装

```bash
# 自动检测与安装全部依赖（Windows PowerShell）
powershell -ExecutionPolicy Bypass -File mm2map/scripts/install_deps.ps1 -Install

# 或手动安装 Python 依赖
pip install -r mm2map/requirements.txt
```

核心依赖：ffmpeg、Python 3.x、yt-dlp、faster-whisper、python-pptx、pymupdf、openai（可选）

### 使用方式

```
/mm2map <文件路径或URL>
/mm2map img1.png img2.png img3.png    # 多文件合并
/mm2map https://www.youtube.com/watch?v=xxx  # 视频URL
/mm2map https://www.bilibili.com/video/BVxxx  # B站链接
/mm2map report.pdf                     # PDF文件
/mm2map presentation.pptx             # PPT文件
/mm2map lecture.mp3                    # 音频文件
```

输出文件：
- `mindmap_<源文件名>.md` — Markdown格式，含内容摘要 + Mermaid导图 + 渲染提示
- `mindmap_<源文件名>.xmind` — XMind格式，可直接打开编辑、拖拽调整、导出PNG/SVG/PDF

详细说明见 [mm2map/SKILL.md](./mm2map/SKILL.md)。

---

## wewrite — 微信公众号内容全流程助手

从热点抓取到推送草稿箱的完整内容创作链路，专为微信公众号运营者打造。

### 功能特性

- **热点抓取**：自动获取热门话题与趋势
- **选题推荐**：基于热点和行业生成选题建议
- **框架生成**：自动构建文章大纲和结构
- **内容增强**：润色文案、增强表达、提升可读性
- **写作输出**：生成完整公众号文章
- **SEO优化**：关键词密度与标题优化
- **配图生成**：AI生成封面图和配图
- **排版推送**：微信格式排版，一键推送到草稿箱
- **风格学习**：从用户历史文章中学习写作风格
- **数据复盘**：文章效果分析与优化建议
- **5种写作人格**：冷峻分析师、犀利记者、温暖编辑、午夜朋友、行业观察者
- **16种排版主题**：从 Bauhaus 到 少数派风格，一键切换

### 依赖安装

```bash
pip install -r wewrite/requirements.txt
```

### 使用方式

```
/wewrite 热点抓取
/wewrite 选题推荐 <行业关键词>
/wewrite 写一篇 <主题>
/wewrite 生成封面图
/wewrite 推送草稿箱
/wewrite 风格设置 <人格名称>
/wewrite 数据复盘
```

详细说明见 [wewrite/SKILL.md](./wewrite/SKILL.md)。

---

## 兼容平台

所有 Skill 基于 Agent Skills 开放标准，兼容以下平台：

- Claude Code
- OpenCode
- Cursor
- VS Code + GitHub Copilot
- Gemini CLI
- OpenAI Codex CLI
- 以及其他支持 SKILL.md 格式的 Agent 工具

## 许可证

[MIT License](./LICENSE)
