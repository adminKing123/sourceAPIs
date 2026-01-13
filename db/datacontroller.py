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
class DB:
    def __init__(self):
        cred = credentials.Certificate(json.loads(CONFIG.FIREBASE_CREDENTIALS))
        firebase_admin.initialize_app(cred)
        self.client = firestore.client()

        self.user = User(self.client)

db = DB()