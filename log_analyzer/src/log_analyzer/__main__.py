import argparse
from json import JSONDecodeError
import logging
from pathlib import Path
import sys
import time
from types import MappingProxyType

from ._config import Config, get_config
from ._logger import build_logging
from ._parser import LogParser
from ._path import get_log_path
from ._report import ReportBuilder


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
    if not config.log_directory.is_dir():
        logger.error(f'Log directory {config.log_directory} does not exist')
        sys.exit(1)
    if not config.report_directory.is_dir():
        logger.error(f'Report directory {config.report_directory} does not exist')
        sys.exit(1)
    log_path = get_log_path(config.log_directory)
    if not log_path:
        logger.info(f'No log to analyze')
        return
    logger.info(f'Log to analyze: {log_path.path}')
    report_builder = ReportBuilder(config.report_directory, log_path.date, config.report_size)
    log_parser = LogParser(reader=log_path.open())
    report_builder.build(log_parser)


if __name__ == "__main__":
    args = parse_args()
    config_path = Path(args.config) if args.config else None
    if config_path and not config_path.is_file():
        print(f'Config file {config_path} not found')
        sys.exit(1)
    try:
        config = get_config(default_config=DEFAULT_CONFIG, custom_config_path=config_path)
    except JSONDecodeError:
        print(f'Config file {config_path} is not valid json')
        sys.exit(1)
    if config.app_logging_path and not config.app_logging_path.is_file():
        print(f'Application logging file {config.app_logging_path} not found')
        sys.exit(1)
    build_logging(path=config.app_logging_path)
    try:
        start = time.time()
        main(config)
        logging.getLogger().info(f'Took: {round(time.time() - start, 2)}s')
    except Exception as exception:
        logging.getLogger().exception(exception)
        sys.exit(1)
