import encrypted_file_operator
import time_converter
from os import path

local_path_to_file = 'WORK_TIME' # Полный путь к файлу будет выглядеть так: путь_к_проекту/local_path_to_file/{имя_пользователя}.worktime


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
    global_path_to_file = path.join(project_directory, local_path_to_file, f'{username}.worktime')
    old_content = encrypted_file_operator.load_worktime_data(global_path_to_file)
    if old_content is not None:
        lines_list = old_content.splitlines()

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
        new_content = f"""User: {username}
Project: {project_name}
--------------------------------
Total hours: 0
--------------------------------
"""
        return encrypted_file_operator.save_worktime_data(global_path_to_file, new_content)
