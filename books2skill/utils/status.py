"""
System status utilities for Books2Skill
"""

import platform
import sys
from pathlib import Path
from typing import Dict, Any, List
import importlib.metadata

from books2skill.config import settings
from books2skill.utils.logging import get_logger

logger = get_logger("status")


def get_system_status() -> Dict[str, Any]:
    """
    Get comprehensive system status

    Returns:
        Dictionary with system status information
    """
    status = {
        "version": get_version(),
        "python_version": get_python_version(),
        "platform": get_platform_info(),
        "directories": get_directory_status(),
        "dependencies": get_dependency_status(),
        "books_distilled": get_books_distilled(),
        "total_skills": get_total_skills(),
        "conflicts_identified": get_conflicts_identified(),
        "health": "healthy",  # Will be updated based on checks
    }

    # Update health status based on checks
    status["health"] = assess_health(status)

    return status


def get_version() -> str:
    """Get Books2Skill version"""
    try:
        # Try to get version from package metadata
        return importlib.metadata.version("books2skill")
    except importlib.metadata.PackageNotFoundError:
        # Fallback to hardcoded version
        return "2.0.0"


def get_python_version() -> str:
    """Get Python version information"""
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def get_platform_info() -> Dict[str, str]:
    """Get platform information"""
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_implementation": platform.python_implementation(),
    }


def get_directory_status() -> Dict[str, Path]:
    """Get status of important directories"""
    directories = {
        "project_root": settings.PROJECT_ROOT,
        "books_raw": settings.BOOKS_RAW_DIR,
        "books_txt": settings.BOOKS_TXT_DIR,
        "books_txt_ocr": settings.BOOKS_TXT_OCR_DIR,
        "library": settings.LIBRARY_DIR,
        "output": settings.OUTPUT_DIR,
        "logs": settings.LOG_FILE.parent,
    }

    return directories


def get_dependency_status() -> Dict[str, str]:
    """Get status of dependencies"""
    dependencies = {}

    # Core dependencies
    core_deps = [
        "click",
        "rich",
        "tqdm",
        "pydantic",
        "python-dotenv",
        "pdfplumber",
        "pymupdf",
        "paddleocr",
        "numpy",
        "pillow",
        "pandas",
    ]

    for dep in core_deps:
        try:
            version = importlib.metadata.version(dep)
            dependencies[dep] = version
        except importlib.metadata.PackageNotFoundError:
            dependencies[dep] = "not installed"

    return dependencies


def get_books_distilled() -> int:
    """Get number of books distilled"""
    try:
        # Check library directory for distilled books
        library_dir = settings.LIBRARY_DIR

        if not library_dir.exists():
            return 0

        # Count directories that look like book distillations
        book_dirs = []
        for item in library_dir.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                # Check if it has an INDEX.md file (indicator of distillation)
                index_file = item / "INDEX.md"
                if index_file.exists():
                    book_dirs.append(item)

        return len(book_dirs)

    except Exception as e:
        logger.warning(f"Failed to count distilled books: {e}")
        return 0


def get_total_skills() -> int:
    """Get total number of skills"""
    try:
        library_dir = settings.LIBRARY_DIR

        if not library_dir.exists():
            return 0

        skill_count = 0

        # Recursively count SKILL.md files
        for skill_md in library_dir.rglob("SKILL.md"):
            # Skip if in rejected or candidates directories
            if "rejected" in str(skill_md) or "candidates" in str(skill_md):
                continue

            skill_count += 1

        return skill_count

    except Exception as e:
        logger.warning(f"Failed to count skills: {e}")
        return 0


def get_conflicts_identified() -> int:
    """Get number of conflicts identified"""
    try:
        conflicts_file = settings.LIBRARY_DIR / "CONFLICTS.md"

        if not conflicts_file.exists():
            return 0

        content = conflicts_file.read_text(encoding="utf-8")

        # Count conflict entries (simple heuristic)
        import re
        conflict_matches = re.findall(r'conflict_id:\s*C\d+', content)
        return len(set(conflict_matches))

    except Exception as e:
        logger.warning(f"Failed to count conflicts: {e}")
        return 0


def assess_health(status: Dict[str, Any]) -> str:
    """
    Assess system health based on status

    Args:
        status: System status dictionary

    Returns:
        Health status: "healthy", "warning", or "error"
    """
    issues = []

    # Check directories
    directories = status.get("directories", {})
    for name, path in directories.items():
        if not path.exists():
            issues.append(f"Directory not found: {name} ({path})")

    # Check dependencies
    dependencies = status.get("dependencies", {})
    missing_deps = [dep for dep, version in dependencies.items() if version == "not installed"]

    if missing_deps:
        issues.append(f"Missing dependencies: {', '.join(missing_deps)}")

    # Check if any books have been distilled
    books_distilled = status.get("books_distilled", 0)
    if books_distilled == 0:
        issues.append("No books have been distilled yet")

    # Determine health status
    if any("not installed" in issue for issue in issues):
        return "error"
    elif issues:
        return "warning"
    else:
        return "healthy"


