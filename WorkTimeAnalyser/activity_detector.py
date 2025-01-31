import asyncio
from pynput import keyboard, mouse
from datetime import datetime, timedelta

last_activity_time = datetime.now()  # Время последней активности
NO_ACTIVITY_TIMEOUT = 60  # Таймаут бездействия в секундах
timeout = False  # Флаг состояния таймаута


def reset_timer():
    """Сброс таймера активности"""
    global last_activity_time, timeout
    last_activity_time = datetime.now()
    timeout = False


# Обработчики событий ввода
def on_key_press(_):
    reset_timer()


def on_mouse_activity(*_):
    reset_timer()


async def track_timeout():
    """Мониторинг времени бездействия"""
    global timeout
    while True:
        inactivity = datetime.now() - last_activity_time
        if inactivity > timedelta(seconds=NO_ACTIVITY_TIMEOUT):
            timeout = True
        await asyncio.sleep(1)


async def start_tracking_activity_timeout():
    """Запуск отслеживания активности"""
    # Инициализация слушателей
    keyboard_listener = keyboard.Listener(on_press=on_key_press)
    mouse_listener = mouse.Listener(
        on_click=on_mouse_activity,
        on_scroll=on_mouse_activity
    )

    # Запуск в фоновом режиме
    keyboard_listener.start()
    mouse_listener.start()

    # Запуск мониторинга таймаута
    await track_timeout()


if __name__ == "__main__":
    try:
        asyncio.run(start_tracking_activity_timeout())
    except KeyboardInterrupt:
        print("Программа остановлена")