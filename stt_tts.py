import tempfile
import logging

# Whisper load
try:
    import whisper
    WHISPER = whisper
except Exception:
    WHISPER = None

# gTTS load
try:
    from gtts import gTTS
    GTTS = gTTS
except Exception:
    GTTS = None

_whisper_model = None

if WHISPER is not None:
    try:
        _whisper_model = WHISPER.load_model("tiny")
    except Exception as e:
        logging.error(f"Whisper load failed: {e}")

def transcribe_audio(path):
    """Speech-to-text using Whisper."""
    if _whisper_model is None:
        return "(Whisper unavailable)"

    try:
        result = _whisper_model.transcribe(path)
        return result.get("text", "")
    except Exception as e:
        logging.error(f"Transcription error: {e}")
        return "(transcription failed)"

def tts_save(text):
    """Text-to-speech using gTTS."""
    if GTTS is None:
        return None

    try:
        t = GTTS(text)
        temp_path = tempfile.mktemp(".mp3")
        t.save(temp_path)
        return temp_path
    except Exception as e:
        logging.error(f"TTS error: {e}")
        return None