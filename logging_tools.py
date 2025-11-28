import logging
import json

LOGFILE = "raybot_pro.log"

logging.basicConfig(
    filename=LOGFILE,
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s"
)

def trace(stage, payload):
    """Log debug traces for agent execution."""
    try:
        payload_summary = json.dumps(payload)[:800]
    except Exception:
        payload_summary = str(payload)[:800]

    logging.debug(f"TRACE stage={stage} payload={payload_summary}")