import pickle


def try_save_data(data, path):
    """
    :param data: Данные для сохранения
    :param path: Путь
    :return: (успех операции, отчёт об ошибке(если есть))
    """
    try:
        with open(path, 'wb') as file:
            pickle.dump(data, file)
            return True, None
    except Exception as exception:
        return False, exception


def try_load_data(path):
    """
    :param path: Путь файла для загрузки
    :return: (загруженные данные или None в случае ошибки, отчёт об ошибке(если есть))
    """
    try:
        with open(path, 'rb') as file:
            return pickle.load(file), None
    except Exception as exception:
        return None, exception