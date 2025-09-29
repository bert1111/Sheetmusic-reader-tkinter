import tkinter as tk
from tkinter import messagebox, colorchooser
from pdf_renderer import PDFRenderer
from page_navigator import PageNavigator
from annotation_widget import AnnotationWidget
from annotation_storage import AnnotationStorage
from page_settings import PageSettings
from file_selector import open_pdf_filechooser

class PDFViewerUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Sheet Music Viewer Tkinter")
        self.pack(fill="both", expand=True)

        self.renderer = PDFRenderer()
        self.navigator = PageNavigator()
        self.annotation_storage = AnnotationStorage()
        self.page_settings = PageSettings()

        self.filepath = None
        self.current_zoom = 1.0
        self.current_rotation = 0

        # Bouw UI
        self.build_ui()

    def build_ui(self):
        # Buttons boven
        btn_frame = tk.Frame(self)
        btn_frame.pack(side="top", fill="x")

        open_btn = tk.Button(btn_frame, text="Open PDF", command=self.open_pdf)
        open_btn.pack(side="left")

        prev_btn = tk.Button(btn_frame, text="Vorige", command=self.prev_page)
        prev_btn.pack(side="left")

        next_btn = tk.Button(btn_frame, text="Volgende", command=self.next_page)
        next_btn.pack(side="left")

        zoom_in_btn = tk.Button(btn_frame, text="Zoom +", command=self.zoom_in)
        zoom_in_btn.pack(side="left")

        zoom_out_btn = tk.Button(btn_frame, text="Zoom -", command=self.zoom_out)
        zoom_out_btn.pack(side="left")

        rotate_btn = tk.Button(btn_frame, text="Draai 90°", command=self.rotate)
        rotate_btn.pack(side="left")

        color_btn = tk.Button(btn_frame, text="Kies Kleur", command=self.choose_color)
        color_btn.pack(side="left")

        clear_ann_btn = tk.Button(btn_frame, text="Wis annotaties", command=self.clear_annotations)
        clear_ann_btn.pack(side="left")

        save_btn = tk.Button(btn_frame, text="Opslaan & Afsluiten", command=self.save_and_quit)
        save_btn.pack(side="left")

        # PDF afbeelding label
        self.img_label = tk.Label(self)
        self.img_label.pack(expand=True, fill="both")

        # Annotatie widget boven de PDF afbeelding
        self.annotation_widget = AnnotationWidget(self.img_label)

    def open_pdf(self):
        def callback(filepath):
            try:
                self.filepath = filepath
                self.renderer.open_pdf(filepath)
                self.navigator.set_total_pages(self.renderer.get_page_count())
                self.current_zoom = 1.0
                self.current_rotation = 0
                self.navigator.current_page = 0
                self.show_page()
            except Exception as e:
                messagebox.showerror("Fout", f"Kon PDF niet openen:\n{e}")

        open_pdf_filechooser(callback)

    def show_page(self):
        if not self.filepath:
            return
        photo = self.renderer.render_page(
            self.navigator.current_page,
            zoom=self.current_zoom,
            rotation=self.current_rotation
        )
        if photo:
            self.img_label.config(image=photo)
            self.img_label.image = photo  # Hou referentie
            # Laad annotaties voor deze pagina
            annotations = self.annotation_storage.get(
                self.filepath,
                self.navigator.current_page
            )
            self.annotation_widget.load_lines(annotations)

    def prev_page(self):
        self.save_annotations()
        self.navigator.prev_page()
        self.show_page()

    def next_page(self):
        self.save_annotations()
        self.navigator.next_page()
        self.show_page()

    def zoom_in(self):
        self.current_zoom *= 1.1
        self.show_page()

    def zoom_out(self):
        self.current_zoom /= 1.1
        self.show_page()

    def rotate(self):
        self.current_rotation = (self.current_rotation + 90) % 360
        self.show_page()

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            # Zet annotatie kleur (optioneel uitbreiden in AnnotationWidget)
            pass

    def clear_annotations(self):
        self.annotation_widget.clear()

    def save_annotations(self):
        if self.filepath:
            self.annotation_storage.set(
                self.filepath,
                self.navigator.current_page,
                self.annotation_widget.lines
            )
            self.annotation_storage.save()

    def save_and_quit(self):
        self.save_annotations()
        self.page_settings.save()
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x700")
    app = PDFViewerUI(root)
    app.mainloop()
