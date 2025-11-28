# quiz_agent.py — Creates quiz questions from text

from tools.summarizer_engine import heuristic_quiz

def quiz_agent(task):
    text = task.get("text", "")
    n = int(task.get("n", 5))

    return {
        "quiz": heuristic_quiz(text, n)
    }