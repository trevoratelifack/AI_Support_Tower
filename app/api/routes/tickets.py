import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.models.ticket import SupportTicket
from app.flows.support_flow import SupportFlow
from app.services.ticket_store import list_tickets, save_ticket

router = APIRouter(prefix="/tickets", tags=["Tickets"])
logger = logging.getLogger(__name__)


@router.get("/")
def get_tickets():
    return {"tickets": list_tickets()}

def _json_value(value):
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    return value


@router.post("/")
def triage_ticket_flow(ticket: SupportTicket):
    ticket_data = ticket.model_dump()
    # Persist intake before running the model so a provider failure cannot lose a customer request.
    save_ticket(ticket_data, {"ticket_id": ticket.ticket_id, "status": "submitted"})
    flow = SupportFlow()
    try:
        flow.kickoff(inputs=ticket_data)
    except Exception:
        logger.exception("Workflow failed for submitted ticket %s", ticket.ticket_id)
        return JSONResponse(
            status_code=202,
            content={"ticket_id": ticket.ticket_id, "status": "submitted", "workflow_status": "pending"},
        )

    response = {
        "ticket_id": ticket.ticket_id,
        "status": "completed",
        "workflow_status": "completed",
        "triage": _json_value(flow.state.get("triage_result")),
        "investigation": _json_value(flow.state.get("investigation_result")),
        "policy": _json_value(flow.state.get("policy_result")),
        "resolution": _json_value(flow.state.get("resolution_result")),
    }
    save_ticket(ticket_data, response)
    return response
