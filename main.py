from datetime import datetime
import asyncio, json
import os

from config import *
from GSheets import load_data
from image_reader import recognize_number

import aiogram
from aiogram import Bot, Dispatcher, F
from aiogram import types, filters, enums



dp = Dispatcher()

@dp.message(filters.CommandStart())
async def start(message: types.Message, command: filters.Command) -> None:
    start_code = command.args
    if start_code:
        new: dict = json.load(open("users.json"))
        if start_code in new.keys():
            new[start_code]['user']['username'] = message.from_user.username
            new[start_code]['chat_id'] = message.chat.id
            new["validated"][message.chat.id] = start_code

            json.dump(new, open("users.json", "w", encoding='utf8'), ensure_ascii=False)
            del new
            await message.answer("Всё круто! Теперь можешь скидывать номерки")
            
        else:
            await message.answer("Такого кода нет")

    else:
        await message.answer("Не введён код")


@dp.message(F.photo)
async def handle_photo(message: types.Message) -> None:
    user = json.load(open("users.json"))
    if str(message.chat.id) in user["validated"].keys():
        user = user[user["validated"][str(message.chat.id)]]
        photo_id = message.photo[-1].file_id
        photo_file = await bot.get_file(photo_id)
        
        destination = f"images/{datetime.now()}.jpg"
        os.mkdir('images/') if not os.path.exists('images/') else None
        await bot.download_file(photo_file.file_path, destination=destination)
        await message.answer("Изображение скачано успешно!")
        await message.answer("Анализируем изображение!")
        
        recognized_data = recognize_number(destination)
        if len(recognized_data) == 0:
            await message.answer("Не удалось распознать номер")
            return
        else:
            number = int(recognized_data[0][1])

        await message.answer("Загружаем данные в таблицу")
        load_data(
            number=number,
            author=user['user']['name'],
            date=datetime.now().date(),
            destination=destination
        )
        del user
        await message.answer("Данные загружены!")

    else:
        await message.answer("Ты не авторизирован")




if __name__ == "__main__":
    print('Bot started')

    bot = Bot(token=BOT_TOKEN)
    asyncio.run(dp.start_polling(bot))
