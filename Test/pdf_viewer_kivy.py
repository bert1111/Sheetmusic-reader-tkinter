# pdf_viewer_kivy.py
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.graphics.texture import Texture

import fitz  # PyMuPDF
import io
from PIL import Image as PILImage

class PDFViewer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.img_widget = Image(size_hint=(1, 1), allow_stretch=True, keep_ratio=True)
        self.add_widget(self.img_widget)

        btn_load = Button(text="Open PDF", size_hint_y=None, height=50)
        btn_load.bind(on_release=self.open_filechooser)
        self.add_widget(btn_load)

        self.doc = None
        self.current_page = 0

    def open_filechooser(self, instance):
        content = FileChooserListView(filters=["*.pdf"])
        popup = Popup(title="Selecteer PDF-bestand", content=content, size_hint=(0.9, 0.9))

        def file_selected(inst, selection, touch):
            if selection:
                popup.dismiss()
                self.load_pdf(selection[0])

        content.bind(on_submit=file_selected)
        popup.open()

    def load_pdf(self, filepath):
        try:
            self.doc = fitz.open(filepath)
            self.current_page = 0
            self.render_page(self.current_page)
        except Exception as e:
            print(f"Fout bij laden PDF: {e}")

    def render_page(self, page_number):
        if not self.doc or not (0 <= page_number < len(self.doc)):
            return

        page = self.doc.load_page(page_number)
        zoom_matrix = fitz.Matrix(2, 2)  # 2x zoom voor scherpere afbeelding
        pix = page.get_pixmap(matrix=zoom_matrix)

        img_data = pix.tobytes("png")
        pil_image = PILImage.open(io.BytesIO(img_data))

        # Zorg dat PIL image in RGBA is
        if pil_image.mode != 'RGBA':
            pil_image = pil_image.convert('RGBA')

        data = pil_image.tobytes()
        texture = Texture.create(size=pil_image.size, colorfmt='rgba')
        texture.blit_buffer(data, colorfmt='rgba', bufferfmt='ubyte')
        texture.flip_vertical()

        self.img_widget.texture = texture
        self.img_widget.size = pil_image.size

class PDFViewerApp(App):
    def build(self):
        return PDFViewer()

if __name__ == '__main__':
    PDFViewerApp().run()
