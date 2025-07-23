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
