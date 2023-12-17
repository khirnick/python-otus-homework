from datetime import date
from pathlib import Path
from string import Template

from ._constants import REPORT_TEMPLATE_PATH
from ._parser import LogParser
from ._stat import UrlsStat, UrlStat


class ReportBuilder:

    def __init__(self, report_directory: Path, report_date: date, report_size: int) -> None:
        self._path = report_directory / f'report-{report_date.strftime("%Y.%m.%d")}.html'
        self._report_size = report_size

    @property
    def path(self) -> Path:
        return self._path
    
    def build(self, log_parser: LogParser) -> str:
        self._check_existing_template()
        urls_stat = UrlsStat()
        for line in log_parser:
            if line:
                urls_stat[line.url] += line.request_time
        print('Read logs, count: ', urls_stat.entries)
        print('Building report...')
        table_json = self._build_table_json(urls_stat)
        print('Report is built')
        print('Reading template...')
        template = self._read_template()
        print('Template is read')
        print('Substituting variable in template...')
        template = template.safe_substitute(table_json=table_json)
        print('Substituting is succeed')
        print('Saving to report directory...')
        with open(self._path, 'wt') as f:
            f.write(template)
        print('Saved!')

    def _read_template(self) -> Template:
        template_data = open(REPORT_TEMPLATE_PATH, 'rt').read()
        return Template(template_data)

    def _check_existing_template(self) -> None:
        if self._path.is_file():
            raise FileExistsError(f'Report {self._path} is already exist')

    def _build_table_json(self, urls_stat: UrlsStat) -> list[dict]:
        report = []
        urls_stat_sum = urls_stat.sum
        urls_stat_entries = urls_stat.entries
        for url, url_stat in sorted(urls_stat.items(), key=lambda s: s[1].sum, reverse=True)[0:self._report_size]:
            url_stat: UrlStat
            report.append(
                {
                    'url': url,
                    'count': url_stat.entries,
                    'count_perc': round(url_stat.entries / urls_stat_entries, 3),
                    'time_sum': round(url_stat.sum, 3),
                    'time_perc': round(url_stat.sum / urls_stat_sum, 3),
                    'time_avg': round(url_stat.average, 3),
                    'time_max': round(url_stat.max, 3),
                    'time_med': round(url_stat.median, 3)   ,
                }
            )
        return report
