# 🌟 Raybot PRO — Multi-Agent AI System (Kaggle-Ready)

Raybot PRO is a fully modular **multi-agent AI system** built with Python, Gradio, Whisper, gTTS, and (optionally) OpenAI GPT models.  
It is designed to run **offline** for Kaggle Notebook submissions while also supporting online LLMs if an API key is provided.

This project includes:

- 🔹 Chat Agent (LLM-powered or offline fallback)
- 🔹 Summarizer Agent (extractive summarization)
- 🔹 Quiz Generator Agent
- 🔹 News Agent (offline-safe sample dataset)
- 🔹 Voice Agent (Whisper STT + gTTS TTS)
- 🔹 Agent Manager (parallel / sequential capable)
- 🔹 Long-running tasks (pause/resume)
- 🔹 Sessions & Memory (SQLite)
- 🔹 Observability (logging, traces)
- 🔹 Gradio UI (Instagram-style icons + tabs)

---

## 🚀 Features Overview

### ✔ Multi-Agent System
Each agent is fully isolated:

- `chat_agent`
- `summarizer_agent`
- `quiz_agent`
- `news_agent`
- `voice_agent`

All registered with a central **AgentManager**.

---

### ✔ Tools Included
- Custom DB layer  
- Memory storage  
- Whisper STT wrapper  
- gTTS TTS wrapper  
- Summarizer engine  
- Logging utilities  

---

### ✔ Long-Running Operations
Supports:
- background tasks  
- pause/resume  
- cancel  

---

### ✔ Sessions + Memory
Raybot PRO stores:
- messages  
- tool calls  
- memory key/value pairs  
in a SQLite DB.

---

### ✔ Gradio UI
Clean, modern interface with:
- top icon strip (Chat / Quiz / News / Voice / Eval)  
- tab-based workspace  
- Chatbot with session handling  

---

## 📦 Installation

```bash
pip install -r requirements.txt
sudo apt-get install -y ffmpeg
```

Whisper needs ffmpeg.

---

## 🔑 Optional: Enable Online LLM

Set:

```bash
export OPENAI_API_KEY="your-key-here"
```

If no key is provided, Raybot runs in **offline mode**.

---

## ▶️ Run Raybot PRO

```bash
python main.py
```

In Colab/Kaggle, this launches Gradio with a public share link.

---

## 📁 Project Structure

```
raybot-pro/
├── main.py
├── config.py
├── requirements.txt
├── .gitignore
│
├── agents/
├── tools/
├── ui/
└── tests/
```

---

## 📚 Kaggle Submission Notes

Raybot PRO is designed to satisfy the Kaggle course requirements:

- Multi-agent architecture  
- Tools (custom + built-in)  
- Sessions/memory  
- LLM agent (optional offline mode)  
- Long-running tasks  
- Observability  
- Evaluation script  
- Deployable agent  

Just include this repo and a Kaggle Notebook that calls `main.py`.

---

## 🤝 Contributing

Pull requests are welcome.  
If you want to extend Raybot PRO with new agents, tools, or UI tabs — feel free!

---

## 📜 License

This project is licensed under the **MIT License** — see the LICENSE file for details.

---

## ⭐ Credits

Created by **Manas O D**.  
Built for the Kaggle **AI Agents Course capstone project**.
