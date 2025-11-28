# summarizer_agent.py — Summarization functionality

from tools.summarizer_engine import extractive_summary

def summarizer_agent(task):
    text = task.get("text", "")
    max_sentences = task.get("max_sentences", 3)

    return {
        "summary": extractive_summary(text, max_sentences)
    }