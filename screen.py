import tkinter as tk
from PIL import ImageGrab
import ctypes
import os

# Фикс для высокого разрешения экрана (DPI), чтобы координаты были точными
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

class SnippingTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-alpha', 0.3)  # Прозрачность окна
        self.root.attributes('-fullscreen', True) # На весь экран
        self.root.attributes("-topmost", True)    # Поверх всех окон
        self.root.config(cursor="cross")         # Курсор-крестик
        
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="grey")
        self.canvas.pack(fill="both", expand=True)
        
        self.start_x = None
        self.start_y = None
        self.rect = None

        # Привязка событий мыши
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        
        # Выход на Esc
        self.root.bind("<Escape>", lambda e: self.root.destroy())

    def on_button_press(self, event):
        # Сохраняем начальные координаты
        self.start_x = event.x
        self.start_y = event.y
        # Создаем прямоугольник выделения
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='red', width=2)

    def on_move_press(self, event):
        # Обновляем размер прямоугольника при движении мыши
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        # Конечные координаты
        end_x, end_y = (event.x, event.y)
        
        # Рассчитываем границы (с учетом того, что можно тянуть влево/вверх)
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)

        # Скрываем прозрачное окно, чтобы оно не попало на скриншот
        self.root.withdraw()
        
        if x2 - x1 > 2 and y2 - y1 > 2:
            self.take_screenshot(x1, y1, x2, y2)
        
        self.root.destroy()

    def take_screenshot(self, x1, y1, x2, y2):
        # Делаем скриншот выбранной области
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        
        # Спрашиваем имя файла прямо в консоли
        print("\nОбласть выбрана!")
        filename = input("Введите имя файла (например, green_part или check_part): ").strip()
        if not filename:
            filename = "captured_area"
        
        full_name = f"{filename}.png"
        img.save(full_name)
        print(f"Успешно сохранено: {os.path.abspath(full_name)}")

if __name__ == "__main__":
    print("=== ИНСТРУКЦИЯ ===")
    print("1. Запустите скрипт.")
    print("2. Зажмите ЛКМ и выделите нужную область на экране.")
    print("3. Отпустите ЛКМ.")
    print("4. В консоли введите имя файла.")
    print("ESC - отмена.")
    
    app = SnippingTool()
    app.root.mainloop()