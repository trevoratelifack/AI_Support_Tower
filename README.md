# AI Operations Control Tower

An internal support operations dashboard and FastAPI service. A submitted ticket is processed by four CrewAI stages that return a structured recommendation with the facts and policy evidence behind it. No stage executes refunds, cancellations, or customer communications.

## Architecture

```text
React dashboard → POST /tickets/ → CrewAI SupportFlow
  → Triage → Investigation → Policy → Resolution recommendation
```

The Flow owns the sequence and passes Pydantic results between crews. Agents do not invoke one another.

- **Triage** classifies the ticket's category, urgency, risk, and confidence.
- **Investigation** retrieves synthetic customer, subscription, payment, and ticket history. Its tools have provider-neutral lookup functions that can later connect to a CRM, Stripe, PostgreSQL, or support platform.
- **Policy** searches the local policy set for duplicate payments, cancellations, failed payments, and invoice requests. The search function is isolated so a retrieval implementation such as BM25 or embeddings can replace it.
- **Resolution** combines the ticket and earlier findings to recommend an action. It does not execute that action.
- **Validation Agent** is intentionally not implemented; it is reserved for the next development stage.

## Requirements and configuration

Python 3.10+ is recommended (the CrewAI dependency may impose a newer supported version). Node.js 18+ is required for the frontend. Configure `OPENAI_API_KEY` and optionally `MODEL_NAME` in `crewai_operations/.env`; `.env.example` lists the current variables. The frontend does not receive secrets.

## Run the backend

From this directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Set OPENAI_API_KEY in .env
uvicorn app.main:app --reload
```

API docs: http://127.0.0.1:8000/docs. Health: `GET /health`.

`GET /tickets/` returns persisted customer submissions for the operator inbox. New requests are saved before AI processing; if workflow processing is unavailable, the request remains queued with a pending workflow status.

`POST /tickets/` accepts `ticket_id`, `customer_id`, `subject`, and `description`. It returns `ticket_id`, `triage`, `investigation`, `policy`, and `resolution`. Synthetic duplicate-payment data uses customer `CUS-001`; a missing customer ID produces missing-record evidence and should be escalated.

## Run the frontend

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. The dashboard submits the selected ticket to the FastAPI service; set `VITE_API_BASE_URL` if the backend runs at another address. API failures appear in the ticket view.

Customers can select **Customer ticket form** in the dashboard header to submit a request. The form requires a customer ID, subject, and description, then posts to the same `POST /tickets/` workflow endpoint. In the current synthetic data, use `CUS-001` or `CUS-002` for known customer records. Submitted tickets and workflow results are stored in a local SQLite database at `app/data/tickets.sqlite3` and appear at the top of the operator inbox. This prototype does not send follow-up messages.

## Tests

From the project directory:

```powershell
pytest
```

Tests cover deterministic synthetic investigation data, local policy retrieval, resolution contracts (including an escalation case), and Flow state passing. Crew calls are mocked in the Flow test, so tests do not require an LLM key or make external calls.

## Safety boundary

Recommendations require operator review. Payment and account tools are read-only synthetic lookups. The project does not process refunds, cancel subscriptions, send emails, authenticate users, or include production RAG infrastructure.
