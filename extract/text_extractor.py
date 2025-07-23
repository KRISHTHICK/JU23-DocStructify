
import fitz  # PyMuPDF

def extract_text_by_sections(pdf_path):
    doc = fitz.open(pdf_path)
    content = {}
    for page_num, page in enumerate(doc, 1):
        text = page.get_text("blocks")
        page_sections = []
        for block in text:
            if block[6] == 0:  # text type
                page_sections.append(block[4])
        content[f"Page_{page_num}"] = page_sections
    return content
