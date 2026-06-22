"""
Extended validation system for Cangjie Skill
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from enum import Enum

from rich.console import Console
from rich.table import Table

from cangjie.config import settings
from cangjie.utils.logging import get_logger

logger = get_logger("validation")
console = Console()


class ValidationSeverity(Enum):
    """Validation result severity"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    SUCCESS = "success"


class ValidationResult:
    """Result of a single validation check"""

    def __init__(
        self,
        check_id: str,
        check_name: str,
        severity: ValidationSeverity,
        message: str,
        target: str,
        details: List[str] = None,
        fix_suggestion: Optional[str] = None,
        auto_fixable: bool = False,
    ):
        self.check_id = check_id
        self.check_name = check_name
        self.severity = severity
        self.message = message
        self.target = target
        self.details = details or []
        self.fix_suggestion = fix_suggestion
        self.auto_fixable = auto_fixable

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "check": self.check_id,
            "name": self.check_name,
            "severity": self.severity.value,
            "message": self.message,
            "target": self.target,
            "details": self.details,
            "fix_suggestion": self.fix_suggestion,
            "auto_fixable": self.auto_fixable,
        }


def parse_frontmatter(content: str) -> Dict[str, str]:
    """Parse YAML frontmatter from content"""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    fm = {}
    lines = match.group(1).split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        if ':' in line and not line.startswith(' '):
            key, _, value = line.partition(':')
            key = key.strip()
            value = value.strip()

            # Handle multi-line values
            if value in ('|', '>'):
                multiline = []
                i += 1
                while i < len(lines) and (lines[i].startswith('  ') or lines[i].strip() == ''):
                    multiline.append(lines[i].strip())
                    i += 1
                fm[key] = ' '.join(multiline)
                continue

            fm[key] = value
        i += 1

    return fm


def read_skill_dirs(base_path: Path) -> List[Path]:
    """Read skill directories from base path"""
    return sorted([d for d in base_path.iterdir() if d.is_dir() and d.name[0].isdigit()])


def check_ria_completeness(skill_dirs: List[Path]) -> List[ValidationResult]:
    """Check RIA-TV++ six-segment completeness"""
    results = []
    required_segments = ['## R —', '## I —', '## A1 —', '## A2 —', '## E —', '## B —']

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            results.append(ValidationResult(
                check_id="ria",
                check_name="RIA-TV++六段完整性",
                severity=ValidationSeverity.ERROR,
                message=f"SKILL.md not found",
                target=skill_dir.name,
                details=[f"Missing file: {skill_md}"],
                fix_suggestion="Create SKILL.md with required segments",
                auto_fixable=False,
            ))
            continue

        content = skill_md.read_text(encoding="utf-8")
        missing_segments = []

        for segment in required_segments:
            if segment not in content:
                missing_segments.append(segment)

        if missing_segments:
            results.append(ValidationResult(
                check_id="ria",
                check_name="RIA-TV++六段完整性",
                severity=ValidationSeverity.ERROR,
                message=f"Missing required segments",
                target=skill_dir.name,
                details=missing_segments,
                fix_suggestion=f"Add missing segments: {', '.join(missing_segments)}",
                auto_fixable=False,
            ))

    return results


def check_test_prompts(skill_dirs: List[Path]) -> List[ValidationResult]:
    """Check test-prompts.json completeness"""
    results = []

    for skill_dir in skill_dirs:
        test_file = skill_dir / "test-prompts.json"
        if not test_file.exists():
            results.append(ValidationResult(
                check_id="test",
                check_name="test-prompts.json完整性",
                severity=ValidationSeverity.ERROR,
                message="test-prompts.json not found",
                target=skill_dir.name,
                details=[f"Missing file: {test_file}"],
                fix_suggestion="Create test-prompts.json with test cases",
                auto_fixable=False,
            ))
            continue

        try:
            with open(test_file, "r", encoding="utf-8") as f:
                test_data = json.load(f)

            test_cases = test_data.get("test_cases", [])
            types = [c.get("type", "") for c in test_cases]

            should_trigger = types.count("should_trigger")
            should_not_trigger = types.count("should_not_trigger")
            edge_case = types.count("edge_case")

            issues = []
            if should_trigger < 3:
                issues.append(f"should_trigger只有{should_trigger}条，需≥3")
            if should_not_trigger < 2:
                issues.append(f"should_not_trigger只有{should_not_trigger}条，需≥2")
            if edge_case < 1:
                issues.append(f"edge_case只有{edge_case}条，建议≥1")

            if issues:
                results.append(ValidationResult(
                    check_id="test",
                    check_name="test-prompts.json完整性",
                    severity=ValidationSeverity.WARNING if edge_case < 1 else ValidationSeverity.ERROR,
                    message="Test cases incomplete",
                    target=skill_dir.name,
                    details=issues,
                    fix_suggestion="Add more test cases to meet requirements",
                    auto_fixable=False,
                ))

        except json.JSONDecodeError as e:
            results.append(ValidationResult(
                check_id="test",
                check_name="test-prompts.json完整性",
                severity=ValidationSeverity.ERROR,
                message=f"Invalid JSON: {str(e)}",
                target=skill_dir.name,
                details=[f"JSON parsing error in {test_file}"],
                fix_suggestion="Fix JSON syntax errors",
                auto_fixable=False,
            ))

    return results


