import mss
import mss.tools
import keyboard
import time
import ctypes
import os

# --- НАСТРОЙКИ ЗАХВАТА ---
offset_up = 15      # На сколько пикселей выше курсора будет центр снимка
crop_size = 30      # Размер квадрата (30x30 пикселей)

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

def get_mouse_pos():
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

print(f"Снайпер запущен. Смещение вверх: {offset_up} пикселей.")
print("Наведи мышь на шкалу и нажми 'V'...")

with mss.mss() as sct:
    while True:
        if keyboard.is_pressed('v'):
            # 1. Получаем координаты мыши
            mx, my = get_mouse_pos()
            
            # 2. Вычисляем новую точку (выше курсора)
            target_x = mx
            target_y = my - offset_up
            
            # 3. Определяем область захвата (центрируем квадрат)
            region = {
                "top": int(target_y - (crop_size // 2)),
                "left": int(target_x - (crop_size // 2)),
                "width": crop_size,
                "height": crop_size
            }
            
            # 4. Делаем скриншот
            img = sct.grab(region)
            
            # 5. Сохраняем
            output_file = "check_part.png"
            mss.tools.to_png(img.rgb, img.size, output=output_file)
            
            print(f"\n[Готово!] Снимок сохранен: {os.path.abspath(output_file)}")
            print(f"Координаты курсора: {mx}, {my}")
            print(f"Координаты центра снимка: {target_x}, {target_y}")
            
            # Короткий звук (опционально), если хочешь знать, что сработало
            time.sleep(0.5) 
            break
            
        if keyboard.is_pressed('esc'):
            break
        time.sleep(0.01)