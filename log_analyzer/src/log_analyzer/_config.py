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
    app_logging_path: Path | None = None

    @classmethod
    def from_dict(cls, dict_: dict) -> Self:
        return cls(
            report_size=dict_['REPORT_SIZE'],
            report_directory=Path(dict_['REPORT_DIR']),
            log_directory=Path(dict_['LOG_DIR']),
            app_logging_path=Path(dict_['APP_LOGGING_PATH']) if 'APP_LOGGING_PATH' in dict_ else None,
        )


def get_config(default_config: dict, custom_config_path: Path | None) -> Config:
    result = {}
    result.update(default_config)
    if custom_config_path:
        content = json.load(custom_config_path.open())
        result.update(content)
    return Config.from_dict(result)
