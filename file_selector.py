import tkinter as tk
from tkinter import filedialog

def open_pdf_filechooser(on_file_selected_callback):
    # Maak een verborgen root window om de dialog te laten werken
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Selecteer PDF-bestand",
        filetypes=[("PDF bestanden", "*.pdf")]
    )
    root.destroy()
    if file_path:
        on_file_selected_callback(file_path)
