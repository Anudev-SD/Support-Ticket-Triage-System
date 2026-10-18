from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv

from database import init_db, save_ticket, update_classification, update_draft, approve_ticket, get_all_tickets, get_ticket
from agents import classify_ticket, draft_response

load_dotenv()

app = FastAPI(title="Support Ticket Triage")
templates = Jinja2Templates(directory="templates")

init_db()


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    tickets = get_all_tickets()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "tickets": tickets
    })


@app.get("/api/tickets")
async def list_tickets():
    return get_all_tickets()


@app.post("/api/tickets/{ticket_id}/approve")
async def approve(ticket_id: int):
    approve_ticket(ticket_id)
    return {"status": "approved", "ticket_id": ticket_id}


@app.post("/webhook/email")
async def receive_email(request: Request, background_tasks: BackgroundTasks):
    secret = request.headers.get("X-Webhook-Secret", "")
    expected = os.getenv("WEBHOOK_SECRET", "")
    if expected and secret != expected:
        raise HTTPException(status_code=401, detail="Invalid webhook secret")

    data = await request.json()

    sender  = data.get("from", "unknown@email.com")
    subject = data.get("subject", "(no subject)")
    body    = data.get("body", "")

    if not body:
        raise HTTPException(status_code=400, detail="Email body is required")

    ticket_id = save_ticket(sender, subject, body)
    background_tasks.add_task(run_agents, ticket_id, sender, subject, body)

    return {"status": "received", "ticket_id": ticket_id}


async def run_agents(ticket_id: int, sender: str, subject: str, body: str):
    classification = classify_ticket(sender, subject, body)
    update_classification(
        ticket_id,
        classification.get("category", "account"),
        classification.get("urgency", "normal"),
        classification.get("reasoning", "")
    )

    draft = draft_response(
        sender, subject, body,
        classification.get("category", "account"),
        classification.get("urgency", "normal")
    )
    update_draft(ticket_id, draft)


# ── THIS WAS MISSING — add these 3 lines at the very bottom ──
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)