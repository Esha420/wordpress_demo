import requests
import uuid

# ===== CONFIG =====
N8N_WEBHOOK_URL = "https://eshap.app.n8n.cloud/webhook-test/wp-agent"
AGENT_KEY = "demo-secret"
AGENT_NAME = "wp-agent-cli"
AGENT_VERSION = "1.0.0"
# ==================


def build_payload(action: str) -> dict:
    """
    Builds a backward-compatible payload
    with intent-based contract (Step 1)
    """

    payload = {
        # 🔴 BACKWARD COMPATIBILITY (DO NOT REMOVE YET)
        "action": action,

        # 🟢 NEW INTENT CONTRACT
        "intent": None,
        "entity": None,
        "data": {},

        # 🟣 SYSTEM METADATA
        "meta": {
            "request_id": str(uuid.uuid4()),
            "agent": AGENT_NAME,
            "version": AGENT_VERSION
        }
    }

    # ---- CONTENT / POST ACTIONS ----
    if action == "create_post":
        payload["intent"] = "content.create"
        payload["entity"] = "post"
        payload["data"] = {
            "title": input("Enter post title: ").strip(),
            "content": input("Enter post content: ").strip(),
            "status": input("Enter status (draft/publish): ").strip()
        }

    elif action == "publish_post":
        payload["intent"] = "content.publish"
        payload["entity"] = "post"
        payload["data"] = {
            "post_id": int(input("Enter post ID to publish: ").strip())
        }

    elif action == "update_post":
        payload["intent"] = "content.update"
        payload["entity"] = "post"
        payload["data"] = {
            "post_id": int(input("Enter post ID to update: ").strip()),
            "title": input("Enter new title: ").strip(),
            "content": input("Enter new content: ").strip()
        }

    # ---- USER ACTIONS ----
    elif action == "create_user":
        payload["intent"] = "user.create"
        payload["entity"] = "user"
        payload["data"] = {
            "username": input("Enter new username: ").strip(),
            "email": input("Enter email: ").strip(),
            "password": input("Enter password: ").strip(),
            "role": input("Enter role (subscriber, editor, etc.): ").strip()
        }

    else:
        raise ValueError(f"Invalid action: {action}")

    return payload


def main():
    print("=== WordPress Agent Demo (Intent-Based v1) ===")
    print("Available actions:")
    print(" - create_post")
    print(" - publish_post")
    print(" - update_post")
    print(" - create_user\n")

    action = input("Enter action: ").strip()

    try:
        payload = build_payload(action)
    except ValueError as e:
        print(f"❌ {e}")
        return

    headers = {
        "Content-Type": "application/json",
        "X-AGENT-KEY": AGENT_KEY
    }

    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json=payload,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()

        print("\n✅ Response from n8n / WordPress:")
        print(response.json())

    except requests.exceptions.RequestException as e:
        print("\n❌ Error sending request:")
        print(e)


if __name__ == "__main__":
    main()
