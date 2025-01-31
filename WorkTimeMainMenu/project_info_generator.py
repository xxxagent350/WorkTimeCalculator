import os
from datetime import datetime


def generate_report(folder_path: str, file_extension: str, report_name: str, ignored_paths: list) -> None:
    """
    Генерирует отчёт о файлах с указанным расширением в папке и подпапках.

    :param folder_path: Путь к корневой папке.
    :param file_extension: Расширение файлов (например, ".py").
    :param report_name: Имя итогового отчёта (txt-файл).
    :param ignored_paths: Список путей для игнорирования (файлы и папки).
    """
    print('Генерирую отчёт...')

    total_files = 0
    total_lines = 0
    total_chars = 0
    files_data = []

    # Перебор файлов и подсчёт строк и символов
    for root, _, files in os.walk(folder_path):
        # Игнорируем папки и файлы, указанные в ignored_paths
        if any(ignored_path in root for ignored_path in ignored_paths):
            continue

        for file in files:
            if file.endswith(file_extension):
                # Игнорируем файлы по имени
                file_path = os.path.join(root, file)
                if any(ignored_path in file_path for ignored_path in ignored_paths):
                    continue

                total_files += 1
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.readlines()
                    line_count = len(content)
                    char_count = sum(len(line) for line in content)
                    total_lines += line_count
                    total_chars += char_count
                    relative_path = os.path.relpath(file_path, folder_path)
                    files_data.append((relative_path, ''.join(content)))

    # Формирование заголовка отчёта
    date = datetime.now().strftime("%d.%m.%Y")
    report_header = (
        f"Отчёт на {date} о файлах *{file_extension}:\n"
        f"Количество файлов - {total_files}\n"
        f"Количество строк - {total_lines}\n"
        f"Количество символов - {total_chars}\n\n"
    )

    # Запись в итоговый файл
    with open(report_name, 'w', encoding='utf-8') as report_file:
        report_file.write(report_header)
        for file_path, content in files_data:
            report_file.write(f"\n\n\n------------------------------------------------------------\n{file_path}:\n")
            report_file.write(content + "\n")

    print(f"Отчёт сохранён в файл: {report_name}")


if __name__ == "__main__":
    folder = os.path.dirname(os.path.abspath(__file__))  # Путь к текущей папке
    extension = ".py"  # Искомое расширение файлов
    report_file = "report.txt"  # Название файла отчёта
    ignored_paths = ['project_info_generator.py', 'run', 'venv']  # Список игнорируемых файлов и папок

    generate_report(folder, extension, report_file, ignored_paths)
