"""扫描曼昆经济学的目录和关键章节"""
import pdfplumber
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

pdf_path = r"D:\我的资料\书籍\经济学原理(第8版) 微观经济学分册（曼昆著）.pdf"

with pdfplumber.open(pdf_path) as pdf:
    total_pages = len(pdf.pages)
    print(f"总页数: {total_pages}")
    print()

    # 找到第一个有实质内容的页
    for i in range(total_pages):
        page = pdf.pages[i]
        text = page.extract_text()
        if text and len(text.strip()) > 100:
            print(f"=== 第 {i+1} 页 (首个有内容页) ===")
            print(text[:2000])
            print()
            # 打印接下来 5 页
            for j in range(i+1, min(i+6, total_pages)):
                page2 = pdf.pages[j]
                text2 = page2.extract_text()
                if text2 and text2.strip():
                    print(f"=== 第 {j+1} 页 ===")
                    print(text2[:2000])
                    print()
            break
