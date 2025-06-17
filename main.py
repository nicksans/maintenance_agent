from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

class CallRequest(BaseModel):
    phone_number: str
    issue_description: str
    availability: str
    ticket_id: str
    vendor_id: str

@app.post("/outgoing-call")
async def outgoing_call(data: CallRequest):
    # Placeholder for Twilio call logic
    print(f"Starting call to: {data.phone_number}")
    return { "message": "Call initiated", "to": data.phone_number }

@app.post("/media-stream")
async def media_stream(request: Request):
    # Placeholder for Twilio media stream logic
    body = await request.body()
    print("Received media stream")
    return { "message": "Media stream received" }

@app.post("/ultravox-response")
async def ultravox_response(request: Request):
    payload = await request.json()
    print("Received Ultravox webhook:", payload)

    # Forward the response to n8n webhook (adjust this URL later)
    async with httpx.AsyncClient() as client:
        await client.post("https://tenantry.app.n8n.cloud/webhook/vendor-response", json=payload)

    return { "message": "Webhook forwarded to n8n" }