#!/usr/bin/env bash
# ────────────────────────────────────────────────────────────────────
# MiMo-V2.5-TTS-VoiceClone provider — voice cloning variant.
#
# Docs:   https://platform.xiaomimimo.com
# Env:    MIMO_API_KEY=...            required
#         MIMO_BASE_URL=...           optional (default: https://api.xiaomimimo.com/v1)
#         MIMO_SAMPLE_DIR=...         optional (default: audio-samples/)
# Model:  mimo-v2.5-tts-voiceclone
#
# Unlike the basic mimo provider (which selects a built-in voice), this
# one uses a reference audio sample for voice cloning. The reference audio
# must be placed in MIMO_SAMPLE_DIR and is referenced by --voice=<name>
# or PRESENTATION_TTS_VOICE=<name> (without extension).
#
# Sample files searched: <voice>.mp3 → <voice>.wav
# Default voice name:    default-sample
#
# Example setup:
#   mkdir -p audio-samples
#   # put your sample in audio-samples/my-voice.mp3
#   MIMO_API_KEY=xxx PRESENTATION_TTS=mimo-voiceclone \
#     npm run synthesize-audio -- --voice=my-voice
# ────────────────────────────────────────────────────────────────────

tts_check() {
  if ! command -v curl >/dev/null; then
    echo "✗ curl not found in PATH." >&2
    return 1
  fi
  if ! command -v jq >/dev/null; then
    echo "✗ jq is required to extract base64 audio from the JSON response." >&2
    return 1
  fi
  if ! command -v base64 >/dev/null; then
    echo "✗ base64 is required to encode/decode audio payloads." >&2
    return 1
  fi
  if [[ -z "${MIMO_API_KEY:-}" ]]; then
    echo "✗ MIMO_API_KEY is not set." >&2
    return 1
  fi
}

tts_install_help() {
  cat <<'EOF' >&2
To use the MiMo-V2.5-TTS-VoiceClone provider:

  1. Set your API key:  export MIMO_API_KEY=...
                         (get one at https://platform.xiaomimimo.com)

  2. Prepare sample audio: place .mp3 or .wav files in audio-samples/
     (or set MIMO_SAMPLE_DIR to a custom path).

  3. Run synthesis, referencing the sample by name:
       PRESENTATION_TTS=mimo-voiceclone npm run synthesize-audio \
         -- --voice=my-sample-name

Optional:
  MIMO_BASE_URL=https://token-plan-cn.xiaomimimo.com/v1
  MIMO_SAMPLE_DIR=/absolute/path/to/samples

Install deps (only if missing):
  curl    — brew install curl    / apt-get install curl
  jq      — brew install jq      / apt-get install jq
  base64  — built-in on most systems (brew install coreutils if on macOS)

Or pick another provider:  PRESENTATION_TTS=<name> npm run synthesize-audio
EOF
}

tts_synthesize() {
  local text="$1"
  local out="$2"
  local voice="${3:-}"
  [[ -z "$voice" ]] && voice="default-sample"

  local base="${MIMO_BASE_URL:-https://api.xiaomimimo.com/v1}"
  local sample_dir="${MIMO_SAMPLE_DIR:-audio-samples}"

  # ── Resolve the reference audio file ──────────────────────────────
  local sample_file="$sample_dir/$voice.mp3"
  [[ -f "$sample_file" ]] || sample_file="$sample_dir/$voice.wav"
  if [[ ! -f "$sample_file" ]]; then
    echo "✗ voice sample not found: $sample_dir/$voice.{mp3,wav}" >&2
    return 1
  fi

  # ── Base64-encode the sample ──────────────────────────────────────
  local input_audio
  input_audio=$(base64 < "$sample_file" | tr -d '\n') || {
    echo "✗ failed to base64-encode sample: $sample_file" >&2
    return 1
  }

  # ── Build request payload ─────────────────────────────────────────
  # VoiceClone uses the same chat-completions envelope as the basic
  # mimo provider, but with input_audio instead of voice; the model
  # derives the timbre from the reference audio.
  local payload
  payload=$(jq -n \
    --arg t "$text" \
    --arg a "$input_audio" \
    '{
      model: "mimo-v2.5-tts-voiceclone",
      messages: [
        {role: "user",      content: "请模仿这个人的声音朗读"},
        {role: "assistant", content: $t}
      ],
      audio: {
        format: "mp3",
        input_audio: $a
      }
    }')

  # ── Synthesize ────────────────────────────────────────────────────
  curl -fsS -X POST "$base/chat/completions" \
    -H "api-key: $MIMO_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$payload" 2>/dev/null \
    | jq -r '.choices[0].message.audio.data' \
    | base64 -d > "$out"
}
