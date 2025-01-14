import firebase_admin
from firebase_admin import credentials, db
import os
import json
from dotenv import load_dotenv

load_dotenv()

firebase_key = os.getenv("FIREBASE_CREDENTIALS")

def initialize_firebase():
    """ Initialize Firebase app with credentials loaded from env """
    cred = credentials.Certificate(json.loads(firebase_key))
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://frisk-dizziedbliss-default-rtdb.firebaseio.com/'
    })

def add_flashcard(question, answer):
    """ Adds a flashcard to the Firebase database """
    ref = db.reference('flashcards')
    ref.push({
        'question': question,
        'answer': answer
    })

def get_flashcards():
    """ Retrieves all flashcards from the Firebase database """
    ref = db.reference('flashcards')
    return ref.get()
