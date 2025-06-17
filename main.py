import os
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
    twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
    twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_PHONE_NUMBER")

    to_number = data.phone_number
    callback_url = "https://voice.ultravox.ai/call"

    # Include details in URL
    params = {
        "issue_description": data.issue_description,
        "availability": data.availability,
        "ticket_id": data.ticket_id,
        "vendor_id": data.vendor_id
    }

    # Convert dict to query string
    from urllib.parse import urlencode
    full_url = f"{callback_url}?{urlencode(params)}"

    # Make the Twilio call
    async with httpx.AsyncClient(auth=(twilio_sid, twilio_token)) as client:
        response = await client.post(
            f"https://api.twilio.com/2010-04-01/Accounts/{twilio_sid}/Calls.json",
            data={
                "To": to_number,
                "From": from_number,
                "Url": full_url,
            },
        )

    print(f"Called {to_number}, response status: {response.status_code}")
    return { "message": "Call initiated", "to": to_number }


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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
