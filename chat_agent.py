# chat_agent.py — Chatbot logic for Raybot PRO

from tools.db import append_event, get_recent_events
from tools.summarizer_engine import extractive_summary

def chat_agent_factory(openai_client=None):
    def chat_agent(task):
        message = task.get("message", "")
        session_id = task.get("session_id")

        # Fetch recent context
        context = ""
        if session_id:
            rows = get_recent_events(session_id, limit=12)
            context = "\n".join([f"{r[0]}: {r[1]}" for r in rows[-10:]]) if rows else ""

        small_context = extractive_summary(context, max_sentences=3) if context else ""

        system_prompt = "You are Raybot PRO, a friendly and helpful AI assistant."
        user_prompt = (small_context + "\n\nUser: " + message) if small_context else message

        # Online mode (if OpenAI exists)
        if openai_client:
            try:
                response = openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.6,
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"(Raybot PRO: LLM error -> {e})"

        # Offline mode
        else:
            reply = f"Raybot PRO (offline): I received: '{message}'"

        # Save reply into DB memory
        if session_id:
            append_event(session_id, "assistant", reply)

        return {"reply": reply}

    return chat_agent