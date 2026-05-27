# 音频合成

把每个章节 `narrations.ts` 里的口播文字按 **step 颗粒度**合成 mp3，
落到 `presentation/public/audio/<chapter-id>/<step-N>.mp3`。运行时
Auto 模式会自动按 step 播放并自动推进——录屏可以一镜到底。

> **真相源**：每个章节的 `src/chapters/<NN>-<id>/narrations.ts` 是 step
> 数 + 口播文本的**唯一来源**。`outline.md` 不再参与音频合成，章节代码
> 也不再手写 `totalSteps`。这一改根除了"网页 step 和音频文件数对不上"
> 这个老问题。

合成器是 **provider-agnostic** 的：runner 本身不绑定任何 TTS 后端，每个
后端是 `scripts/tts-providers/<name>.sh` 一个文件。**内置 4 个 provider**：

| Provider | 默认 | 何时用 |
|---|---|---|
| `minimax` | ✓ | 中文口播首选（用 `mmx-cli`，要 MiniMax API key） |
| `openai`  | —— | 多数 agent 已有 `OPENAI_API_KEY`；curl-based、响应快 |
| `mimo`    | —— | 小米 MiMo-V2.5-TTS；chat-completions 接口，base64 回包；中文音色丰富，免费试用 |
| `mimo-voiceclone` | —— | 小米 MiMo-V2.5-TTS 音色克隆；需参考音频样本，与 `mimo` 同 API key |

换 / 加 provider 见
[`scripts/tts-providers/README.md`](../templates/scripts/tts-providers/README.md)
（脚手架跑完后路径是 `presentation/scripts/tts-providers/README.md`）。
README 里还附了 5 套**可粘贴**的现成片段（ElevenLabs / edge-tts / macOS say /
Azure / Google Cloud）和写自定义 provider 的三函数契约。

---

## 文件命名约定

```
presentation/public/audio/
├── coldopen/
│   ├── 1.mp3
│   ├── 2.mp3
│   └── ...
├── hook/
│   └── ...
└── ...
```

- 章节子目录名 = `chapters.ts` 里的 `id`
- 文件名 = `<step-N>.mp3`（**1-indexed**，对齐 narrations 数组的 index + 1）
- 格式默认 mp3。如果你写的 provider 只能出 wav，在函数里加一步 `ffmpeg`
  转 mp3（参见 `tts-providers/README.md` 的 `say.sh` 示例）

---

## 标准流程

### 1. 抽取 segments

```bash
cd presentation
npm run extract-narrations
```

这会扫所有章节的 `narrations.ts`，按 `chapters.ts` 注册顺序生成
`audio-segments.json`：

```json
[
  { "chapter": "coldopen", "step": 1, "text": "...", "audio": "coldopen/1.mp3" },
  { "chapter": "coldopen", "step": 2, "text": "...", "audio": "coldopen/2.mp3" },
  ...
]
```

让用户**先扫一眼这个 json**，确认文本和切分都对，再开始烧 token 合成。

> 空字符串的 narration 会被自动跳过（不烧 TTS token）——运行时 Auto 模式
> 按字数估时撑过这种"无声过场"step。

### 2. 选 provider

```bash
ls scripts/tts-providers/    # 看本项目带了哪些
```

