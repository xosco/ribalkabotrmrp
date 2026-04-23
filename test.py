import cv2
import numpy as np
import mss
import pydirectinput
import time
import keyboard
import os

# --- НАСТРОЙКИ ---
pydirectinput.PAUSE = 0
# Область поиска [top, left, width, height]
search_area = {"top": 200, "left": 600, "width": 700, "height": 700} 

threshold_fish = 0.7   # Точность для зеленого триггера (рыбалка)
threshold_check = 0.8  # Точность для триггера заброса (check_part)

# Загрузка шаблонов
template_fish = cv2.imread('green_part.png', cv2.IMREAD_COLOR)
template_check = cv2.imread('check_part.png', cv2.IMREAD_COLOR)

if template_fish is None or template_check is None:
    print("ОШИБКА: Файлы шаблонов (green_part.png / check_part.png) не найдены!")
    exit()

print("=== БОТ С ЗАДЕРЖКОЙ ЗАБРОСА ЗАПУЩЕН ===")
print("F10 - СТАРТ / ПАУЗА | Q - ВЫХОД")

active = False

with mss.mss() as sct:
    while True:
        # Управление состоянием (Вкл/Выкл)
        if keyboard.is_pressed('f10'):
            active = not active
            print("СТАТУС:", "РАБОТАЕТ" if active else "ПАУЗА")
            time.sleep(0.5)

        if keyboard.is_pressed('q'):
            print("Выход...")
            break

        if not active:
            time.sleep(0.1)
            continue

        # 1. Захват экрана
        screenshot = np.array(sct.grab(search_area))
        frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

        # 2. ПОИСК ЗЕЛЕНОГО ТРИГГЕРА (Активная фаза ловли)
        res_fish = cv2.matchTemplate(frame, template_fish, cv2.TM_CCOEFF_NORMED)
        _, max_val_fish, _, _ = cv2.minMaxLoc(res_fish)

        if max_val_fish >= threshold_fish:
            # Быстрый клик без задержек пока видим зеленый
            pydirectinput.mouseDown()
            pydirectinput.mouseUp()
            continue # Сразу переходим к следующему кадру

        # 3. ПОИСК ТРИГГЕРА ЗАБРОСА (check_part.png)
        res_check = cv2.matchTemplate(frame, template_check, cv2.TM_CCOEFF_NORMED)
        _, max_val_check, _, _ = cv2.minMaxLoc(res_check)

        if max_val_check >= threshold_check:
            print(f"Триггер заброса найден! Жду 0.3 сек...")
            
            # Ждем 0.3 секунды по твоему запросу
            time.sleep(0.3)
            
            # Делаем один клик
            pydirectinput.click()
            print("Клик для заброса выполнен.")
            
            # Большая пауза (3 секунды), чтобы иконка заброса исчезла
            # и персонаж успел закинуть удочку.
            time.sleep(3.0) 
            print("Жду появления рыбы...")