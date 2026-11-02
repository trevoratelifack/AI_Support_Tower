from pydantic import BaseModel, Field

class SupportTicket(BaseModel):
    ticket_id: str = Field(..., description="Unique identifier for the ticket")
    customer_id: str = Field(..., description="Unique identifier for the customer")
    subject: str
    description: str