- 用默认 `minimax` → 走 [2.A](#2a-用内置-minimax-合成)
- 用内置 `openai` → 走 [2.B](#2b-用内置-openai-合成)
- 用内置 `mimo`（基础 TTS）→ 走 [2.C](#2c-用内置-mimo-合成基础-tts)
- 用内置 `mimo-voiceclone`（音色克隆）→ 走 [2.C.i](#2ci-用内置-mimo-voiceclone-合成音色克隆)
- 想用别的 TTS / 自带 TTS → 走 [2.D](#2d-换-provider--加自定义-provider)
- 一个都没装好 → 走 [2.E](#2e-退化路径)

#### 2.A 用内置 minimax 合成

```bash
npm run synthesize-audio              # 增量：跳过已存在的 mp3
npm run synthesize-audio -- --force   # 全部重合成
npm run synthesize-audio -- --voice=<voice-id>  # 指定音色
```

启动时 runner 会先调 provider 的 `tts_check`：

- mmx 未安装 → 报 `mmx CLI not found in PATH`，并打印安装说明
- mmx 未登录 → 报 `mmx is not authenticated`，并提示登录命令

修完再跑。每条段打印进度：

```
[  3/24] coldopen/3.mp3   ✓ 4s
[  4/24] coldopen/4.mp3   skip (exists)
```

合成串行（避免 rate limit），**自动跳过已存在文件**（断点续合，不烧
重复 token）。

#### 2.B 用内置 openai 合成

```bash
export OPENAI_API_KEY=sk-...                   # 在 platform.openai.com 拿
PRESENTATION_TTS=openai npm run synthesize-audio
# 换音色 + HD 模型
OPENAI_TTS_MODEL=tts-1-hd PRESENTATION_TTS=openai \
  npm run synthesize-audio -- --voice=nova
```

可选 env：

| 变量 | 默认 | 作用 |
|---|---|---|
| `OPENAI_API_KEY` | —— **必须** | API key |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | 切代理 / Azure-OpenAI |
| `OPENAI_TTS_MODEL` | `tts-1` | `tts-1` 快 / `tts-1-hd` 高质量约 2× 价 |
| `--voice=` / `PRESENTATION_TTS_VOICE` | `alloy` | 可选 alloy / echo / fable / onyx / nova / shimmer |

`tts_check` 会检查 curl / jq / `OPENAI_API_KEY` 三件套，缺哪个报哪个。

#### 2.C 用内置 MiMo 合成（基础 TTS）

```bash
export MIMO_API_KEY=mimo_xxx...                         # 在 platform.xiaomimimo.com 获取
PRESENTATION_TTS=mimo npm run synthesize-audio
# 换音色
PRESENTATION_TTS=mimo npm run synthesize-audio -- --voice=冰糖
```

可选 env：

| 变量 | 默认 | 作用 |
|---|---|---|
| `MIMO_API_KEY` | —— **必须** | API key（从 platform.xiaomimimo.com 获取） |
| `MIMO_BASE_URL` | `https://api.xiaomimimo.com/v1` | 可选，中国区 token-plan 用户可换成 `https://token-plan-cn.xiaomimimo.com/v1` |
| `--voice=` / `PRESENTATION_TTS_VOICE` | `mimo_default` | 预置音色：`冰糖`、`茉莉`、`苏打`、`白桦`、`Mia`、`Chloe` |

`tts_check` 会检查 curl / jq / base64 / `MIMO_API_KEY` 四件套，缺哪个报哪个。

> **MiMo 特殊之处**：它走 OpenAI 兼容的 chat completions 端点而非专用 TTS API，
> 响应体是 JSON（base64 编码的音频在 `choices[0].message.audio.data`），
> 并非直接返回音频流。`mimo.sh` 内部通过 `curl | jq | base64 -d` 管道
> 自动处理解码，对用户透明。

#### 2.C.i 用内置 MiMo VoiceClone 合成（音色克隆）

VoiceClone 用一段参考音频样本克隆音色，而不是从预置音色列表里选。

先准备样本文件：

```bash
mkdir -p audio-samples
# 把参考音频放进去（.mp3 或 .wav）
# 目录结构：
#   audio-samples/
#   ├── my-voice.mp3
#   └── narrator-female.wav
```

合成：

```bash
export MIMO_API_KEY=mimo_xxx...
# 使用 audio-samples/my-voice.mp3 作为参考音色
PRESENTATION_TTS=mimo-voiceclone npm run synthesize-audio -- --voice=my-voice
# 换一个样本
PRESENTATION_TTS=mimo-voiceclone npm run synthesize-audio -- --voice=narrator-female
```

可选 env：

| 变量 | 默认 | 作用 |
|---|---|---|
| `MIMO_API_KEY` | —— **必须** | API key（与基础 MiMo 共用） |
| `MIMO_BASE_URL` | `https://api.xiaomimimo.com/v1` | 可选 |
| `MIMO_SAMPLE_DIR` | `audio-samples/` | 参考音频目录路径 |
| `--voice=` / `PRESENTATION_TTS_VOICE` | `default-sample` | 样本文件名（不含扩展名） |

`tts_check` 会检查 curl / jq / base64 / `MIMO_API_KEY` 四件套。

> **VoiceClone 特殊之处**：它在请求体里用 `input_audio` 字段（base64 编码的
> 参考音频），而不是 `voice` 字段。`--voice` 参数在 VoiceClone 中的语义是
> "在 `MIMO_SAMPLE_DIR` 里找哪个样本文件"，而非选择预置音色。
> 参考音频建议 5~30 秒，单人声、无背景噪音，格式 mp3 或 wav。单文件上限
> 10MB。

#### 2.D 换 provider / 加自定义 provider

内置之外的常见后端在 `scripts/tts-providers/README.md` 里有 5 段
**可粘贴**代码片段（ElevenLabs / edge-tts / macOS `say` / Azure / Google
Cloud）。

挑一个 → 复制 README 里的代码块 → 保存为
`scripts/tts-providers/<name>.sh` → 设好环境变量 → 切换 provider 跑：

```bash
PRESENTATION_TTS=elevenlabs npm run synthesize-audio
# 或
npm run synthesize-audio -- --provider=edge-tts
```

如果用户的 TTS 完全自研，**按三函数契约**写一个 `<name>.sh` 即可：

| 函数 | 必需 | 作用 |
|---|---|---|
| `tts_synthesize <text> <out_path> [<voice>]` | ✓ | 把一段文字写成 mp3 到指定路径 |
| `tts_check` | 可选 | 启动时校验环境（CLI / key / auth），未就绪 return 非零 |
| `tts_install_help` | 可选 | `tts_check` 失败时打印怎么修 |

抄 `openai.sh`（HTTP-based）或 `minimax.sh`（CLI-based）起手最快。
详细规范在 `scripts/tts-providers/README.md`。

#### 2.E 退化路径

如果所有内置 provider 都没就绪（没装 mmx / 没有 OpenAI key / 没有 MiMo key）告诉用户：

```
我可以：

  1. 用内置 openai provider（如果你已有 OpenAI key）
     export OPENAI_API_KEY=sk-...
     PRESENTATION_TTS=openai npm run synthesize-audio

  2. 用内置 MiMo provider（如果你有小米 MiMo API key）
     基础 TTS:  PRESENTATION_TTS=mimo npm run synthesize-audio
     音色克隆:  PRESENTATION_TTS=mimo-voiceclone npm run synthesize-audio -- --voice=样本名
     API key 在 https://platform.xiaomimimo.com 获取

  3. 帮你装 MiniMax CLI（默认 provider，中文音色更稳）
     npm install -g mmx-cli && mmx auth login --api-key sk-xxxxx
     API key 在 https://platform.minimaxi.com 获取

  4. 换其它 provider
     scripts/tts-providers/README.md 里有 5 种现成代码片段：
       • ElevenLabs  (要 ELEVENLABS_API_KEY，英文音色最佳)
       • edge-tts    (免费 / 无 key / pip install edge-tts)
       • macOS say   (零依赖离线，质量一般，适合预览)
       • Azure       (要 AZURE_SPEECH_KEY)
       • Google      (要 gcloud auth)
     复制一段保存成 tts-providers/<name>.sh，
     再 PRESENTATION_TTS=<name> npm run synthesize-audio

  5. 暂时跳过
     稿子和 narrations 都在，你自己用任意 TTS 录制即可——文件
     按 audio-segments.json 的 audio 字段命名就行。
```

不要假装合成成功。

---

## 校验时长

合成完后跑：

```bash
for f in public/audio/*/*.mp3; do
  d=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$f")
  echo "$f  ${d}s"
done
```

把每条的实际秒数汇总告诉用户。**重点关注 ≥ 15s 的条目**——口播太长意味
着该 step 的 narration 写得过密，或者 step 没拆够。让用户决定**改稿子
重合**还是**回章节代码拆 step**。

---

## 运行时如何使用合成的音频

合成完成后，**不需要任何额外配置**——脚手架的 `App.tsx` 已经接好：

| 模式 | 触发方式 | 行为 |
|---|---|---|
| **Manual**（默认） | 直接打开页面 | 不播音频，点击 / 方向键推进 |
| **Audio**（半自动） | URL `?audio=1` 或按 `M` 键 | 进入 step 自动播音频，但你手动推进（点鼠标） |
| **Auto**（全自动） | URL `?auto=1` 或按两次 `M` 键 | 进入 step 播音频 → 播完自动 next() → 进下个 step → ... |

Auto 模式首次需要按一次 `Space` 启动（绕过浏览器自动播放限制），之后
全自动跑。**录屏时打开屏幕录制 → 按 Space → 整片自动跑完 → stop**。

> **Auto 模式的推进规则就一句话**：每段音频播完 + 200ms 缓冲 → 自动 next。
> **没有"等动画跑完"的兜底**——如果你写的视觉动画比口播长，会被当场切。
> 解决办法：写更长口播 / 拆 step / 调动画速度（详见
> [`CHAPTER-CRAFT.md`](CHAPTER-CRAFT.md) 「代码层最小约束」）。
>
> 音频文件缺失（还没合成 / 404）或 narration 是空串 → 退化到字数估时
> （`max(1500ms, 字数 × 250ms)`），保证预览也能整片跑通。

---

## 故障排查

通用：

| 现象 | 原因 / 修法 |
|---|---|
| `chapter id "X" registered but no matching folder found` | 章节文件夹应命名为 `NN-<id>`；id 必须等于 chapters.ts 里注册的 |
| `narrations.ts in X must export an array named "narrations"` | 该章节的 narrations.ts 没 export 名为 narrations 的数组 |
| `TTS provider 'X' not found` | `scripts/tts-providers/X.sh` 不存在；列出来看哪些可用，或抄 README 加一个 |
| `provider 'X' does not define tts_synthesize` | 你的 `<X>.sh` 没定义必需的函数。看 README 的契约部分 |
| 中间断了几条没合成 | `npm run synthesize-audio` 重跑 —— 已存在文件会跳过 |
| 浏览器没播音频 | Auto / Audio 模式下首次需要用户手势——确认你按了 SPACE 启动 Auto，或者点过页面 |
| 音频 404 但 Auto 模式还能跑 | 找不到 mp3 时 useAudioPlayer 退化到字数估时（4 字/秒），保证预览不中断 |

minimax 专属：

| 现象 | 原因 / 修法 |
|---|---|
| `mmx: command not found` | `npm install -g mmx-cli`；npm 全局 bin 不在 PATH 时 `npm config get prefix` 看一下 |
| `mmx is not authenticated` | `mmx auth login --api-key sk-xxxxx` 重新登录 |
| 中文音色不自然 | mmx 默认音色未必最佳；查 `mmx speech --help` 看 `--voice` 可选项，传 `--voice=<id>` |
| 整段合成被截断 | 单段过长（mmx 默认上限约 5000 字符）。在 narrations.ts 里把这条拆成两条（也意味着该 step 应该拆成两个 step） |

openai 专属：

| 现象 | 原因 / 修法 |
|---|---|
| `OPENAI_API_KEY is not set` | `export OPENAI_API_KEY=sk-...`，或者把它加到 shell rc / `.env` |
| 全部段 FAILED + key 是对的 | 多半 model / voice 名字错。`--voice=alloy` 试默认值；`OPENAI_TTS_MODEL=tts-1` 试默认模型；用 `bash -x scripts/synthesize-audio.sh` 看请求体 |
| 走代理 / 走 Azure-OpenAI | `export OPENAI_BASE_URL=https://your-proxy/v1` |
| HD 太慢 | 改成 `OPENAI_TTS_MODEL=tts-1`（默认）；HD 大约慢 2 倍 |
| 中文音色不像真人 | OpenAI 6 种音色都是英语偏向；中文角色用 `minimax` 或 `mimo` 更合适 |

mimo 专属：

| 现象 | 原因 / 修法 |
|---|---|
| `MIMO_API_KEY is not set` | `export MIMO_API_KEY=...`，key 在 https://platform.xiaomimimo.com 获取 |
| 全部段 FAILED + key 是对的 | 检查 `MIMO_BASE_URL` 是否正确（中国区 token-plan 用 `https://token-plan-cn.xiaomimimo.com/v1`）；用 `bash -x scripts/synthesize-audio.sh` 看响应体 |
| `base64: invalid input` | API 返回了非 JSON 响应（多半网络问题或 key 无效）。`bash -x` 看原始响应 |
| 合成的 mp3 是空文件或损坏 | 同上 —— `jq` 可能没找到 `choices[0].message.audio.data`，`base64` 解码了 "null" 字符串。检查 API key 和响应结构 |

mimo-voiceclone 专属：

| 现象 | 原因 / 修法 |
|---|---|
| `voice sample not found: ...` | 在 `MIMO_SAMPLE_DIR`（默认 `audio-samples/`）里没找到 `--voice` 指定文件。确认文件名正确，且格式为 `.mp3` 或 `.wav` |
| `failed to base64-encode sample` | 样本文件存在但读取失败。检查文件权限和路径 |
| 合成结果声音不对（不是样本音色） | 参考音频质量差。建议 5~30 秒干净人声，无背景噪音，单声道为佳 |
| 全部段 FAILED + 样本文件存在 | 可能参考音频超 10MB 上限。用 `ffprobe` 或 `ls -lh` 检查文件大小 |

换其它（自定义）provider 之后：

| 现象 | 原因 / 修法 |
|---|---|
| `<X>_API_KEY not set` | 你的 provider 需要 API key，但 env 里没设。`export <X>_API_KEY=...` 或写到 `.env` 再 `set -a; source .env; set +a` |
| 合成的 mp3 浏览器播不了 | 检查 provider 是否真的出了 mp3（不是 wav / opus / aac）。`file public/audio/*/*.mp3` 看 magic header |
| 一切看起来都对，但全部 FAILED | `bash -x scripts/synthesize-audio.sh` 看每段实际调了什么 |

---

## 相关链接

- Provider 契约 + 现成片段：[`scripts/tts-providers/README.md`](../templates/scripts/tts-providers/README.md)
- mmx-cli 仓库：<https://github.com/MiniMax-AI/cli>
- mmx 官方文档：<https://platform.minimaxi.com/docs/token-plan/minimax-cli>
- mmx 参数 / 音色查询：`mmx speech --help`
