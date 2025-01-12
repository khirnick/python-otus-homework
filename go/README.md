# Golang mem loader

Сбилдить прото-структуру
```
protoc --go_out=. appsinstalled.proto
go install appsinstalled.pb.go
```



### Запуск

```bash
$ go run memc_load_multi.go -h

Usage of memc_load_multi:
  -adid string
         (default "127.0.0.1:33015")
  -attempts int
         (default 3)
  -buffer int
         (default 100)
  -dry
    
  -dvid string
         (default "127.0.0.1:33016")
  -gaid string
         (default "127.0.0.1:33014")
  -idfa string
         (default "127.0.0.1:33013")
  -log string
    
  -pattern string
         (default "/appsinstalled/*.tsv.gz")
  -test
```




### Testing results

**Python**

В одном потоке:

```bash
$ time python memc_load.py --pattern=*.tsv.gz

real	153m21.440s
user	33m3.855s
sys	102m11.213s


В многопоточном режиме

```bash
$ time python memc_load_multi.py --pattern=*.tsv.gz

real	23m31.991s
user	30m14.477s
sys	16m1.729s
```


**Go**

В одном потоке:

```bash
$ time go run memc_load.go --pattern=*.tsv.gz

real	13m9.986s
user	6m22.093s
sys	6m11.167s
```

В многопоточном режиме

```bash
$ time go run memc_load_multi.go --pattern=*.tsv.gz

real	4m23.219s
user	5m40.546s
sys	4m4.942s
```