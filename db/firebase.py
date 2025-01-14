import firebase_admin
from firebase_admin import credentials, db
import os
import json
from dotenv import load_dotenv
import random
import asyncio

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

async def practice_flashcards(ctx, bot):
    """ Get a random flashcard question and wait for the answer from the user """
    flashcards = get_flashcards()
    if not flashcards:
        await ctx.send("No flashcards available.")  # Send message to the Discord channel
        return
    
    key = random.choice(list(flashcards.keys()))
    card = flashcards[key]
    
    await ctx.send(f"Flashcard: {card['question']}")  # Send the question to the Discord channel
    
    def check(m):
        # Check if the message is from the same user who triggered the command and in the same channel
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        # Wait for a response from the user
        msg = await bot.wait_for('message', check=check, timeout=30.0)
        if msg.content.lower() == card['answer'].lower():
            await ctx.send("Correct!")  # Notify the user if the answer is correct
        else:
            await ctx.send(f"Incorrect! The answer is: {card['answer']}")  # If wrong, show the correct answer
    except asyncio.TimeoutError:
        await ctx.send("You took too long to answer! Try again.")  # If the user doesn't answer in time