# main.py — Entry point for Raybot PRO

from ui.app import make_app
from config import APP_TITLE

def main():
    print(f"🚀 Starting {APP_TITLE}")
    
    # Build Gradio app
    app = make_app()

    # Launch server
    # In Colab use share=True
    app.launch(
        share=True,
        debug=False,   # set True if you want python exceptions visible in UI
        server_name="0.0.0.0"
    )

if __name__ == "__main__":
    main()