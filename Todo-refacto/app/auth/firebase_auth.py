from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer
import firebase_admin
from firebase_admin import auth, credentials

security = HTTPBearer()

def verify_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except firebase_admin.exceptions.FirebaseError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(token: str = Security(security)):
    decoded_token = verify_token(token.credentials)
    return decoded_token
