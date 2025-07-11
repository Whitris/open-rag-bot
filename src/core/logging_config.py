import logging
import sys


def setup_logging(
    level: int = logging.INFO, log_to_file: bool = False, file_path: str | None = "app.log"
):
    """Set up global logging configuration."""
    handlers = []
    if log_to_file:
        handlers.append(logging.FileHandler(file_path, encoding="utf-8"))
    else:
        handlers.append(logging.StreamHandler(sys.stdout))

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=handlers,
        force=True,
    )
