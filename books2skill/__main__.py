#!/usr/bin/env python3
"""
Books2Skill - Main Entry Point
A generator workflow for turning books into reusable AI skills
"""

import sys
import logging
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from books2skill.config import settings
from books2skill.utils.logging import setup_logging

# Initialize console
console = Console()

# Setup logging
logger = setup_logging()

@click.group()
@click.version_option(version="2.0.0", prog_name="Books2Skill")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option("--debug", "-d", is_flag=True, help="Enable debug mode")
@click.option("--config", "-c", type=click.Path(exists=True), help="Path to config file")
@click.pass_context
def cli(ctx, verbose, debug, config):
    """Books2Skill - Turn books into reusable AI skills"""
    # Store context
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["debug"] = debug
    ctx.obj["config"] = config

    # Update settings
    if config:
        settings.load_config(config)
    if debug:
        settings.DEBUG = True
        logger.setLevel(logging.DEBUG)
    elif verbose:
        logger.setLevel(logging.INFO)

    logger.debug(f"Books2Skill started with config: {config}")

@cli.command()
@click.argument("book_path", type=click.Path(exists=True))
@click.option("--output-dir", "-o", type=click.Path(), help="Output directory")
@click.option("--skip-ocr", is_flag=True, help="Skip OCR processing")
@click.option("--skip-validation", is_flag=True, help="Skip validation")
@click.option("--fast", is_flag=True, help="Fast mode (skip some checks)")
@click.pass_context
def distill(ctx, book_path, output_dir, skip_ocr, skip_validation, fast):
    """Distill a book into skills (RIA-TV++ stages 0-4)"""
    from books2skill.pipeline.distill import run_distillation

    console.print("[bold blue]Starting book distillation...[/bold blue]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Distilling book...", total=None)

        try:
            result = run_distillation(
                book_path=book_path,
                output_dir=output_dir,
                skip_ocr=skip_ocr,
                skip_validation=skip_validation,
                fast_mode=fast,
                progress=progress,
                task_id=task,
            )

            progress.update(task, completed=True, visible=False)

            if result["success"]:
                console.print(f"[bold green]✓ Distillation completed successfully![/bold green]")
                console.print(f"   Skills created: {result['skills_created']}")
                console.print(f"   Output directory: {result['output_dir']}")
                console.print(f"   Time taken: {result['time_taken']:.2f}s")

                # Show next steps
                console.print("\n[bold]Next steps:[/bold]")
                console.print("  1. Review skills in the output directory")
                console.print("  2. Run validation: books2skill validate")
                console.print("  3. Update global index: books2skill index-update")
            else:
                console.print(f"[bold red]✗ Distillation failed![/bold red]")
                console.print(f"   Error: {result['error']}")
                sys.exit(1)

        except Exception as e:
            logger.exception("Distillation failed")
            console.print(f"[bold red]✗ Distillation failed with error: {str(e)}[/bold red]")
            sys.exit(1)

@cli.command()
@click.argument("intent")
@click.option("--books", "-b", multiple=True, help="Books to consider (default: all)")
@click.option("--output-format", "-f", type=click.Choice(["markdown", "json", "both"]),
              default="markdown", help="Output format")
@click.option("--detailed", "-d", is_flag=True, help="Detailed output with reasoning")
@click.pass_context
def orchestrate(ctx, intent, books, output_format, detailed):
    """Orchestrate multiple books for an intent (stages 5-6)"""
    from books2skill.pipeline.orchestrate import run_orchestration

    console.print("[bold blue]Starting multi-book orchestration...[/bold blue]")

    try:
        result = run_orchestration(
            intent=intent,
            books=list(books) if books else None,
            output_format=output_format,
            detailed=detailed,
        )

        if result["success"]:
            console.print(f"[bold green]✓ Orchestration completed![/bold green]")

            if output_format in ["markdown", "both"]:
                console.print("\n" + "="*60)
                console.print(result["output_markdown"])
                console.print("="*60)

            if output_format in ["json", "both"]:
                import json
                console.print("\n[bold]JSON Output:[/bold]")
                console.print(json.dumps(result["output_json"], indent=2, ensure_ascii=False))

            console.print(f"\n[dim]Time taken: {result['time_taken']:.2f}s[/dim]")
            console.print(f"[dim]Skills used: {len(result['skills_used'])}[/dim]")
            console.print(f"[dim]Conflicts resolved: {result['conflicts_resolved']}[/dim]")

        else:
            console.print(f"[bold red]✗ Orchestration failed![/bold red]")
            console.print(f"   Error: {result['error']}")
            sys.exit(1)

    except Exception as e:
        logger.exception("Orchestration failed")
        console.print(f"[bold red]✗ Orchestration failed with error: {str(e)}[/bold red]")
        sys.exit(1)

