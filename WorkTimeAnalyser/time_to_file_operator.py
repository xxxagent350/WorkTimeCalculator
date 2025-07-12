import os

import encrypted_file_operator
import time_converter
from os import path

LOCAL_PATH_TO_FILE = 'WORK_TIME' # Полный путь к файлу будет выглядеть так: путь_к_проекту/local_path_to_file/{username} - {project_name}.{FILE_EXTENSION}
FILE_EXTENSION = 'worktime'


async def try_update_work_time_file(username, project_directory, project_name, date, delta_time):
    """
    Изменяет время работы над проектом в файле по пути указанному пути
    :param username: имя пользователя
    :param project_directory: путь к проекту
    :param project_name: имя проекта
    :param date: дата, для которой изменить время работы
    :param delta_time: изменение времени работы
    :return: успех операции
    """
    global_path = path.join(project_directory, LOCAL_PATH_TO_FILE)
    if not os.path.isdir(global_path):
        os.makedirs(global_path)
    global_path_to_file = path.join(global_path, f'{username} - {project_name}.{FILE_EXTENSION}')
    old_content = encrypted_file_operator.load_worktime_data(global_path_to_file)
    if old_content is not None:
        lines_list = old_content.splitlines()
        old_proj_names = lines_list[1][9:].split(' ⁂ ')
        if not project_name in old_proj_names:
            lines_list[1] += f" ⁂ {project_name}"

        all_time = 0
        line_detected = False
        for line_num in range(5, len(lines_list)):
            date_time = lines_list[line_num][lines_list[line_num].find(' - ') + 3:]
            date_time_seconds = time_converter.hms_to_seconds(date_time)
            all_time += date_time_seconds
            if not line_detected and date in lines_list[line_num]:
                lines_list[line_num] = f'{date} - {time_converter.seconds_to_hms(date_time_seconds + delta_time)}'
                line_detected = True

        total_hours = all_time / float(3600)
        if total_hours < 1:
            total_hours = round(total_hours, 2)
        elif total_hours < 24:
            total_hours = round(total_hours, 1)
        else:
            total_hours = round(total_hours)

        lines_list[3] = f'Total hours: {total_hours}'
        if not line_detected:
            lines_list.append(f'{date} - {time_converter.seconds_to_hms(delta_time)}')

        new_content = ''
        for line in lines_list:
            new_content += f'{line}\n'
        new_content = new_content.rstrip()
        return encrypted_file_operator.save_worktime_data(global_path_to_file, new_content)
    else:
        # Проверка на старый формат названия
        folder = global_path
        for filename in os.listdir(folder):
            if filename == f"{username}.{FILE_EXTENSION}":
                old_filepath = path.join(global_path, filename)
                new_filepath = path.join(global_path, f'{username} - {project_name}.{FILE_EXTENSION}')
                os.rename(old_filepath, new_filepath)
                return

        # Создание нового файла
        new_content = f"""User: {username}
Project: {project_name}
--------------------------------
Total hours: 0
--------------------------------
"""
        return encrypted_file_operator.save_worktime_data(global_path_to_file, new_content)
