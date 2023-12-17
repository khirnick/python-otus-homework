import gzip
from log_analyzer._parser import LogParser, LogLine


def test_LogParser(log_directory):
    # arrange
    parser = LogParser(gzip.open(log_directory / 'nginx-access-ui.log-20230101.gz', 'rt'))

    # act
    result = list(parser)

    # assert
    assert result == [
        LogLine(url='/api/v1/banner/1/', request_time=1.2),
        LogLine(url='/api/v1/banner/1/', request_time=1.6),
        None,
        None,
        LogLine(url='/api/v1/banner/2/', request_time=0.9),
        LogLine(url='/api/v1/banner/3/', request_time=0.8),
        LogLine(url='/api/v1/banner/4/', request_time=0.6),
        LogLine(url='/api/v1/banner/5/', request_time=5.5),
        LogLine(url='/api/v1/banner/5/', request_time=6.1),
        LogLine(url='/api/v1/banner/6/', request_time=0.8),
    ]
