# Concurrency

Для начала необходимо установить memcache и запустить его

Сбилдить прото-структуру:
`protoc --python_out=. appsinstalled.proto`


Результаты:

В одном потоке:

$ time python memc_load.py --pattern=*.tsv.gz

real	153m21.440s
user	33m3.855s
sys	102m11.213s


В многопоточном режиме

$ time python memc_load_multi.py --pattern=*.tsv.gz

real	23m31.991s
user	30m14.477s
sys	16m1.729s
