from fastapi import FastAPI, Request
from pydantic import BaseModel
import httpx

app = FastAPI()

class RetellWebhook(BaseModel):
    selected_time: str
    vendor_id: str
    ticket_id: str

@app.post("/retell-response")
async def handle_retell_response(data: RetellWebhook):
    print("✅ Received Retell webhook:", data.dict())

    # Forward this to n8n or Supabase
    async with httpx.AsyncClient() as client:
        await client.post(
            "https://tenantry.app.n8n.cloud/webhook/vendor-response",
            json=data.dict()
        )

    return {"message": "Received and forwarded"}
