import os
import tkinter as tk
from tkinter import messagebox

MAX_USERNAME_LENGTH = 30


def get_username():
    """
    Открывает меню с надписью 'введите имя пользователя'
    :return: Имя пользователя
    """
    def on_submit():
        username_ = entry.get().strip()
        if not username_:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите своё имя пользователя!")
        elif len(username_) > MAX_USERNAME_LENGTH:
            messagebox.showwarning("Предупреждение", f"Имя пользователя не может быть длиннее {MAX_USERNAME_LENGTH} символов!")
        else:
            nonlocal user_input
            user_input = username_
            root.destroy()

    user_input = None

    root = tk.Tk()
    root.title("Анализатор времени работы над проектами")
    root.iconbitmap(os.path.join(os.environ.get("SystemDrive", "C:"), '/Program Files/WorkTimeAnalyser/alpha_games_logo_v3.ico'))
    root.geometry("450x200")
    root.resizable(False, False)

    # Фокусировка на окне
    root.lift()
    root.attributes("-topmost", True)
    root.after(0, lambda: root.attributes("-topmost", False))  # Снимаем "поверх всех окон", чтобы не мешало

    tk.Label(root, text="Добро пожаловать!", font=("Arial", 14)).pack(pady=10)
    tk.Label(root, text="Введите имя пользователя:").pack()

    entry = tk.Entry(root, width=30)
    entry.pack(pady=5)

    submit_button = tk.Button(root, text="Ок", command=on_submit)
    submit_button.pack(pady=10)

    tk.Label(root, text=f"Alpha Technologies", font=("Arial", 8)).pack(pady=10)

    root.mainloop()

    return user_input

# Пример использования
if __name__ == "__main__":
    username = get_username()
    if username:
        print(f"Введённое имя пользователя: {username}")