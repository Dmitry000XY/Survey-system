# Survey System (Beta)

## Описание

Backend-система анкетирования на FastAPI с синхронизацией форм и ответов с существующим сайтом на WordPress и
Formidable Forms.

Проект находится в активной разработке: публичный предметный API и клиент Telegram ещё не реализованы.

## Быстрый старт

1. Клонируйте репозиторий и перейдите в его директорию.
2. Создайте `.env` на основе `.env.example` и укажите параметры подключения к PostgreSQL и WordPress/MySQL.
3. Установите [uv](https://docs.astral.sh/uv/getting-started/installation/), если он ещё не доступен в системе.
4. Создайте окружение и установите зафиксированные зависимости:

   ```sh
   uv sync --locked
   ```

5. Запустите сервер:

   ```sh
   uv run uvicorn src.main:app --reload
   ```
