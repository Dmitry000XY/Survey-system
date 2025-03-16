# Survey System (Beta)

## Описание

Данная система анкетирования находится в стадии бета-тестирования. Она предназначена для сбора данных пользователей с использованием API, реализованного на FastAPI.

## Быстрый старт

1. Клонируйте репозиторий и перейдите в его директорию.
2. Создайте файл `.env` и пропишите в нем переменные для подключения к базе данных. Пример доступен в файле `.env.example`.
3. Установите зависимости с помощью:
   ```sh
   pip install -r requirements.txt
   ```
4. Запустите сервер командой:

   **For Windows:**

   ```sh
   python.exe -m uvicorn src.main:app --reload
   ```
   **For Linux:**

   ```sh
   python3 -m uvicorn src.main:app --reload
   ```

## Структура проекта

```
src/
├── configurations/
│   ├── __init__.py
│   ├── database.py
│   ├── settings.py
│   └── constants.py
├── dependencies/
│   ├── __init__.py
│   └── dependencies.py
├── models/
│   ├── __init__.py
│   ├── base.py
│   ├── custom_types.py
│   ├── users.py
│   ├── clients.py
│   ├── users_clients.py
│   ├── questionnaire_answers.py
│   ├── answers.py
│   ├── questionnaires.py
│   ├── questions.py
│   └── settings.py
├── repositories/
│   ├── __init__.py
│   ├── users.py
│   ├── clients.py
│   ├── users_clients.py
│   ├── questionnaire_answers.py
│   ├── answers.py
│   ├── questionnaires.py
│   ├── questions.py
│   └── settings.py
├── routers/
│   ├── __init__.py
│   ├── debug/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── clients.py
│   │   ├── users_clients.py
│   │   ├── questionnaire_answers.py
│   │   ├── answers.py
│   │   ├── questionnaires.py
│   │   ├── questions.py
│   │   └── settings.py
├── schemas/
│   ├── __init__.py
│   ├── users.py
│   ├── clients.py
│   ├── users_clients.py
│   ├── questionnaire_answers.py
│   ├── answers.py
│   ├── questionnaires.py
│   ├── questions.py
│   └── settings.py
├── services/
│   ├── __init__.py
│   ├── users.py
│   ├── clients.py
│   ├── users_clients.py
│   ├── questionnaire_answers.py
│   ├── answers.py
│   ├── questionnaires.py
│   ├── questions.py
│   └── settings.py
├── main.py
└── __init__.py
.env
.env.example
requirements.txt
README.md
```

