import firebase_admin
from firebase_admin import credentials, firestore
import os

cred = credentials.Certificate("app/auth/fast-todo-a0ceb-firebase-adminsdk-9fezn-0c82867738.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

