import argparse
from json import JSONDecodeError
from pathlib import Path
import sys
from types import MappingProxyType

from ._config import Config, get_config
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
    log_path = get_log_path(config.log_directory)
    print('Got log_path', log_path)
    if not log_path:
        return
    report_builder = ReportBuilder(config.report_directory, log_path.date)
    print('Initialize ReportBuilder', report_builder)
    log_parser = LogParser(reader=log_path.open())
    print('Got log_parser', log_parser)
    try:
        report_builder.build(log_parser)
    except FileExistsError:
        print(f'Report for date {log_path.date} is already exist')


if __name__ == "__main__":
    args = parse_args()
    try:
        config = get_config(default_config=DEFAULT_CONFIG, custom_config=Path(args.config) if args.config else None)
    except FileNotFoundError:
        print(f'Config {args.config} not found')
        sys.exit(1)
    except JSONDecodeError:
        print(f'Config {args.config} is not valid json')
        sys.exit(1)
    print(config)
    main(config)
