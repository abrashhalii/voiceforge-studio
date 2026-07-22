"""
Centralized configuration for Voice Studio.
All values are read from environment variables (.env file) with sensible
defaults, so the app runs identically on Windows, Linux, and inside Docker.
"""
import os
import sys
import shutil
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


def _path(env_key: str, default_subdir: str) -> str:
    """Resolve a directory from env, falling back to a folder next to the app."""
    value = os.getenv(env_key)
    return str(Path(value)) if value else str(BASE_DIR / default_subdir)


def _resolve_executable(name: str) -> str:
    """
    Find a CLI tool cross-platform.
    Order: PATH -> the running interpreter's Scripts/bin folder.
    Works on Windows (.exe) and Linux (no extension) without hardcoding.
    """
    found = shutil.which(name)
    if found:
        return found
    bin_dir = Path(sys.executable).parent
    for candidate in (bin_dir / name, bin_dir / f"{name}.exe"):
        if candidate.exists():
            return str(candidate)
    return name  # let subprocess raise a clear error if truly missing


# ─── Directories ───
SAVED_VOICES_DIR = _path("SAVED_VOICES_DIR", "saved_voices")
TRAINING_DIR     = _path("TRAINING_DIR", "training_data")
TEMP_DIR         = _path("TEMP_DIR", "temp")
HF_CACHE_DIR     = _path("HF_CACHE_DIR", "hf_cache")
RVC_MODELS_DIR   = _path("RVC_MODELS_DIR", "rvc_models")
RAW_AUDIO_DIR    = _path("RAW_AUDIO_DIR", "raw_audio")

# ─── Executables ───
EDGE_TTS_EXE     = os.getenv("EDGE_TTS_EXE")  or _resolve_executable("edge-tts")
F5_TTS_EXE       = os.getenv("F5_TTS_EXE")    or _resolve_executable("f5-tts_infer-cli")
RVC_PYTHON_EXE   = os.getenv("RVC_PYTHON_EXE") or sys.executable
RVC_INFER_SCRIPT = str(BASE_DIR / "rvc_infer.py")

# ─── Inference settings ───
DEVICE               = os.getenv("DEVICE", "cuda")
REF_AUDIO_MAX_SEC    = int(os.getenv("REF_AUDIO_MAX_SEC", "8"))
F5_TIMEOUT_SEC       = int(os.getenv("F5_TIMEOUT_SEC", "600"))
F5_NFE_STEP   = int(os.getenv("F5_NFE_STEP", "16"))
F5_SPEED      = float(os.getenv("F5_SPEED", "1.0"))
F5_CROSS_FADE = float(os.getenv("F5_CROSS_FADE", "0.15"))
F5_FORCE_FP32 = os.getenv("F5_FORCE_FP32", "true").lower() == "true"

# ─── Podcast settings ───
DEFAULT_PAUSE_MS     = int(os.getenv("DEFAULT_PAUSE_MS", "500"))
CROSSFADE_MS         = int(os.getenv("CROSSFADE_MS", "120"))

# ─── Training pipeline settings ───
CHUNK_SECONDS        = int(os.getenv("CHUNK_SECONDS", "10"))
NORMALIZE_DBFS       = float(os.getenv("NORMALIZE_DBFS", "-20.0"))
SILENCE_THRESH_DB    = float(os.getenv("SILENCE_THRESH_DB", "-40.0"))
MIN_SILENCE_LEN_MS   = int(os.getenv("MIN_SILENCE_LEN_MS", "500"))
KEEP_SILENCE_MS      = int(os.getenv("KEEP_SILENCE_MS", "150"))
NOISE_REDUCTION_AMT  = float(os.getenv("NOISE_REDUCTION_AMT", "0.75"))

# ─── Server settings ───
SERVER_NAME          = os.getenv("SERVER_NAME", "127.0.0.1")
SERVER_PORT          = int(os.getenv("SERVER_PORT", "7860"))
SHARE                = os.getenv("SHARE", "false").lower() == "true"

# Ensure required directories exist
for d in (SAVED_VOICES_DIR, TRAINING_DIR, TEMP_DIR, RVC_MODELS_DIR):
    os.makedirs(d, exist_ok=True)