from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore, auth
import json
from config import CONFIG

class User:
    def __init__(self, client):
        self.client = client
    
    def authenticate(self, token):
        decoded = auth.verify_id_token(token)
        return decoded

class File:
    def __init__(self, client):
        self.client = client
    
    def add_file(self, user_id, file_data, chat_id="", parent_id="root"):
        try:
            file_id = file_data.get("file_id")
            if not file_id:
                raise ValueError("file_data must contain 'file_id'")
            data = {
                "id": file_id,
                "type": "file",
                "meta_data": file_data,
                "parent_id": parent_id,
                "owner_id": user_id,
                "created_at": datetime.utcnow().isoformat() + "Z",
                "chat_id": chat_id
            }
            
            doc_ref = self.client.collection("files").document(data["id"])
            doc_ref.set(data)
            return doc_ref.id
        except Exception as e:
            print(f"Error adding file: {e}")

    def remove_file(self, file_id):
        try:
            doc_ref = self.client.collection("files").document(file_id)
            doc_ref.delete()
            return True
        except Exception as e:
            print(f"Error removing file: {e}")
            return False
    
    def get_file(self, file_id):
        try:
            doc_ref = self.client.collection("files").document(file_id)
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            else:
                return None
        except Exception as e:
            print(f"Error getting file: {e}")
            return None

class DB:
    def __init__(self):
        cred = credentials.Certificate(json.loads(CONFIG.FIREBASE_CREDENTIALS))
        firebase_admin.initialize_app(cred)
        self.client = firestore.client()

        self.user = User(self.client)
        self.file = File(self.client)

db = DB()