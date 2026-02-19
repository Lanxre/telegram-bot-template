# Aiogram Clean Architecture Template

Современный шаблон Telegram-бота на базе **aiogram 3.x**, построенный по принципам чистой архитектуры (**Clean Architecture**). Проект поддерживает быструю смену СУБД (SQLite/PostgreSQL) и использует современный менеджер пакетов **uv**.

## 🚀 Стек технологий

*   **Language:** Python 3.14+
*   **Framework:** [aiogram 3.x](https://github.com/aiogram/aiogram)
*   **Database:** Pure SQL (поддержка SQLite и PostgreSQL)
*   **Data Validation:** Pydantic v2
*   **Package Manager:** [uv](https://github.com/astral-sh/uv)
*   **Logging:** Кастомный логгер с поддержкой цветов и форматирования

## 🏗 Архитектура

Проект разделен на логические слои для обеспечения масштабируемости и тестируемости:

1.  **Infrastructure Layer (`core/infrastructure`):**
    *   **Database:** Коннекторы для работы с разными БД и менеджер инициализации схем.
    *   **Repositories:** Работа с сырым SQL. Реализуют методы доступа к данным.
    *   **Services:** Бизнес-логика приложения. Координируют работу репозиториев и внешних API.
2.  **Internal Layer (`core/internal`):**
    *   Общие типы, перечисления (Enums), константы и базовые Pydantic-модели.
3.  **Presentation Layer:**
    *   **Handlers:** Обработка входящих обновлений от Telegram.
    *   **Middleware:** Внедрение зависимостей (Services) в хендлеры и обработка контекста.

## 📁 Структура проекта

```text
.
├── core
│   ├── infrastructure
│   │   ├── database        # Коннекторы (SQLite/Postgres), менеджер БД и SQL-модели
│   │   ├── repositories    # Слой доступа к данным (UserRepo и др.)
│   │   └── services        # Бизнес-логика (UserService и др.)
│   └── internal
│       └── types           # Enums, константы и DTO (Pydantic модели)
├── handlers                # Роутеры и обработчики команд/сообщений
├── middleware              # Посредники (инъекция сервисов в хендлеры)
├── config                  # Конфигурация проекта (pydantic-settings / env)
├── logger                  # Настройка красивого логирования
├── utils                   # Вспомогательные утилиты (билдеры строк, команды)
├── assets                  # Статика (изображения, иконки)
├── main.py                 # Точка входа в приложение
├── dispatcher.py           # Настройка диспетчера и регистрация роутеров
├── pyproject.toml          # Зависимости проекта (uv)
└── bot.db                  # Локальная база данных (SQLite)
```

## ⚙️ Установка и запуск

1. **Подготовка**
Убедитесь, что у вас установлен uv.

2. **Клонирование и установка зависимостей**
```
git clone <repository_url>
cd <project_directory>
uv sync
```
3. **Настройка окружения**
Создайте файл **.env** в корне проекта (настройте параметры в config/config.py):

SQLite example
```
# TELEGRAM_BOT_TOKEN
TELEGRAM_BOT_TOKEN=<TELEGRAM_BOT_TOKEN>

# DATABASE
db_name=bot.db
db_user=admin
db_password=secret
db_host=localhost
db_port=5432
db_driver=aiosqlite
```