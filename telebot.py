import AppKit
import emoji
import pyttsx3
import re
import sys
import time
from queue import Queue
from telethon import TelegramClient, events

# Replace the values below with your own API ID, API hash, and phone number
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
phone_number = '+1YOUR_PHONE_NUMBER'
speaking_rate = 400

# Connect to Telegram API
client = TelegramClient('session_name', api_id, api_hash)

# Start the client and authenticate with your phone number
client.start(phone=phone_number)

# Initialize the NSSpeechSynthesizer text-to-speech engine for the message text
message_engine = AppKit.NSSpeechSynthesizer.alloc().initWithVoice_(AppKit.NSSpeechSynthesizer.defaultVoice())

# Set the speaking rate of the speech synthesizer
message_engine.setRate_(speaking_rate)

# Define a regular expression pattern that matches all emoji characters
emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

# Define an asynchronous message handler function
@client.on(events.NewMessage)
async def handle_message(event):
    global selected_chat_name

    # Get the chat entity of the incoming message
    message_chat = await event.client.get_entity(event.chat_id)

    # Ignore messages from other chats
    if message_chat.title != selected_chat_name:
        return

    # Ignore messages with no text or with URLs, stickers, or media
    if not event.message.text or event.message.sticker or event.message.media or re.search("(?P<url>https?://[^\s]+)", event.message.text):
        return

    # Remove any emojis from the message text
    message_text = emoji_pattern.sub(r'', event.message.text)

    user = await event.client.get_entity(event.message.from_id)

    # Get your own user ID
    me = await client.get_me()

    # Ignore messages that you wrote or from bots
    if user.id == me.id or user.bot:
        return

    if user.last_name:
        name = f"{user.first_name} {user.last_name}"
    else:
        name = f"{user.first_name}"

    print(name + ": " + message_text)

    # Check if the message contains Cyrillic symbols
    if re.search('[а-яА-Я]', message_text):
        # If the message contains Cyrillic symbols, set the voice to a Russian voice identifier string
        voice_id = 'com.apple.speech.synthesis.voice.milena'
        message_engine.setVoice_(voice_id)
    else:
        # Otherwise, use the default voice
        message_engine.setVoice_(AppKit.NSSpeechSynthesizer.defaultVoice())

    # Speak the author's name and the message text using the same NSSpeechSynthesizer instance
    message_engine.startSpeakingString_(name + " says: " + message_text)
    while message_engine.isSpeaking():
        time.sleep(0.1)

# Get the 20 most recent dialogs
dialogs = client.loop.run_until_complete(client.get_dialogs(limit=20))

# Print out the list of dialogs for the user to select from
for i, dialog in enumerate(dialogs):
    print(f"{i + 1}: {dialog.title}")

# Ask the user to select a chat to read messages from
selected_dialog = input("Enter the number of the chat to read messages from: ")

# Get the chat entity from the user's selection
selected_chat = dialogs[int(selected_dialog) - 1].entity

# Set the selected chat's name depending on whether it's a User or a Chat
if hasattr(selected_chat, 'title'):
    selected_chat_name = selected_chat.title
elif hasattr(selected_chat, 'first_name'):
    selected_chat_name = selected_chat.first_name
    if selected_chat.last_name:
        selected_chat_name += f" {selected_chat.last_name}"
else:
    selected_chat_name = getattr(selected_chat, 'username', None)
    if selected_chat_name is None:
        print("Selected chat is not a User or a Chat object")
        client.disconnect()
        sys.exit()

# Start the event loop to listen for new messages in the selected chat
client.run_until_disconnected()

# Disconnect from the Telegram API
client.disconnect()
