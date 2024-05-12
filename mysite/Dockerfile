# Используйте официальный образ Python как базовый
FROM python:3.11

# Установите рабочую директорию в контейнере
WORKDIR /app

# Установите зависимости
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируйте исходный код проекта в контейнер
COPY . .

# Откройте порт 8000 для внешнего мира
EXPOSE 8000

# Запустите сервер разработки Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]