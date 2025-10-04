# MireaNumbers - бот для сохранения фото номерков из гардероба в Google Таблицу

## Описание

Этот проект представляет собой Telegram-бота, написанного на Python 3.12, который позволяет отправлять фотографии номерков из гардероба. Бот сохраняет полученные фотографии в Google Таблицу, размещая их в соответствующих ячейках.

## Функционал

- Приём фотографий номерков из Telegram.
- Сохранение фотографий в Google Таблицу.
- Автоматическое размещение фото в нужной ячейке таблицы.

## Требования

- Docker (для запуска контейнера)
- Аккаунт Google с доступом к Google Sheets API
- Telegram-бот (токен)

## Установка и запуск через Docker

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Mukhachan/MireaNumbers.git
2. Перейдите в директорию:
   ```bash
   cd MireaNumbers
2. Получите файл credentials.json. [Инструкция](https://support.google.com/workspacemigrate/answer/10839762?hl=ru#zippy=)
3. Создайте файл params.json:
   ```JSON
    {
     "bot_token" : <API TOKEN бота>,
     "folder_id" : <FOLDER ID гугл таблицы>
    }
    
4. Запустите докер-контейнер:
   ```bash
   docker build -t mirea-numbers .
   ```
