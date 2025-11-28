import re
import random

stopwords = set(["the","and","is","in","to","of","a","it","for","on","with","as","are","was","were","be","by","this","an"])

# Offline fallback news
SAMPLE_NEWS = [
    {
        "title": "Indian Politics: New Reform Announcement",
        "body": "Government introduces several policy changes to improve infrastructure and digital access."
    },
    {
        "title": "Space Science: Rocket Launch Success",
        "body": "The national space agency completes a successful launch of its next-gen satellite vehicle."
    },
    {
        "title": "AI News: Massive Breakthrough",
        "body": "Researchers announce a new model capable of real-time reasoning on edge devices."
    }
]

def extractive_summary(text, max_sentences=3):
    """Simple keyword-based extractive summarizer."""
    text = (text or "").strip()
    if not text:
        return ""

    sentences = [s.strip() for s in re.split(r"(?<=[.!?]) +", text) if s.strip()]
    if len(sentences) <= max_sentences:
        return text

    words = re.findall(r"\w+", text.lower())
    freq = {}

    for w in words:
        if w not in stopwords:
            freq[w] = freq.get(w, 0) + 1

    score_map = {}
    for s in sentences:
        score = sum(freq.get(w.lower(), 0) for w in re.findall(r"\w+", s))
        score_map[s] = score

    best = sorted(score_map, key=score_map.get, reverse=True)[:max_sentences]
    return " ".join(best)

def heuristic_quiz(text, n=5):
    """Generates simple quiz questions from text."""
    sents = [s.strip() for s in re.split(r"(?<=[.!?]) +", text) if s.strip()]
    if not sents:
        return ["Cannot generate quiz — empty text"]

    questions = []

    for s in random.sample(sents, min(n, len(sents))):
        words = s.split()
        if len(words) < 4:
            continue

        blank_index = random.randint(1, len(words) - 2)
        answer = words[blank_index]
        words[blank_index] = "_____"
        q = " ".join(words)

        questions.append({
            "question": q,
            "answer": answer
        })

    return questions

def news_fetch(query):
    """Offline + Optional online news."""
    if not query:
        return SAMPLE_NEWS

    result = [n for n in SAMPLE_NEWS if query.lower() in n["title"].lower()]
    return result if result else SAMPLE_NEWS