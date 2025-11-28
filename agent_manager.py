# agent_manager.py — Manages all Raybot PRO agents

from typing import Dict, Any
import threading

class AgentManager:
    def __init__(self):
        self.agents = {}
        self.lock = threading.Lock()
        self.paused = False  # supports pause/resume

    def register(self, name: str, func):
        self.agents[name] = func

    def send_to(self, name: str, task: Dict[str, Any]):
        if name not in self.agents:
            return {"error": f"Agent '{name}' not found"}

        if self.paused:
            return {"error": "Agents are paused"}

        return self.agents[name](task)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False