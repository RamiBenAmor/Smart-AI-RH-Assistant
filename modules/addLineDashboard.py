import pandas as pd
import os
def add_to_dashboard(CSV_PATH, name, email, date, cv_path, sent_date,job_title):
    new_row = {
        "Candidate Name": name,
        "Email": email,
        "Interview Date": date,
        "CV Path": cv_path,
        "Sent Date": sent_date,
        "job_title":job_title
    }
    # Si le fichier n'existe pas, on le crée avec le premier candidat
    if not os.path.exists(CSV_PATH):
        df = pd.DataFrame([new_row])
    else:
        df = pd.read_csv(CSV_PATH)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Enregistrer les données
    df.to_csv(CSV_PATH, index=False)
