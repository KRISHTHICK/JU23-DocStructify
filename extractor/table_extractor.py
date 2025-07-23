import pdfplumber
import pandas as pd

def extract_tables_from_pdf(pdf_path):
    tables = {}
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_tables = page.extract_tables()
            page_data = []
            for table in page_tables:
                df = pd.DataFrame(table[1:], columns=table[0])
                page_data.append(df.to_dict(orient="records"))
            if page_data:
                tables[f"Page_{i+1}"] = page_data
    return tables
