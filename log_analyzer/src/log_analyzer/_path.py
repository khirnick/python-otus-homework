from dataclasses import InitVar, dataclass, field
from datetime import date, datetime
import gzip
from pathlib import Path
import re


@dataclass(frozen=True)
class LogPath:

    path: Path
    date: date
    extension: str | None

    def open(self, mode: str = 'rt'):
        open_method = gzip.open if self.extension == '.gz' else open
        return open_method(self.path, mode)


def get_log_path(log_directory: Path) -> LogPath | None:
    pattern = re.compile(r'^nginx-access-ui.log-(?P<date>\d+)(?P<extension>.gz)?$')
    paths = (
        LogPath(path=path, date=_parse_date(match.groupdict()['date']), extension=match.groupdict()['extension']) 
        for path in log_directory.iterdir() 
        if (match := pattern.match(path.name))
    )
    fresh = None
    for path in paths:
        if not fresh:
            fresh = path
        else:
            fresh = path if path.date > fresh.date else fresh
    return fresh


def _parse_date(date_string: str) -> date:
    return datetime.strptime(date_string, '%Y%m%d').date()
