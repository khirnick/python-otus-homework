from datetime import date
import gzip
from pathlib import Path
from log_analyzer._parser import LogParser
from log_analyzer._report import ReportBuilder


def test_ReportBuilder(log_directory, reports_directory, reports_result_directory):
    # arrange
    builder = ReportBuilder(report_directory=reports_directory, report_date=date(2023, 1, 1), report_size=5, unparsed_logs_coef=1)
    builder.path.unlink(missing_ok=True)
    parser = LogParser(gzip.open(Path(log_directory / 'nginx-access-ui.log-20230101.gz'), 'rt'))

    # act
    builder.build(parser)

    # assert
    assert builder.path.is_file()
    assert builder.path.open('rt').read() == Path(reports_result_directory / 'report-2023.01.01.html').open('rt').read()

    # cleanup
    builder.path.unlink()


def test_ReportBuilder__exceed_unparsed_logs_coef(log_directory, reports_directory):
    # arrange
    unparsed_logs_coef = 0.1
    builder = ReportBuilder(report_directory=reports_directory, report_date=date(2023, 1, 1), report_size=5, unparsed_logs_coef=unparsed_logs_coef)
    builder.path.unlink(missing_ok=True)
    parser = LogParser(gzip.open(Path(log_directory / 'nginx-access-ui.log-20230101.gz'), 'rt'))

    # act
    builder.build(parser)

    # assert
    assert not builder.path.is_file()


def test_ReportBuilder__report_exists(mocker, reports_directory):
    # arrange
    builder = ReportBuilder(report_directory=reports_directory, report_date=date(2023, 1, 2), report_size=5, unparsed_logs_coef=1)
    builder._read_logs = mocker.Mock()

    # act
    builder.build('some logs')

    # assert
    assert builder._is_report_exists
    builder._read_logs.assert_not_called()

