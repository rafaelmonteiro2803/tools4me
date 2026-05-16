import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
EXAMPLES_DIR = BASE_DIR / "examples"

DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
EXAMPLES_DIR.mkdir(exist_ok=True)

APP_CONFIG = {
    "title": "LinkedIn Data Enrichment Tool",
    "version": "1.0.0",
    "author": "Senior Software Engineer",
    "theme": "dark",
    "geometry": "1200x800",
    "resizable": True,
}

SEARCH_CONFIG = {
    "max_threads": 5,
    "timeout": 10,
    "retry_attempts": 3,
    "delay_min": 1,
    "delay_max": 3,
    "rate_limit_requests": 50,
    "rate_limit_window": 60,
}

LINKEDIN_CONFIG = {
    "search_domain": "linkedin.com",
    "profile_patterns": [
        r"linkedin\.com/in/[a-z0-9\-]+",
        r"linkedin\.com/company/[a-z0-9\-]+",
    ],
}

MATCH_CONFIG = {
    "min_confidence": 0.5,
    "name_weight": 0.4,
    "company_weight": 0.35,
    "title_weight": 0.25,
}

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": str(LOGS_DIR / "app.log"),
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"],
    },
}
