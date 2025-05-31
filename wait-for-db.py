import os
import sys
import time
import socket


def wait_for_db():
    db_url = os.getenv('DATABASE_URL')
    host = db_url.split('@')[1].split(':')[0]
    port = int(db_url.split(':')[-1].split('/')[0])
    timeout = 60
    start = time.time()

    print(f"Ожидание PostgreSQL ({host}:{port})...")
    while time.time() - start < timeout:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((host, port))
                print("✅ PostgreSQL доступен")
                return
        except Exception as e:
            print(f"⏳ Ожидание... ({int(time.time() - start)}с)")
            time.sleep(1)

    print("⛔ Таймаут подключения к PostgreSQL!")
    sys.exit(1)


if __name__ == "__main__":
    wait_for_db()