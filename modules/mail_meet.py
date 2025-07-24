import asyncio
from datetime import datetime
from openai import OpenAI
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from mcp_use import MCPClient, MCPAgent
from langchain_openai import ChatOpenAI
import time
def create_event(start_iso, end_iso, attendees_emails, summary="Meeting"):
    creds = Credentials(
        token=None,
        refresh_token="token",
        token_uri="https://oauth2.googleapis.com/token",
        client_id="id",
        client_secret="secret",
        scopes=["https://www.googleapis.com/auth/calendar"]
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

async def send_email(agent, to_email, body, subject="Meeting Invitation", meet_link=None):
    final_body = body
    if meet_link:
        final_body += f"\n\nJoin via Google Meet: {meet_link}"

    command = (
        "send email with these exact parameters: "
        "{"
        f"'to': '{to_email}', "
        f"'subject': '{subject}', "
        f"'body': '''{final_body}''', "
        f"'cc': '', "
        f"'bcc': ''"
        "}"
    )
    
    result = await agent.run(command)
    return result
import pytz

def format_email_body(start_iso, end_iso, meet_link, accepted=True):
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
        paris_tz = pytz.timezone("Europe/Paris")
        dt_start = dt_start.astimezone(paris_tz)
        dt_end = dt_end.astimezone(paris_tz)

        date_str = dt_start.strftime("%A %d %B %Y")  # e.g. Tuesday 22 July 2025
        start_str = dt_start.strftime("%H:%M")
        end_str = dt_end.strftime("%H:%M")

        body = (
            f"Hello,\n\n"
            f"We are pleased to inform you that your application has been accepted for a technical interview.\n"
            f"The interview is scheduled on {date_str} from {start_str} to {end_str} (Europe/Paris time).\n\n"
            f"Please join the Google Meet using the following link:\n{meet_link}\n\n"
            f"Best regards,"
        )
    else:
        body = (
            "Hello,\n\n"
            "Thank you for your interest. Unfortunately, we regret to inform you that your application has not been accepted.\n\n"
            "We wish you the best in your future endeavors.\n\n"
            "Best regards,"
        )
    return body
async def main():
    config = {
  "mcpServers": {
    "google-workspace": {
      "command": "node",
      "args": ["C:\\Users\\ramib\\google-workspace-mcp-server\\build\\index.js"],
      "env": {
        "GOOGLE_CLIENT_ID": "clientid",
        "GOOGLE_CLIENT_SECRET": "clientsecret",
        "GOOGLE_REFRESH_TOKEN": "token"
      }
    }
  }
}

    # 1. Charger config du serveur MCP
    client = MCPClient.from_dict(config)
    llm = ChatOpenAI(model="gpt-4o-mini",api_key="API_KEY")
    # 3. Créer un agent MCP (LLM + outil)
    agent = MCPAgent(llm=llm, client=client, max_steps=10)
    # Créer l'événement
    meet_link = create_event(
        start_iso="2025-07-22T15:00:00+01:00",
        end_iso="2025-07-22T16:00:00+01:00",
        attendees_emails=["xxxx.com"]
    )

    # Envoyer l'e-mail avec le lien Meet
    email_body = format_email_body("2025-07-22T15:00:00+01:00","2025-07-22T16:00:00+01:00",meet_link,False)
    result = await send_email(agent, to_email="xxxx@gmail.com", body=email_body, meet_link=meet_link)

    print("Résultat:", result)
if __name__ == "__main__":
    asyncio.run(main())

