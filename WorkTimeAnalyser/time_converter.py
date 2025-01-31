
def seconds_to_hms(seconds):
    """Переводит секунды в формат ЧЧ:ММ:СС"""
    seconds = round(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def seconds_to_hm(seconds):
    """Переводит секунды в формат ЧЧ:ММ"""
    seconds = round(seconds)
    hours = seconds // 3600
    minutes = int((seconds % 3600) / 60)
    return f"{hours:02}:{minutes:02}"


def hms_to_seconds(hms : str):
    """Переводит время в формате 'ЧЧ:ММ:СС' или 'ЧЧ:ММ' обратно в секунды"""
    parts = list(map(int, hms.split(':')))
    if len(parts) == 3:
        hours, minutes, seconds = parts
        return hours * 3600 + minutes * 60 + seconds
    elif len(parts) == 2:
        hours, minutes = parts
        return hours * 3600 + minutes * 60
    else:
        print('Ошибка в time_converter.hms_to_seconds: некорректный формат времени, читай описание функции')
    return 0
