from pathlib import Path

from ._parser import LogParser


class Report:

    def __init__(self, report_directory: Path, report_date: str) -> None:
        self._path = report_directory / f'report-{report_date}.html'

    @property
    def path(self) -> Path:
        return self._path
    
    def build(self, log_parser: LogParser):
        # read logs from parser and build report
        ...
