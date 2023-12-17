from pathlib import Path
import pytest


@pytest.fixture
def log_directory():
    return Path(__file__).parent / 'data/log/'


@pytest.fixture
def reports_directory():
    return Path(__file__).parent / 'data/reports/'


@pytest.fixture
def logs():
    return [
        '1.2.3.4 -  - [01/Jun/2023:12:00:00 +0300] "GET /api/v1/banner/1/ HTTP/1.1" 200 123 "-" "Python/urllib" "-" "1234-567" "abcdef" 1.2',
        '1.2.3.4 -  - [01/Jun/2023:12:00:00 +0300] "GET /api/v1/banner/1/ HTTP/1.1" 200 123 "-" "Python/urllib" "-" "1234-567" "abcdef" 1.6',
        # следующие 2 лога - битые, в запросе указан "Х"
        '1.2.3.4 -  - [01/Jun/2023:12:00:00 +0300] "X" 200 123 "-" "Python/urllib" "-" "1234-567" "abcdef" 0.1234',
        '1.2.3.4 -  - [01/Jun/2023:12:00:00 +0300] "X" 200 123 "-" "Python/urllib" "-" "1234-567" "abcdef" 0.1234',
        '1.2.3.4 -  - [01/Jun/2023:12:00:00 +0300] "GET /api/v1/banner/2/ HTTP/1.1" 200 123 "-" "Python/urllib" "-" "1234-567" "abcdef" 0.9',
        '1.2.3.4 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v1/banner/3/ HTTP/1.1" 200 123 "-" "Python/urllib" "-" "1234-567" "abcdef" 0.8',
        '1.2.3.4 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v1/banner/4/ HTTP/1.1" 200 123 "-" "Python/urllib" "-" "1234-567" "abcdef" 0.6',
        '1.2.3.4 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v1/banner/5/ HTTP/1.1" 200 123 "-" "Python/urllib" "-" "1234-567" "abcdef" 5.5',
        '1.2.3.4 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v1/banner/5/ HTTP/1.1" 200 123 "-" "Python/urllib" "-" "1234-567" "abcdef" 6.1',
        '1.2.3.4 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v1/banner/6/ HTTP/1.1" 200 123 "-" "Python/urllib" "-" "1234-567" "abcdef" 0.8',
    ]


@pytest.fixture
def reports_result_directory():
    return Path(__file__).parent / 'data/reports_result/'
