# Log Analyzer
Анализирует лог Nginx и собирает отчет со статистикой по URL.

### Установка
*Для корректной работы необходимо использовать Python `>= 3.11`*

Перейти в каталог с проектом и установить пакет:
```bash
$ cd log_analyzer/ && pip install .
```

### Запуск
```bash
$ python -m log_analyzer --config path/to/config.json
```
Команда принимает опциональный аргумент `--config`, в котром указывается путь до пользовательской конфигурации. Конфигурация в файле должна быть в формате json. Пользовательская конфигурация имеет приоритет над конфигурацией по умолчанию.

Конфигурация по умолчанию:
```json
{
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log",
    "APP_LOGGING_PATH": null
}
```
- `REPORT_SIZE`: максимальный размер отчета
- `REPORT_DIR`: путь до папки с отчетами
- `LOG_DIR`: путь до папки с логами nginx
- `APP_LOGGING_PATH`: путь, куда приложение будет писать логи. Если null или не указано, то логи пишутся в stdout

*Для анализа будет выбран последний лог nginx из директории `LOG_DIR`*

### Тесты
Для запуска тестов необходимо установить тестовые зависимости
```bash
$ pip install -e ".[test]"
```
И запустить тесты
```bash
$ pytest tests/
```
