import ctypes
from ctypes import wintypes
import sys

def is_already_running():
    """
    Проверяет, запущено ли приложение с использованием мьютекса Windows.
    :return: True, если приложение уже запущено. False, если нет.
    """
    # Уникальное имя мьютекса
    mutex_name = "Global\\WorkTimeAnalyser"

    # Создание мьютекса через WinAPI
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    CreateMutex = kernel32.CreateMutexW
    CreateMutex.argtypes = [wintypes.LPVOID, wintypes.BOOL, wintypes.LPCWSTR]
    CreateMutex.restype = wintypes.HANDLE

    # Проверка последней ошибки
    GetLastError = kernel32.GetLastError
    ERROR_ALREADY_EXISTS = 183

    # Создаём мьютекс
    handle = CreateMutex(None, False, mutex_name)

    # Проверяем, существует ли уже мьютекс
    if not handle or GetLastError() == ERROR_ALREADY_EXISTS:
        return True  # Приложение уже запущено

    return False