@cli.command()
@click.option("--check", "-c", multiple=True, help="Specific checks to run")
@click.option("--fix", "-f", is_flag=True, help="Attempt to fix issues")
@click.option("--strict", "-s", is_flag=True, help="Strict mode (treat warnings as errors)")
@click.pass_context
def validate(ctx, check, fix, strict):
    """Validate system consistency and quality"""
    from books2skill.validation.validate_system import run_validation

    console.print("[bold blue]Running system validation...[/bold blue]")

    checks_to_run = list(check) if check else None

    try:
        results = run_validation(
            checks=checks_to_run,
            fix=fix,
            strict=strict,
        )

        # Display results
        total_checks = len(results)
        passed_checks = sum(1 for r in results if r["status"] == "passed")
        failed_checks = sum(1 for r in results if r["status"] == "failed")
        warning_checks = sum(1 for r in results if r["status"] == "warning")

        console.print(f"\n[bold]Validation Results:[/bold]")
        console.print(f"  Total checks: {total_checks}")
        console.print(f"  Passed: [green]{passed_checks}[/green]")
        console.print(f"  Failed: [red]{failed_checks}[/red]")
        console.print(f"  Warnings: [yellow]{warning_checks}[/yellow]")

        # Show details for failures and warnings
        for result in results:
            if result["status"] == "failed":
                console.print(f"\n[red]✗ {result['check']}[/red]")
                console.print(f"   {result['message']}")
                if "details" in result:
                    for detail in result["details"]:
                        console.print(f"   - {detail}")
            elif result["status"] == "warning":
                console.print(f"\n[yellow]⚠ {result['check']}[/yellow]")
                console.print(f"   {result['message']}")

        if failed_checks > 0:
            console.print(f"\n[bold red]Validation failed with {failed_checks} errors[/bold red]")
            if not fix:
                console.print("Run with --fix to attempt automatic fixes")
            sys.exit(1)
        elif warning_checks > 0 and strict:
            console.print(f"\n[bold yellow]Validation passed with {warning_checks} warnings (strict mode)[/bold yellow]")
            sys.exit(1)
        else:
            console.print(f"\n[bold green]✓ All checks passed![/bold green]")

    except Exception as e:
        logger.exception("Validation failed")
        console.print(f"[bold red]✗ Validation failed with error: {str(e)}[/bold red]")
        sys.exit(1)

@cli.command()
@click.option("--all", "-a", is_flag=True, help="Update all indices")
@click.option("--force", "-f", is_flag=True, help="Force rebuild")
@click.pass_context
def index_update(ctx, all, force):
    """Update global indices (stage 4.5)"""
    from books2skill.library.index_builder import build_global_indices

    console.print("[bold blue]Updating global indices...[/bold blue]")

    try:
        result = build_global_indices(
            rebuild_all=all,
            force=force,
        )

        if result["success"]:
            console.print(f"[bold green]✓ Indices updated successfully![/bold green]")
            console.print(f"   Global index: {result['global_index_path']}")
            console.print(f"   Glossary: {result['glossary_path']}")
            console.print(f"   Conflicts: {result['conflicts_path']}")
            console.print(f"   Skills indexed: {result['skills_indexed']}")
            console.print(f"   Conflicts found: {result['conflicts_found']}")
            console.print(f"   Time taken: {result['time_taken']:.2f}s")
        else:
            console.print(f"[bold red]✗ Index update failed![/bold red]")
            console.print(f"   Error: {result['error']}")
            sys.exit(1)

    except Exception as e:
        logger.exception("Index update failed")
        console.print(f"[bold red]✗ Index update failed with error: {str(e)}[/bold red]")
        sys.exit(1)

@cli.command()
@click.option("--host", "-h", default="127.0.0.1", help="Host to bind to")
@click.option("--port", "-p", default=8000, type=int, help="Port to bind to")
@click.option("--reload", "-r", is_flag=True, help="Enable auto-reload")
@click.pass_context
def serve(ctx, host, port, reload):
    """Start web server (future feature)"""
    console.print("[bold yellow]Web interface is not yet implemented[/bold yellow]")
    console.print("This feature is planned for future releases")
    console.print("\nFor now, please use the CLI commands:")
    console.print("  books2skill distill <book>    - Distill a book")
    console.print("  books2skill orchestrate <intent> - Multi-book orchestration")
    console.print("  books2skill validate         - Validate system")
    console.print("  books2skill index-update     - Update indices")

