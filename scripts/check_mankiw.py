"""检查曼昆经济学哪些页有文本"""
import pdfplumber
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

pdf_path = r"D:\我的资料\书籍\经济学原理(第8版) 微观经济学分册（曼昆著）.pdf"

with pdfplumber.open(pdf_path) as pdf:
    total_pages = len(pdf.pages)
    print(f"总页数: {total_pages}")
    print()

    # 检查前 50 页哪些有文本
    text_pages = []
    for i in range(min(50, total_pages)):
        page = pdf.pages[i]
        text = page.extract_text()
        if text and len(text.strip()) > 50:
            text_pages.append((i+1, len(text.strip())))

    print(f"前 50 页中有文本的页: {text_pages}")
    print()

    # 检查中间几页
    mid_pages = []
    for i in [100, 200, 300, 400, 500]:
        if i < total_pages:
            page = pdf.pages[i]
            text = page.extract_text()
            if text:
                mid_pages.append((i+1, len(text.strip()), text[:200]))
            else:
                mid_pages.append((i+1, 0, "无文本"))

    print("中间页检查:")
    for p in mid_pages:
        print(f"  第 {p[0]} 页: {p[1]} 字符")
        if p[2] != "无文本":
            print(f"    预览: {p[2]}")
        print()
