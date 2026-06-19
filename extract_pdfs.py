"""Batch extract text from all PDF books in books_raw/书股/ to txt files."""
import os
import sys
import pdfplumber

SOURCE_DIR = r"d:\常用脚本\cangjie-skill\books_raw\书股"
OUTPUT_DIR = r"d:\常用脚本\cangjie-skill\books_txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)

pdf_files = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith('.pdf')]
print(f"Found {len(pdf_files)} PDF files")

for idx, pdf_name in enumerate(pdf_files, 1):
    pdf_path = os.path.join(SOURCE_DIR, pdf_name)
    txt_name = os.path.splitext(pdf_name)[0] + ".txt"
    txt_path = os.path.join(OUTPUT_DIR, txt_name)

    if os.path.exists(txt_path) and os.path.getsize(txt_path) > 1000:
        print(f"[{idx}/{len(pdf_files)}] SKIP (already extracted): {pdf_name}")
        continue

    print(f"[{idx}/{len(pdf_files)}] Extracting: {pdf_name}")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"  Pages: {total_pages}")
            text_parts = []
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    text = page.extract_text() or ""
                    text_parts.append(f"\n=== 第 {page_num} 页 ===\n{text}")
                except Exception as e:
                    text_parts.append(f"\n=== 第 {page_num} 页 ===\n[EXTRACT ERROR: {e}]")

                if page_num % 50 == 0:
                    print(f"  Progress: {page_num}/{total_pages}")

            full_text = "\n".join(text_parts)
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(full_text)
            print(f"  Saved: {txt_path} ({len(full_text)} chars)")
    except Exception as e:
        print(f"  ERROR: {e}")

print("\nDone!")
