import tkinter as tk
from tkinter import messagebox
import time
import os
import sys

# ---------------- ДАННЫЕ ----------------
questions = [
    {
        "code": "x = 10\ny = x + 5\nz = y * 2",
        "questions": [
            "1. Какое значение имеет переменная z?",
            "2. Какая переменная используется для вычисления y?"
        ]
    },
    {
        "code": "def square(n):\n    result = n * n\n    return result\n\nvalue = square(4)",
        "questions": [
            "1. Что возвращает square(4)?",
            "2. Назовите переменную внутри функции.",
            "3. Сколько параметров у функции?"
        ]
    },
    {
        "code": "def outer(x):\n    y = x + 1\n\n    def inner(z):\n        return z + y\n\n    return inner(x)",
        "questions": [
            "1. Что возвращает outer(2)?",
            "2. Какая переменная используется внутри inner, но объявлена снаружи?",
            "3. Сколько функций определено?"
        ]
    }
]

# ---------------- ПОДСКАЗКИ ----------------
def get_base_path():
    """Возвращает путь для сохранения файлов (работает с exe)."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)

def center_window(root, width=600, height=400):
    """Центрирует окно на экране."""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

# ---------------- ПРИЛОЖЕНИЕ ----------------
class SurveyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Опрос по пониманию кода")
        center_window(self.root)

        self.index = 0
        self.answers = []
        self.timestamps = []
        self.start_time = time.time()

        self.code_label = tk.Label(root, text="", font=("Courier", 12), justify="left")
        self.code_label.pack(pady=10)

        self.entries = []
        self.question_labels = []

        self.next_btn = tk.Button(root, text="Далее", command=self.next_question)
        self.next_btn.pack(pady=10)

        self.load_question()

    def load_question(self):
        for widget in self.entries + self.question_labels:
            widget.destroy()

        self.entries.clear()
        self.question_labels.clear()

        q = questions[self.index]

        self.code_label.config(text=q["code"])

        for question in q["questions"]:
            label = tk.Label(self.root, text=question)
            label.pack()
            self.question_labels.append(label)

            entry = tk.Entry(self.root, width=50)
            entry.pack()
            self.entries.append(entry)

        self.question_start_time = time.time()

    def next_question(self):
        answers = [e.get() for e in self.entries]
        time_spent = time.time() - self.question_start_time

        self.answers.append(answers)
        self.timestamps.append(time_spent)

        self.index += 1

        if self.index < len(questions):
            self.load_question()
        else:
            self.finish()

    def finish(self):
        total_time = time.time() - self.start_time
        base_path = get_base_path()
        file_path = os.path.join(base_path, "результаты.txt")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("Результаты опроса\n")
            f.write(f"Общее время: {total_time:.2f} сек\n\n")

            for i, (ans, t) in enumerate(zip(self.answers, self.timestamps)):
                f.write(f"Задание {i+1}:\n")
                f.write(f"Время выполнения: {t:.2f} сек\n")
                for j, a in enumerate(ans):
                    f.write(f"Вопрос {j+1}: {a}\n")
                f.write("\n")

        messagebox.showinfo("Готово", f"Результаты сохранены в файле:\n{file_path}")
        self.root.destroy()

# ---------------- ЗАПУСК ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SurveyApp(root)
    root.mainloop()