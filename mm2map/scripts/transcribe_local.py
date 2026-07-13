import sys
import os
import json

def transcribe_local(audio_path, model_size="base"):
    if not os.path.exists(audio_path):
        print(json.dumps({
            "error": "File not found",
            "message": f"Audio file not found: {audio_path}"
        }, ensure_ascii=False))
        sys.exit(1)

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print(json.dumps({
            "error": "faster-whisper not installed",
            "message": "Run: pip install faster-whisper, then reinstall via install_deps.ps1 -Install"
        }, ensure_ascii=False))
        sys.exit(1)

    model_sizes = {
        "tiny": "~75MB, fastest, lowest accuracy",
        "base": "~150MB, balanced speed/accuracy (recommended)",
        "small": "~500MB, good accuracy, slower",
        "medium": "~1.5GB, high accuracy, very slow",
        "large-v3": "~3GB, best accuracy, extremely slow"
    }

    if model_size not in model_sizes:
        print(json.dumps({
            "error": f"Invalid model size: {model_size}",
            "message": f"Available sizes: {', '.join(model_sizes.keys())}",
            "details": model_sizes
        }, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps({"status": "loading_model", "model_size": model_size}, ensure_ascii=False))
    sys.stdout.flush()

    try:
        compute_type = "int8" if not _has_gpu() else "float16"
        model = WhisperModel(model_size, device="cpu" if not _has_gpu() else "cuda", compute_type=compute_type)
    except Exception as e:
        print(json.dumps({
            "error": "Failed to load Whisper model",
            "message": str(e),
            "hint": "Try a smaller model size (tiny/base) or check disk space for model download"
        }, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps({"status": "transcribing", "file": audio_path}, ensure_ascii=False))
    sys.stdout.flush()

    try:
        segments_iter, info = model.transcribe(audio_path, beam_size=5, language=None)
        segments = []
        for seg in segments_iter:
            segments.append({
                "start": round(seg.start, 2),
                "end": round(seg.end, 2),
                "text": seg.text.strip()
            })

        full_text = " ".join(s["text"] for s in segments)

        result = {
            "full_text": full_text,
            "segments": segments,
            "duration_seconds": round(info.duration, 2) if info.duration else 0,
            "language": info.language if info.language else "unknown",
            "language_probability": round(info.language_probability, 2) if info.language_probability else 0,
            "model_size": model_size,
            "transcription_method": "local_faster_whisper"
        }

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({
            "error": "Transcription failed",
            "message": str(e),
            "hint": "For long audio (>30min), try a smaller model or split the file first"
        }, ensure_ascii=False))
        sys.exit(1)

def _has_gpu():
    try:
        import torch
        return torch.cuda.is_available()
    except ImportError:
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "No audio file path provided",
            "message": "Usage: python transcribe_local.py <audio_file_path> [model_size]",
            "model_sizes": ["tiny", "base (recommended)", "small", "medium", "large-v3"]
        }, ensure_ascii=False))
        sys.exit(1)

    audio_path = sys.argv[1]
    model_size = sys.argv[2] if len(sys.argv) > 2 else "base"

    transcribe_local(audio_path, model_size)
