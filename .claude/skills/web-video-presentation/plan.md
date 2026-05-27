# Plan: 新增 MiMo-V2.5-TTS 音频合成 Provider

## 背景

MiMo-V2.5-TTS 是**小米**的全链路语音大模型系列，通过 OpenAI 兼容的 chat completions 接口提供 TTS 能力。与现有 provider 的核心区别：

- 使用 `POST /v1/chat/completions` 而非专用 TTS 端点
- 文本放在 `assistant` role，风格指令放在 `user` role
- 响应体是 JSON（base64 音频位于 `choices[0].message.audio.data`），而非原始音频流
- 支持中文预置音色（默认 `冰糖`/`mimo_default`）

---

## 改动清单

### 1. 新建：`templates/scripts/tts-providers/mimo.sh`

新增第三个内置 provider，遵循三函数契约：

**`tts_check`** — 校验：
- `curl` / `jq` 已安装
- `MIMO_API_KEY` 已设置

**`tts_install_help`** — 打印：从 platform.xiaomimimo.com 获取 API key

**`tts_synthesize`** — 核心逻辑：
- 接受 `MIMO_BASE_URL` env（默认 `https://api.xiaomimimo.com/v1`）
- 构造 OpenAI 兼容的 chat 请求体：
  - `model`: `mimo-v2.5-tts`
  - `messages[0]`: `{ role: "user", content: "用自然平实的语调朗读" }`（固定风格指令）
  - `messages[1]`: `{ role: "assistant", content: <实际文本> }`
  - `audio`: `{ voice: <音色>, format: "mp3" }`
- curl POST → jq 提取 `choices[0].message.audio.data` → base64 -d 写到输出文件
- voice 参数映射到 `audio.voice`（默认 `mimo_default`）

设计考虑：
- 抄 `openai.sh` 起手（同是 curl + jq 架构），但处理 base64 回包而非直接 -o
- 风格指令用固定默认值（自然平实），不暴露给用户 — 保持简单
- 用户可通过 `--voice=音色名` 切换音色

### 2. 修改：`references/AUDIO.md`

| 改点 | 内容 |
|------|------|
| § 内置 provider 表 | 加第 3 行 `mimo`：MiMo-V2.5-TTS / `MIMO_API_KEY` / 中文音色丰富，免费试用 |
| § 2.C 后加新小节 | **§ 2.C MiMo 合成**：用法示例（`MIMO_API_KEY=xxx PRESENTATION_TTS=mimo npm run synthesize-audio`）、env 变量表（`MIMO_API_KEY` 必选 / `MIMO_BASE_URL` 可选） |
| § 故障排查 | 加一行 MiMo 专属：`API key 格式不对 / base64 解码失败 / 文本超限` |
| § 退化路径 | 加到选项列表 |

### 3. 修改：`templates/scripts/tts-providers/README.md`

| 改点 | 内容 |
|------|------|
| § 内置 provider 表 | 加第 3 行 `mimo.sh`：MiMo-V2.5-TTS / `MIMO_API_KEY` / OpenAI 兼容 chat 接口，base64 回包 |
| § 设计要点 | 第 3 条 mp3 输出附注：如果 provider 返回 JSON+base64（如 MiMo），需在函数内解码 |
| § / 可选项 | 在"现成片段"区后或单独一段放 MiMo 的参考实现简述（指向 `mimo.sh` 本身） |

### 4. 修改：`SKILL.md`

| 改点 | 内容 |
|------|------|
| 文件树 (§ Phase 2.1) | `├── mimo.sh` 加到 tts-providers/ 列表，"内置 2 个" → "内置 3 个" |
| 音频合成段落 | 内置 provider 列表加 `mimo` 描述 |
| 相关链接 | 加平台链接 platform.xiaomimimo.com |

---

## 不动的文件

- `synthesize-audio.sh` — provider-agnostic runner，不需要改
- `extract-narrations.ts` — 只处理 narrations.ts 到 segments，无关
- `minimax.sh` / `openai.sh` — 不动
- 所有主题文件 / 章节模板 / 组件 — 无关

---

## 实现顺序

1. 写 `mimo.sh`（新 provider）
2. 改 `templates/scripts/tts-providers/README.md`
3. 改 `references/AUDIO.md`
4. 改 `SKILL.md`
5. 清零复查：全文搜索 `minimax` / `openai` 看有无遗漏的"内置 2 个"字眼
