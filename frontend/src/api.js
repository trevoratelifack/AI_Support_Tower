const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export async function getSubmittedTickets() {
  const response = await fetch(`${API_BASE}/tickets/`);
  if (!response.ok) throw new Error(`Could not load submitted tickets (${response.status})`);
  return response.json();
}

export async function runTicketWorkflow(ticket) {
  const response = await fetch(`${API_BASE}/tickets/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(ticket),
  });
  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    throw new Error(detail.detail || `Workflow request failed (${response.status})`);
  }
  return response.json();
}
