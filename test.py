from config import users

for key in users.keys():
    print(f"{users[key]['user']['name']} - https://t.me/MireaNumbersBot?start={key}")