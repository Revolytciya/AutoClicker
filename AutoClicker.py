import pyautogui
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
    root.mainloop()
