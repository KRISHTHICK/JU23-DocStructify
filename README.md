# JU23-DocStructify
Gen AI

DocStructify – Structured Data Extractor from Unstructured Documents

🔍 Problem Statement
Documents such as reports, scanned contracts, or whitepapers often contain mixed content: paragraphs, tables, and images. Businesses need to extract these elements in a structured format for analysis, archiving, or processing.

🎯 Project Objective
Build a system that:

Accepts unstructured PDF documents

Extracts:

Text by sections

All tables (in structured JSON)

All images

Saves extracted content in an organized JSON format

🧱 Folder Structure
bash
Copy
Edit
docstructify/
├── app.py                        # Streamlit UI
├── extractor/
│   ├── text_extractor.py        # Extract text section-wise
│   ├── table_extractor.py       # Extract tables
│   ├── image_extractor.py       # Extract images
├── outputs/
│   ├── extracted_text.json
│   ├── extracted_tables.json
│   ├── images/
├── samples/
│   └── sample_document.pdf
└── requirements.txt
📦 Install Requirements
bash
Copy
Edit
pip install streamlit PyMuPDF pdfplumber pandas pillow
📝 Sample Input File
Place a sample PDF named sample_document.pdf in the samples/ folder with:

A heading

Two paragraphs

One table

One image

(If needed, I can help generate one.)

🔧 Step-by-step Code Setup
1️⃣ extractor/text_extractor.py
python
Copy
Edit
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
2️⃣ extractor/table_extractor.py
python
Copy
Edit
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
3️⃣ extractor/image_extractor.py
python
Copy
Edit
import fitz
import os

def extract_images(pdf_path, output_dir="outputs/images"):
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    images = []
    for i, page in enumerate(doc):
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            img_bytes = base_image["image"]
            img_ext = base_image["ext"]
            img_path = f"{output_dir}/page_{i+1}_img_{img_index + 1}.{img_ext}"
            with open(img_path, "wb") as f:
                f.write(img_bytes)
            images.append(img_path)
    return images
4️⃣ app.py (Streamlit Interface)
python
Copy
Edit
import streamlit as st
import json
from extractor.text_extractor import extract_text_by_sections
from extractor.table_extractor import extract_tables_from_pdf
from extractor.image_extractor import extract_images

st.title("📄 DocStructify - Structured Document Extractor")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ File uploaded and saved!")

    with st.spinner("Extracting text..."):
        text_data = extract_text_by_sections("temp.pdf")
        with open("outputs/extracted_text.json", "w") as f:
            json.dump(text_data, f, indent=2)
        st.subheader("📘 Extracted Text")
        st.json(text_data)

    with st.spinner("Extracting tables..."):
        table_data = extract_tables_from_pdf("temp.pdf")
        with open("outputs/extracted_tables.json", "w") as f:
            json.dump(table_data, f, indent=2)
        st.subheader("📊 Extracted Tables")
        st.json(table_data)

    with st.spinner("Extracting images..."):
        image_paths = extract_images("temp.pdf")
        st.subheader("🖼️ Extracted Images")
        for path in image_paths:
            st.image(path, caption=path)
5️⃣ requirements.txt
nginx
Copy
Edit
streamlit
PyMuPDF
pdfplumber
pandas
Pillow
✅ Example Output (for 1 sample PDF)
json
Copy
Edit
{
  "Page_1": [
    "Title: Monthly Report",
    "This document contains key highlights...",
    "Table: Sales data (see table)",
    "Image: Market trend chart"
  ]
}
🧠 Explanation
Feature	Explanation
extract_text_by_sections	Uses PyMuPDF to extract text per block (good for section-wise)
extract_tables_from_pdf	Uses pdfplumber to parse structured tables as nested JSON
extract_images	Uses PyMuPDF to extract embedded images page-wise
Streamlit UI	Simple front-end to upload PDFs and show all results visually
Output	Organized JSON and image folders for audit, ML pipeline, or database ingestion

🧑‍💻 To Run
bash
Copy
Edit
streamlit run app.py
