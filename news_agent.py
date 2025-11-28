# news_agent.py — AI News from API or offline samples

from tools.summarizer_engine import news_fetch

def news_agent(task):
    query = task.get("query", "")
    return {"news": news_fetch(query)}