import logging
from pathlib import Path


FORMAT = '[%(asctime)s] %(levelname).1s %(message)s'
DATE_FORMAT = '%Y.%m.%d %H:%M:%S'
LEVEL = logging.INFO


def build_logging(path: Path | None) -> logging.Logger:
    logging.basicConfig(
        format=FORMAT,
        datefmt=DATE_FORMAT,
        level=logging.INFO,
        filename=path,
        force=True,
    )
