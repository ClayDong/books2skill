"""快速检查PDF哪些页有文本层
用法: python check_pdf_text.py <pdf_path>
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import pdfplumber

pdf_path = sys.argv[1]
with pdfplumber.open(pdf_path) as pdf:
    total = len(pdf.pages)
    with_text = 0
    with_good_text = 0
    print(f"总页数: {total}")

    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            with_text += 1
            if len(text.strip()) > 50:
                with_good_text += 1
                if i < 5 or i % 50 == 0:
                    print(f"  第 {i+1} 页: {len(text.strip())} 字符 - 样例: {text.strip()[:60]}...")

    print(f"\n有文本层: {with_text}/{total} ({with_text*100//total}%)")
    print(f"文本足够 (>50字符): {with_good_text}/{total} ({with_good_text*100//total}%)")
