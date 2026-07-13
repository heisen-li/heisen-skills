## API 配置指南

### 两种转录方式

mm2map 支持两种语音转录方式：

| 方式 | 需要API Key | 费用 | 速度 | 适用场景 |
|------|------------|------|------|----------|
| **本地 faster-whisper** | 不需要 | 免费 | 较慢 | 无OpenAI Key、离线、隐私敏感 |
| **Whisper API** | 需要 | $0.006/分钟 | 快 | 有OpenAI Key、追求速度 |

**如果你使用 GLM/Claude 等非 OpenAI 模型，推荐使用本地转录——完全免费，无需任何 API Key。**

### API Key 复用逻辑

mm2map 的语音转录使用 OpenAI Whisper API。API Key 查找优先级如下：

1. **`OPENAI_API_KEY`**（推荐） — OpenAI 官方标准环境变量名。如果你当前聊天已经在使用 OpenAI 模型（如 GPT-4o），这个变量很可能已经存在，**无需额外配置，直接复用**。
2. **`WHISPER_API_KEY`** — 专用变量名。仅在 OPENAI_API_KEY 不存在时作为备选。

如果两个都不存在 → 自动切换到 **本地 faster-whisper 转录**，无需配置任何 Key。

**图片和PPT不需要任何转录，无论哪种方式都不影响。**

---

### 本地 faster-whisper 转录（默认，无需API Key）

安装后自动可用，无需配置。首次使用会下载模型权重：

| 模型大小 | 下载体积 | 推理速度 | 准确度 |
|----------|----------|----------|--------|
| tiny | ~75MB | 最快 | 最低 |
| base (推荐) | ~150MB | 平衡 | 好 |
| small | ~500MB | 较慢 | 较好 |
| medium | ~1.5GB | 很慢 | 高 |
| large-v3 | ~3GB | 极慢 | 最高 |

使用方式：
```
/mm2map audio.mp3
```
Skill 会自动检测：无 API Key → 使用本地转录。

手动指定模型大小：
```
python transcribe_local.py audio.mp3 small
```

---

### Whisper API (OpenAI) — 云端转录（可选）

Whisper API 用于将音频和视频中的语音内容转录为文本。

#### 获取 API Key

1. 访问 https://platform.openai.com/api-keys
2. 注册/登录 OpenAI 账号
3. 创建新的 API Key
4. 复制 Key（格式：`sk-...`）

#### 配置环境变量

**Windows PowerShell (当前会话):**
```powershell
# 推荐：使用 OPENAI_API_KEY（可复用聊天模型的 Key）
$env:OPENAI_API_KEY = "sk-your-api-key-here"

# 或使用专用 WHISPER_API_KEY（仅在 OPENAI_API_KEY 不存在时生效）
$env:WHISPER_API_KEY = "sk-your-api-key-here"
```

**Windows PowerShell (持久化):**
```powershell
# 推荐
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-your-api-key-here", "User")

# 或
[Environment]::SetEnvironmentVariable("WHISPER_API_KEY", "sk-your-api-key-here", "User")
```

**验证配置:**
```powershell
# 检查哪个 Key 可用
if ($env:OPENAI_API_KEY) { "OPENAI_API_KEY 已配置，可直接复用" }
elseif ($env:WHISPER_API_KEY) { "WHISPER_API_KEY 已配置" }
else { "未配置任何 API Key" }
```

#### 费用参考

- Whisper API: $0.006/分钟
- 10分钟音频 ≈ $0.06
- 60分钟音频 ≈ $0.36
- 25MB 文件大小限制（单次请求）

#### 大文件处理

超过25MB的音频文件需要分段：
```powershell
ffmpeg -i long_audio.wav -f segment -segment_time 600 -c copy part_%03d.wav
```

---

### GitMind API (可选) — 另一种导图生成方式

GitMind API 是可选的替代方案。mm2map 默认使用 AI 直接生成 Mermaid，无需 GitMind API。

如果你希望使用 GitMind API 作为替代：

#### 获取 API Key

1. 访问 https://gitmind.cn 并注册账号
2. 在设置中找到 API Token
3. 复制 Token

#### 配置环境变量

```powershell
$env:GITMIND_API_KEY = "your-gitmind-token"
```

#### 注意

- GitMind API 目前可能需要付费订阅
- mm2map 默认不依赖 GitMind API
- 仅在需要将结果导入 GitMind 平台编辑时才配置

---

### 安全提醒

- **不要**将 API Key 写入 SKILL.md 或任何代码文件
- **不要**将 API Key 提交到 Git 仓库
- 使用环境变量存储，不要硬编码
- 定期轮换 API Key
- 设置 API 使用限额避免意外高额费用
