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
