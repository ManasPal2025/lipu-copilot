"""Application logging configuration."""

import logging
import sys
from logging.config import dictConfig
from typing import Any

from pythonjsonlogger import jsonlogger

from app.core.config import Settings


class AppJsonFormatter(jsonlogger.JsonFormatter):
    """JSON formatter with stable service metadata."""

    def __init__(self, *args: Any, app_name: str, app_version: str, environment: str, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.app_name = app_name
        self.app_version = app_version
        self.environment = environment

    def add_fields(self, log_record: dict[str, Any], record: logging.LogRecord, message_dict: dict[str, Any]) -> None:
        super().add_fields(log_record, record, message_dict)
        log_record.setdefault("service", self.app_name)
        log_record.setdefault("version", self.app_version)
        log_record.setdefault("environment", self.environment)
        log_record.setdefault("level", record.levelname)
        log_record.setdefault("logger", record.name)


def configure_logging(settings: Settings) -> None:
    """Configure root, app, access, and error loggers."""

    formatter: dict[str, Any]
    if settings.log_format == "json":
        formatter = {
            "()": AppJsonFormatter,
            "fmt": "%(asctime)s %(level)s %(name)s %(message)s %(request_id)s %(path)s %(method)s %(status_code)s",
            "app_name": settings.app_name,
            "app_version": settings.app_version,
            "environment": settings.app_env,
        }
    else:
        formatter = {
            "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        }

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {"default": formatter},
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "stream": sys.stdout,
                    "formatter": "default",
                }
            },
            "root": {"handlers": ["default"], "level": settings.log_level},
            "loggers": {
                "app": {"handlers": ["default"], "level": settings.log_level, "propagate": False},
                "uvicorn": {"handlers": ["default"], "level": settings.log_level, "propagate": False},
                "uvicorn.error": {"handlers": ["default"], "level": settings.log_level, "propagate": False},
                "uvicorn.access": {"handlers": ["default"], "level": settings.log_level, "propagate": False},
                "sqlalchemy.engine": {
                    "handlers": ["default"],
                    "level": "INFO" if settings.database_echo else "WARNING",
                    "propagate": False,
                },
            },
        }
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

