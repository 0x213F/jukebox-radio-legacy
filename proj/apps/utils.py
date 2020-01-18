import json


def broadcast_message(obj):
    return {
        "type": "broadcast",
        "text": json.dumps({"system": {"message": "start", "sent_at": obj,}}),
    }
