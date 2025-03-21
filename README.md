AutoClicker

Этот скрипт — это простая программа автокликера с графическим интерфейсом, который использует библиотеку tkinter для интерфейса и pyautogui для выполнения кликов. Давайте разберём каждый его компонент.

Основные компоненты:
tkinter — для создания окна и элементов управления (кнопки, слайдеры).
pyautogui — для выполнения кликов мыши в заданных координатах.
pynput.mouse.Listener — для отслеживания кликов мыши.
keyboard — для обработки горячих клавиш.

Описание:
AutoClicker — это мощный автокликер с функцией записи и автоматического повторения действий. Программа позволяет записывать координаты кликов мыши и автоматически воспроизводить их с заданной скоростью. В дополнение, она может автоматически повторять нажатия клавиш F1 и F5, что упрощает управление процессом без необходимости вручную нажимать клавиши.

Описание работы программы:
Графический интерфейс (GUI):

Создаётся окно с настройками.
В нем есть слайдер для регулировки скорости кликов (от 0.1 до 2.0 секунд).
Кнопки для старта и остановки записи кликов, воспроизведения и очистки.
Метка для отображения текущей скорости кликов.

Запись кликов: Когда нажимается кнопка Старт/Стоп записи или клавиша F1, скрипт начинает записывать координаты кликов мыши (только левой кнопкой мыши). Клики сохраняются в список self.clicks.

Воспроизведение кликов: Когда нажимается кнопка Воспроизведение или клавиша F5, скрипт воспроизводит все записанные клики с заданной скоростью.

Очистка: Кнопка Очистка или клавиша Delete очищает список кликов и останавливает текущую запись и воспроизведение.

Горячие клавиши:
F1 — Старт/Стоп записи кликов.
F5 — Старт/Стоп воспроизведения кликов.
Del — Очистка кликов.

Механизм записи кликов: Когда начинается запись, используется pynput.mouse.Listener для отслеживания кликов мыши. Только клики левой кнопкой мыши записываются в список с координатами (x, y).

Механизм воспроизведения кликов: Когда начинается воспроизведение, скрипт поочередно выполняет сохранённые клики с интервалом, заданным в слайдере.

Скорость кликов: Значение слайдера определяет, с какой задержкой (в секундах) будут выполняться клики. Состояние скорости обновляется каждую 1/10 секунды.

План выполнения:
Запускаем приложение.
Используем горячие клавиши или кнопки для управления:
Записываем клики с помощью F1.
Воспроизводим клики с помощью F5.
Очищаем клики с помощью Del.

Важные замечания:
Убедитесь, что у вас есть права на выполнение всех библиотек, особенно на использование клавиатуры и мыши (на некоторых системах могут понадобиться дополнительные разрешения).
Эта программа будет работать на большинстве ОС, но для Windows могут понадобиться дополнительные настройки для работы с keyboard (например, запуск от имени администратора)..

AutoClicker — идеальное решение для автоматизации повторяющихся действий на вашем компьютере, будь то тестирование, игры или выполнение рутинных задач.

```import pyautogui
import threading
import time
import tkinter as tk
from tkinter import ttk
from pynput.mouse import Listener as MouseListener
import keyboard

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Автокликер")
        self.root.geometry("300x250")

        # Хранение кликов
        self.clicks = []
        self.recording = False
        self.playing = False
        self.click_speed = 0.3  # По умолчанию 300 мс

        # Интерфейс
        ttk.Label(root, text="Скорость кликов (сек):").pack(pady=5)
        self.speed_var = tk.DoubleVar(value=self.click_speed)
        self.speed_slider = ttk.Scale(root, from_=0.1, to=2.0, orient='horizontal', variable=self.speed_var)
        self.speed_slider.pack(fill='x', padx=10)

        self.speed_label = ttk.Label(root, text=f"Текущая скорость: {self.click_speed:.2f} сек")
        self.speed_label.pack(pady=5)

        self.start_button = ttk.Button(root, text="Старт/Стоп записи (F1)", command=self.toggle_recording)
        self.start_button.pack(pady=5)

        self.play_button = ttk.Button(root, text="Воспроизведение (F5)", command=self.toggle_playing)
        self.play_button.pack(pady=5)

        self.clear_button = ttk.Button(root, text="Очистка (Del)", command=self.clear_clicks)
        self.clear_button.pack(pady=5)

        # Горячие клавиши
        keyboard.add_hotkey("f1", self.toggle_recording)
        keyboard.add_hotkey("f5", self.toggle_playing)
        keyboard.add_hotkey("delete", self.clear_clicks)
        
        # Обновление скорости кликов
        self.update_speed_label()

    def update_speed_label(self):
        """ Обновляет отображение скорости кликов. """
        self.click_speed = self.speed_var.get()
        self.speed_label.config(text=f"Текущая скорость: {self.click_speed:.2f} сек")
        self.root.after(100, self.update_speed_label)  # Каждые 100 мс обновляет метку

    def toggle_recording(self):
        """ Запускает или останавливает запись кликов """
        if not self.recording:
            self.clicks.clear()
            self.recording = True
            # Используем pynput для отслеживания кликов мыши
            self.listener = MouseListener(on_click=self.on_click)
            self.listener.start()
        else:
            self.recording = False
            self.listener.stop()

    def on_click(self, x, y, button, pressed):
        """ Записывает координаты кликов при нажатии ЛКМ. """
        if pressed and self.recording and button.name == 'left':  # Только ЛКМ
            self.clicks.append((x, y))

    def toggle_playing(self):
        """ Запускает или останавливает воспроизведение кликов """
        if not self.playing and self.clicks:
            self.playing = True
            self.play_thread = threading.Thread(target=self.play_clicks, daemon=True)
            self.play_thread.start()
        else:
            self.playing = False

    def play_clicks(self):
        """ Воспроизводит сохраненные клики с заданной скоростью """
        while self.playing:
            for x, y in self.clicks:
                if not self.playing:
                    break
                pyautogui.click(x, y)
                time.sleep(self.click_speed)

    def clear_clicks(self):
        """ Очищает список кликов и останавливает запись/воспроизведение """
        self.clicks.clear()
        self.recording = False
        self.playing = False
        if hasattr(self, 'listener'):
            self.listener.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()```
