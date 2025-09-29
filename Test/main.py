# main.py
from file_selector import select_pdf_file
from pdf_handler import PDFHandler

pdf_path = select_pdf_file()
if pdf_path:
    handler = PDFHandler(pdf_path)
    print("Aantal pagina's:", handler.get_num_pages())
    print("Eerste pagina tekst:", handler.get_page_text(0))
else:
    print("Geen bestand geselecteerd.")
