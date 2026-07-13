import sys
import os
import json

def transcribe_audio(audio_path):
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("WHISPER_API_KEY")
    key_source = "OPENAI_API_KEY" if os.environ.get("OPENAI_API_KEY") else "WHISPER_API_KEY" if api_key else None
    if not api_key:
        print(json.dumps({
            "error": "No OpenAI API Key found",
            "message": "Set OPENAI_API_KEY (recommended, reusable with your chat) or WHISPER_API_KEY. Example: $env:OPENAI_API_KEY = 'sk-xxx'"
        }, ensure_ascii=False))
        sys.exit(1)

    if not os.path.exists(audio_path):
        print(json.dumps({
            "error": "File not found",
            "message": f"Audio file not found: {audio_path}"
        }, ensure_ascii=False))
        sys.exit(1)

    file_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
    if file_size_mb > 25:
        print(json.dumps({
            "error": "File too large",
            "message": f"File size {file_size_mb:.1f}MB exceeds 25MB limit. Please split the audio into smaller segments.",
            "file_size_mb": round(file_size_mb, 1)
        }, ensure_ascii=False))
        sys.exit(1)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        with open(audio_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="verbose_json",
                timestamp_grants="segment"
            )
    except Exception as e:
        print(json.dumps({
            "error": "Whisper API call failed",
            "message": str(e)
        }, ensure_ascii=False))
        sys.exit(1)

    segments = []
    if hasattr(transcript, 'segments') and transcript.segments:
        for seg in transcript.segments:
            segments.append({
                "start": round(seg.start, 2),
                "end": round(seg.end, 2),
                "text": seg.text.strip()
            })

    full_text = transcript.text.strip() if hasattr(transcript, 'text') else ""

    result = {
        "full_text": full_text,
        "segments": segments,
        "duration_seconds": round(segments[-1]["end"], 2) if segments else 0,
        "language": getattr(transcript, 'language', 'unknown')
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "No audio file path provided",
            "message": "Usage: python transcribe.py <audio_file_path>"
        }, ensure_ascii=False))
        sys.exit(1)

    transcribe_audio(sys.argv[1])
