import os


def try_read_file(directory):
    """
    :return: текст .txt файла (или None в случае ошибки)
    """
    try:
        with open(directory, "r", encoding="utf-8") as file:
            content = file.read()  # Чтение всего содержимого файла
            return content
    except:
        return None


def try_write_file(directory, content):
    """
    Сохраняет или обновляет .txt файл. Если директория не существует, создаёт её.
    :param directory: путь, по которому записать файл
    :param content: текст, который записать в файл
    :return: успех операции
    """
    try:
        # Получаем путь к директории
        dir_path = os.path.dirname(directory)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)  # Создаем директорию, если её нет

        # Записываем в файл
        with open(directory, "w", encoding="utf-8") as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"Ошибка при записи файла: {e}")
        return False

