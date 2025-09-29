import tkinter as tk
from viewer_ui import PDFViewerUI

def main():
    root = tk.Tk()
    root.geometry("900x700")
    app = PDFViewerUI(root)
    app.pack(fill="both", expand=True)
    
    # Event voor netjes afsluiten en eventueel instellingen opslaan
    def on_closing():
        app.save_annotations()
        app.page_settings.save()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
