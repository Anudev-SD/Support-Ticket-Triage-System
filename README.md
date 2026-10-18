# Support Ticket Triage System

An AI-powered support ticket triage prototype built with **Python, FastAPI, OpenAI, and SQLite**. It receives customer support requests through a webhook, classifies each ticket by category and urgency, generates a draft response, and stores the results for review in a simple dashboard.

## Features

- **Ticket intake:** Receive support requests through a webhook endpoint.
- **AI classification:** Categorize tickets as `billing`, `technical`, or `account`.
- **Urgency detection:** Assign an urgency level: `urgent`, `high`, `normal`, or `low`.
- **AI-generated replies:** Draft a short customer support response based on the ticket category and urgency.
- **SQLite storage:** Store incoming messages, classifications, draft replies, and approval status.
- **Dashboard:** View tickets and review their generated replies.
- **Human approval:** Mark a draft as approved before any separate email-sending integration is added.
- **Sample data:** Send three example support requests to test the workflow.

## How It Works

1. `webhook.py` sends sample customer emails to the FastAPI webhook.
2. `main.py` receives each request and saves the ticket.
3. `agents.py` calls the OpenAI API to classify the ticket and draft a response.
4. `database.py` stores the ticket and processing results in `tickets.db`.
5. The dashboard displays the tickets and lets a reviewer mark drafts as approved.

> **Note:** This project currently drafts replies and records approval status. It does not send emails to customers automatically. The included webhook is a local test endpoint, not a connection to a real email inbox.

## Tech Stack

- Python
- FastAPI
- Uvicorn
- OpenAI API (`gpt-4o-mini`)
- SQLite
- Jinja2 templates
- `python-dotenv`
- `httpx`

## Project Structure

```text
support_triage/
├── main.py
├── agents.py
├── database.py
├── webhook.py
├── requirements.txt
├── tickets.db                 # Created/updated by the application
├── .env                       # Create this locally; do not commit it
└── templates/
    └── dashboard.html
```

## Requirements

- Python 3.10 or newer recommended
- An OpenAI API key with API access enabled
- Visual Studio Code or another code editor

## Setup and Run

### 1. Open the project

Open the `support_triage` folder in VS Code, then open **Terminal → New Terminal**.

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate it with:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a file named `.env` in the project root:

```dotenv
OPENAI_API_KEY=your_openai_api_key_here
WEBHOOK_SECRET=mysecrettoken123
```

Replace `your_openai_api_key_here` with your own OpenAI API key. Do not share or commit the key. The webhook secret must match the secret configured in `webhook.py`.

### 5. Check the dashboard template

The application expects a file at `templates/dashboard.html`. Make sure the `templates` folder and `dashboard.html` file exist before opening the dashboard. If the template is missing, the homepage will return a template error.

### 6. Start the application

```bash
python main.py
```

The server runs on port `8000`. Keep this terminal open.

Open these URLs in your browser:

- Dashboard: <http://127.0.0.1:8000>
- Interactive API docs: <http://127.0.0.1:8000/docs>

### 7. Send the sample tickets

Open a **second terminal** in the project folder and activate the virtual environment:

```bash
source .venv/bin/activate
```

Then run:

```bash
python webhook.py
```

The script submits three sample tickets: a duplicate billing charge, an urgent API outage, and a subscription cancellation.

Return to the dashboard and refresh it to view the results. AI processing can take a few seconds.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Display the ticket dashboard |
| `GET` | `/api/tickets` | Return all tickets as JSON |
| `POST` | `/api/tickets/{ticket_id}/approve` | Mark a ticket draft as approved |
| `POST` | `/webhook/email` | Receive a support ticket through a webhook |

### Example webhook payload

```json
{
  "from": "customer@example.com",
  "subject": "Charged twice this month — need refund",
  "body": "My card was charged twice. Could you help me request a refund?"
}
```

Send the payload as JSON to `/webhook/email` with the header:

```text
X-Webhook-Secret: mysecrettoken123
```

If `WEBHOOK_SECRET` is set in `.env`, the request must provide the matching header.

## Troubleshooting

### `ModuleNotFoundError`

Make sure the virtual environment is active, then install the requirements again:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### OpenAI authentication or API error

Check that `.env` exists in the project root and contains a valid `OPENAI_API_KEY`. Confirm that your OpenAI API account has API access and available usage.

### `TemplateNotFound: dashboard.html`

Create `templates/dashboard.html` and confirm the folder is alongside `main.py`.

### `Invalid webhook secret`

Ensure `WEBHOOK_SECRET` in `.env` matches the `SECRET` value in `webhook.py`.

### Dashboard does not show the new AI results

Wait a few seconds and refresh the dashboard. Check the terminal for errors from the AI-processing task.

### Port 8000 is already in use

Stop the other server process or configure this application to use another port.

## Security Notes

- Never commit `.env` or expose your OpenAI API key.
- Use a strong webhook secret outside local development.
- Do not expose this development server directly to the public internet.
- Add authentication, input validation, logging, rate limiting, and appropriate error handling before production use.
- Review AI-generated replies for correctness before sending them to customers.

## Future Improvements

- Connect a real email provider or support platform.
- Send approved replies through an email service.
- Add authentication and user roles to the dashboard.
- Improve error handling and ticket-processing status updates.
- Add automated tests and evaluation metrics for classification quality.
- Add audit logs and stronger production security.

## License

No license has been specified yet. Add a license file if you plan to publish or distribute this project.
