import asyncio
import os
import random
import time
from datetime import datetime
from tkinter import messagebox

import pygetwindow as gw
import psutil
import win32gui

import time_to_file_operator
from project import Project
from app_another_instance_checker import is_already_running
import activity_detector
import pickle_operator

from new_project_ui import open_new_project_ui
from enum import Enum

from start_ui import get_username
from network_operator import send_worktime_data
from icon_manager import start_tray_async, update_tray_state

USER_SETTINGS_DATA_PATH = os.path.join(os.environ.get("SystemDrive", "C:"), '/Program Files/WorkTimeAnalyser/user_data.pkl')
PROJECTS_DATA_PATH = os.path.join(os.environ.get("SystemDrive", "C:"), '/Program Files/WorkTimeAnalyser/projects.pkl')

PROJECTS_SEARCH_DELAY = 5 # Интервал поиска новых проектов
TIME_ADD_DELAY = 5 # Интервал добавления времени
FILES_UPDATE_DELAY = 10 # Интервал обновления файлов с временем работы
MIN_TIME_TO_REGISTER_PROJECT = 30 # Проект должен быть открыт как минимум столько секунд, чтобы появилось окошко с предложением добавить проект

username = 'default'
monitored_programs = {'pycharm', 'unity', 'microsoft visual studio', 'fl studio'}
registered_projects = dict()  # key - название проекта, value - экземпляр класса Project
active_project = '' # Название активного проекта

unknown_project_name = ''
unknown_project_time = 0


class SupportedPrograms(Enum):
    NOT_SUPPORTED_PROGRAM = 0,
    PYCHARM = 1,
    UNITY = 2,
    VS = 3,
    FL_STUDIO = 4


def get_pid_from_hwnd(hwnd):
    """Получает PID процесса по HWND окна"""
    import win32process
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        return pid
    except Exception as e:
        print(f"Error getting PID: {e}")
        return None

def get_program_type(window, hwnd):
    """Определяет, поддерживается ли программа, и в положительном случае её тип"""
    pid = get_pid_from_hwnd(hwnd)
    if pid:
        try:
            proc = psutil.Process(pid)
            proc_name = proc.name().lower()
            window_title = window.title.lower()

            if 'pycharm' in monitored_programs and 'pycharm' in proc_name and window_title[:window_title.rfind(' – ')] != '':
                return SupportedPrograms.PYCHARM
            elif ('unity' in monitored_programs and
                  'unity' in proc_name and
                  len(window_title.split(' - ')) >= 4 and
                  'unity hub' not in proc_name and
                  'unity package manage' not in proc_name and
                  'unity' in window_title and
                  not 'unity.ex' in window_title):
                return SupportedPrograms.UNITY
            elif 'microsoft visual studio' in monitored_programs and 'microsoft visual studio' in window_title:
                return SupportedPrograms.VS
            elif 'fl studio' in monitored_programs and 'fl studio' in window_title and len(window_title.split(" - ")) >= 2:
                return SupportedPrograms.FL_STUDIO
            else:
                return SupportedPrograms.NOT_SUPPORTED_PROGRAM
        except (psutil.NoSuchProcess, psutil.AccessDenied, ValueError) as e:
            print(f"Ошибка при обработке PID {pid}: {e}")
            return SupportedPrograms.NOT_SUPPORTED_PROGRAM
    return SupportedPrograms.NOT_SUPPORTED_PROGRAM

def get_project_name_from_program_title(program_type: str, program_title: str):
    match program_type:
        case SupportedPrograms.PYCHARM:
            return program_title[:program_title.rfind(' – ')]
        case SupportedPrograms.UNITY:
            return program_title[:program_title.find(' - ')]
        case SupportedPrograms.VS:
            return program_title[:program_title.find(' - ')]
        case SupportedPrograms.FL_STUDIO:
            proj_name = program_title[:program_title.find(' - ')]
            if proj_name.endswith('.flp'):
                proj_name = proj_name[:-4]
            return proj_name


async def search_active_projects():
    global active_project, registered_projects, unknown_project_name, unknown_project_time
    
    while True:
        await asyncio.sleep(PROJECTS_SEARCH_DELAY)
        active_window = gw.getActiveWindow()
        if active_window:
            hwnd = win32gui.GetForegroundWindow()
            #print(f'{get_program_type(active_window, hwnd).name}: {get_project_name_from_program_title(get_program_type(active_window, hwnd), active_window.title)}')

            program_type = get_program_type(active_window, hwnd)
            if program_type is not SupportedPrograms.NOT_SUPPORTED_PROGRAM:
                loaded_projects, error = pickle_operator.try_load_data(PROJECTS_DATA_PATH)
                if loaded_projects and 'needs_update_13571' in loaded_projects:
                    print('Настройки проектов были изменены, загружаю...')
                    registered_projects, _ = pickle_operator.try_load_data(PROJECTS_DATA_PATH)
                    registered_projects.pop('needs_update_13571')
                    pickle_operator.try_save_data(registered_projects, PROJECTS_DATA_PATH)

                project_name = get_project_name_from_program_title(program_type, active_window.title)
                if not project_name in registered_projects.keys():
                    if unknown_project_name == project_name:
                        if unknown_project_time < MIN_TIME_TO_REGISTER_PROJECT:
                            unknown_project_time += PROJECTS_SEARCH_DELAY
                    else:
                        unknown_project_time = 0
                        unknown_project_name = project_name
                    print(f'{unknown_project_name}: {unknown_project_time}')

                    if unknown_project_time >= MIN_TIME_TO_REGISTER_PROJECT:
                        unknown_project_time = 0
                        ignore, project_path = open_new_project_ui(program_type.name, project_name)
                        registered_projects[project_name] = Project(project_name, project_path, ignore)
                        pickle_operator.try_save_data(registered_projects, PROJECTS_DATA_PATH)
                else:
                    active_project = project_name
                    unknown_project_time = 0
            else:
                active_project = None
                unknown_project_time = 0
        else:
            active_project = None
            unknown_project_time = 0
        #if active_project in registered_projects:
            #print(f'{active_project}: {registered_projects[active_project].delta_time}')
        
        
