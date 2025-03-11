import json

BOT_TOKEN = json.load(open("params.json"))['bot_token']
FOLDER_ID = json.load(open("params.json"))['folder_id']
users: dict = json.load(open("users.json"))
