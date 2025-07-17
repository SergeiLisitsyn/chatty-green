. Настраиваем PostgreSQL на Webdock
в терминале WEBDOCK
Предположим, ты уже установил PostgreSQL. Теперь:

✅ Создай пользователя и базу:
bash
создаем user
sudo -u postgres createuser chatty --pwprompt
cоздаем DB
sudo -u postgres createdb chatty_db -O chatty
и так user у нас chatty, db cahtty_db, password chatty_db


🔹 Вариант 1: Миграции → Дамп → Импорт (рекомендуется)
Создай структуру базы через миграции:

bash
python manage.py migrate
Это создаст пустые таблицы на Webdock.

На Render (старом сервере) создай SQL-дамп только с данными (без DROP/CREATE TABLE):

bash
pg_dump -U olduser -h oldhost -d olddb --data-only > data_only.sql
Загрузи дамп на Webdock и импортируй:

bash
psql -U chatty -d chatty_db -h localhost -f data_only.sql
👉 Это зальёт только данные в уже подготовленные таблицы, не ломая их структуру.

для роботы на гите в webdock shell используй webdock tocken из .env

🐘 Создание дампа PostgreSQL
🔧 На сервере Webdock выполни:

bash
pg_dump -U chatty -h localhost -Fc chatty_clean_db> chatty_backup_$(date +%Y-%m-%d).dump

🧾 Пояснения:
-U postgres — имя пользователя БД

-Fc — PostgreSQL custom format (удобно для восстановления)

$(date +%Y-%m-%d) — добавляет дату в название файла

✅ Как создать JSON-дамп базы через manage.py
python manage.py dumpdata --natural-primary --natural-foreign --indent 2 > backup_$(date +%Y-%m-%d).json
🔹 Пояснения:

--natural-primary и --natural-foreign — делают связи понятными (не только по ID)

--indent 2 — форматирует JSON (удобнее читать)

> backup_2025-07-17.json — имя файла (можно с датой)

