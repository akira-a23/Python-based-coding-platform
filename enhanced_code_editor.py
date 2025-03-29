import tkinter as tk
from tkinter import filedialog, messagebox, Menu, scrolledtext
import subprocess
import os

class CodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Code Editor")
        self.root.geometry("800x600")

        # Create a menu bar
        self.menu_bar = Menu(root)
        root.config(menu=self.menu_bar)

        # Create File menu
        self.file_menu = Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)

        # Create a toolbar
        self.toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.new_button = tk.Button(self.toolbar, text="New", command=self.new_file)
        self.new_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.open_button = tk.Button(self.toolbar, text="Open", command=self.open_file)
        self.open_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.save_button = tk.Button(self.toolbar, text="Save", command=self.save_file)
        self.save_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.run_button = tk.Button(self.toolbar, text="Run", command=self.run_code)
        self.run_button.pack(side=tk.LEFT, padx=2, pady=2)

        # Create a text area with line numbers
        self.text_area = scrolledtext.ScrolledText(root, wrap="none")
        self.text_area.pack(expand=1, fill="both")

        # Create a status bar
        self.status_bar = tk.Label(root, text="Ln 1, Col 1", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.text_area.bind("<KeyRelease>", self.update_status_bar)

        # Create an output panel for error messages
        self.output_panel = scrolledtext.ScrolledText(root, height=10, state="disabled")
        self.output_panel.pack(side=tk.BOTTOM, fill=tk.X)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.INSERT, content)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)
                messagebox.showinfo("File Saved", "File saved successfully")

    def run_code(self):
        code = self.text_area.get(1.0, tk.END)
        file_path = "temp_code.py"
        with open(file_path, "w") as file:
            file.write(code)

        try:
            result = subprocess.run(["python", file_path], capture_output=True, text=True)
            output = result.stdout + result.stderr
        except Exception as e:
            output = str(e)

        self.output_panel.config(state="normal")
        self.output_panel.delete(1.0, tk.END)
        self.output_panel.insert(tk.INSERT, output)
        self.output_panel.config(state="disabled")

        os.remove(file_path)

    def update_status_bar(self, event=None):
        line, col = self.text_area.index(tk.INSERT).split(".")
        self.status_bar.config(text=f"Ln {line}, Col {col}")

if __name__ == "__main__":
    root = tk.Tk()
    editor = CodeEditor(root)
    root.mainloop()