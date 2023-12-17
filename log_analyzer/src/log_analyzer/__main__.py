from pathlib import Path

from ._parser import LogParser
from ._path import get_log_path
from ._report import ReportBuilder


CONFIG = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log"
}


def main(config: dict) -> None:
    log_path = get_log_path(Path(config['LOG_DIR']))
    print('Got log_path', log_path)
    if not log_path:
        return
    report_builder = ReportBuilder(Path(config['REPORT_DIR']), log_path.date)
    print('Initialize ReportBuilder', report_builder)
    log_parser = LogParser(reader=log_path.open())
    print('Got log_parser', log_parser)
    try:
        report_builder.build(log_parser)
    except FileExistsError:
        print(f'Report for date {log_path.date} is already exist')


if __name__ == "__main__":
    main(CONFIG)
