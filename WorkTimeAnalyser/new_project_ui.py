import tkinter as tk
from tkinter import filedialog, messagebox
import os


def open_new_project_ui(program_type: str, project_name: str):
    """
    Открывает UI меню с выбором пути нового проекта.
    :param program_type: Тип программы (юнити, пайчарм и т. д.), будет выведен текстом в меню.
    :param project_name: Имя проекта, будет выведено текстом в меню.
    :return: Игнорировать ли проект, указанный путь к проекту.
    """
    result = {"ignore": True, "path": None}  # Для хранения результата

    def browse_path():
        selected_path = filedialog.askdirectory(title="Выберите путь к проекту")
        if selected_path:
            path_var.set(selected_path)

    def on_ok():
        project_path = path_var.get()
        if not project_path:
            messagebox.showwarning("Ошибка", "Пожалуйста, укажите путь сохранения файла!")
        elif not os.path.exists(project_path):
            messagebox.showerror("Ошибка", "Указанный путь не существует!")
        else:
            result["ignore"] = False
            result["path"] = project_path
            root.destroy()  # Завершаем главное окно

    def on_ignore():
        result["ignore"] = True
        result["path"] = None
        root.destroy()  # Завершаем главное окно

    def on_closing():
        if messagebox.askokcancel("Игнорировать проект?",
                                  "Этот проект будет игнорирован, вы можете позже изменить это в меню управления проектами. Продолжить?"):
            result["ignore"] = True
            result["path"] = None
            root.destroy()  # Завершаем главное окно

    # Создаем главное окно
    root = tk.Tk()
    root.title("Новый проект (отслеживание времени работы)")
    root.iconbitmap(os.path.join(os.environ.get("SystemDrive", "C:"), '/Program Files/WorkTimeAnalyser/alpha_games_logo_v3.ico'))

    root.geometry("700x300")
    root.resizable(True, True)

    # Фокусировка на окне
    root.lift()
    root.attributes("-topmost", True)
    root.after(0, lambda: root.attributes("-topmost", False))  # Снимаем "поверх всех окон", чтобы не мешало

    # Обработка закрытия окна
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Создаем надписи
    tk.Label(root, text=f"Обнаружен новый проект на {program_type}: {project_name}", font=("Arial", 14)).pack(pady=10)
    tk.Label(root, text="Укажите путь, по которому будет создана папка WORK_TIME, в которой будет файл с временем работы:", font=("Arial", 10)).pack()

    # Переменная для хранения пути
    path_var = tk.StringVar()

    # Поле ввода пути
    path_entry = tk.Entry(root, textvariable=path_var, width=40, font=("Arial", 10))
    path_entry.pack(pady=5)

    # Кнопка для открытия проводника
    browse_button = tk.Button(root, text="Обзор...", command=browse_path, font=("Arial", 10))
    browse_button.pack(pady=5)

    # Контейнер для кнопок "ОК" и "Игнорировать"
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    ignore_button = tk.Button(button_frame, text="Игнорировать проект", command=on_ignore, font=("Arial", 10), width=15)
    ok_button = tk.Button(button_frame, text="ОК", command=on_ok, font=("Arial", 10), width=15)

    ignore_button.pack(side="left", padx=5)
    ok_button.pack(side="left", padx=5)

    tk.Label(root, text=f"GO software", font=("Arial", 8)).pack(pady=10)

    # Запуск главного цикла приложения
    root.mainloop()

    # Возвращаем результат после завершения mainloop
    return result["ignore"], result["path"]


# Пример использования
if __name__ == "__main__":
    open_new_project_ui('PYCHARM', 'TEST')
