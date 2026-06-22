"""OCR 扫描版 PDF → 文本文件 (增量写版本)
用法: python ocr_pdf.py <pdf_path> <output_txt> [--start N] [--end N]

改进:
- 每页处理完就追加写入, 中途中断不会丢
- 用 .tmp 中间文件, 完成后改名
- 日志输出更友好
"""
import os
os.environ['FLAGS_use_mkldnn'] = '0'

import sys
import io
import argparse
import time
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import pdfplumber
import numpy as np
from paddleocr import PaddleOCR


def clean_filename(s):
    """清理文件名(用于日志)"""
    return re.sub(r'[^\w]', '_', s)[:50]


def ocr_pdf(pdf_path, output_txt, start_page=0, end_page=None, dpi=150, skip_existing=True):
    """OCR 处理, 每页增量写"""
    print(f"[OCR] 启动: {pdf_path}", flush=True)
    print(f"[OCR] 输出: {output_txt}", flush=True)

    print(f"[OCR] 初始化 PaddleOCR...", flush=True)
    ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
    print(f"[OCR] PaddleOCR 初始化完成", flush=True)

    # 准备输出目录
    output_dir = os.path.dirname(output_txt)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 用 .tmp 文件保存中间结果
    tmp_txt = output_txt + '.tmp'

    # 跳过已处理的页(如果 skip_existing=True)
    processed_pages = set()
    if skip_existing and os.path.exists(tmp_txt):
        with open(tmp_txt, 'r', encoding='utf-8') as f:
            content = f.read()
            for m in re.finditer(r'=== 第 (\d+) 页 ===', content):
                processed_pages.add(int(m.group(1)))
        print(f"[OCR] 已处理页: {len(processed_pages)} (从 .tmp 恢复)", flush=True)

    # 用 a+ 模式追加
    f_out = open(tmp_txt, 'a+', encoding='utf-8')

    try:
        # 尝试 pypdfium2
        try:
            import pypdfium2
            use_pypdfium2 = True
            pdf_doc = pypdfium2.PdfDocument(pdf_path)
            print(f"[OCR] 使用 pypdfium2 渲染, DPI={dpi}", flush=True)
        except ImportError:
            use_pypdfium2 = False
            print(f"[OCR] pypdfium2 不可用", flush=True)

        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            if end_page is None or end_page > total_pages:
                end_page = total_pages

            print(f"[OCR] 总页数: {total_pages}, 处理: {start_page+1}-{end_page}", flush=True)

            success_count = 0
            fail_count = 0
            start_time = time.time()

            for i in range(start_page, end_page):
                page_num = i + 1

                # 跳过已处理
                if page_num in processed_pages:
                    continue

                # 方法1: 先尝试直接提取文本层
                page = pdf.pages[i]
                text = page.extract_text()
                page_text = None

                if text and len(text.strip()) > 50:
                    page_text = text.strip()
                    method = "text-layer"
                else:
                    # 方法2: 渲染为图片 OCR
                    if use_pypdfium2:
                        try:
                            pdf_page = pdf_doc[i]
                            bitmap = pdf_page.render(scale=dpi/72)
                            pil_image = bitmap.to_pil()
                            img_array = np.array(pil_image)

                            result = ocr.ocr(img_array, cls=True)
                            if result and result[0]:
                                lines = [line[1][0] for line in result[0] if line[1][0].strip()]
                                page_text = '\n'.join(lines)
                                method = "ocr-pypdfium2"
                        except Exception as e:
                            print(f"\n[OCR] 第 {page_num} 页 OCR 失败: {e}", flush=True)

                # 写入
                f_out.write(f"\n=== 第 {page_num} 页 ===\n")
                if page_text:
                    f_out.write(page_text)
                    f_out.write("\n")
                    f_out.flush()  # 立即刷盘
                    success_count += 1
                else:
                    f_out.write(f"[第 {page_num} 页 OCR 失败]\n")
                    f_out.flush()
                    fail_count += 1

                # 进度日志
                elapsed = time.time() - start_time
                avg_per_page = elapsed / (success_count + fail_count) if (success_count + fail_count) > 0 else 0
                remaining = (end_page - page_num) * avg_per_page
                print(
                    f"[OCR] {page_num}/{end_page} | 成功:{success_count} 失败:{fail_count} | "
                    f"耗时:{elapsed:.0f}s | 剩余:{remaining/60:.0f}min | "
                    f"方法:{method if 'method' in dir() else 'text-layer'}",
                    flush=True
                )

        if use_pypdfium2:
            pdf_doc.close()

    finally:
        f_out.close()

    # 完成后改名为正式文件
    if os.path.exists(output_txt):
        os.remove(output_txt)
    os.rename(tmp_txt, output_txt)

    # 统计
    file_size = os.path.getsize(output_txt)
    print(f"\n[OCR] 完成! 文件: {output_txt}", flush=True)
    print(f"[OCR] 大小: {file_size/1024:.0f} KB", flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='OCR 扫描版 PDF')
    parser.add_argument('pdf_path', help='PDF 文件路径')
    parser.add_argument('output_txt', help='输出文本文件路径')
    parser.add_argument('--start', type=int, default=0, help='起始页(0-based)')
    parser.add_argument('--end', type=int, default=None, help='结束页(exclusive)')
    parser.add_argument('--dpi', type=int, default=150, help='DPI (default: 150, lower=faster)')
    parser.add_argument('--no-skip', action='store_true', help='不跳过已处理页')
    args = parser.parse_args()

    ocr_pdf(args.pdf_path, args.output_txt, args.start, args.end, args.dpi, not args.no_skip)
