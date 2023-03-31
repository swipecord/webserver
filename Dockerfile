FROM python:3.10-slim
EXPOSE 8000
# Установите рабочую директорию
WORKDIR /app

# Установите зависимости из файла poetry.lock
COPY poetry.lock pyproject.toml /app/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

# Скопируйте все файлы в рабочую директорию
COPY . /app

# Установите переменные окружения
ENV MYSQL_DATABASE=se_backend \
    MYSQL_USER=root \
    MYSQL_PASSWORD=bebrasus69 \
    MYSQL_HOST=db \
    MYSQL_PORT=3306

# Запустите сервер FastAPI
CMD ["poetry", "run", "start"]
