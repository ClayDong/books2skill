#!/usr/bin/env python3
"""
Advanced OCR processor with parallel processing and caching
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import fitz  # PyMuPDF
import numpy as np
from PIL import Image
from paddleocr import PaddleOCR
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table

from cangjie.config import settings
from cangjie.utils.logging import get_logger

logger = get_logger("ocr_processor")
console = Console()


class OCRProcessor:
    """Advanced OCR processor with parallel processing"""

    def __init__(
        self,
        use_gpu: bool = False,
        max_workers: Optional[int] = None,
        dpi: int = 200,
        lang: str = "ch",
    ):
        """
        Initialize OCR processor

        Args:
            use_gpu: Whether to use GPU acceleration
            max_workers: Maximum number of parallel workers
            dpi: DPI for PDF rendering
            lang: Language for OCR
        """
        self.use_gpu = use_gpu or settings.OCR_USE_GPU
        self.max_workers = max_workers or min(settings.MAX_WORKERS, multiprocessing.cpu_count())
        self.dpi = dpi or settings.OCR_DPI
        self.lang = lang or settings.OCR_LANG

        # Watermark patterns to remove
        self.watermark_patterns = [
            # Common watermarks
            r'白云居', r'baiyunju\.cc', r'baiyunju',
            r'股窜网', r'gucuan\.com', r'gucuan',
            r'55188\.com', r'55188', r'理想在线证券网', r'理想在线',
            r'老庄易财经博客', r'老庄易', r'laozhuangyi\.cn', r'laozhuangyi',
            r'挥剑斩浮云',
            r'7help\.net', r'7help',
            r'全国最低交易手续费.*', r'零佣金.*', r'期货开户和书籍下载.*',
            r'客服QQ.*', r'客服微信.*',
            r'lunarora\.com', r'lunarora',
            # Broken watermark fragments
            r'『.*?整理', r'』.*?整理', r'丨https?://.*整理',
            r'^『\s*$', r'^』\s*$', r'^丨https?://\s*$',
            r'^整理\s*$', r'^https?://\s*$',
            # Page numbers
            r'^\s*\d+\s*$',
        ]

        # Initialize OCR engine
        logger.info(f"Initializing PaddleOCR (GPU: {self.use_gpu}, Lang: {self.lang})")
        self.ocr_engine = PaddleOCR(
            use_angle_cls=settings.OCR_USE_ANGLE_CLS,
            lang=self.lang,
            use_gpu=self.use_gpu,
            show_log=False,
        )
        logger.info("PaddleOCR initialized successfully")

    def render_page_to_image(self, page) -> np.ndarray:
        """Render a PDF page to numpy array"""
        mat = fitz.Matrix(self.dpi / 72, self.dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        img_data = pix.tobytes("png")
        import io
        img = Image.open(io.BytesIO(img_data))
        return np.array(img)

    def clean_text(self, text: str) -> str:
        """Remove watermarks and clean up text"""
        import re
        watermark_regex = re.compile('|'.join(self.watermark_patterns), re.IGNORECASE)

        lines = text.split('\n')
        cleaned = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            # Skip lines that are entirely watermark
            if watermark_regex.search(stripped):
                remaining = watermark_regex.sub('', stripped).strip()
                if remaining:
                    cleaned.append(remaining)
                continue

            cleaned.append(stripped)

        return '\n'.join(cleaned)

    def process_page(self, page_data: Tuple[int, fitz.Page]) -> Tuple[int, str]:
        """Process a single page"""
        page_num, page = page_data
        try:
            img_array = self.render_page_to_image(page)
            result = self.ocr_engine.ocr(img_array, cls=True)

            page_text = []
            if result and result[0]:
                for line in result[0]:
                    if line and len(line) >= 2:
                        text_info = line[1]  # (text, confidence)
                        if isinstance(text_info, tuple) and len(text_info) >= 1:
                            page_text.append(text_info[0])

            raw_text = '\n'.join(page_text)
            cleaned = self.clean_text(raw_text)

            return page_num, cleaned

        except Exception as e:
            logger.error(f"Error processing page {page_num}: {e}")
            return page_num, f"[OCR ERROR: {e}]"

    def process_pdf(self, pdf_path: Path, output_path: Path) -> Dict:
        """Process a single PDF file with parallel page processing"""
        logger.info(f"Processing PDF: {pdf_path.name}")

        start_time = sys.maxsize
        doc = fitz.open(pdf_path)
        total_pages = len(doc)

        # Prepare page data
        page_data = [(i, doc[i]) for i in range(total_pages)]

        # Process pages in parallel
        results = []
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all pages
            future_to_page = {
                executor.submit(self.process_page, data): data[0]
                for data in page_data
            }

            # Collect results as they complete
            for future in as_completed(future_to_page):
                page_num, text = future.result()
                results.append((page_num, text))

        # Sort results by page number
        results.sort(key=lambda x: x[0])

        # Write to file
        with open(output_path, "w", encoding="utf-8") as f:
            for page_num, text in results:
                f.write(f"\n=== 第 {page_num + 1} 页 ===\n{text}\n")

        doc.close()

        # Calculate statistics
        total_chars = sum(len(text) for _, text in results)
        elapsed_time = sys.maxsize - start_time

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
            "success": True,
            "pdf_path": pdf_path,
            "output_path": output_path,
            "pages": total_pages,
            "chars": total_chars,
            "quality": quality,
            "time_taken": elapsed_time,
        }

    def batch_process(self, pdf_paths: List[Path], output_dir: Path) -> List[Dict]:
        """Process multiple PDF files in batch"""
        results = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Processing PDFs...", total=len(pdf_paths))

            for pdf_path in pdf_paths:
                progress.update(task, description=f"Processing {pdf_path.name}")

                # Determine output path
                output_path = output_dir / f"{pdf_path.stem}.txt"

                # Skip if already processed and has content
                if output_path.exists() and output_path.stat().st_size > 5000:
                    with open(output_path, "r", encoding="utf-8") as f:
                        existing_chars = len(f.read())

                    if existing_chars > 3000:
                        progress.update(task, advance=1, description=f"Skipping {pdf_path.name}")
                        results.append({
                            "success": True,
                            "pdf_path": pdf_path,
                            "output_path": output_path,
                            "status": "skipped",
                            "chars": existing_chars,
                            "quality": "existing",
                        })
                        continue

                # Process PDF
                try:
                    result = self.process_pdf(pdf_path, output_path)
                    results.append(result)
                    logger.info(f"Processed {pdf_path.name}: {result['pages']} pages, {result['chars']} chars")

                except Exception as e:
                    logger.error(f"Failed to process {pdf_path.name}: {e}")
                    results.append({
                        "success": False,
                        "pdf_path": pdf_path,
                        "error": str(e),
                        "status": "failed",
                    })

                progress.update(task, advance=1)

        return results


def get_scanned_pdfs(source_dir: Path, existing_txt_dir: Path, threshold_kb: int = 100) -> List[Path]:
    """Identify scanned PDFs by checking existing txt file sizes"""
    pdf_files = list(source_dir.glob("*.pdf"))
    scanned = []

    for pdf_path in pdf_files:
        txt_path = existing_txt_dir / f"{pdf_path.stem}.txt"

        if not txt_path.exists():
            scanned.append(pdf_path)
            continue

        size_kb = txt_path.stat().st_size / 1024
        if size_kb < threshold_kb:
            scanned.append(pdf_path)

    return scanned


def display_results(results: List[Dict]):
    """Display OCR processing results in a table"""
    table = Table(title="OCR Processing Results")
    table.add_column("PDF File", style="cyan", no_wrap=True)
    table.add_column("Status", style="magenta")
    table.add_column("Pages", justify="right")
    table.add_column("Chars", justify="right")
    table.add_column("Quality", style="green")
    table.add_column("Time", justify="right")

    total_chars = 0
    total_pages = 0
    successful = 0
    failed = 0
    skipped = 0

    for result in results:
        if result.get("status") == "skipped":
            status = "SKIPPED"
            skipped += 1
        elif result.get("success"):
            status = "SUCCESS"
            successful += 1
        else:
            status = "FAILED"
            failed += 1

        pages = result.get("pages", 0)
        chars = result.get("chars", 0)
        quality = result.get("quality", "-")
        time_taken = result.get("time_taken", 0)

        total_pages += pages
        total_chars += chars

        table.add_row(
            Path(result["pdf_path"]).name[:30],
            status,
            str(pages),
            str(chars),
            quality,
            f"{time_taken:.1f}s" if time_taken > 0 else "-"
        )

    console.print(table)

    # Summary
    console.print(f"\n[bold]Summary:[/bold]")
    console.print(f"  Total PDFs: {len(results)}")
    console.print(f"  Successful: [green]{successful}[/green]")
    console.print(f"  Skipped: [yellow]{skipped}[/yellow]")
    console.print(f"  Failed: [red]{failed}[/red]")
    console.print(f"  Total pages processed: {total_pages}")
    console.print(f"  Total characters extracted: {total_chars}")


def main():
    """Main OCR processing function"""
    console.print("[bold blue]Starting OCR Processing...[/bold blue]")

    # Setup directories
    source_dir = settings.BOOKS_RAW_DIR
    output_dir = settings.BOOKS_TXT_OCR_DIR
    existing_txt_dir = settings.BOOKS_TXT_DIR

    output_dir.mkdir(parents=True, exist_ok=True)

    # Get PDFs to process
    pdf_paths = get_scanned_pdfs(source_dir, existing_txt_dir, threshold_kb=100)

    if not pdf_paths:
        console.print(f"[yellow]No scanned PDFs found in {source_dir}[/yellow]")
        console.print("Scanned PDFs are those with small or no existing text extraction.")
        return

    console.print(f"Found {len(pdf_paths)} scanned PDFs to process")

    # Initialize processor
    processor = OCRProcessor(
        use_gpu=settings.OCR_USE_GPU,
        max_workers=settings.MAX_WORKERS,
        dpi=settings.OCR_DPI,
        lang=settings.OCR_LANG,
    )

    # Process PDFs
    results = processor.batch_process(pdf_paths, output_dir)

    # Display results
    display_results(results)

    # Save results to file
    import json
    results_file = output_dir / "ocr_results.json"
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump([
            {
                "pdf_path": str(r["pdf_path"]),
                "output_path": str(r.get("output_path", "")),
                "status": r.get("status", "unknown"),
                "pages": r.get("pages", 0),
                "chars": r.get("chars", 0),
                "quality": r.get("quality", ""),
                "success": r.get("success", False),
            }
            for r in results
        ], f, indent=2, ensure_ascii=False)

    console.print(f"\n[green]OCR processing completed![/green]")
    console.print(f"  Results saved to: {results_file}")
    console.print(f"  Output directory: {output_dir}")


if __name__ == "__main__":
    main()
