# sender.py (отправщик - Windows)
# -*- coding: utf-8 -*-

"""
Этот скрипт используется для отправки текстовых данных через сокетное соединение.

Функционал:
1. Отправка содержимого текстового файла на указанный сервер.
2. Отправка произвольного текста, переданного в функцию.

Используемые технологии:
- socket: для создания и управления соединением.
- os: для работы с путями файловой системы.

Как использовать:
1. Укажите параметры соединения (IP-адрес и порт) и путь к файлу.
2. Выберите метод отправки: из файла или передача текста через функцию.
"""
import asyncio
import random
import socket
import os

import project
import time_to_file_operator
from encrypted_file_operator import load_worktime_data


async def send_worktime_data(registered_projects, active_project, username):
    try:
        if active_project in registered_projects:
            project_path = registered_projects[active_project].project_path
            global_file_path = os.path.join(project_path, time_to_file_operator.LOCAL_PATH_TO_FILE, f'{username}.worktime')
            content = load_worktime_data(global_file_path)
            lines = content.splitlines()
            user_nick = lines[0][6:]
            project_name = lines[1][9:]
            content = f"{user_nick} - {project_name}\n{content}"
            if content:
                return await send_text_info_async(content)
        return False
    except Exception as e:
        print(f'Ошибка при отправке данных: {e}')
        return False

def get_file_to_send():
    """
    Возвращает путь к файлу для отправки, находящемуся на рабочем столе пользователя.

    :return: Путь к файлу в виде строки.
    """
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    return os.path.join(desktop, "file_to_send.txt")

def send_data(data, host, port):
    """
    Отправляет данные на указанный сервер.

    :param data: Данные для отправки (bytes).
    :param host: IP-адрес сервера (str).
    :param port: Порт сервера (int).
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            print(f"Соединение с {host}:{port}")
            s.sendall(data)
            print("Данные успешно отправлены.")
    except Exception as e:
        print(f"Ошибка: {e}")

def send_file(file_path, host, port):
    """
    Отправляет содержимое файла на указанный сервер.

    :param file_path: Путь к файлу для отправки (str).
    :param host: IP-адрес сервера (str).
    :param port: Порт сервера (int).
    """
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            send_data(data, host, port)
    except FileNotFoundError:
        print(f"Файл '{file_path}' не найден.")
    except Exception as e:
        print(f"Ошибка: {e}")

def send_text_info(text, host="178.250.186.26", port=54545):
    """
    Отправляет текст, переданный в функцию, на указанный сервер.

    :param text: Текст для отправки (str).
    :param host: IP-адрес сервера (str).
    :param port: Порт сервера (int).
    """
    print(text)
    try:
        data = text.encode('utf-8')
        send_data(data, host, port)
    except Exception as e:
        print(f"Ошибка: {e}")

def send_file_info(file_path=None, host="178.250.186.26", port=54545):
    """
    Отправляет содержимое файла на указанный сервер.

    :param file_path: Путь к файлу для отправки (str, optional).
    :param host: IP-адрес сервера (str).
    :param port: Порт сервера (int).
    """
    if file_path is None:
        file_path = get_file_to_send()
    print(f"Отправка файла: {file_path}")
    send_file(file_path, host, port)

# Добавляем асинхронные версии функций
async def async_send_data(data, host, port):
    """Асинхронная отправка данных"""
    try:
        reader, writer = await asyncio.open_connection(host, port)
        writer.write(data)
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        print(f"Данные успешно отправлены на {host}:{port}")
        return True
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return False

async def send_text_info_async(text, host="178.250.186.26", port=54545):
    """Асинхронная отправка текста"""
    try:
        data = text.encode('utf-8')
        return await async_send_data(data, host, port)
    except Exception as e:
        print(f"Ошибка: {e}")
        return False

