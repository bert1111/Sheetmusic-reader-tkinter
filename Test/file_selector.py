# file_selector.py
import tkinter as tk
from tkinter import filedialog

def select_pdf_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        filetypes=[("PDF bestanden", "*.pdf")])
    return file_path
