import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

class FileManager:
    def __init__(self, master):
        self.master = master
        self.master.title("File Manager")
        self.master.geometry("600x400")

        self.path_label = tk.Label(master, text="Current Path")
        self.path_label.pack()

        self.path_entry = tk.Entry(master, width=50)
        self.path_entry.pack()

        self.browse_button = tk.Button(master, text="Browse", command=self.browse)
        self.browse_button.pack()

        self.file_listbox = tk.Listbox(master, width=80, height=20)
        self.file_listbox.pack()

        self.refresh_button = tk.Button(master, text="Refresh", command=self.refresh)
        self.refresh_button.pack()

        self.copy_button = tk.Button(master, text="Copy", command=self.copy_file)
        self.copy_button.pack(side=tk.LEFT)

        self.move_button = tk.Button(master, text="Move", command=self.move_file)
        self.move_button.pack(side=tk.LEFT)

        self.delete_button = tk.Button(master, text="Delete", command=self.delete_file)
        self.delete_button.pack(side=tk.LEFT)

    def browse(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)
            self.refresh()

    def refresh(self):
        path = self.path_entry.get()
        if os.path.isdir(path):
            self.file_listbox.delete(0, tk.END)
            for item in os.listdir(path):
                self.file_listbox.insert(tk.END, item)
        else:
            messagebox.showerror("Error", "Invalid path")

    def copy_file(self):
        src = self.get_selected_file()
        if src:
            dst = filedialog.asksaveasfilename()
            if dst:
                shutil.copy(src, dst)
                messagebox.showinfo
