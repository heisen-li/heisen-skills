# heisen-skills

个人 Claude Code Skill 合集，收录各类实用技能，用于增强 AI 编程助手的多模态处理与内容生成能力。

## Skill 列表

| Skill | 简介 | 状态 |
|-------|------|------|
| [mm2map](./mm2map/) | 多模态内容（图片/视频/音频/PPT/URL）→ Mermaid 思维导图 | ✅ 可用 |
| [wewrite](https://github.com/oaker-io/wewrite) | 微信公众号内容全流程助手（外部仓库） | ✅ 可用 |

## 安装方式

将所需 skill 目录复制到 Claude Code 的 skills 目录下即可：

```bash
# 克隆仓库
git clone https://github.com/heisen-li/heisen-skills.git

# 复制单个 skill 到 Claude skills 目录
# Windows
xcopy /E /I heisen-skills\mm2map %USERPROFILE%\.claude\skills\mm2map
# macOS/Linux
cp -r heisen-skills/mm2map ~/.claude/skills/mm2map
```

## mm2map — 多模态转思维导图

将图片、视频、语音、PPT 以及视频 URL（YouTube/Bilibili 等）转换为 Mermaid mindmap 格式思维导图。

### 功能特性

- 支持图片（OCR式提取内容与层级关系）
- 支持视频（音频转录 + 关键帧画面分析）
- 支持音频（本地/API 两种转录方式）
- 支持 PPT（提取幻灯片结构与内容层级）
- 支持视频 URL（YouTube、Bilibili、Twitter/X 等 1000+ 平台）
- 支持多文件合并处理
- 自动生成 `.md` + `.mmd` 双格式输出
- 本地转录无需任何 API Key（使用 faster-whisper）

### 依赖安装

```bash
# 自动检测与安装依赖
powershell -ExecutionPolicy Bypass -File mm2map/scripts/install_deps.ps1 -Install

# 或手动安装 Python 依赖
pip install -r mm2map/requirements.txt
```

核心依赖：ffmpeg、Python 3.x、yt-dlp、faster-whisper、python-pptx

### 使用方式

在 Claude Code 中调用：

```
/mm2map <文件路径或URL>
/mm2map img1.png img2.png img3.png    # 多文件合并
/mm2map https://www.youtube.com/watch?v=xxx  # 视频URL
/mm2map https://www.bilibili.com/video/BVxxx  # B站链接
```

详细说明见 [mm2map/SKILL.md](./mm2map/SKILL.md)。

## 许可证

[MIT License](./LICENSE)
