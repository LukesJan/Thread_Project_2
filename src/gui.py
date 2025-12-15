import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from threads import CsvReaderThread, ValidationThread, DatabaseWriterThread, VALIDATOR_COUNT
from config import CSV_FILE

class App:
    def __init__(self, root):
        """
         Initialize the GUI application.

         Args:
             root (tk.Tk): The main Tkinter window

         Sets up:
         - CSV file selection button
         - Label showing selected file
         - Progress bar
         - Import button
         - Default CSV file path and total rows
         - Window close protocol
         """
        self.root = root
        self.root.title("CSV Importer")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.btn_select = tk.Button(root, text="Select CSV", command=self.select_file)
        self.btn_select.pack(pady=10)

        self.lbl_file = tk.Label(root, text="No file selected")
        self.lbl_file.pack()

        self.progress = ttk.Progressbar(root, length=400)
        self.progress.pack(pady=20)

        self.btn_import = tk.Button(root, text="Import CSV", command=self.import_csv)
        self.btn_import.pack(pady=10)

        self.file_path = CSV_FILE
        self.total_rows = 0

    def select_file(self):
        """
        Open a file dialog to select a CSV file

        Updates:
        - self.file_path with the selected file
        - self.lbl_file to show selected file path
        - self.total_rows by counting rows in CSV (excluding header)
        - self.progress maximum value for progress bar
        """

        self.file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.file_path:
            self.lbl_file.config(text=self.file_path)
            with open(self.file_path, newline="", encoding="utf-8") as f:
                self.total_rows = sum(1 for i in f) - 1
            self.progress["maximum"] = self.total_rows

    def import_csv(self):
        """
        Start the CSV import process using multiple threads

        Process:
        Starts CsvReaderThread to read CSV rows
        Starts VALIDATOR_COUNT x ValidationThread to validate rows
        Starts DatabaseWriterThread to insert rows into the database
        Starts a background thread to wait for all threads to finish
        Shows a message box when import completes

        """

        if not self.file_path:
            messagebox.showwarning("Warning", "Please select a CSV file first")
            return

        reader = CsvReaderThread(self.file_path)
        reader.start()

        validators = [ValidationThread() for i in range(VALIDATOR_COUNT)]
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

    def on_close(self):
        """
        Handle application close event.

        Actions:
        - Destroys the Tkinter root window
        - Exits the program
        """

        self.root.destroy()
        import sys
        sys.exit(0)
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
