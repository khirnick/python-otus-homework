from dataclasses import dataclass
import json
from pathlib import Path
from types import MappingProxyType
from typing import Self


@dataclass(frozen=True)
class Config:

    report_size: int
    report_directory: Path
    log_directory: Path

    @classmethod
    def from_dict(cls, dict_: dict) -> Self:
        return cls(
            report_size=dict_['REPORT_SIZE'],
            report_directory=Path(dict_['REPORT_DIR']),
            log_directory=Path(dict_['LOG_DIR']),
        )


def get_config(default_config: dict, custom_config: Path | None) -> Config:
    if custom_config and not custom_config.is_file():
        raise FileNotFoundError
    result = {}
    result.update(default_config)
    if custom_config:
        content = json.load(custom_config.open())
        result.update(content)
    return Config.from_dict(result)
