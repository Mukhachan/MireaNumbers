# Выбор базового образа с Python
FROM python:3.13

# Создание виртуального окружения
RUN python3 -m venv /app/env

# Установка рабочей директории
WORKDIR /app

# Копирование файлов проекта
COPY . /app
COPY *.json /app/

# Активация виртуального окружения
ENV PATH="/app/env/bin:$PATH"

# Установка зависимостей
RUN pip3 install -r requirements.txt

# Открытие порта для взаимодействия с приложением
EXPOSE 8080

# Запуск приложения
CMD python3 main.py