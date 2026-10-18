import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def classify_ticket(sender: str, subject: str, body: str) -> dict:
    prompt = f"""From: {sender}
Subject: {subject}
Body:
{body}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=300,
        messages=[
            {
                "role": "system",
                "content": """You are a support ticket classifier.
Read the email and respond ONLY with a JSON object — no extra text, no markdown.
Use exactly this format:
{
  "category": "billing" | "technical" | "account",
  "urgency": "urgent" | "high" | "normal" | "low",
  "reasoning": "one short phrase of max 8 words"
}"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"}
    )

    raw = response.choices[0].message.content.strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {
            "category": "account",
            "urgency": "normal",
            "reasoning": "Could not parse classification"
        }

    return result


def draft_response(sender: str, subject: str, body: str,
                   category: str, urgency: str) -> str:
    urgency_note = ""
    if urgency == "urgent":
        urgency_note = "This is URGENT — the customer needs a fast, empathetic reply that escalates immediately."
    elif urgency == "high":
        urgency_note = "This is high priority — be prompt and reassuring."
    else:
        urgency_note = "Standard priority — be warm and professional."

    system_map = {
        "billing":   "You are a billing support specialist. You handle payments, refunds, and subscription issues.",
        "technical": "You are a technical support engineer. You troubleshoot product issues and bugs.",
        "account":   "You are an account support specialist. You handle cancellations, upgrades, and account settings.",
    }
    system_prompt = system_map.get(category, system_map["account"])

    prompt = f"""A customer sent this support email. Draft a helpful reply.

From: {sender}
Subject: {subject}
Body:
{body}

Priority note: {urgency_note}

Write only the email body (3-5 sentences). Sign off as "Support Team". Do not include a subject line."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=500,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()