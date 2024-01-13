from dataclasses import dataclass
from functools import cached_property
import re
from typing import Iterator


@dataclass(frozen=True)
class LogLine:

    url: str
    request_time: float

    @classmethod
    def from_dict(cls, dict_: dict) -> 'LogLine':
        return cls(url=dict_['url'], request_time=float(dict_['request_time']))


class LogParser:

    def __init__(self, reader: Iterator[str]) -> None:
        self._reader = reader
    
    def __iter__(self):
        return self

    def __next__(self) -> LogLine | None:
        line = next(self._reader)
        match = self._pattern.match(line)
        if not match:
            return None
        return LogLine.from_dict(match.groupdict())

    @cached_property
    def _pattern(self) -> re.Pattern:
        return re.compile(
            r'\S+ \S+  \S+ \[\S+ \S+\] "\S+ (?P<url>\S+) \S+" \S+ \S+ "\S+" ".*?" "\S+" "\S+" "\S+" (?P<request_time>\S+)')
