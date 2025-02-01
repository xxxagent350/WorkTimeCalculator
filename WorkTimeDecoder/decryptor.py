import random
import sys
import subprocess
from cryptography.fernet import Fernet
import os

# Ключ для расшифровки (замените на свой сгенерированный ключ)
SHARED_KEY = b'rjE884AvlhsJCHdcgB5Ub-S08fPq9IH-GcKqLpjG_n0='
fernet = Fernet(SHARED_KEY)

def decrypt_and_open(filepath):
    """Расшифровывает файл .worktime и открывает его в блокноте"""
    try:
        with open(filepath, "rb") as file:
            encrypted_data = file.read()
            decrypted_data = fernet.decrypt(encrypted_data).decode("utf-8")

        # Удаляем последнюю строку, это - хеш
        decrypted_data = "\n".join(decrypted_data.splitlines()[:-1])

        temp_file = "decrypted_temp.txt"
        with open(temp_file, "w", encoding="utf-8") as temp:
            temp.write(decrypted_data)

        # Открыть в блокноте
        subprocess.run(["notepad", temp_file])

        # Удалить временный файл после использования
        os.remove(temp_file)
    except Exception as e:
        print(f"Ошибка при расшифровке или открытии файла: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: decryptor.py <путь_к_файлу>")
    else:
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            decrypt_and_open(file_path)
        else:
            print(f"Файл не найден: {file_path}")
