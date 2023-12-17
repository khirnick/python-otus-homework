from datetime import date
from log_analyzer._path import get_log_path, LogPath, _get_log_paths


def test_get_log_path(log_directory):
    # act
    path = get_log_path(log_directory)

    # assert
    assert path == LogPath(path=log_directory / 'nginx-access-ui.log-20230104.gz', date=date(2023, 1, 4), extension='.gz')


def test_get_log_paths(log_directory):
    # act
    paths = _get_log_paths(log_directory)

    # assert
    assert set(paths) == {
        LogPath(path=log_directory / 'nginx-access-ui.log-20230101.gz', date=date(2023, 1, 1), extension='.gz'),
        LogPath(path=log_directory / 'nginx-access-ui.log-20230102.gz', date=date(2023, 1, 2), extension='.gz'),
        LogPath(path=log_directory / 'nginx-access-ui.log-20230103', date=date(2023, 1, 3), extension=None),
        LogPath(path=log_directory / 'nginx-access-ui.log-20230104.gz', date=date(2023, 1, 4), extension='.gz'),
    }
