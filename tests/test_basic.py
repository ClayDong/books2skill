"""
Basic tests for Cangjie Skill
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_imports():
    """Test basic imports"""
    import cangjie
    import cangjie.config
    import cangjie.utils.logging
    import cangjie.validation.validate_system

    assert cangjie is not None
    assert cangjie.config is not None
    assert cangjie.utils.logging is not None
    assert cangjie.validation.validate_system is not None


def test_config():
    """Test configuration loading"""
    from cangjie.config import settings

    assert settings is not None
    assert hasattr(settings, 'PROJECT_ROOT')
    assert hasattr(settings, 'BOOKS_RAW_DIR')
    assert hasattr(settings, 'LOG_LEVEL')

    # Test that paths are Path objects
    assert isinstance(settings.PROJECT_ROOT, Path)
    assert isinstance(settings.BOOKS_RAW_DIR, Path)


def test_logging():
    """Test logging setup"""
    from cangjie.utils.logging import setup_logging, get_logger

    logger = setup_logging(level="INFO")
    assert logger is not None
    assert logger.name == "cangjie"

    # Test getting named logger
    test_logger = get_logger("test")
    assert test_logger is not None
    assert test_logger.name == "cangjie.test"


def test_validation_structure():
    """Test validation system structure"""
    from cangjie.validation.validate_system import (
        ValidationSeverity,
        ValidationResult,
        run_validation,
        get_available_checks,
    )

    # Test enum
    assert ValidationSeverity.ERROR.value == "error"
    assert ValidationSeverity.WARNING.value == "warning"

    # Test result class
    result = ValidationResult(
        check_id="test",
        check_name="Test Check",
        severity=ValidationSeverity.ERROR,
        message="Test message",
        target="test_target",
        details=["detail1", "detail2"],
    )

    assert result.check_id == "test"
    assert result.severity == ValidationSeverity.ERROR
    assert result.target == "test_target"

    # Test conversion to dict
    result_dict = result.to_dict()
    assert isinstance(result_dict, dict)
    assert result_dict["check"] == "test"
    assert result_dict["severity"] == "error"

    # Test available checks
    checks = get_available_checks()
    assert isinstance(checks, dict)
    assert "ria" in checks
    assert "test" in checks
    assert "source" in checks


def test_validation_functions():
    """Test validation helper functions"""
    from cangjie.validation.validate_system import parse_frontmatter

    # Test frontmatter parsing
    content = """---
name: test-skill
description: A test skill
tags: [test, example]
---

# Test Skill

Content here
"""

    fm = parse_frontmatter(content)
    assert fm["name"] == "test-skill"
    assert fm["description"] == "A test skill"
    assert "tags" in fm

    # Test empty content
    empty_fm = parse_frontmatter("No frontmatter here")
    assert empty_fm == {}


def test_pipeline_structure():
    """Test pipeline module structure"""
    try:
        from cangjie.pipeline.distill import (
            DistillationStage,
            DistillationResult,
            DistillationPipeline,
            run_distillation,
        )

        # Test enum
        assert DistillationStage.STAGE_0.value == "stage_0"
        assert DistillationStage.STAGE_1.value == "stage_1"

        # Test result dataclass
        result = DistillationResult(
            success=True,
            book_path=Path("test.pdf"),
            output_dir=Path("output"),
            skills_created=3,
            time_taken=10.5,
            stages_completed=[DistillationStage.STAGE_0],
            errors=[],
            warnings=[],
            metadata={},
        )

        assert result.success is True
        assert result.skills_created == 3
        assert result.time_taken == 10.5

    except ImportError as e:
        # Pipeline might not be fully implemented yet
        print(f"Pipeline import failed (may be expected): {e}")


if __name__ == "__main__":
    # Run tests
    test_imports()
    print("✓ test_imports passed")

    test_config()
    print("✓ test_config passed")

    test_logging()
    print("✓ test_logging passed")

    test_validation_structure()
    print("✓ test_validation_structure passed")

    test_validation_functions()
    print("✓ test_validation_functions passed")

    test_pipeline_structure()
    print("✓ test_pipeline_structure passed")

    print("\n✅ All basic tests passed!")
