from pathlib import Path

from ._parse import LogParser
from ._path import get_log_path
from ._stat import UrlsStat


CONFIG = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log"
}


def main(config: dict) -> None:
    log_path = get_log_path(Path(config['LOG_DIR']))
    lines = (line for line in LogParser(reader=log_path.open()))
    not_empty_lines = (line for line in lines if line)
    urls_stat = UrlsStat()
    for line in not_empty_lines:
        urls_stat[line.url] += line.request_time
    print('Sum', urls_stat.sum)
    print('Entries', urls_stat.entries)


if __name__ == "__main__":
    main(CONFIG)
