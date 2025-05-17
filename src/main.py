import os
import shutil
import customtkinter as ctk
from tkinter import filedialog, messagebox
from threading import Thread

# Конфигурация сортировки: расширение → имя папки
EXTENSION_MAP = {
    ".jpg": "Pictures",
    ".jpeg": "Pictures",
    ".png": "Pictures",
    ".gif": "Pictures",
    ".jfif": "Pictures",
    ".webp": "Pictures",
    ".HEIC": "Pictures",
    ".mp4": "Videos",
    ".mkv": "Videos",
    ".webm": "Videos",
    ".mp3": "Audio",
    ".wav": "Audio",
    ".pdf": "Documents",
    ".cfg": "Documents",
    ".md": "Documents",
    ".odt": "Documents",
    ".docx": "Documents",
    ".xlsx": "Documents",
    ".pptx": "Documents",
    ".txt": "Documents",
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".py": "Code",
    ".java": "Code",
    ".c": "Code",
    ".cpp": "Code",
    ".html": "Code",
    ".css": "Code",
    ".js": "Code",
    ".json": "Code",
    ".jar": "Code"
}

def sort_files(folder):
    try:
        files = os.listdir(folder)
        for filename in files:
            full_path = os.path.join(folder, filename)
            if os.path.isfile(full_path):
                _, ext = os.path.splitext(filename)
                ext = ext.lower()
                if ext in EXTENSION_MAP:
                    target_dir = os.path.join(folder, EXTENSION_MAP[ext])
                    os.makedirs(target_dir, exist_ok=True)
                    target_path = os.path.join(target_dir, filename)

                    # Если файл уже существует, переименуем
                    if os.path.exists(target_path):
                        name, extension = os.path.splitext(filename)
                        i = 1
                        while os.path.exists(target_path):
                            new_name = f"{name}_{i}{extension}"
                            target_path = os.path.join(target_dir, new_name)
                            i += 1

                    shutil.move(full_path, target_path)
    except Exception as e:
        raise RuntimeError(f"Ошибка при сортировке: {e}")

class FileOrganizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Файловый органайзер")
        self.geometry("500x220")
        self.resizable(False, False)

        self.folder_var = ctk.StringVar()

        ctk.CTkLabel(self, text="Выберите папку для сортировки:", font=("Arial", 14)).pack(pady=(15, 5))

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack()

        ctk.CTkEntry(frame, width=340, textvariable=self.folder_var).pack(side="left", padx=(0, 10))
        ctk.CTkButton(frame, text="Обзор...", command=self.choose_folder).pack(side="left")

        ctk.CTkButton(self, text="Сортировать файлы", command=self.start_sort, width=200).pack(pady=20)

        ctk.CTkLabel(self, text="Фоновые потоки используются для ускорения работы", font=("Arial", 11), text_color="gray").pack()

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)

    def start_sort(self):
        folder = self.folder_var.get()
        if not folder or not os.path.exists(folder):
            messagebox.showerror("Ошибка", "Папка не выбрана или не существует.")
            return
        Thread(target=self.run_sort, args=(folder,), daemon=True).start()

    def run_sort(self, folder):
        try:
            sort_files(folder)
            messagebox.showinfo("Успешно", "Файлы успешно отсортированы.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # или "Dark"/"Light"
    ctk.set_default_color_theme("blue")  # можно "green", "dark-blue", etc.
    app = FileOrganizerApp()
    app.mainloop()
