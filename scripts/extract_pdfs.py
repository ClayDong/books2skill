#!/usr/bin/env python3
"""
Batch extract text from all PDF books using pdfplumber
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pdfplumber
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

from books2skill.config import settings
from books2skill.utils.logging import get_logger

logger = get_logger("extract_pdfs")
console = Console()

SOURCE_DIR = settings.BOOKS_RAW_DIR
OUTPUT_DIR = settings.BOOKS_TXT_DIR

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_pdf(pdf_path: Path, txt_path: Path) -> dict:
    """Extract text from a single PDF file"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            text_parts = []

            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    text = page.extract_text() or ""
                    text_parts.append(f"\n=== 第 {page_num} 页 ===\n{text}")
                except Exception as e:
                    text_parts.append(f"\n=== 第 {page_num} 页 ===\n[EXTRACT ERROR: {e}]")

            full_text = "\n".join(text_parts)

            # Save to file
            txt_path.write_text(full_text, encoding="utf-8")

            return {
                "success": True,
                "pages": total_pages,
                "chars": len(full_text),
                "path": txt_path,
            }

    except Exception as e:
        logger.error(f"Failed to extract {pdf_path.name}: {e}")
        return {
            "success": False,
            "error": str(e),
            "path": pdf_path,
        }

def main():
    """Main extraction function"""
    console.print("[bold blue]Starting PDF text extraction...[/bold blue]")

    # Find PDF files
    pdf_files = list(SOURCE_DIR.glob("*.pdf"))
    if not pdf_files:
        console.print(f"[yellow]No PDF files found in {SOURCE_DIR}[/yellow]")
        return

    console.print(f"Found {len(pdf_files)} PDF files in {SOURCE_DIR}")

    # Track results
    results = []
    skipped = 0
    failed = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Extracting PDFs...", total=len(pdf_files))

        for pdf_path in pdf_files:
            txt_name = pdf_path.stem + ".txt"
            txt_path = OUTPUT_DIR / txt_name

            # Skip if already extracted and has content
            if txt_path.exists() and txt_path.stat().st_size > 1000:
                skipped += 1
                progress.update(task, advance=1, description=f"Skipping {pdf_path.name}")
                continue

            progress.update(task, description=f"Extracting {pdf_path.name}")

            # Extract PDF
            result = extract_pdf(pdf_path, txt_path)
            results.append(result)

            if result["success"]:
                logger.info(f"Extracted {pdf_path.name}: {result['pages']} pages, {result['chars']} chars")
            else:
                failed += 1
                logger.error(f"Failed to extract {pdf_path.name}: {result['error']}")

            progress.update(task, advance=1)

    # Summary
    console.print(f"\n[bold]Extraction Summary:[/bold]")
    console.print(f"  Total PDFs: {len(pdf_files)}")
    console.print(f"  Successfully extracted: {len(pdf_files) - skipped - failed}")
    console.print(f"  Skipped (already extracted): {skipped}")
    console.print(f"  Failed: {failed}")

    if failed > 0:
        console.print(f"\n[yellow]Some PDFs failed to extract. Check logs for details.[/yellow]")

    console.print(f"\n[green]Extraction completed![/green]")
    console.print(f"  Output directory: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
