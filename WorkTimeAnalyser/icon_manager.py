import asyncio
import os
import threading
import time

from pystray import Icon
from pystray import Menu as TrayMenu, MenuItem as TrayMenuItem
from PIL import Image, ImageDraw

# Возможные состояния: 'waiting', 'paused', 'active'
tray_state = 'waiting'
_icon_instance = None
ICON_PATH = os.path.join(os.environ.get("SystemDrive", "C:"), '/Program Files/WorkTimeAnalyser/alpha_games_logo_v3.ico')

def generate_icon(color: str) -> Image.Image:
    """Создаёт круглую иконку заданного цвета"""
    img = Image.new('RGB', (64, 64), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.ellipse((16, 16, 48, 48), fill=color)
    return img

def get_state_description_and_icon(state: str):
    mapping = {
        'waiting': ('Ожидание начала работы над проектом...', '#007bff'),
        'paused':  ('Время работы не идёт, продолжите работать над проектом чтобы возобновить...', '#f6ff00'),
        'ignored': ('Проект игнорируется, вы можете изменить это в Time Analyser Menu, который найдёте в меню пуск', '#ff0000'),
        'active':  ('Всё ок, время идёт', '#00ff00'),
    }
    desc, color = mapping.get(state, ('Неизвестное состояние', '#000000'))
    path = ICON_PATH

    try:
        base_icon = Image.open(path).convert("RGBA").resize((64, 64))
    except Exception as e:
        print(f"Не удалось загрузить иконку {path}: {e}")
        base_icon = Image.new('RGBA', (64, 64), (0, 0, 0, 255))  # чёрный квадрат

    # Рисуем кружочек в нижнем правом углу
    overlay = Image.new('RGBA', base_icon.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    radius = 30
    x, y = base_icon.size[0] - radius - 4, base_icon.size[1] - radius
    draw.ellipse((x, y, x + radius, y + radius), fill=color)

    # Накладываем кружок на иконку
    result_icon = Image.alpha_composite(base_icon, overlay)

    return desc, result_icon


def run_tray_loop_sync():
    global _icon_instance

    icon = Icon("WorkTimeAnalyser")

    def on_exit(icon, item):
        icon.stop()

    icon.menu = TrayMenu(TrayMenuItem('Выход', on_exit))
    description, image = get_state_description_and_icon(tray_state)
    icon.icon = image
    icon.title = f"Статус: {description}"

    def update_icon():
        while True:
            description, image = get_state_description_and_icon(tray_state)
            icon.icon = image
            icon.title = f"Статус: {description}"
            time.sleep(1)

    _icon_instance = icon
    threading.Thread(target=update_icon, daemon=True).start()
    icon.run()

def start_tray_async():
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, run_tray_loop_sync)

def update_tray_state(state: str):
    """Обновление глобального состояния иконки"""
    global tray_state
    tray_state = state
