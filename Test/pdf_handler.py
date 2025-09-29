# pdf_handler.py
from pypdf import PdfReader

class PDFHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.reader = PdfReader(self.file_path)
        self.num_pages = len(self.reader.pages)

    def get_page_text(self, page_number):
        if 0 <= page_number < self.num_pages:
            return self.reader.pages[page_number].extract_text()
        return None

    def get_num_pages(self):
        return self.num_pages
