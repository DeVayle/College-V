import ssl
import socket
from datetime import datetime


def get_ssl_expiry_days(hostname):
    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        expiry_date_str = cert['notAfter']
        expiry_date = datetime.strptime(expiry_date_str, '%b %d %H:%M:%S %Y %Z')

        current_date = datetime.utcnow()
        days_left = (expiry_date - current_date).days

        return days_left
    except ssl.SSLError:
        return None  # Если сайт не поддерживает SSL
    except Exception as e:
        raise e  # Обработка других возможных ошибок


def main():
    hostname = input("Введите адрес сайта (без 'https://'): ")
    try:
        days_left = get_ssl_expiry_days(hostname)
        if days_left is None:
            print(f"Сайт {hostname} не поддерживает SSL-сертификаты.")
        elif days_left > 0:
            print(
                f"До окончания срока действия SSL-сертификата сайта {hostname} осталось {days_left} дней! Не забудьте обновить сертификат!")
        else:
            print(f"Срок действия SSL-сертификата сайта {hostname} истек! Срочно обновите его!")
    except Exception as e:
        print(f"Ошибка при получении информации: {e}")

    input("\nНажмите Enter, чтобы закрыть программу...")


if __name__ == "__main__":
    main()
