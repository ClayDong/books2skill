"""检查所有 PDF 的文本层状态"""
import pdfplumber
import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

books_dir = r"D:\我的资料\书籍"
pdf_files = [
    "共同富裕.pdf",
    "炒股的智慧.pdf",
    "经济学原理(第8版) 微观经济学分册（曼昆著）.pdf",
]

for pdf_file in pdf_files:
    pdf_path = os.path.join(books_dir, pdf_file)
    if not os.path.exists(pdf_path):
        print(f"文件不存在: {pdf_file}")
        continue

    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            text_pages = 0
            total_chars = 0

            # 检查前 30 页
            for i in range(min(30, total_pages)):
                page = pdf.pages[i]
                text = page.extract_text()
                if text and len(text.strip()) > 50:
                    text_pages += 1
                    total_chars += len(text.strip())

            # 检查中间页
            mid_text = 0
            for i in [total_pages//2, total_pages//4, total_pages*3//4]:
                if i < total_pages:
                    page = pdf.pages[i]
                    text = page.extract_text()
                    if text and len(text.strip()) > 50:
                        mid_text += 1

            print(f"=== {pdf_file} ===")
            print(f"  总页数: {total_pages}")
            print(f"  前30页有文本: {text_pages}/30")
            print(f"  前30页总字符: {total_chars}")
            print(f"  中间页有文本: {mid_text}/3")
            if text_pages > 5:
                print(f"  状态: ✅ 有文本层")
            elif text_pages > 0:
                print(f"  状态: ⚠️ 部分有文本层")
            else:
                print(f"  状态: ❌ 扫描版，需要OCR")
            print()
    except Exception as e:
        print(f"=== {pdf_file} ===")
        print(f"  错误: {e}")
        print()
