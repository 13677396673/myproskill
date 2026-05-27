# Plan: 新增 MiMo-V2.5-TTS-VoiceClone Provider

## 背景

`mimo-v2.5-tts-voiceclone` 是小米 MiMo 语音系列的**音色克隆**模型。与已有 `mimo.sh`
（基础 TTS）的核心差异：

| 维度 | 基础 TTS (`mimo.sh`) | VoiceClone (本次新增) |
|------|---------------------|----------------------|
| model | `mimo-v2.5-tts` | `mimo-v2.5-tts-voiceclone` |
| 预置音色 | ✓ 200+ 种 | ✗ 不能指定，由参考音频决定 |
| 参考音频 | 不需要 | **必须**：`audio.input_audio` 字段传入 base64 编码的音频 |
| audio.voice | `mimo_default` 等 | 无此字段 |
| audio.input_audio | 无 | base64 编码的参考音频 |

---

## 设计要点

### Provider 命名

`mimo-voiceclone` — 与 `mimo` 并列的两个独立 provider，因为请求体结构差异大（一个用 `voice`、一个用 `input_audio`），合并到一个文件会引入复杂分支逻辑。

### 参考音频来源

用户把样本文件放在 `presentation/audio-samples/` 目录下，通过约定文件名来引用：

```
presentation/audio-samples/
├── my-voice.mp3        # 默认
├── narrator-female.wav
└── narrator-male.mp3
```

### 如何指定用哪个样本

复用 `--voice` 参数 / `PRESENTATION_TTS_VOICE` env var，语义变为"样本文件名（不含扩展名）"：

```bash
# 用 audio-samples/my-voice.mp3（默认）
PRESENTATION_TTS=mimo-voiceclone npm run synthesize-audio

# 用 audio-samples/narrator-female.wav
PRESENTATION_TTS=mimo-voiceclone npm run synthesize-audio -- --voice=narrator-female
```

额外 env：
- `MIMO_SAMPLE_DIR` — 样本目录（默认 `audio-samples/`，相对于 presentation 根目录）
- 搜索顺序：`<voice>.mp3` → `<voice>.wav` → 报错

### 请求体结构

```json
{
  "model": "mimo-v2.5-tts-voiceclone",
  "messages": [
    { "role": "user",      "content": "请模仿这个人的声音朗读" },
    { "role": "assistant", "content": "<实际合成文本>" }
  ],
  "audio": {
    "format": "mp3",
    "input_audio": "<base64 编码的参考音频>"
  }
}
```

注意：
- 没有 `audio.voice` 字段
- `input_audio` 是 base64 编码的完整音频文件内容
- 参考音频大小限制 10MB（对口播样本绰绰有余）

---

## 改动清单

### 1. 新建：`templates/scripts/tts-providers/mimo-voiceclone.sh`

三函数契约实现：

**`tts_check`** — 校验：
- curl / jq / base64 已安装
- `MIMO_API_KEY` 已设置

**`tts_install_help`** — 打印获取 key 和准备样本的说明

**`tts_synthesize`** — 核心逻辑：
1. 解析 `$3`（voice）为样本文件名，在 `MIMO_SAMPLE_DIR` 里找 `<name>.mp3` 或 `<name>.wav`
2. base64 编码找到的样本文件
3. 构建 JSON 请求体（含 `input_audio`）
4. curl → jq 提取 base64 音频 → base64 -d 写入 mp3

### 2. 修改：`references/AUDIO.md`

| 改点 | 内容 |
|------|------|
| 内置 provider 表 | 将 `mimo` 拆为两行（`mimo` 基础 TTS + `mimo-voiceclone` 音色克隆） |
| §2.C 后加 §2.C.ii | MiMo VoiceClone 用法：说明样本目录约定、示例命令、env 变量 |
| 故障排查 | 加 VoiceClone 专属行：样本文件找不到 / base64 编码失败 / 参考音频超限 |

### 3. 修改：`templates/scripts/tts-providers/README.md`

| 改点 | 内容 |
|------|------|
| 内置表 | 加 `mimo-voiceclone.sh` 行 |

### 4. 修改：`SKILL.md` / `README.md` / `README.zh-CN.md`

- 文件树 tts-providers/ 列表加 `mimo-voiceclone.sh`
- "内置 N 个" 文案更新（基础 TTS 和 VoiceClone 若同属 MiMo 家族，可写作
  `mimo（基础 TTS + VoiceClone）` 避免计数膨胀）

---

## 不动的文件

- `synthesize-audio.sh` — runner，不需要改
- `mimo.sh` / `minimax.sh` / `openai.sh` — 不动
- `extract-narrations.ts` — 无关
- 所有主题 / 章节模板 / 组件 — 无关

---

## 实现顺序

1. 写 `mimo-voiceclone.sh`
2. 改 `templates/scripts/tts-providers/README.md`
3. 改 `references/AUDIO.md`
4. 改 `SKILL.md` + `README.md` + `README.zh-CN.md`
5. 清零复查
