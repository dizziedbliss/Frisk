import firebase_admin
from firebase_admin import credentials, db
import os
import json
from dotenv import load_dotenv
import random

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

def delete_flashcard(question):
    """ Deletes a flashcard from the Firebase database """
    flashcards = get_flashcards()
    for key, card in flashcards.items():
        if card['question'] == question:
            ref = db.reference(f'flashcards/{key}')
            ref.delete()
            return True
    return False

def practice_flashcards():
    """Get a random flashcard question and waits for the answer from the user"""
    flashcards = get_flashcards()
    if not flashcards:
        print("No flashcards available.")
        return
    
    key = random.choice(list(flashcards.keys()))
    card = flashcards[key]
    
    print(f"Flashcard: {card['question']}")
    answer = input("What is the answer? ")
    if answer == card['answer']:
        print("Correct!")
    else:
        print(f"Incorrect! The answer is: {card['answer']}")
