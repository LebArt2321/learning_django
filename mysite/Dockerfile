# Используем официальный образ Python как базовый
FROM python:3.11

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей в рабочую директорию
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем psycopg2-binary
RUN pip install psycopg2-binary

# Копируем остальные файлы проекта
COPY . .

# Открытие порта 8000
EXPOSE 8000

# Команда для запуска приложения
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "mysite.wsgi:application"]
