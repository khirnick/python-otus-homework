from pathlib import Path
import pytest


@pytest.fixture
def log_directory():
    return Path(__file__).parent / 'data/log/'


@pytest.fixture
def reports_directory():
    return Path(__file__).parent / 'data/reports/'


@pytest.fixture
def reports_result_directory():
    return Path(__file__).parent / 'data/reports_result/'
