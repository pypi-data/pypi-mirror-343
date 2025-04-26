def message_payload(recipient_id, message_text):
    return {
        "messaging_type": "RESPONSE",
        "recipient": {"id": recipient_id},
        "message": {"text": message_text},
    }


def attachment_payload(recipient_id, attachment_url):
    return {
        "messaging_type": "RESPONSE",
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {"type": "image", "payload": {"url": attachment_url}}
        },
    }
