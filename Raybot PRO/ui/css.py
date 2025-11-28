# ui/css.py
# Central place for CSS used by the Gradio UI.

CSS = """
/* White container with yellow/orange accent */
body, html { background: linear-gradient(90deg, #FFFDF5, #FFF8E6); font-family: Inter, sans-serif; }
.gradio-container { background: #ffffff !important; color: #111 !important; border-radius: 16px; padding: 18px; box-shadow: 0 6px 24px rgba(0,0,0,0.08); }
h1 { text-align: center; margin-bottom: 6px; }
.app-header { text-align: center; margin-bottom: 12px; }
.icon-row { display:flex; gap:12px; justify-content:center; margin-bottom:12px; flex-wrap:wrap; }
.icon-btn { padding:10px 12px; border-radius:12px; border: 1px solid transparent; cursor:pointer; display:inline-flex; align-items:center; gap:8px; font-weight:600; background: transparent; }
.icon-btn.selected { border-color: rgba(255,153,0,0.9); box-shadow: 0 4px 10px rgba(255,153,0,0.12); background: linear-gradient(90deg,#FFD66B,#FF7A00); color:white; }
.tab-label { font-size:14px; }

/* Chat messages */
.gr-chatbot { border-radius:12px !important; padding:8px !important; background:#f7f7f7 !important; }
.gr-message.user { background: #fffbe6 !important; }
.gr-message.bot { background: #ffffff !important; border:1px solid #f0f0f0 !important; }

/* Inputs */
input, textarea { border-radius: 10px !important; padding: 8px !important; }

/* Buttons */
button { border-radius: 10px !important; padding: 8px 12px !important; font-weight:600 !important; }

/* Small responsive tweaks */
@media (max-width:720px) {
  .icon-row { gap:8px; }
  .icon-btn { padding:8px 10px; font-size:14px; }
}
"""