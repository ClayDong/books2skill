# -*- coding: utf-8 -*-
"""
OCR extract text from scanned PDF books using PaddleOCR + PyMuPDF.

Usage:
    python ocr_pdfs.py                  # process all scanned PDFs
    python ocr_pdfs.py "海龟交易法则.pdf"  # process single file
    python ocr_pdfs.py --test           # process only 海龟交易法则 as test
"""
import os
import re
import sys
import time
import numpy as np
import fitz  # PyMuPDF
from PIL import Image
from paddleocr import PaddleOCR

# ── Paths ──────────────────────────────────────────────
SOURCE_DIR = r"d:\常用脚本\cangjie-skill\books_raw\书股"
OUTPUT_DIR = r"d:\常用脚本\cangjie-skill\books_txt_ocr"
EXISTING_TXT_DIR = r"d:\常用脚本\cangjie-skill\books_txt"

# Files with existing txt < this threshold (KB) are considered scanned
SCANNED_THRESHOLD_KB = 100

# DPI for PDF→image rendering (200 is good balance of quality/speed)
RENDER_DPI = 200

# ── Watermark patterns ────────────────────────────────
WATERMARK_PATTERNS = [
    # 白云居
    r'白云居', r'baiyunju\.cc', r'baiyunju',
    # 股窜网
    r'股窜网', r'gucuan\.com', r'gucuan',
    # 55188 / 理想在线证券网
    r'55188\.com', r'55188', r'理想在线证券网', r'理想在线',
    # 老庄易财经博客
    r'老庄易财经博客', r'老庄易', r'laozhuangyi\.cn', r'laozhuangyi',
    # 挥剑斩浮云
    r'挥剑斩浮云',
    # 7help.net / 交易手续费
    r'7help\.net', r'7help',
    r'全国最低交易手续费.*', r'零佣金.*', r'期货开户和书籍下载.*',
    r'客服QQ.*', r'客服微信.*',
    # lunarora
    r'lunarora\.com', r'lunarora',
    # Broken watermark fragments (OCR splits 『 白云居丨https://baiyunju.cc 』整理)
    r'『.*?整理', r'』.*?整理', r'丨https?://.*整理',
    r'^『\s*$', r'^』\s*$', r'^丨https?://\s*$',
    r'^整理\s*$', r'^https?://\s*$',
    # Common page-number-only lines
    r'^\s*\d+\s*$',
]

WATERMARK_REGEX = re.compile('|'.join(WATERMARK_PATTERNS), re.IGNORECASE)


def clean_text(text: str) -> str:
    """Remove watermark lines and clean up text."""
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        # Skip lines that are entirely watermark
        if WATERMARK_REGEX.search(stripped):
            # If the line is ONLY watermark, skip entirely
            remaining = WATERMARK_REGEX.sub('', stripped).strip()
            if not remaining:
                continue
            cleaned.append(remaining)
        else:
            cleaned.append(stripped)
    return '\n'.join(cleaned)


def render_page_to_image(page, dpi=RENDER_DPI):
    """Render a PDF page to numpy array using PyMuPDF."""
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat)
    img_data = pix.tobytes("png")
    import io
    img = Image.open(io.BytesIO(img_data))
    return np.array(img)


def ocr_pdf(pdf_path: str, ocr_engine: PaddleOCR, txt_path: str) -> dict:
    """OCR a single PDF and save text. Returns stats dict."""
    start_time = time.time()
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    pages_with_text = 0
    total_chars = 0

    print(f"  Total pages: {total_pages}", flush=True)

    # Write incrementally to avoid losing progress on crash
    with open(txt_path, "w", encoding="utf-8") as f:
        for page_num in range(total_pages):
            try:
                img_array = render_page_to_image(doc[page_num])
                result = ocr_engine.ocr(img_array, cls=True)

                page_text = []
                if result and result[0]:
                    for line in result[0]:
                        if line and len(line) >= 2:
                            text_info = line[1]  # (text, confidence)
                            if isinstance(text_info, tuple) and len(text_info) >= 1:
                                page_text.append(text_info[0])

                raw_text = '\n'.join(page_text)
                cleaned = clean_text(raw_text)

                if cleaned:
                    pages_with_text += 1
                    total_chars += len(cleaned)

                f.write(f"\n=== 第 {page_num + 1} 页 ===\n{cleaned}\n")
                f.flush()

            except Exception as e:
                f.write(f"\n=== 第 {page_num + 1} 页 ===\n[OCR ERROR: {e}]\n")
                f.flush()

            if (page_num + 1) % 10 == 0 or page_num + 1 == total_pages:
                elapsed = time.time() - start_time
                print(f"  Progress: {page_num + 1}/{total_pages} pages "
                      f"({elapsed:.0f}s elapsed, {pages_with_text} with text)", flush=True)

    doc.close()

    elapsed = time.time() - start_time
    file_size = os.path.getsize(txt_path)

    # Quality assessment
    if total_chars > 10000:
        quality = "完整"
    elif total_chars > 3000:
        quality = "部分"
    elif total_chars > 500:
        quality = "稀少"
    else:
        quality = "失败"

    return {
        'pages': total_pages,
        'pages_with_text': pages_with_text,
        'chars': total_chars,
        'file_size': file_size,
        'elapsed_sec': elapsed,
        'quality': quality,
    }


