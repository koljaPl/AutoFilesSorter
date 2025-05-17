# src/gui.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
from threading import Thread
from sorter import sort_files

class FileOrganizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Файловый органайзер")
        self.geometry("450x200")
        # Поле для отображения выбранной папки
        self.folder_var = ctk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Папка для сортировки:").pack(pady=5)
        ctk.CTkEntry(self, textvariable=self.folder_var, width=300).pack(pady=5)
        ctk.CTkButton(self, text="Выбрать папку", command=self.choose_folder).pack(pady=5)
        ctk.CTkButton(self, text="Начать сортировку", command=self.start_sort).pack(pady=10)

    def choose_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_var.set(path)

    def start_sort(self):
        folder = self.folder_var.get()
        if folder:
            # Запускаем сортировку в отдельном потоке, чтобы GUI оставался отзывчивым:contentReference[oaicite:7]{index=7}
            Thread(target=self.run_sort, args=(folder,), daemon=True).start()

    def run_sort(self, folder):
        try:
            sort_files(folder)
            messagebox.showinfo("Готово", "Сортировка завершена")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

if __name__ == "__main__":
    app = FileOrganizerApp()
    app.mainloop()
