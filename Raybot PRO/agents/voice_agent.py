# voice_agent.py — Voice (Speech-to-Text & Text-to-Speech)

from tools.stt_tts import transcribe_audio, tts_save

def voice_agent(task):
    action = task.get("action", "transcribe")

    if action == "transcribe":
        file_path = task.get("path")
        return {"transcript": transcribe_audio(file_path)}

    if action == "tts":
        text = task.get("text", "")
        return {"tts_path": tts_save(text)}

    return {"error": "Unknown action in voice agent"}