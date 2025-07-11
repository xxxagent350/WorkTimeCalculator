import hashlib
import os

from cryptography.fernet import Fernet

# Генерация и использование общего ключа (замените на свой сгенерированный ключ)
SHARED_KEY = b'rjE884AvlhsJCHdcgB5Ub-S08fPq9IH-GcKqLpjG_n0='
fernet = Fernet(SHARED_KEY)

def calculate_hash(content):
    """Вычисляет SHA256-хэш для строки"""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def verify_and_read_file(filepath):
    """Проверяет целостность файла с использованием хэша и расшифровывает его содержимое"""
    try:
        with open(filepath, "rb") as file:
            encrypted_data = file.read()
            decrypted_data = fernet.decrypt(encrypted_data).decode("utf-8")
            lines = decrypted_data.splitlines()
            content = "\n".join(lines[:-1])  # Все строки, кроме последней
            stored_hash = lines[-1].strip()  # Последняя строка — хэш

            if calculate_hash(content) == stored_hash:
                return content
            else:
                print("Целостность файла нарушена!")
                return None
    except FileNotFoundError:
        print("Файл не найден!")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

def write_file_with_hash(filepath, content):
    """Шифрует содержимое, добавляет хэш и сохраняет файл"""
    try:
        content_with_hash = f"{content}\n{calculate_hash(content)}"
        encrypted_data = fernet.encrypt(content_with_hash.encode("utf-8"))

        with open(filepath, "wb") as file:
            file.write(encrypted_data)
        return True
    except Exception as e:
        print(f"Ошибка при записи файла: {e}")
        return False

# Интеграция в проект
# Используйте write_file_with_hash и verify_and_read_file везде, где происходит чтение/запись файлов .worktime

def save_worktime_data(filepath, content):
    """Сохраняет данные о времени работы в зашифрованный файл"""
    # Получаем путь к директории
    dir_path = os.path.dirname(filepath)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path)  # Создаем директорию, если её нет

    success = write_file_with_hash(filepath, content)
    if success:
        pass
    else:
        print(f"Не удалось сохранить данные в {filepath}")

def load_worktime_data(filepath):
    """Загружает данные о времени работы из зашифрованного файла"""
    content = verify_and_read_file(filepath)
    if content:
        return content
    else:
        print(f"Не удалось загрузить данные из {filepath}")
        return None

# Пример использования в проекте
if __name__ == "__main__":
    test_path = "WORK_TIME/Lomi22880.worktime"
    loaded_content = load_worktime_data(test_path)
    if loaded_content:
        print("Загруженные данные:")
        print(loaded_content)
