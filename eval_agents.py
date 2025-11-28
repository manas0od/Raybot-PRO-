"""
tests/eval_agents.py

Simple offline-safe test suite for Raybot PRO's agents.
Run with:
    python tests/eval_agents.py
"""

import json
import sys
import os
sys.path.append(".")

# Import your components
from agents.agent_manager import AgentManager
from agents.summarizer_agent import summarizer_agent
from agents.quiz_agent import quiz_agent
from agents.news_agent import news_agent
from agents.voice_agent import voice_agent
from agents.chat_agent import chat_agent_factory

# Fake minimal functions for STT/TTS so tests don’t require Whisper or gTTS
def fake_transcribe(path):
    return "(mock transcription)"

def fake_tts(text):
    return "/tmp/fake_tts.mp3"


def run_tests():
    print("=== Running Raybot PRO Agent Tests ===")

    # Init manager
    am = AgentManager()

    # Register agents
    am.register("summarizer", summarizer_agent)
    am.register("quiz", quiz_agent)
    am.register("news", news_agent)
    am.register("voice", voice_agent)

    # Chat agent (offline mode → pass None)
    chat_agent = chat_agent_factory(openai_client=None)
    am.register("chat", chat_agent)

    sample_text = (
        "Alice went to the market. She bought apples. "
        "Then she returned home and cooked an apple pie."
    )

    results = {}

    # Summarizer Test
    print("\n[1] Testing Summarizer Agent...")
    s = am.send_to("summarizer", {"text": sample_text, "max_sentences": 2})
    print("Summary:", s)
    results["summarizer"] = s

    # Quiz Agent
    print("\n[2] Testing Quiz Agent...")
    q = am.send_to("quiz", {"text": sample_text, "n": 3})
    print("Quiz:", json.dumps(q, indent=2))
    results["quiz"] = q

    # News Agent
    print("\n[3] Testing News Agent...")
    n = am.send_to("news", {"query": "indian"})
    print("News:", n)
    results["news"] = n

    # Voice Agent — tests structure (no Whisper/gTTS required)
    print("\n[4] Testing Voice Agent (mocked)...")
    v1 = am.send_to("voice", {"action": "transcribe", "path": "fake.wav"})
    v2 = am.send_to("voice", {"action": "tts", "text": "Hello"})
    print("Transcribe:", v1)
    print("TTS:", v2)
    results["voice"] = {"transcribe": v1, "tts": v2}

    # Chat Agent
    print("\n[5] Testing Chat Agent (offline fallback)...")
    c = am.send_to("chat", {"message": "Hello, what can you do?"})
    print("Chat reply:", c)
    results["chat"] = c

    print("\n=== ALL TESTS COMPLETED ===")
    print(json.dumps(results, indent=2))

    return results


if __name__ == "__main__":
    run_tests()


you can test this with : 

python tests/eval_agents.py