async def add_work_time():
    await asyncio.sleep(TIME_ADD_DELAY)
    system_last_time = time.time()

    while True:
        await asyncio.sleep(TIME_ADD_DELAY)
        system_time_delta = abs(time.time() - system_last_time)
        multiplier = float(system_time_delta) / TIME_ADD_DELAY
        #print(f'm: {multiplier}')


        if multiplier < 0.9 or multiplier > 1.1:
            print('Слишком большой разрыв времени, кто-то пытается жульничать? Ай-яй')
        else:
            if active_project is not None and not activity_detector.timeout:
                if active_project in registered_projects:
                    registered_projects[active_project].delta_time += system_time_delta
                else:
                    print(f'Непредвиденная ошибка: активный проект ({active_project}) отсутствует в словаре проектов')
        system_last_time = time.time()

async def control_icon():
    while True:
        await asyncio.sleep(PROJECTS_SEARCH_DELAY)
        active_proj = registered_projects.get(active_project)
        if active_proj is not None:
            if not active_proj.ignore:
                if not activity_detector.timeout:
                    update_tray_state("active", f"Время идёт ({active_project} - {active_proj.project_path}/{time_to_file_operator.LOCAL_PATH_TO_FILE})")
                else:
                    update_tray_state("paused", "Продолжите работать для возобновления подсчёта времени")
            else:
                update_tray_state("ignored", f"Проект игнорируется. Вы можете изменить это: Пуск -> Time Analyzer Menu -> {active_project}")
        else:
            update_tray_state("waiting", "Ожидание работы в поддерживаемой среде разработки")


async def update_work_time_files():
    while True:
        await asyncio.sleep(FILES_UPDATE_DELAY)
        if active_project is not None and active_project in registered_projects:
            # Форматирование текущей даты в ДД.ММ.ГГГГ
            current_date = datetime.now().strftime("%d.%m.%Y")

            if not registered_projects[active_project].ignore and type(registered_projects[active_project].project_path) == str and os.path.exists(registered_projects[active_project].project_path):
                try:
                    asyncio.create_task(time_to_file_operator.try_update_work_time_file(username, registered_projects[active_project].project_path, active_project, current_date, int(registered_projects[active_project].delta_time)))
                    registered_projects[active_project].delta_time -= int(registered_projects[active_project].delta_time)
                except Exception as e:
                    print(f'Непредвиденная ошибка при обновлении файла с временем работы: {e}')


async def send_data_regularly():
    while True:
        await asyncio.sleep(random.randint(300, 600))
        try:
            # Запускаем отправку с тайм-аутом в 60 секунд
            await asyncio.wait_for(
                send_worktime_data(registered_projects, active_project, username),
                timeout=10
            )
        except asyncio.TimeoutError:
            print('Превышено время ожидания отправки данных')
        except Exception as e:
            print(f'Ошибка: {e}')


async def start():
    try:
        # Проверяем, не запущено ли ещё одно такое же приложение
        if is_already_running():
            messagebox.showerror("Ошибка", "Приложение уже запущено!")
            return

        # Приветственное окно + ввод ника
        global username
        username, _ = pickle_operator.try_load_data(USER_SETTINGS_DATA_PATH)
        if username is None:
            username = get_username()
            if not username:
                return
            pickle_operator.try_save_data(username, USER_SETTINGS_DATA_PATH)

        # Загрузка проектов
        global registered_projects
        registered_projects, error = pickle_operator.try_load_data(PROJECTS_DATA_PATH)
        if error is not None:
            print(f'Error loading projects data: {error}, creating new file')
            registered_projects = dict()
            pickle_operator.try_save_data(registered_projects, PROJECTS_DATA_PATH)

        # Иконка
        start_tray_async()

        # Запуск корутин
        await asyncio.gather(
            activity_detector.start_tracking_activity_timeout(),
            search_active_projects(),
            add_work_time(),
            update_work_time_files(),
            send_data_regularly(),
            control_icon()
        )
    except Exception as e:
        messagebox.showerror(f"Непредвиденная ошибка, Work Time Analyzer остановлен ({e})", "Приложение уже запущено!")


if __name__ == "__main__":
    asyncio.run(start())
