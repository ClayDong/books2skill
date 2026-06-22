#!/usr/bin/env python3
"""
Installation script for Cangjie Skill
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.panel import Panel

console = Console()


def check_python_version() -> bool:
    """Check Python version requirements"""
    import sys

    required_version = (3, 8)
    current_version = sys.version_info[:2]

    if current_version < required_version:
        console.print(
            f"[red]❌ Python {required_version[0]}.{required_version[1]}+ required. "
            f"Found {current_version[0]}.{current_version[1]}[/red]"
        )
        return False

    console.print(f"[green]✓ Python {current_version[0]}.{current_version[1]} detected[/green]")
    return True


def check_dependencies() -> Dict[str, bool]:
    """Check if required dependencies are available"""
    import importlib.util

    dependencies = {
        "pip": False,
        "venv": False,
        "git": False,
    }

    # Check pip
    pip_spec = importlib.util.find_spec("pip")
    dependencies["pip"] = pip_spec is not None

    # Check venv
    venv_spec = importlib.util.find_spec("venv")
    dependencies["venv"] = venv_spec is not None

    # Check git (external command)
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        dependencies["git"] = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        dependencies["git"] = False

    return dependencies


def create_virtual_environment(venv_path: Path) -> bool:
    """Create virtual environment"""
    console.print(f"[blue]Creating virtual environment at {venv_path}[/blue]")

    try:
        import venv as venv_module

        builder = venv_module.EnvBuilder(with_pip=True)
        builder.create(venv_path)

        console.print("[green]✓ Virtual environment created[/green]")
        return True

    except Exception as e:
        console.print(f"[red]❌ Failed to create virtual environment: {e}[/red]")
        return False


def install_dependencies(venv_path: Optional[Path] = None) -> bool:
    """Install dependencies"""
    console.print("[blue]Installing dependencies...[/blue]")

    pip_cmd = [sys.executable, "-m", "pip", "install", "-e", "."]

    if venv_path:
        # Use venv's python if available
        venv_python = venv_path / "bin" / "python"
        if not venv_python.exists():
            venv_python = venv_path / "Scripts" / "python.exe"

        if venv_python.exists():
            pip_cmd = [str(venv_python), "-m", "pip", "install", "-e", "."]

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Installing...", total=None)

            result = subprocess.run(
                pip_cmd,
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent,
            )

            progress.update(task, completed=True)

            if result.returncode == 0:
                console.print("[green]✓ Dependencies installed successfully[/green]")
                return True
            else:
                console.print(f"[red]❌ Failed to install dependencies[/red]")
                console.print(f"Error: {result.stderr}")
                return False

    except Exception as e:
        console.print(f"[red]❌ Installation failed: {e}[/red]")
        return False


def setup_pre_commit() -> bool:
    """Setup pre-commit hooks"""
    console.print("[blue]Setting up pre-commit hooks...[/blue]")

    try:
        # Install pre-commit
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "pre-commit"],
            capture_output=True,
            check=True,
        )

        # Install hooks
        result = subprocess.run(
            ["pre-commit", "install"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        if result.returncode == 0:
            console.print("[green]✓ Pre-commit hooks installed[/green]")
            return True
        else:
            console.print(f"[yellow]⚠ Pre-commit installation failed: {result.stderr}[/yellow]")
            return False

    except Exception as e:
        console.print(f"[yellow]⚠ Pre-commit setup failed: {e}[/yellow]")
        return False


def create_config_files() -> bool:
    """Create configuration files"""
    console.print("[blue]Creating configuration files...[/blue]")

    project_root = Path(__file__).parent.parent

    # Create .env from .env.example
    env_example = project_root / ".env.example"
    env_file = project_root / ".env"

    if env_example.exists() and not env_file.exists():
        try:
            import shutil
            shutil.copy2(env_example, env_file)
            console.print("[green]✓ Created .env file from template[/green]")
        except Exception as e:
            console.print(f"[yellow]⚠ Failed to create .env: {e}[/yellow]")

    # Create logs directory
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)

    # Create data directories
    data_dirs = [
        project_root / "data",
        project_root / "data" / "books_raw",
        project_root / "data" / "books_txt",
        project_root / "data" / "books_txt_ocr",
        project_root / "data" / "library",
        project_root / "data" / "output",
    ]

    for dir_path in data_dirs:
        dir_path.mkdir(parents=True, exist_ok=True)

    console.print("[green]✓ Configuration files and directories created[/green]")
    return True


def run_tests() -> bool:
    """Run basic tests"""
    console.print("[blue]Running basic tests...[/blue]")

    try:
        test_script = Path(__file__).parent.parent / "tests" / "test_basic.py"

        if not test_script.exists():
            console.print("[yellow]⚠ Test script not found, skipping tests[/yellow]")
            return True

        result = subprocess.run(
            [sys.executable, str(test_script)],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        if result.returncode == 0:
            console.print("[green]✓ Basic tests passed[/green]")
            return True
        else:
            console.print(f"[yellow]⚠ Tests failed: {result.stderr}[/yellow]")
            return False

    except Exception as e:
        console.print(f"[yellow]⚠ Test execution failed: {e}[/yellow]")
        return False


def print_success_message(venv_path: Optional[Path] = None) -> None:
    """Print success message with next steps"""
    console.print(Panel(
        "[bold green]✅ Cangjie Skill installation completed successfully![/bold green]",
        title="Installation Complete",
        border_style="green",
    ))

    console.print("\n[bold]Next steps:[/bold]")

    if venv_path:
        activate_cmd = "source venv/bin/activate" if sys.platform != "win32" else "venv\\Scripts\\activate"
        console.print(f"  1. Activate virtual environment:")
        console.print(f"     [cyan]{activate_cmd}[/cyan]")

    console.print("  2. Configure your environment:")
    console.print("     [cyan]Edit .env file to customize settings[/cyan]")

    console.print("  3. Try it out:")
    console.print("     [cyan]cangjie --help[/cyan] - Show all commands")
    console.print("     [cyan]cangjie status[/cyan] - Check system status")

    console.print("  4. Get started with a book:")
    console.print("     [cyan]cangjie distill path/to/book.pdf[/cyan]")

    console.print("\n[bold]Documentation:[/bold]")
    console.print("  - README.md - Getting started guide")
    console.print("  - SKILL.md - Detailed methodology")
    console.print("  - methodology/ - Stage-by-stage guides")

    console.print("\n[bold]Need help?[/bold]")
    console.print("  - Check the logs in logs/ directory")
    console.print("  - Review the configuration in .env file")
    console.print("  - Run validation: [cyan]cangjie validate[/cyan]")


def main():
    """Main installation function"""
    console.print(Panel(
        "[bold blue]Cangjie Skill Installation[/bold blue]",
        subtitle="Turning books into reusable AI skills",
        border_style="blue",
    ))

    # Parse arguments
    import argparse
    parser = argparse.ArgumentParser(description="Install Cangjie Skill")
    parser.add_argument("--venv", type=Path, help="Path for virtual environment")
    parser.add_argument("--no-venv", action="store_true", help="Skip virtual environment creation")
    parser.add_argument("--skip-tests", action="store_true", help="Skip running tests")
    parser.add_argument("--skip-pre-commit", action="store_true", help="Skip pre-commit setup")

    args = parser.parse_args()

    # Step 1: Check Python version
    console.print("\n[bold]Step 1: Checking Python version[/bold]")
    if not check_python_version():
        sys.exit(1)

    # Step 2: Check dependencies
    console.print("\n[bold]Step 2: Checking dependencies[/bold]")
    deps = check_dependencies()

    for dep, available in deps.items():
        if available:
            console.print(f"  [green]✓ {dep}[/green]")
        else:
            console.print(f"  [yellow]⚠ {dep} not found[/yellow]")

    # Step 3: Create virtual environment (optional)
    venv_path = None
    if not args.no_venv:
        console.print("\n[bold]Step 3: Setting up virtual environment[/bold]")
        if args.venv:
            venv_path = args.venv
        else:
            venv_path = Path(__file__).parent.parent / "venv"

        if venv_path.exists():
            console.print(f"[yellow]⚠ Virtual environment already exists at {venv_path}[/yellow]")
            use_existing = input("Use existing? (y/n): ").lower().strip()
            if use_existing != 'y':
                console.print("[yellow]⚠ Please remove or specify different path[/yellow]")
                sys.exit(1)
        else:
            if not create_virtual_environment(venv_path):
                console.print("[yellow]⚠ Virtual environment creation failed[/yellow]")
                sys.exit(1)

    # Step 4: Install dependencies
    console.print("\n[bold]Step 4: Installing dependencies[/bold]")
    if not install_dependencies(venv_path):
        console.print("[red]❌ Dependency installation failed[/red]")
        sys.exit(1)

    # Step 5: Setup pre-commit (optional)
    if not args.skip_pre_commit:
        console.print("\n[bold]Step 5: Setting up development tools[/bold]")
        setup_pre_commit()

    # Step 6: Create config files
    console.print("\n[bold]Step 6: Creating configuration[/bold]")
    create_config_files()

    # Step 7: Run tests (optional)
    if not args.skip_tests:
        console.print("\n[bold]Step 7: Running tests[/bold]")
        run_tests()

    # Success!
    print_success_message(venv_path)


if __name__ == "__main__":
    main()