@cli.command()
@click.argument("pdf_path", type=click.Path(exists=True))
@click.option("--output-dir", "-o", type=click.Path(), help="Output directory")
@click.option("--parallel", "-p", is_flag=True, help="Use parallel processing")
@click.option("--gpu", "-g", is_flag=True, help="Use GPU acceleration")
@click.pass_context
def ocr(ctx, pdf_path, output_dir, parallel, gpu):
    """Extract text from scanned PDF using OCR"""
    from books2skill.ocr.processor import process_pdf_ocr

    console.print("[bold blue]Starting OCR processing...[/bold blue]")

    try:
        result = process_pdf_ocr(
            pdf_path=pdf_path,
            output_dir=output_dir,
            parallel=parallel,
            use_gpu=gpu,
        )

        if result["success"]:
            console.print(f"[bold green]✓ OCR processing completed![/bold green]")
            console.print(f"   Output file: {result['output_path']}")
            console.print(f"   Pages processed: {result['pages_processed']}")
            console.print(f"   Characters extracted: {result['characters_extracted']}")
            console.print(f"   Quality: {result['quality']}")
            console.print(f"   Time taken: {result['time_taken']:.2f}s")
        else:
            console.print(f"[bold red]✗ OCR processing failed![/bold red]")
            console.print(f"   Error: {result['error']}")
            sys.exit(1)

    except Exception as e:
        logger.exception("OCR processing failed")
        console.print(f"[bold red]✗ OCR processing failed with error: {str(e)}[/bold red]")
        sys.exit(1)

@cli.command()
@click.option("--skill-id", "-s", help="Specific skill to test")
@click.option("--all", "-a", is_flag=True, help="Test all skills")
@click.option("--output-dir", "-o", type=click.Path(), help="Output directory for reports")
@click.pass_context
def test(ctx, skill_id, all, output_dir):
    """Run skill tests"""
    from books2skill.testing.runner import run_skill_tests

    console.print("[bold blue]Running skill tests...[/bold blue]")

    try:
        results = run_skill_tests(
            skill_id=skill_id,
            test_all=all,
            output_dir=output_dir,
        )

        # Display summary
        total_tests = len(results)
        passed_tests = sum(1 for r in results if r["status"] == "passed")
        failed_tests = sum(1 for r in results if r["status"] == "failed")

        console.print(f"\n[bold]Test Results:[/bold]")
        console.print(f"  Total tests: {total_tests}")
        console.print(f"  Passed: [green]{passed_tests}[/green]")
        console.print(f"  Failed: [red]{failed_tests}[/red]")

        # Show failed tests
        if failed_tests > 0:
            console.print(f"\n[bold red]Failed tests:[/bold red]")
            for result in results:
                if result["status"] == "failed":
                    console.print(f"\n  [red]✗ {result['skill_id']}[/red]")
                    console.print(f"     Test: {result['test_name']}")
                    console.print(f"     Error: {result['error']}")

        if failed_tests > 0:
            console.print(f"\n[bold red]Testing failed with {failed_tests} failures[/bold red]")
            sys.exit(1)
        else:
            console.print(f"\n[bold green]✓ All tests passed![/bold green]")

    except Exception as e:
        logger.exception("Testing failed")
        console.print(f"[bold red]✗ Testing failed with error: {str(e)}[/bold red]")
        sys.exit(1)

@cli.command()
def status():
    """Show system status"""
    from books2skill.utils.status import get_system_status

    try:
        status_info = get_system_status()

        console.print("[bold blue]Books2Skill System Status[/bold blue]")
        console.print("="*50)

        # Basic info
        console.print(f"\n[bold]Version:[/bold] {status_info['version']}")
        console.print(f"[bold]Python:[/bold] {status_info['python_version']}")
        console.print(f"[bold]Platform:[/bold] {status_info['platform']}")

        # Books and skills
        console.print(f"\n[bold]Books distilled:[/bold] {status_info['books_distilled']}")
        console.print(f"[bold]Total skills:[/bold] {status_info['total_skills']}")
        console.print(f"[bold]Conflicts identified:[/bold] {status_info['conflicts_identified']}")

        # Directories
        console.print(f"\n[bold]Directories:[/bold]")
        for dir_name, dir_path in status_info['directories'].items():
            exists = "✓" if dir_path.exists() else "✗"
            console.print(f"  {exists} {dir_name}: {dir_path}")

        # Dependencies
        console.print(f"\n[bold]Dependencies:[/bold]")
        for dep, version in status_info['dependencies'].items():
            console.print(f"  ✓ {dep}: {version}")

        # Health status
        health = status_info['health']
        if health == "healthy":
            console.print(f"\n[bold green]✓ System is healthy[/bold green]")
        elif health == "warning":
            console.print(f"\n[bold yellow]⚠ System has warnings[/bold yellow]")
        else:
            console.print(f"\n[bold red]✗ System has issues[/bold red]")

    except Exception as e:
        logger.exception("Status check failed")
        console.print(f"[bold red]✗ Status check failed: {str(e)}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    cli()
