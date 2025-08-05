import asyncio
from datetime import datetime
from openai import OpenAI
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from mcp_use import MCPClient, MCPAgent
from langchain_openai import ChatOpenAI
import time
from fastapi import FastAPI, Request
from fastapi import APIRouter

router=APIRouter()

def create_event(start_iso, end_iso, attendees_emails, summary="Meeting"):
    creds = Credentials(
        token=None,
        refresh_token="xxxx",
        token_uri="https://oauth2.googleapis.com/token",
        client_id="xxx",
        client_secret="xxx",
scopes = ["https://www.googleapis.com/auth/calendar","https://www.googleapis.com/auth/gmail.send","https://www.googleapis.com/auth/gmail.readonly"]
    )
    
    service = build('calendar', 'v3', credentials=creds)

    event_body = {
        "summary": summary,
        "start": {
            "dateTime": start_iso,
            "timeZone": "Europe/Paris",
        },
        "end": {
            "dateTime": end_iso,
            "timeZone": "Europe/Paris",
        },
        "attendees": [{"email": email} for email in attendees_emails],
        "conferenceData": {
            "createRequest": {
                "requestId": f"meet-{int(time.time())}",
                "conferenceSolutionKey": {"type": "hangoutsMeet"},
            }
        },
    }

    event = service.events().insert(
        calendarId="primary",
        body=event_body,
        conferenceDataVersion=1,
        sendUpdates="all"
    ).execute()

    # Extraire lien Google Meet
    meet_link = None
    if "conferenceData" in event:
        for ep in event["conferenceData"].get("entryPoints", []):
            if ep.get("entryPointType") == "video":
                meet_link = ep.get("uri")
                break

    return meet_link

async def send_email(agent, to_email, body, subject="Application Status", meet_link=None):
    final_body = body
    command = (
    "Send an email with the exact following parameters. Do not omit anything. "
    "Be sure to include the body exactly as written.\n"
    "{"
    f"'to': '{to_email}', "
    f"'subject': '{subject}', "
    f"'body': '''{final_body}''', "
    f"'cc': '', "
    f"'bcc': ''"
    "}"
)
    print("COMMAND SENT TO AGENT:\n", command)   
    result = await agent.run(command)
    return result
import pytz

def format_email_body(start_iso, end_iso, meet_link="", accepted=True,job_title=""):
    """
    Generate the email body depending on acceptance or rejection.

    Args:
        start_iso (str): start datetime in ISO 8601 format
        end_iso (str): end datetime in ISO 8601 format
        meet_link (str): Google Meet link (optional if rejected)
        accepted (bool): True if accepted, False if rejected

    Returns:
        str: formatted email body
    """
    if accepted:
        # Format dates and times nicely
        dt_start = datetime.strptime(start_iso[:19], "%Y-%m-%dT%H:%M:%S")
        dt_end = datetime.strptime(end_iso[:19], "%Y-%m-%dT%H:%M:%S")  
        paris_tz = pytz.timezone("Africa/Tunis")
        dt_start = dt_start.astimezone(paris_tz)
        dt_end = dt_end.astimezone(paris_tz)

        date_str = dt_start.strftime("%A %d %B %Y")  # e.g. Tuesday 22 July 2025
        start_str = dt_start.strftime("%H:%M")
        end_str = dt_end.strftime("%H:%M")

        body = (
            f"Hello,\n\n"
            f"We are pleased to inform you that your application has been accepted for a technical interview for the position of {job_title} .\n"
            f"The interview is scheduled on {date_str} from {start_str} to {end_str} (Europe/Paris time).\n\n"
            f"Please join the Google Meet using the following link:\n{meet_link}\n\n"
            f"Best regards,"
        )
    else:
        body = (
            "Hello,\n\n"
            f"Thank you for your interest. Unfortunately, we regret to inform you that your application has not been accepted for the position of {job_title[:-3]}.\n\n"
            "We wish you the best in your future endeavors.\n\n"
            "Best regards,"
        )
    return body
# 🎯 Point d’entrée FastAPI
@router.post("/email_meet")
async def email_meet(request:Request):
    data = await request.json()
     # Extraction des champs de la requête
    start_iso = data.get("start_iso", "2025-09-22T15:00:00+01:00")
    end_iso = data.get("end_iso", "2025-09-22T16:00:00+01:00")
    attendees_emails = data.get("attendees_emails")
    status = data.get("accepted", True)
    job_title=data.get("job_title","")
    config = {
  "mcpServers": {
    "google-workspace": {
      "command": "node",
      "args": ["C:\\Users\\ramib\\google-workspace-mcp-server\\build\\index.js"],
      "env": {
        "GOOGLE_CLIENT_ID": "xxxx",
        "GOOGLE_CLIENT_SECRET": "xxxx",
        "GOOGLE_REFRESH_TOKEN": "xxx"
      }
    }
  }
}

    # 1. Charger config du serveur MCP
    client = MCPClient.from_dict(config)
    llm = ChatOpenAI(model="gpt-4o-mini",api_key="xxx")
    # 3. Créer un agent MCP (LLM + outil)
    agent = MCPAgent(llm=llm, client=client, max_steps=10)
    # Créer l'événement
    if (status==True):
     meet_link = create_event(
        start_iso=start_iso,
        end_iso=end_iso,
        attendees_emails=attendees_emails
    )
    else :
        meet_link=""
    # Envoyer l'e-mail avec le lien Meet
    email_body = format_email_body(start_iso,end_iso,meet_link,status,job_title)
    result = await send_email(agent, to_email=attendees_emails, body=email_body, meet_link=meet_link)

    return {"result": result}


