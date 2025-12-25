from collections import defaultdict
from datetime import datetime

# chat_store["vm-001"] = [ {sender, text, time}, ... ]
chat_store = defaultdict(list)

CHAT_LIMIT = 20  # keep only last 20 messages

def add_message(device_id, sender_role, text):
    chat_store[device_id].append({
        "sender": sender_role,
        "text": text,
        "time": datetime.utcnow().isoformat()
    })

    # keep last 20 only
    chat_store[device_id] = chat_store[device_id][-CHAT_LIMIT:]


def get_messages(device_id):
    return chat_store.get(device_id, [])


def clear_chat(device_id):
    if device_id in chat_store:
        del chat_store[device_id]
