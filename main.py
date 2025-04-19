from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# 🚨 Add this middleware for WeWeb / browser-based access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can change this later to a specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CaseSubmission(BaseModel):
    first_name: str
    last_name: str
    offence: str
    police_station_id: str

@app.post("/notify-case-submitted")
async def notify_case(data: CaseSubmission):
    subject = f"New Case Submitted: {data.first_name} {data.last_name}"
    body = f"""
    First Name: {data.first_name}
    Last Name: {data.last_name}
    Offence: {data.offence}
    Police Station ID: {data.police_station_id}
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = os.getenv("EMAIL_USERNAME")
    msg["To"] = os.getenv("EMAIL_TO")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.getenv("EMAIL_USERNAME"), os.getenv("EMAIL_PASSWORD"))
        server.send_message(msg)

    return {"status": "received", "data": data.dict()}
