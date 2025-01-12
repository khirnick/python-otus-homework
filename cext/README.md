# C ext.

Сборка прото-структуры:

```bash
cd deviceapps
protoc --c_out=. deviceapps.proto
```

Запуск:

```python
import pb

file_name = 'test.pb.gz'
deviceapps = [
    {"device": {"type": "idfa", "id": "e7e1a50c0ec2747ca56cd9e1558c0d7c"},
     "lat": 67.7835424444, "lon": -22.8044005471, "apps": [1, 2, 3, 4]},
]

# Write
total_bytes = pb.deviceapps_xwrite_pb(deviceapps, file_name)
print(total_bytes)  # 76
# Read
result = list(pb.deviceapps_xread_pb(file_name))
print(result == deviceapps)  # True
```
