import tkinter as tk
from tkinter import ttk, messagebox
import time
import datetime
import threading
import winsound  # Для Windows. На других ОС можно использовать другие решения


class ClockTimerAlarmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Часы, Таймер и Будильник")
        self.root.geometry("1000x1000")
        self.root.resizable(False, False)

        # Переменные
        self.current_time_var = tk.StringVar()
        self.timer_var = tk.StringVar(value="00:00:00")
        self.timer_running = False
        self.timer_paused = False
        self.timer_seconds = 0
        self.timer_thread = None

        self.alarms = []
        self.alarm_check_thread = None
        self.alarm_running = False

        # Создание вкладок
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Вкладка Часы
        self.clock_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.clock_frame, text="Часы")
        self.setup_clock()

        # Вкладка Таймер
        self.timer_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.timer_frame, text="Таймер")
        self.setup_timer()

        # Вкладка Будильник
        self.alarm_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.alarm_frame, text="Будильник")
        self.setup_alarm()

        # Запуск обновления времени
        self.update_clock()

        # Запуск проверки будильников
        self.alarm_running = True
        self.alarm_check_thread = threading.Thread(target=self.check_alarms)
        self.alarm_check_thread.daemon = True
        self.alarm_check_thread.start()

    def setup_clock(self):
        clock_label = ttk.Label(self.clock_frame, text="Текущее время:", font=("Helvetica", 14))
        clock_label.pack(pady=(50, 10))

        time_label = ttk.Label(self.clock_frame, textvariable=self.current_time_var, font=("Helvetica", 36))
        time_label.pack(pady=10)

        date_frame = ttk.Frame(self.clock_frame)
        date_frame.pack(pady=20)

        self.date_label = ttk.Label(date_frame, text="", font=("Helvetica", 14))
        self.date_label.pack()

    def setup_timer(self):
        # Верхняя рамка для ввода времени
        input_frame = ttk.Frame(self.timer_frame)
        input_frame.pack(pady=(30, 10))

        # Поля для ввода часов, минут и секунд
        ttk.Label(input_frame, text="Ч:").grid(row=0, column=0, padx=5)
        self.hours_spinbox = ttk.Spinbox(input_frame, from_=0, to=99, width=5, format="%02.0f")
        self.hours_spinbox.grid(row=0, column=1, padx=5)
        self.hours_spinbox.set("00")

        ttk.Label(input_frame, text="М:").grid(row=0, column=2, padx=5)
        self.minutes_spinbox = ttk.Spinbox(input_frame, from_=0, to=59, width=5, format="%02.0f")
        self.minutes_spinbox.grid(row=0, column=3, padx=5)
        self.minutes_spinbox.set("00")

        ttk.Label(input_frame, text="С:").grid(row=0, column=4, padx=5)
        self.seconds_spinbox = ttk.Spinbox(input_frame, from_=0, to=59, width=5, format="%02.0f")
        self.seconds_spinbox.grid(row=0, column=5, padx=5)
        self.seconds_spinbox.set("00")

        # Отображение времени таймера
        timer_display = ttk.Label(self.timer_frame, textvariable=self.timer_var, font=("Helvetica", 36))
        timer_display.pack(pady=20)

        # Кнопки управления
        buttons_frame = ttk.Frame(self.timer_frame)
        buttons_frame.pack(pady=10)

        self.start_button = ttk.Button(buttons_frame, text="Старт", command=self.start_timer)
        self.start_button.grid(row=0, column=0, padx=10)

        self.pause_button = ttk.Button(buttons_frame, text="Пауза", command=self.pause_timer, state="disabled")
        self.pause_button.grid(row=0, column=1, padx=10)

        self.reset_button = ttk.Button(buttons_frame, text="Сброс", command=self.reset_timer, state="disabled")
        self.reset_button.grid(row=0, column=2, padx=10)

    def setup_alarm(self):
        # Верхняя рамка для установки будильника
        setup_frame = ttk.Frame(self.alarm_frame)
        setup_frame.pack(pady=(30, 10))

        ttk.Label(setup_frame, text="Установить будильник на:").grid(row=0, column=0, padx=5, pady=10, columnspan=2)

        ttk.Label(setup_frame, text="Ч:").grid(row=1, column=0, padx=5)
        self.alarm_hours_spinbox = ttk.Spinbox(setup_frame, from_=0, to=23, width=5, format="%02.0f")
        self.alarm_hours_spinbox.grid(row=1, column=1, padx=5)
        self.alarm_hours_spinbox.set("12")

        ttk.Label(setup_frame, text="М:").grid(row=1, column=2, padx=5)
        self.alarm_minutes_spinbox = ttk.Spinbox(setup_frame, from_=0, to=59, width=5, format="%02.0f")
        self.alarm_minutes_spinbox.grid(row=1, column=3, padx=5)
        self.alarm_minutes_spinbox.set("00")

        # Кнопка добавления будильника
        add_button = ttk.Button(setup_frame, text="Добавить будильник", command=self.add_alarm)
        add_button.grid(row=1, column=4, padx=10)

        # Рамка для списка будильников
        list_frame = ttk.Frame(self.alarm_frame)
        list_frame.pack(pady=10, fill="both", expand=True)

        ttk.Label(list_frame, text="Активные будильники:").pack(pady=(0, 5))

        # Создаем фрейм с прокруткой для списка будильников
        scroll_frame = ttk.Frame(list_frame)
        scroll_frame.pack(fill="both", expand=True)

        self.alarm_listbox = tk.Listbox(scroll_frame, height=8)
        self.alarm_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=self.alarm_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.alarm_listbox.config(yscrollcommand=scrollbar.set)

        # Кнопка удаления будильника
        delete_button = ttk.Button(list_frame, text="Удалить выбранный будильник", command=self.delete_alarm)
        delete_button.pack(pady=10)

    def update_clock(self):
        # Получаем текущее время и дату
        now = datetime.datetime.now()
        time_string = now.strftime("%H:%M:%S")
        date_string = now.strftime("%A, %d %B %Y")

        # Обновляем отображение
        self.current_time_var.set(time_string)
        self.date_label.config(text=date_string)

        # Рекурсивно вызываем функцию каждую секунду
        self.root.after(1000, self.update_clock)

    def start_timer(self):
        if not self.timer_running:
            try:
                hours = int(self.hours_spinbox.get())
                minutes = int(self.minutes_spinbox.get())
                seconds = int(self.seconds_spinbox.get())

                if hours == 0 and minutes == 0 and seconds == 0:
                    messagebox.showwarning("Предупреждение", "Пожалуйста, установите время таймера.")
                    return

                self.timer_seconds = hours * 3600 + minutes * 60 + seconds
                self.timer_running = True
                self.timer_paused = False

                # Обновляем состояние кнопок
                self.start_button.config(state="disabled")
                self.pause_button.config(state="normal")
                self.reset_button.config(state="normal")

                # Запускаем таймер в отдельном потоке
                self.timer_thread = threading.Thread(target=self.run_timer)
                self.timer_thread.daemon = True
                self.timer_thread.start()
            except ValueError:
                messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числовые значения.")
        elif self.timer_paused:
            # Возобновляем таймер после паузы
            self.timer_paused = False
            self.pause_button.config(text="Пауза")

    def run_timer(self):
        while self.timer_seconds > 0 and self.timer_running:
            if not self.timer_paused:
                # Преобразуем секунды в формат ЧЧ:ММ:СС
                hours, remainder = divmod(self.timer_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

                # Обновляем отображение в главном потоке
                self.root.after(0, lambda: self.timer_var.set(time_str))

                # Уменьшаем счетчик
                self.timer_seconds -= 1

                # Ждем 1 секунду
                time.sleep(1)
            else:
                # Если на паузе, просто ждем
                time.sleep(0.1)

        # Если таймер закончился нормально (не был сброшен)
        if self.timer_running and not self.timer_paused and self.timer_seconds <= 0:
            self.root.after(0, self.timer_finished)

    def timer_finished(self):
        self.timer_var.set("00:00:00")
        self.timer_running = False
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")
        self.reset_button.config(state="disabled")

        # Воспроизводим звук
        self.play_alarm_sound()

        # Показываем сообщение
        messagebox.showinfo("Таймер", "Время истекло!")

    def pause_timer(self):
        if self.timer_running:
            if not self.timer_paused:
                self.timer_paused = True
                self.pause_button.config(text="Продолжить")
            else:
                self.timer_paused = False
                self.pause_button.config(text="Пауза")

    def reset_timer(self):
        self.timer_running = False
        self.timer_paused = False
        self.timer_seconds = 0
        self.timer_var.set("00:00:00")

        # Обновляем состояние кнопок
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled", text="Пауза")
        self.reset_button.config(state="disabled")

    def add_alarm(self):
        try:
            hours = int(self.alarm_hours_spinbox.get())
            minutes = int(self.alarm_minutes_spinbox.get())

            if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
                messagebox.showwarning("Некорректное время",
                                       "Пожалуйста, введите корректное время (часы: 0-23, минуты: 0-59).")
                return

            # Форматируем время для отображения
            alarm_time = f"{hours:02d}:{minutes:02d}"

            # Проверяем, не существует ли уже такой будильник
            if alarm_time in self.alarms:
                messagebox.showinfo("Информация", f"Будильник на {alarm_time} уже существует.")
                return

            # Добавляем будильник
            self.alarms.append(alarm_time)
            self.alarm_listbox.insert(tk.END, alarm_time)

            messagebox.showinfo("Будильник добавлен", f"Будильник установлен на {alarm_time}.")
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числовые значения.")

    def delete_alarm(self):
        try:
            # Получаем индекс выбранного элемента
            selected_index = self.alarm_listbox.curselection()[0]
            alarm_time = self.alarm_listbox.get(selected_index)

            # Удаляем будильник из списка и listbox
            self.alarms.remove(alarm_time)
            self.alarm_listbox.delete(selected_index)

            messagebox.showinfo("Будильник удален", f"Будильник на {alarm_time} удален.")
        except IndexError:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите будильник для удаления.")

    def check_alarms(self):
        """Функция проверки будильников, работает в отдельном потоке"""
        while self.alarm_running:
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M")

            # Проверяем все будильники
            for alarm_time in self.alarms:
                if alarm_time == current_time and now.second == 0:  # Проверяем только в начале минуты
                    # Воспроизводим звук будильника в главном потоке
                    self.root.after(0, self.alarm_triggered, alarm_time)

            # Ждем 1 секунду перед следующей проверкой
            time.sleep(1)

    def alarm_triggered(self, alarm_time):
        """Вызывается, когда срабатывает будильник"""
        # Воспроизводим звук
        self.play_alarm_sound()

        # Показываем сообщение
        result = messagebox.askquestion("Будильник!", f"Сработал будильник на {alarm_time}.\nОтключить будильник?")

        if result == "yes":
            # Удаляем будильник из списка
            self.alarms.remove(alarm_time)

            # Обновляем отображение в listbox
            for i in range(self.alarm_listbox.size()):
                if self.alarm_listbox.get(i) == alarm_time:
                    self.alarm_listbox.delete(i)
                    break

    def play_alarm_sound(self):
        """Воспроизведение звука будильника"""
        # На Windows используем winsound
        try:
            winsound.Beep(1000, 500)  # Частота (Гц), длительность (мс)
            winsound.Beep(1500, 500)
            winsound.Beep(2000, 500)
        except:
            # На других ОС можно использовать другие решения
            pass

    def on_closing(self):
        """Обработчик закрытия окна"""
        self.alarm_running = False
        self.timer_running = False
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ClockTimerAlarmApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()