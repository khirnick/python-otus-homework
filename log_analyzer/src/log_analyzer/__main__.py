import argparse
from json import JSONDecodeError
import logging
from pathlib import Path
import sys
import time
from types import MappingProxyType

from .config import Config, get_config
from .logger import build_logging
from .parser import LogParser
from .path import get_log_path
from .report import ReportBuilder


DEFAULT_CONFIG = MappingProxyType({
    'REPORT_SIZE': 1000,
    'REPORT_DIR': './reports',
    'LOG_DIR': './log',
})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='Log Analyzer', 
        description='Analyze nginx logs and build statistics report')
    parser.add_argument('-c', '--config')
    return parser.parse_args()


def main(config: Config) -> None:
    logger = logging.getLogger()
    log_path = get_log_path(config.log_directory)
    if not log_path:
        logger.info('No log to analyze')
        return
    logger.info(f'Log to analyze: {log_path.path}')
    report_builder = ReportBuilder(config.report_directory, log_path.date, config.report_size)
    log_parser = LogParser(reader=log_path.open())
    report_builder.build(log_parser)


if __name__ == "__main__":
    start = time.time()
    build_logging()
    args = parse_args()
    config_path = Path(args.config) if args.config else None
    try:
        config = get_config(default_config=DEFAULT_CONFIG, custom_config_path=config_path)
        build_logging(path=config.app_logging_path)
        main(config)
    except (FileNotFoundError, NotADirectoryError, JSONDecodeError) as exception:
        logging.getLogger().exception(exception, exc_info=False)
        sys.exit(1)
    except Exception as exception:
        logging.getLogger().exception(exception, exc_info=True)
        sys.exit(1)
    duration = time.time() - start
    logging.getLogger().info(f'Took: {round(duration, 2)}s')
