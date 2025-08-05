import os
from datetime import datetime, timedelta
from mcp_use import MCPClient, MCPAgent
from langchain_openai import ChatOpenAI
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
from download_attachment import download_attachment
from fastapi import APIRouter,Request
router=APIRouter()
def parse_result(result):
    try:
        if isinstance(result, str):
            data = json.loads(result)
        else:
            data = result

        if isinstance(data, dict):
            return data.get('message_ids', [])
        elif isinstance(data, list):
            return [item.get('id') for item in data if isinstance(item, dict) and 'id' in item]
        else:
            return []
    except Exception as e:
        print("❌ Erreur parsing JSON:", e)
        return []
creds = Credentials(
        token=None,
        refresh_token="xxx",
        token_uri="https://oauth2.googleapis.com/token",
        client_id="xxxxxxxx",
        client_secret="xxxxxxxxxxx",
scopes = ["https://www.googleapis.com/auth/calendar","https://www.googleapis.com/auth/gmail.send","https://www.googleapis.com/auth/gmail.readonly"]
)
config = {
  "mcpServers": {
    "google-workspace": {
      "command": "node",
      "args": ["C:\\Users\\ramib\\google-workspace-mcp-server\\build\\index.js"],
      "env": {
        "GOOGLE_CLIENT_ID": "xxxxxxxxxxx",
        "GOOGLE_CLIENT_SECRET": "xxxxxxxxx",
        "GOOGLE_REFRESH_TOKEN": "xxxxxxxxxxx",
                "GOOGLE_REDIRECT_URI": "urn:ietf:wg:oauth:2.0:oob",
                "GOOGLE_SCOPES": "https://www.googleapis.com/auth/gmail.readonly"
      }
    }
  }
}
service = build('gmail', 'v1', credentials=creds)
async def  fetch_and_store_recent_cv_emails(job_name: str, days: int = 5, max_results: int = 50) -> dict:
    """
    Récupère les emails récents non lus contenant "Application_{job_name}" dans l'objet,
    télécharge les pièces jointes PDF (CVs) dans le dossier 'cv_FromMails/', et retourne
    un dictionnaire {job_name: [list de noms de fichiers PDF]}.

    Args:
        job_name (str): Titre du poste visé.
        days (int): Période de recherche en jours.
        max_results (int): Limite d'emails à traiter.

    Returns:
        dict: {job_name: [list de noms de fichiers PDF]}
    """
    # Calculer la date
    after_date = datetime.now() - timedelta(days=days)
    after_str = after_date.strftime('%Y/%m/%d')
    # Initialiser LLM et MCP client
    llm = ChatOpenAI(model="gpt-4o-mini", api_key="xxxxxxxxx")
    client = MCPClient.from_dict(config)
    agent = MCPAgent(llm=llm, client=client, max_steps=10)
    # 1. Define the folder to save the resumes
# 3. Ask the agent to retrieve unread emails with attachments
   
    prompt = (
    f"Search Gmail for all emails received after {after_str} "
    f"with a subject containing 'Application_{job_name}'. "
    f"Return the result STRICTLY as a JSON object with this exact structure:\n"
    f"{{\"message_ids\": [\"abc123\", \"def456\"]}}\n"
    f"Do not return any explanation, text, or formatting. Return ONLY the JSON object.")
    # 1. Recherche et liste des emails
    response = await agent.run(prompt)
    if isinstance(response, str):
        try:
            data = json.loads(response)
        except json.JSONDecodeError as e:
            print("❌ Erreur parsing JSON:", e)
            data = []
    elif isinstance(response, (list, dict)):
        data = response
    else:
        data = []
    print(f"Type de data: {type(data)}")
    return data
@router.post("/downoald_search")
async def downoald_search(request:Request):
    data = await request.json()
    job_name=data.get("job_description_name")
    days=data.get("days")
    max_results=100
   # job_name = "data_scientist"
    result = await fetch_and_store_recent_cv_emails(job_name, days, max_results)
    print("Type de result:", type(result))
    print(result)
    message_ids = parse_result(result)
    print("Liste des IDs :", message_ids)
    file_paths=[]
    for message_id in message_ids:
        file_path = download_attachment(service, 'me', message_id)
        if file_path:
            file_paths.append(file_path)
    return file_paths
