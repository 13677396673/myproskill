"""MiMo VoiceClone synthesis helper — reads sample file directly."""

import json
import urllib.request
import base64
import sys
import os

def main():
    text = sys.argv[1]
    out_path = sys.argv[2]
    api_key = sys.argv[3]
    base_url = sys.argv[4]
    sample_file = sys.argv[5]


    # Read and encode the reference audio sample directly
    with open(sample_file, "rb") as f:
        voice_bytes = f.read()
    voice_b64 = base64.b64encode(voice_bytes).decode("ascii")

    # Per official MiMo VoiceClone API docs
    voice_data_url = f"data:audio/mpeg;base64,{voice_b64}"
    payload = {
        "model": "mimo-v2.5-tts-voiceclone",
        "messages": [
            {"role": "user", "content": ""},
            {"role": "assistant", "content": text},
        ],
        "audio": {
            "format": "mp3",
            "voice": voice_data_url,
        },
    }

    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "api-key": api_key,
            "Content-Type": "application/json",
        },
    )

    try:
        resp = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code} error: {body[:500]}", file=sys.stderr)
        raise

    audio_b64 = resp["choices"][0]["message"]["audio"]["data"]
    with open(out_path, "wb") as f:
        f.write(base64.b64decode(audio_b64))

if __name__ == "__main__":
    main()
