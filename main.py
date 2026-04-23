import cv2
import numpy as np
import mss
import pydirectinput
import time
import keyboard
import os

# --- НАСТРОЙКИ ---
pydirectinput.PAUSE = 0
# Область поиска (можно расширить, если шкала в другом месте)
# [top, left, width, height]
search_area = {"top": 300, "left": 700, "width": 500, "height": 500} 
threshold = 0.7  # Точность совпадения (от 0.1 до 1.0)

# Проверка наличия картинки
template_path = 'green_part.png'
if not os.path.exists(template_path):
    print(f"ОШИБКА: Файл {template_path} не найден в папке со скриптом!")
    print("Сначала запустите скрипт-снайпер, чтобы сделать снимок зеленого цвета.")
    exit()

# Загружаем шаблон
template = cv2.imread(template_path, cv2.IMREAD_COLOR)

print("=== БОТ ДЛЯ РЫБАЛКИ ЗАПУЩЕН ===")
print(f"Ищу образец: {template_path}")
print("F10 - СТАРТ / ПАУЗА")
print("Q - ПОЛНЫЙ ВЫХОД")

active = False
is_fishing = False

with mss.mss() as sct:
    while True:
        # Управление кнопками
        if keyboard.is_pressed('f10'):
            active = not active
            print("СТАТУС:", "РАБОТАЕТ" if active else "ПАУЗА")
            time.sleep(0.5)

        if keyboard.is_pressed('q'):
            print("Выход из программы...")
            break

        if not active:
            time.sleep(0.1)
            continue

        # 1. Захват экрана
        screenshot = np.array(sct.grab(search_area))
        frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

        # 2. Поиск картинки на экране
        res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)

        # 3. Логика действий
        if max_val >= threshold:
            # Нашли зеленый цвет (триггер активен)
            if not is_fishing:
                print(f"Рыба на крючке! (Совпадение: {max_val:.2f})")
                is_fishing = True
            
            # Сверхбыстрый клик
            pydirectinput.mouseDown()
            pydirectinput.mouseUp()
            
        else:
            # Зеленый цвет пропал
            if is_fishing:
                print("Шкала пропала. Жду 1.5 сек для заброса...")
                is_fishing = False
                
                # Пауза после ловли
                time.sleep(1.5)
                
                # Клик для нового заброса
                pydirectinput.click()
                print("Удочка заброшена. Жду новую рыбу...")
                
                # Пауза, чтобы не поймать ложный триггер во время анимации
                time.sleep(2.0)