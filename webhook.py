"""
Run this script to send a test email to your local server.
Usage:  python webhook.py
"""
import httpx

# Make sure your FastAPI server is running first (python main.py)
#SERVER_URL = "http://localhost:8000/webhook/email"
#SECRET     = "mysecrettoken123"   # must match .env WEBHOOK_SECRET
import os
from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv("WEBHOOK_SECRET", "")

test_emails = [
    {
        "from": "sarah.chen@acme.io",
        "subject": "Charged twice this month — need refund",
        "body": "Hi, I noticed my card was charged $49 twice in October. I only have one subscription. Can you issue a refund for the duplicate charge? Account: sarah.chen@acme.io. Thanks."
    },
    {
        "from": "cto@bigcorp.com",
        "subject": "URGENT: API completely down — production impacted",
        "body": "Your API has been returning 503 errors for 45 minutes. This is impacting our production environment. We have 500k users affected. Escalate immediately."
    },
    {
        "from": "james.miller@oldco.com",
        "subject": "Please cancel my subscription",
        "body": "Hello, I'd like to cancel my subscription at the end of this billing cycle. We're switching vendors. Please confirm the cancellation and don't charge me next month."
    },
]

def send_test_email(email: dict):
    response = httpx.post(
        SERVER_URL,
        json=email,
        headers={"X-Webhook-Secret": SECRET}
    )
    print(f"Sent: '{email['subject']}'")
    print(f"Response: {response.status_code} — {response.json()}")
    print()

if __name__ == "__main__":
    for email in test_emails:
        send_test_email(email)