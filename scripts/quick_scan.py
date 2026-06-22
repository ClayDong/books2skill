"""快速扫描脚本 - 阶段 -1
提取 PDF 的目录页、序言、首尾章节，用于评估书的角色和优先级。
"""
import pdfplumber
import sys
import os

def scan_pdf(pdf_path, max_pages=20):
    """提取 PDF 前 max_pages 页的文本"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"=== {os.path.basename(pdf_path)} ===")
            print(f"总页数: {total_pages}")
            print()

            # 提取前 max_pages 页
            scan_pages = min(max_pages, total_pages)
            for i in range(scan_pages):
                page = pdf.pages[i]
                text = page.extract_text()
                if text:
                    # 只打印前 500 字符
                    print(f"--- 第 {i+1} 页 ---")
                    print(text[:500])
                    print()

            # 如果书很厚，也提取最后几页
            if total_pages > max_pages + 5:
                print(f"--- 最后 3 页 ---")
                for i in range(total_pages - 3, total_pages):
                    page = pdf.pages[i]
                    text = page.extract_text()
                    if text:
                        print(f"--- 第 {i+1} 页 ---")
                        print(text[:500])
                        print()

    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    books_dir = r"D:\我的资料\书籍"
    pdf_files = [
        "共同富裕.pdf",
        "炒股的智慧.pdf",
        "经济学原理(第8版) 微观经济学分册（曼昆著）.pdf",
    ]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(books_dir, pdf_file)
        if os.path.exists(pdf_path):
            scan_pdf(pdf_path, max_pages=15)
            print("\n" + "="*80 + "\n")
        else:
            print(f"文件不存在: {pdf_path}")
