import fitz  # PyMuPDF
from PIL import Image, ImageTk
import io

class PDFRenderer:
    def __init__(self):
        self.doc = None

    def open_pdf(self, filepath):
        self.doc = fitz.open(filepath)

    def get_page_count(self):
        if self.doc:
            return self.doc.page_count
        return 0

    def render_page(self, page_number, zoom=1.0, rotation=0):
        if not self.doc or page_number < 0 or page_number >= self.doc.page_count:
            return None
        page = self.doc.load_page(page_number)
        mat = fitz.Matrix(zoom, zoom).prerotate(rotation)
        pix = page.get_pixmap(matrix=mat)
        img_data = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_data))
        photo = ImageTk.PhotoImage(image)
        return photo
