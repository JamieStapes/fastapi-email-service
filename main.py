from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from email.mime.text import MIMEText
import smtplib
import os
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input structure
class CaseSubmission(BaseModel):
    first_name: str
    last_name: str
    offence: str
    police_station_id: str

@app.post("/notify-case-submitted")
async def notify_case(data: CaseSubmission):
    send_email(data)
    return {"status": "email sent", "data": data.dict()}

def send_email(data):
    subject = "🚨 New Case Submitted"
    body = f"""
    New case submitted:

    Name: {data.first_name} {data.last_name}
    Offence: {data.offence}
    Police Station ID: {data.police_station_id}
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USERNAME
    msg["To"] = EMAIL_TO

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)
