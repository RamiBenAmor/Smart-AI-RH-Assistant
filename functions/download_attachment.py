import base64
import os

def download_attachment(service, user_id, msg_id, save_path='C:\\Users\\ramib\\OneDrive\\Bureau\\CV_RH\\uploads\\cv'):
    try:
        # Récupérer le message complet
        message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()

        # Parcourir les parties du message pour trouver l'attachement PDF
        for part in message['payload']['parts']:
            if 'filename' in part and part['filename'].endswith('.pdf'):
                attachment_id = part['body']['attachmentId']
                attachment = service.users().messages().attachments().get(
                    userId=user_id, messageId=msg_id, id=attachment_id).execute()

                # Décoder le contenu de l'attachement
                data = attachment['data']
                file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))

                # Créer le dossier de sauvegarde si nécessaire
                if not os.path.exists(save_path):
                    os.makedirs(save_path)

                # Sauvegarder le fichier
                file_path = os.path.join(save_path, part['filename'])
                with open(file_path, 'wb') as f:
                    f.write(file_data)

                print(f"✅ Fichier téléchargé : {file_path}")
                return file_path

        print("❌ Aucun fichier PDF trouvé dans cet e-mail.")

    except Exception as e:
        print(f"❌ Erreur lors du téléchargement de l'attachement : {e}")