def get_scanned_pdfs():
    """Identify scanned PDFs by checking existing txt file sizes."""
    pdf_files = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith('.pdf')]
    scanned = []
    for pdf_name in pdf_files:
        txt_name = os.path.splitext(pdf_name)[0] + ".txt"
        txt_path = os.path.join(EXISTING_TXT_DIR, txt_name)
        if not os.path.exists(txt_path):
            scanned.append(pdf_name)
            continue
        size_kb = os.path.getsize(txt_path) / 1024
        if size_kb < SCANNED_THRESHOLD_KB:
            scanned.append(pdf_name)
    return scanned


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Determine which files to process
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == '--test':
            # Test mode: only 海龟交易法则
            target_files = [f for f in os.listdir(SOURCE_DIR)
                           if f.lower().endswith('.pdf') and '海龟' in f]
        else:
            target_files = [arg]
    else:
        target_files = get_scanned_pdfs()

    if not target_files:
        print("No PDFs to process.")
        return

    print(f"{'=' * 60}")
    print(f"OCR Processing: {len(target_files)} PDF(s)")
    print(f"Output dir: {OUTPUT_DIR}")
    print(f"{'=' * 60}")

    # Initialize PaddleOCR (load model once)
    print("\nInitializing PaddleOCR (first run downloads ~100MB model)...")
    ocr_engine = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
    print("PaddleOCR ready.\n")

    results = []
    for idx, pdf_name in enumerate(target_files, 1):
        pdf_path = os.path.join(SOURCE_DIR, pdf_name)
        txt_name = os.path.splitext(pdf_name)[0] + ".txt"
        txt_path = os.path.join(OUTPUT_DIR, txt_name)

        # Skip if already processed and has content
        if os.path.exists(txt_path) and os.path.getsize(txt_path) > 5000:
            existing_chars = 0
            with open(txt_path, 'r', encoding='utf-8') as f:
                existing_chars = len(f.read())
            if existing_chars > 3000:
                print(f"[{idx}/{len(target_files)}] SKIP (already OCR'd): {pdf_name}")
                results.append({
                    'name': pdf_name,
                    'status': 'skipped',
                    'chars': existing_chars,
                    'file_size': os.path.getsize(txt_path),
                })
                continue

        print(f"\n[{idx}/{len(target_files)}] Processing: {pdf_name}")
        try:
            stats = ocr_pdf(pdf_path, ocr_engine, txt_path)
            stats['name'] = pdf_name
            stats['status'] = 'done'
            results.append(stats)
            print(f"  => {stats['quality']} | {stats['chars']} chars | "
                  f"{stats['file_size'] / 1024:.1f} KB | {stats['elapsed_sec']:.0f}s")
        except Exception as e:
            print(f"  ERROR: {e}")
            results.append({
                'name': pdf_name,
                'status': 'error',
                'error': str(e),
            })

    # ── Summary report ─────────────────────────────────
    print(f"\n{'=' * 60}")
    print("OCR RESULTS SUMMARY")
    print(f"{'=' * 60}")
    print(f"{'Book':<45} {'Status':<8} {'Chars':>8} {'SizeKB':>8} {'Quality':<8}")
    print(f"{'-' * 45} {'-' * 8} {'-' * 8} {'-' * 8} {'-' * 8}")

    for r in results:
        name = r['name'][:43]
        status = r.get('status', '?')
        chars = r.get('chars', 0)
        size_kb = r.get('file_size', 0) / 1024 if r.get('file_size') else 0
        quality = r.get('quality', '-')
        print(f"{name:<45} {status:<8} {chars:>8} {size_kb:>8.1f} {quality:<8}")

    total_done = sum(1 for r in results if r.get('status') == 'done')
    total_skip = sum(1 for r in results if r.get('status') == 'skipped')
    total_err = sum(1 for r in results if r.get('status') == 'error')
    print(f"\nDone: {total_done} | Skipped: {total_skip} | Errors: {total_err}")


if __name__ == "__main__":
    main()
