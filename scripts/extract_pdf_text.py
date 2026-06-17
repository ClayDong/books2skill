"""提取有文本层的 PDF 全文"""
import pdfplumber
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

pdf_path = r"D:\我的资料\书籍\炒股的智慧.pdf"
output_path = r"D:\我的资料\书籍\炒股的智慧.txt"

with pdfplumber.open(pdf_path) as pdf:
    total_pages = len(pdf.pages)
    all_text = []

    for i in range(total_pages):
        page = pdf.pages[i]
        text = page.extract_text()
        if text and text.strip():
            all_text.append(f"\n=== 第 {i+1} 页 ===\n")
            all_text.append(text.strip())
        if (i+1) % 10 == 0:
            print(f"已处理 {i+1}/{total_pages} 页", end='\r')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_text))

    total_chars = sum(len(t) for t in all_text)
    print(f"\n完成! 总字符数: {total_chars}, 输出: {output_path}")
