"""
Cangjie Skill Configuration Module
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """Main application settings"""

    # Project Paths
    PROJECT_ROOT: Path = Field(default=Path("."), env="PROJECT_ROOT")
    BOOKS_RAW_DIR: Path = Field(default=Path("./books_raw/书股"), env="BOOKS_RAW_DIR")
    BOOKS_TXT_DIR: Path = Field(default=Path("./books_txt"), env="BOOKS_TXT_DIR")
    BOOKS_TXT_OCR_DIR: Path = Field(default=Path("./books_txt_ocr"), env="BOOKS_TXT_OCR_DIR")
    LIBRARY_DIR: Path = Field(default=Path("./library"), env="LIBRARY_DIR")
    OUTPUT_DIR: Path = Field(default=Path("./output"), env="OUTPUT_DIR")

    # OCR Configuration
    OCR_DPI: int = Field(default=200, env="OCR_DPI")
    OCR_LANG: str = Field(default="ch", env="OCR_LANG")
    OCR_USE_ANGLE_CLS: bool = Field(default=True, env="OCR_USE_ANGLE_CLS")
    OCR_USE_GPU: bool = Field(default=False, env="OCR_USE_GPU")

    # Processing Configuration
    MAX_WORKERS: int = Field(default=4, env="MAX_WORKERS")
    CHUNK_SIZE: int = Field(default=1000, env="CHUNK_SIZE")
    CACHE_ENABLED: bool = Field(default=True, env="CACHE_ENABLED")
    CACHE_TTL: int = Field(default=86400, env="CACHE_TTL")  # 24 hours

    # Validation Configuration
    VALIDATION_STRICT: bool = Field(default=True, env="VALIDATION_STRICT")
    VALIDATION_TIMEOUT: int = Field(default=300, env="VALIDATION_TIMEOUT")
    MIN_SKILL_QUALITY_SCORE: float = Field(default=0.7, env="MIN_SKILL_QUALITY_SCORE")

    # Logging Configuration
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(default="json", env="LOG_FORMAT")
    LOG_FILE: Path = Field(default=Path("./logs/cangjie.log"), env="LOG_FILE")
    LOG_ROTATION: str = Field(default="10 MB", env="LOG_ROTATION")
    LOG_RETENTION: str = Field(default="30 days", env="LOG_RETENTION")

    # Performance Configuration
    ENABLE_PROFILING: bool = Field(default=False, env="ENABLE_PROFILING")
    PROFILING_OUTPUT: Path = Field(default=Path("./profiling"), env="PROFILING_OUTPUT")
    MAX_MEMORY_USAGE: str = Field(default="2GB", env="MAX_MEMORY_USAGE")

    # Development Configuration
    DEBUG: bool = Field(default=False, env="DEBUG")
    TEST_MODE: bool = Field(default=False, env="TEST_MODE")
    SKIP_VALIDATION: bool = Field(default=False, env="SKIP_VALIDATION")
    FAST_MODE: bool = Field(default=False, env="FAST_MODE")

    # Export Configuration
    EXPORT_FORMAT: str = Field(default="markdown", env="EXPORT_FORMAT")
    EXPORT_INCLUDE_METADATA: bool = Field(default=True, env="EXPORT_INCLUDE_METADATA")
    EXPORT_INCLUDE_VALIDATION: bool = Field(default=True, env="EXPORT_INCLUDE_VALIDATION")

    # API Configuration (optional)
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @validator("PROJECT_ROOT", "BOOKS_RAW_DIR", "BOOKS_TXT_DIR", "BOOKS_TXT_OCR_DIR",
               "LIBRARY_DIR", "OUTPUT_DIR", "LOG_FILE", "PROFILING_OUTPUT", pre=True)
    def validate_paths(cls, v):
        """Convert string paths to Path objects"""
        if isinstance(v, str):
            return Path(v)
        return v

    @validator("MAX_WORKERS")
    def validate_max_workers(cls, v):
        """Ensure MAX_WORKERS is reasonable"""
        import multiprocessing
        max_cpus = multiprocessing.cpu_count()
        if v > max_cpus * 2:
            return max_cpus * 2
        if v < 1:
            return 1
        return v

    def load_config(self, config_path: Path) -> None:
        """Load configuration from file"""
        if config_path.exists():
            from importlib.machinery import SourceFileLoader
            config_module = SourceFileLoader("config", str(config_path)).load_module()

            for key, value in vars(config_module).items():
                if key.isupper() and hasattr(self, key):
                    setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary"""
        return {
            k: str(v) if isinstance(v, Path) else v
            for k, v in self.dict().items()
        }

    def ensure_directories(self) -> None:
        """Ensure all required directories exist"""
        directories = [
            self.BOOKS_RAW_DIR,
            self.BOOKS_TXT_DIR,
            self.BOOKS_TXT_OCR_DIR,
            self.LIBRARY_DIR,
            self.OUTPUT_DIR,
            self.LOG_FILE.parent,
            self.PROFILING_OUTPUT,
        ]

        for directory in directories:
            if directory:
                directory.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()

# Ensure directories exist
settings.ensure_directories()
