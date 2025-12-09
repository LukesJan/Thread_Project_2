import tkinter as tk
import threading
from tkinter import filedialog, messagebox, ttk
from threads import CsvReaderThread, ValidationThread, DatabaseWriterThread, VALIDATOR_COUNT


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Importer")


        self.btn_select = tk.Button(root, text="Select CSV", command=self.select_file)
        self.btn_select.pack(pady=10)


        self.lbl_file = tk.Label(root, text="No file selected")
        self.lbl_file.pack()


        self.progress = ttk.Progressbar(root, length=400)
        self.progress.pack(pady=20)


        self.btn_import = tk.Button(root, text="Import CSV", command=self.import_csv)
        self.btn_import.pack(pady=10)

        self.file_path = None
        self.total_rows = 0

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.file_path:
            self.lbl_file.config(text=self.file_path)

            with open(self.file_path, newline="", encoding="utf-8") as f:
                self.total_rows = sum(1 for _ in f) - 1
            self.progress["maximum"] = self.total_rows

    def import_csv(self):
        if not self.file_path:
            messagebox.showwarning("Warning", "Please select a CSV file first")
            return


        reader = CsvReaderThread(self.file_path)
        reader.start()

        validators = [ValidationThread() for _ in range(VALIDATOR_COUNT)]
        for v in validators:
            v.start()

        writer = DatabaseWriterThread(self.progress, self.total_rows)
        writer.start()


        def wait_thread():
            reader.join()
            for v in validators:
                v.join()
            writer.join()
            messagebox.showinfo("Info", "CSV import completed!")

        threading.Thread(target=wait_thread, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
