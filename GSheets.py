from datetime import date, datetime
import json
import os.path

from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google.oauth2 import service_account


CREDENTIALS_FILE = json.load(open('credentials.json'))
spreadsheet_id = "1-DJbY7dupeyDLoqduzLhJNYZ2798nsE7GYDX-aJi2eA"

def change_permissions(image_id: str):
    body = {
        'role': 'reader',
        'type': 'anyone'
    }

    response = drive_service.permissions().create(
        fileId=image_id,
        body=body
    ).execute()

    return response

def load_text(number: int, author: str, date: date):
    data = [str(number), author, str(date)]
    # values = sheets_service.spreadsheets().values().append(
    #     spreadsheetId = spreadsheet_id,
    #     range = f'A{number}:C{number}',
    #     valueInputOption = 'USER_ENTERED',
    #     body = {
    #          'values' : [data]
    #         },

    # ).execute()

    return data


def load_photo(number: int, destination: str):
    # Загрузка картинки в Google Drive
    file_metadata = {'name': destination.replace("image/", "")}
    media = MediaFileUpload(destination, mimetype='image/jpeg')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    insert_image = f'=IMAGE("https://drive.google.com/uc?export=view&id={file.get("id")}")'

    # values = sheets_service.spreadsheets().values().append(
    #     spreadsheetId = spreadsheet_id,
    #     range = f'D{number}:D{number}',
    #     valueInputOption = 'USER_ENTERED',
    #     body = {
    #          'values' : [insert_image]
    #         },

    # ).execute()

    return file, insert_image

def delete_photo(destination: str):
    os.remove(destination) if os.path.exists(destination) else None


def load_data(number: int, author: str, date: date, destination: str):
    global credentials, drive_service, sheets_service
    credentials = service_account.Credentials.from_service_account_info(CREDENTIALS_FILE)
    drive_service = build('drive', 'v3', credentials=credentials)
    sheets_service = build('sheets', 'v4', credentials=credentials) # http=httpAuth

    file, insert_image = load_photo(number, destination) # Загружаем картинку в Google Drive и вставляем в таблицу
    change_permissions(file.get("id")) # Меняем права доступа к картинке
    data = load_text(number, author, date) # Вставляем текст в картинку
    delete_photo(destination) # Удаляем картинку с компьютера


    data.append(insert_image)
    response = sheets_service.spreadsheets().values().append(
        spreadsheetId = spreadsheet_id,
        range = f'A{number}:D{number}',
        valueInputOption = 'USER_ENTERED',
        body = {
             'values' : [data]
             },


    ).execute()



if __name__ == "__main__":
	print(load_data(18, "Артём", datetime.now().date(), "images/IMG_3108.JPG"))
