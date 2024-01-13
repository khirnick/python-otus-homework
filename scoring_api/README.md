# Scoring API
Подсчет очков по переданным данным

### Установка
*Для корректной работы необходимо использовать Python `>= 3.11`*

Перейти в каталог с проектом и установить пакет:
```bash
$ cd scoring_api/ && pip install .
```

### Запуск
```bash
$ python -m scoring_api --port 8080 --log path/to/log.txt
```
Команда принимает опциональный аргументы:
`--port` (опциональный, по умолчанию 8080) - на каком порту запустить сервер
`--log` (опциональный) - куда писать логи

### Как пользоваться
#### Структура тела запроса
```json
{"account": "<имя компании партнера>", "login": "<имя пользователя>", "method": "<имя метода>", "token": "<аутентификационный токен>", "arguments": {<словарь с аргументами вызываемого метода>}}
```

Параметры:
- `account` - строка, опционально, может быть пустым
- `login` - строка, обязательно, может быть пустым
- `method` - строка, обязательно, может быть пустым
- `token` - строка, обязательно, может быть пустым
- `arguments` - словарь (объект в терминах json), обязательно, может быть пустым

#### Подсчет очков
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"account": "ACCOUT", "login": "LOGIN", "method": "online_score", "token": "TOKEN", "arguments": {"phone": "PHONE", "email": "EMAIL", "first_name": "NAME", "last_name": "NAME", "birthday": "01.01.1990", "gender": 1}}' http://127.0.0.1:8080/method/
```

Ответ:
```json
{"code": 200, "response": {"score": 5.0}}
```

#### Интересы клиента
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"account": "ACCOUNT", "login": "LOGIN", "method": "clients_interests", "token": "TOKEN", 
"arguments": {"client_ids": [1,2,3,4], "date": "20.07.2017"}}' http://127.0.0.1:8080/method/
```

Ответ:
```json
{"code": 200, "response": {"1": ["books", "hi-tech"], "2": ["pets", "tv"], "3": ["travel", "music"], "4": ["cinema", "geek"]}}
```


### Тесты
Для запуска тестов необходимо установить тестовые зависимости
```bash
$ pip install -e ".[test]"
```
И запустить тесты
```bash
$ pytest tests/
```