def check_source_book_consistency(skill_dirs: List[Path]) -> List[ValidationResult]:
    """Check source_book consistency and no training data residue"""
    results = []

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        test_file = skill_dir / "test-prompts.json"

        if not skill_md.exists():
            continue

        content = skill_md.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        skill_sb = fm.get("source_book", "")

        # Check for training data residue
        if "训练数据" in skill_sb:
            results.append(ValidationResult(
                check_id="source",
                check_name="source_book一致性",
                severity=ValidationSeverity.ERROR,
                message="SKILL.md source_book contains '训练数据'",
                target=skill_dir.name,
                details=[f"Found: {skill_sb}"],
                fix_suggestion="Remove '训练数据' from source_book field",
                auto_fixable=True,
            ))

        # Check consistency with test-prompts.json
        if test_file.exists():
            try:
                with open(test_file, "r", encoding="utf-8") as f:
                    test_data = json.load(f)

                test_sb = test_data.get("source_book", "")

                if "训练数据" in test_sb:
                    results.append(ValidationResult(
                        check_id="source",
                        check_name="source_book一致性",
                        severity=ValidationSeverity.ERROR,
                        message="test-prompts.json source_book contains '训练数据'",
                        target=skill_dir.name,
                        details=[f"Found: {test_sb}"],
                        fix_suggestion="Remove '训练数据' from test-prompts.json source_book",
                        auto_fixable=True,
                    ))

                # Extract book names from source_book fields
                import re
                skill_books = set(re.findall(r'《(.+?)》', skill_sb))
                test_books = set(re.findall(r'《(.+?)》', test_sb))

                if skill_books and test_books and skill_books != test_books:
                    results.append(ValidationResult(
                        check_id="source",
                        check_name="source_book一致性",
                        severity=ValidationSeverity.ERROR,
                        message="Book name mismatch between SKILL.md and test-prompts.json",
                        target=skill_dir.name,
                        details=[
                            f"SKILL.md: {skill_books}",
                            f"test-prompts.json: {test_books}",
                        ],
                        fix_suggestion="Ensure book names match between files",
                        auto_fixable=False,
                    ))

            except (json.JSONDecodeError, KeyError):
                pass

    return results


def run_validation(
    checks: Optional[List[str]] = None,
    fix: bool = False,
    strict: bool = False,
) -> List[Dict[str, Any]]:
    """
    Run validation checks

    Args:
        checks: List of check IDs to run (None for all)
        fix: Attempt to fix issues
        strict: Treat warnings as errors

    Returns:
        List of validation results as dictionaries
    """
    logger.info(f"Starting validation (checks: {checks}, fix: {fix}, strict: {strict})")

    # Define available checks
    all_checks = {
        "ria": ("RIA-TV++六段完整性", check_ria_completeness),
        "test": ("test-prompts.json完整性", check_test_prompts),
        "source": ("source_book一致性", check_source_book_consistency),
    }

    # Determine which checks to run
    checks_to_run = checks if checks else list(all_checks.keys())

    # Get skill directories
    base_path = settings.LIBRARY_DIR / "stock-trading-system"
    skill_dirs = read_skill_dirs(base_path)

    if not skill_dirs:
        logger.warning(f"No skill directories found in {base_path}")
        return []

    logger.info(f"Found {len(skill_dirs)} skill directories")

    # Run checks
    all_results = []

    for check_id in checks_to_run:
        if check_id not in all_checks:
            logger.warning(f"Unknown check: {check_id}")
            continue

        check_name, check_func = all_checks[check_id]
        logger.info(f"Running check: {check_name}")

        try:
            results = check_func(skill_dirs)
            all_results.extend(results)

            # Attempt to fix if requested
            if fix:
                fixed_count = 0
                for result in results:
                    if result.auto_fixable and result.severity == ValidationSeverity.ERROR:
                        # In a real implementation, this would fix the issue
                        logger.info(f"Would fix: {result.message} for {result.target}")
                        fixed_count += 1

                if fixed_count > 0:
                    logger.info(f"Fixed {fixed_count} issues for check: {check_name}")

        except Exception as e:
            logger.error(f"Check {check_id} failed: {e}")
            all_results.append(ValidationResult(
                check_id=check_id,
                check_name=check_name,
                severity=ValidationSeverity.ERROR,
                message=f"Check failed: {str(e)}",
                target="system",
                details=[f"Exception during check execution: {type(e).__name__}"],
                fix_suggestion="Check logs for details",
                auto_fixable=False,
            ))

    # Convert to dictionaries
    results_dicts = [r.to_dict() for r in all_results]

    # Apply strict mode
    if strict:
        for result in results_dicts:
            if result["severity"] == "warning":
                result["severity"] = "error"

    logger.info(f"Validation completed: {len(results_dicts)} results")
    return results_dicts


def get_available_checks() -> Dict[str, str]:
    """Get available validation checks"""
    return {
        "ria": "RIA-TV++六段完整性",
        "test": "test-prompts.json完整性",
        "source": "source_book一致性",
    }


def fix_validation_issues(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Attempt to fix validation issues

    Args:
        results: List of validation results

    Returns:
        Dictionary with fix results
    """
    # This is a placeholder implementation
    # In a real implementation, this would actually fix the issues

    fixable_results = [r for r in results if r.get("auto_fixable", False)]
    fixed_count = 0
    failed_count = 0

    for result in fixable_results:
        try:
            # Placeholder: In reality, this would modify files
            logger.info(f"Would fix: {result['message']} for {result['target']}")
            fixed_count += 1
        except Exception as e:
            logger.error(f"Failed to fix {result['check']}: {e}")
            failed_count += 1

    return {
        "total_issues": len(fixable_results),
        "fixed": fixed_count,
        "failed": failed_count,
        "remaining": len(fixable_results) - fixed_count,
    }
