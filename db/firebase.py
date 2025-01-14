import firebase_admin
from firebase_admin import credentials, db




def initialize_firebase():
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://frisk-dizziedbliss-default-rtdb.firebaseio.com/'
})
    
def add_flashcard(question, answer):
    ref = db.reference('flashcards')
    ref.push({
        'question': question,
        'answer': answer
    })

def get_flashcards():
    ref = db.reference('flashcards')
    return ref.get()
    