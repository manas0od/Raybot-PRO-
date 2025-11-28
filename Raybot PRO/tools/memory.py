# memory.py — wrapper over db.py

from tools.db import remember, recall

def memory_write(session_id, key, value):
    remember(session_id, key, value)

def memory_read(session_id, key):
    return recall(session_id, key)