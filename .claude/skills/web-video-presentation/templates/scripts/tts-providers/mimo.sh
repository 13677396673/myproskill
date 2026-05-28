#!/usr/bin/env bash
# ────────────────────────────────────────────────────────────────────
# MiMo-V2.5-TTS provider — uses Xiaomi's chat-completions-based TTS API.
#
# Docs:  https://platform.xiaomimimo.com
# Env:   MIMO_API_KEY=...          required (get at platform.xiaomimimo.com)
#        MIMO_BASE_URL=...         optional (default: https://api.xiaomimimo.com/v1)
# Model: mimo-v2.5-tts
# Voices: mimo_default, 冰糖, 茉莉, 苏打, 白桦, Mia, Chloe, ...
#         (default: mimo_default)
#
# Unlike minimax (CLI-based) and openai (dedicated TTS REST endpoint),
# MiMo uses OpenAI-compatible chat completions and returns base64 audio
# in a JSON envelope. Response must be piped through jq + base64 rather
# than written directly with curl -o.
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
    echo "✗ base64 is required to decode the audio payload." >&2
    return 1
  fi
  if [[ -z "${MIMO_API_KEY:-}" ]]; then
    echo "✗ MIMO_API_KEY is not set." >&2
    return 1
  fi
}

tts_install_help() {
  cat <<'EOF' >&2
To use the MiMo-V2.5-TTS provider:

  1. Set your API key — two ways:
       export MIMO_API_KEY=...               # via env var
       echo "MIMO_API_KEY=..." >> .env        # or via .env in presentation/
     (get one at https://platform.xiaomimimo.com)

  Optional:          export MIMO_BASE_URL=https://token-plan-cn.xiaomimimo.com/v1

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
  [[ -z "$voice" ]] && voice="mimo_default"

  local base="${MIMO_BASE_URL:-https://api.xiaomimimo.com/v1}"

  # MiMo uses a chat-completions-style request:
  #   messages[0] (user)      = style/tone instruction
  #   messages[1] (assistant) = the text to synthesize
  local payload
  payload=$(jq -n \
    --arg t "$text" \
    --arg v "$voice" \
    '{
      model: "mimo-v2.5-tts",
      messages: [
        {role: "user",      content: "用自然平实的语调朗读"},
        {role: "assistant", content: $t}
      ],
      audio: {
        voice: $v,
        format: "mp3"
      }
    }')

  # curl → jq extracts the base64 payload → base64 decodes to mp3
  # If curl returns an error, jq gets empty stdin and fails;
  # if the JSON is malformed, jq fails;
  # all three exit non-zero (runner has pipefail), so FAILED is marked.
  curl -fsS -X POST "$base/chat/completions" \
    -H "api-key: $MIMO_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$payload" 2>/dev/null \
    | jq -r '.choices[0].message.audio.data' \
    | base64 -d > "$out"
}
