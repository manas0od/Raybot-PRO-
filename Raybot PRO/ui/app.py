# ui/app.py
"""
Builds and returns a Gradio Blocks app for Raybot PRO.

Usage:
    from ui.app import make_app
    app = make_app(
        agent_manager=agent_manager,
        create_session=create_session,
        append_event=append_event,
        get_recent_events=get_recent_events,
        remember=remember,
        transcribe_audio=transcribe_audio,
        tts_save=tts_save,
        openai_client=openai_client,   # optional
    )
    app.launch(share=True)

make_app provides defaults (safe no-op) so you can import the UI without wiring everything,
but to enable features pass your real functions.
"""
from typing import Callable, Optional
import json
import gradio as gr
from ui.css import CSS

# ---- default no-op helpers (so the UI imports even if some backend pieces are not passed) ----
def _noop_create_session(name="default"):
    return 0

def _noop_append_event(session_id, role, content):
    return None

def _noop_get_recent_events(session_id, limit=50):
    return []

def _noop_remember(session_id, key, value):
    return None

def _noop_transcribe_audio(path):
    return "(stt not available)"

def _noop_tts_save(text):
    return None

# ---- make_app function ----
def make_app(
    agent_manager,
    create_session: Callable[[str], int] = _noop_create_session,
    append_event: Callable[[int, str, str], None] = _noop_append_event,
    get_recent_events: Callable[[int, int], list] = _noop_get_recent_events,
    remember: Callable[[int, str, str], None] = _noop_remember,
    transcribe_audio: Callable[[str], str] = _noop_transcribe_audio,
    tts_save: Callable[[str], Optional[str]] = _noop_tts_save,
    openai_client=None,
    share: bool = True,
    debug: bool = False,
):
    """
    Builds the Gradio Blocks UI.
    - agent_manager: object with send_to(name, task) method
    - create_session, append_event, get_recent_events, remember: DB helpers
    - transcribe_audio, tts_save: stt/tts helpers
    - openai_client: optional OpenAI SDK client (not required)
    """
    css = CSS

    with gr.Blocks(css=css) as demo:
        gr.Markdown("<div class='app-header'><h1>🌟 Raybot PRO — Kaggle Multi-Agent Demo</h1>"
                    "<div style='text-align:center;color:#666;'>Agents: Chat, Summarizer, Quiz, News, Voice • Sessions & Memory • Observability</div></div>")

        with gr.Row(elem_classes="icon-row"):
            btn_quiz = gr.Button("❓  Quiz", elem_classes="icon-btn")
            btn_news = gr.Button("📰  News", elem_classes="icon-btn")
            btn_voice = gr.Button("🎤  Voice", elem_classes="icon-btn")
            btn_chat = gr.Button("💬  Chat", elem_classes="icon-btn")
            btn_sum = gr.Button("✉️  Summarizer", elem_classes="icon-btn")
            btn_eval = gr.Button("🧪  Eval", elem_classes="icon-btn")

        # Tabs
        with gr.Tabs() as tabs:
            with gr.Tab("Chat"):
                chatbot = gr.Chatbot(elem_id="chatbot")
                msg = gr.Textbox(placeholder="Type a message and press Enter", show_label=False)
                session_name = gr.Textbox(value="default", label="Session name (create -> use this id)")
                create_btn = gr.Button("Create Session")
                sid_box = gr.Textbox(value="", label="Session ID", interactive=False)

                def _create_session(name):
                    sid = create_session(name or f"default_{int(time.time())}")
                    return str(sid)
                create_btn.click(_create_session, session_name, sid_box)

                def _send_msg(message, sid):
                    if not sid:
                        return gr.update(value=None), "Create a session first."
                    try:
                        sid_i = int(sid)
                    except:
                        return gr.update(value=None), "Invalid session id."

                    append_event(sid_i, "user", message)
                    res = agent_manager.send_to("chat", {"message": message, "session_id": sid_i})
                    reply = res.get("reply", str(res))
                    return [(message, reply)], reply

                msg.submit(_send_msg, [msg, sid_box], [chatbot, msg])

            with gr.Tab("Summarizer"):
                sum_in = gr.Textbox(lines=6, label="Paste text to summarize")
                sum_btn = gr.Button("Summarize (Agent)")
                sum_out = gr.Textbox(label="Summary")

                def _run_summarize(text, sid):
                    sid_i = int(sid) if sid else None
                    out = agent_manager.send_to("summarizer", {"text": text, "max_sentences": 3})
                    if sid_i:
                        append_event(sid_i, "tool", json.dumps({"tool":"summarizer","output": out}))
                    return out.get("summary","")

                sum_btn.click(_run_summarize, [sum_in, sid_box], sum_out)

            with gr.Tab("Quiz Maker"):
                q_text = gr.Textbox(lines=6, label="Text for quiz")
                q_n = gr.Slider(1,20, value=5, label="Questions")
                q_btn = gr.Button("Generate Quiz")
                q_out = gr.Textbox(label="Quiz JSON")

                def _run_quiz(text, n, sid):
                    sid_i = int(sid) if sid else None
                    out = agent_manager.send_to("quiz", {"text": text, "n": n})
                    if sid_i:
                        append_event(sid_i, "tool", json.dumps({"tool":"quiz","count": len(out.get("quiz",[]))}))
                    return json.dumps(out.get("quiz",[]), indent=2)

                q_btn.click(_run_quiz, [q_text, q_n, sid_box], q_out)

            with gr.Tab("News"):
                news_q = gr.Textbox(label="Topic (leave blank for sample news)")
                news_btn = gr.Button("Fetch News")
                news_out = gr.Textbox(label="News results")

                def _run_news(q, sid):
                    sid_i = int(sid) if sid else None
                    out = agent_manager.send_to("news", {"query": q})
                    if sid_i:
                        append_event(sid_i, "tool", json.dumps({"tool":"news","count": len(out.get("news",[]))}))
                    return json.dumps(out.get("news",[]), indent=2)

                news_btn.click(_run_news, [news_q, sid_box], news_out)

            with gr.Tab("Voice"):
                audio_in = gr.Audio(type="filepath", label="Upload audio (wav/mp3)")
                trans_btn = gr.Button("Transcribe")
                trans_out = gr.Textbox(label="Transcription")

                def _transcribe(audio_file, sid):
                    if not audio_file:
                        return "Upload audio first."
                    sid_i = int(sid) if sid else None
                    out = agent_manager.send_to("voice", {"action":"transcribe", "path": audio_file})
                    txt = out.get("transcript","")
                    if sid_i:
                        append_event(sid_i, "user", "[VOICE] " + txt[:300])
                        append_event(sid_i, "tool", json.dumps({"tool":"voice_transcribe","output": txt[:200]}))
                    return txt

                trans_btn.click(_transcribe, [audio_in, sid_box], trans_out)

                tts_in = gr.Textbox(label="Text to synthesize")
                tts_btn = gr.Button("Synthesize (TTS)")
                tts_audio = gr.Audio(label="TTS output")

                def _synthesize(text):
                    out = agent_manager.send_to("voice", {"action":"tts", "text": text})
                    return out.get("tts_path", None)

                tts_btn.click(_synthesize, tts_in, tts_audio)

            with gr.Tab("Tools & Ops"):
                start_btn = gr.Button("Start long background task (demo)")
                pause_btn = gr.Button("Pause agents")
                resume_btn = gr.Button("Resume agents")
                cancel_btn = gr.Button("Cancel long task")
                long_status = gr.Textbox(label="Long task status")

                def _start_task():
                    r = agent_manager.send_to("start_long_task", {"seconds": 15}) if hasattr(agent_manager, "send_to") else {"error": "not implemented"}
                    return json.dumps(r)

                def _pause():
                    if hasattr(agent_manager, "pause"): agent_manager.pause(); return "Paused agents."
                    return "Pause not available."

                def _resume():
                    if hasattr(agent_manager, "resume"): agent_manager.resume(); return "Resumed agents."
                    return "Resume not available."

                def _cancel():
                    if hasattr(agent_manager, "send_to"): return agent_manager.send_to("cancel_long_task", {}) 
                    return {"error":"not implemented"}

                start_btn.click(_start_task, None, long_status)
                pause_btn.click(_pause, None, long_status)
                resume_btn.click(_resume, None, long_status)
                cancel_btn.click(_cancel, None, long_status)

                eval_btn = gr.Button("Run agent evaluation")
                eval_out = gr.Textbox(label="Evaluation results")

                def _run_eval():
                    if hasattr(agent_manager, "send_to"):
                        r = agent_manager.send_to("eval", {})
                        return json.dumps(r.get("result",{}), indent=2)
                    return "(evaluation not available)"

                eval_btn.click(_run_eval, None, eval_out)

            with gr.Tab("Session & Memory"):
                show_btn = gr.Button("Show recent events")
                ev_out = gr.Textbox(label="Recent Events")

                def _show_events(sid):
                    if not sid: return "Create a session first."
                    evs = get_recent_events(int(sid), limit=100)
                    lines=[]
                    for role, c, ts in evs:
                        lines.append(f"{ts} | {role.upper()} | {c[:150]}")
                    return "\n".join(lines) if lines else "(no events)"

                show_btn.click(_show_events, sid_box, ev_out)

                mem_k = gr.Textbox(label="Memory key")
                mem_v = gr.Textbox(label="Memory value")
                mem_save = gr.Button("Save Memory")
                mem_res = gr.Textbox(label="Result")

                def _save_mem(k, v, sid):
                    if not sid: return "Create session first."
                    remember(int(sid), k, v)
                    return "Saved."

                mem_save.click(_save_mem, [mem_k, mem_v, sid_box], mem_res)

        # top icon buttons: cosmetic / lightweight mapping (Gradio doesn't provide direct JS tab-switch)
        btn_quiz.click(lambda: gr.update(visible=True), None, None)
        btn_news.click(lambda: gr.update(visible=True), None, None)
        btn_voice.click(lambda: gr.update(visible=True), None, None)
        btn_chat.click(lambda: gr.update(visible=True), None, None)
        btn_sum.click(lambda: gr.update(visible=True), None, None)
        btn_eval.click(lambda: gr.update(visible=True), None, None)

    return demo