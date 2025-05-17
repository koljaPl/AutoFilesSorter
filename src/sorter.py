# src/sorter.py
import os
import shutil
from src.config import EXTENSION_MAP

def sort_files(folder):
    """
    Переносит файлы из папки `folder` в подкаталоги согласно EXTENSION_MAP.
    """
    # Итерируем содержимое папки
    for entry in os.listdir(folder):
        source = os.path.join(folder, entry)
        # Проверяем, что это файл
        if os.path.isfile(source):
            _, ext = os.path.splitext(entry)
            ext = ext.lower()
            # Находим папку-назначение по расширению
            if ext in EXTENSION_MAP:
                target_dir = os.path.join(folder, EXTENSION_MAP[ext])
                os.makedirs(target_dir, exist_ok=True)       # создаём папку, если нет
                shutil.move(source, os.path.join(target_dir, entry))  # перемещаем файл
