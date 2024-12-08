# http_server

## Тестирование
Результат тестирования `ab -n 1000 -c 10 http://localhost:8080/index.html`:
```
Concurrency Level:      10
Time taken for tests:   1.531 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      80000 bytes
HTML transferred:       36000 bytes
Requests per second:    653.37 [#/sec] (mean)
Time per request:       15.305 [ms] (mean)
Time per request:       1.531 [ms] (mean, across all concurrent requests)
Transfer rate:          51.04 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    7  88.2      0    1057
Processing:     2    5  25.4      3     471
Waiting:        1    4  25.4      2     470
Total:          2   13 110.9      3    1527
```

