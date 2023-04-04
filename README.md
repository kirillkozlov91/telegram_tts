# Telegram Text To Speech Script for Group Chats

Created with the help of ChatGPT 3.5

This is a Python script to read Telegram messages locally and read them aloud through Text To Speech. 
<br>
Supports Cyrillic words. Made for macOS to run with maOS voice libraries. Tested on macOS only.

Replace the APP IDs in the script with your IDs that you can find here:
<br>
https://my.telegram.org/apps

Replace the phone number with your phone number that you use for Telegram, in the following format:
<br>
+18005551234

Run the script via the following command:
<br>
`python3 telebot.py`

If it complains about any missing packages, install them via:
<br>
`pip3 install <missingpackagename>`

Once you run the script, it will fetch the latest 20 most recent active chats.
You will select some chat, and the script will start listening for new incoming messages for that chat.
Using Apple's TTS it will read messages aloud and will print the messages as it goes through each one.

URLs, stickers, attachements are ignored.
If you know how to make them work, please reach out or feel free to fork