def get_detailed_status() -> Dict[str, Any]:
    """
    Get detailed system status with additional information

    Returns:
        Detailed status dictionary
    """
    basic_status = get_system_status()

    # Add additional details
    detailed_status = {
        **basic_status,
        "system_resources": get_system_resources(),
        "performance_metrics": get_performance_metrics(),
        "recent_activity": get_recent_activity(),
        "configuration_summary": get_configuration_summary(),
    }

    return detailed_status


def get_system_resources() -> Dict[str, Any]:
    """Get system resource information"""
    import psutil

    try:
        return {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage(str(settings.PROJECT_ROOT)).percent,
            "process_memory_mb": psutil.Process().memory_info().rss / 1024 / 1024,
        }
    except ImportError:
        return {"error": "psutil not installed"}
    except Exception as e:
        return {"error": str(e)}


def get_performance_metrics() -> Dict[str, Any]:
    """Get performance metrics (placeholder)"""
    # In a real implementation, this would track actual performance metrics
    return {
        "average_distillation_time": None,
        "skills_per_hour": None,
        "ocr_speed_pages_per_minute": None,
        "validation_success_rate": None,
    }


def get_recent_activity() -> List[Dict[str, Any]]:
    """Get recent activity (placeholder)"""
    # In a real implementation, this would read from logs or activity tracking
    return [
        {
            "timestamp": "2026-06-22 10:00:00",
            "activity": "System started",
            "details": "Books2Skill initialized",
        }
    ]


def get_configuration_summary() -> Dict[str, Any]:
    """Get configuration summary"""
    return {
        "ocr_enabled": not settings.SKIP_VALIDATION,
        "validation_strict": settings.VALIDATION_STRICT,
        "fast_mode": settings.FAST_MODE,
        "debug_mode": settings.DEBUG,
        "max_workers": settings.MAX_WORKERS,
        "cache_enabled": settings.CACHE_ENABLED,
    }


def print_status_summary() -> None:
    """Print status summary to console"""
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel

    console = Console()
    status = get_system_status()

    # Create main table
    table = Table(title="Books2Skill System Status", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")

    # Add basic info
    table.add_row("Version", status["version"])
    table.add_row("Python", status["python_version"])
    table.add_row("Platform", f"{status['platform']['system']} {status['platform']['release']}")

    # Add project metrics
    table.add_row("Books distilled", str(status["books_distilled"]))
    table.add_row("Total skills", str(status["total_skills"]))
    table.add_row("Conflicts identified", str(status["conflicts_identified"]))

    # Add health status with color
    health = status["health"]
    if health == "healthy":
        health_display = f"[green]{health}[/green]"
    elif health == "warning":
        health_display = f"[yellow]{health}[/yellow]"
    else:
        health_display = f"[red]{health}[/red]"

    table.add_row("Health", health_display)

    console.print(table)

    # Show directory status
    dir_table = Table(title="Directory Status", show_header=True, header_style="bold blue")
    dir_table.add_column("Directory", style="cyan")
    dir_table.add_column("Path", style="white")
    dir_table.add_column("Status", style="green")

    directories = status["directories"]
    for name, path in directories.items():
        exists = path.exists()
        status_icon = "✓" if exists else "✗"
        status_color = "green" if exists else "red"
        dir_table.add_row(name, str(path), f"[{status_color}]{status_icon}[/{status_color}]")

    console.print(dir_table)

    # Show dependency status
    dep_table = Table(title="Core Dependencies", show_header=True, header_style="bold yellow")
    dep_table.add_column("Dependency", style="cyan")
    dep_table.add_column("Version", style="white")

    dependencies = status["dependencies"]
    for dep, version in sorted(dependencies.items()):
        if version == "not installed":
            dep_table.add_row(dep, f"[red]{version}[/red]")
        else:
            dep_table.add_row(dep, f"[green]{version}[/green]")

    console.print(dep_table)

    # Show issues if any
    if health != "healthy":
        console.print(Panel(
            "[yellow]⚠️  System has issues that need attention[/yellow]",
            title="Health Issues",
            border_style="yellow",
        ))


if __name__ == "__main__":
    print_status_summary()
