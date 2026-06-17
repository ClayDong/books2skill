"""提取 DOCX 全文"""
from docx import Document
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

docx_path = r"D:\我的资料\书籍\大师兄.docx"
output_path = r"D:\我的资料\书籍\大师兄.txt"

doc = Document(docx_path)
all_text = []

for i, para in enumerate(doc.paragraphs):
    if para.text.strip():
        all_text.append(para.text.strip())

with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(all_text))

total_chars = sum(len(t) for t in all_text)
print(f"完成! 总段落数: {len(all_text)}, 总字符数: {total_chars}, 输出: {output_path}")
