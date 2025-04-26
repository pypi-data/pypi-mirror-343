# KittenServer

KittenServer可以让您扩展海龟函数的功能

# 示例
## 代码
```python
from kittenserver import KittenServer

def func_event(event):
    print(event)
    return '{"errno": 0, "result": "https://pypi.org/project/kittenserver/"}'

ks = KittenServer()
ks.run(func_event)
```
## 运行结果
```
> python test.py
https://localhost:8964/
Client ('::1', 19425, 0, 0) lost — peer dropped the TLS connection suddenly, during handshake: (1, '[SSL: SSLV3_ALERT_CERTIFICATE_UNKNOWN] sslv3 alert certificate unknown (_ssl.c:992)')
::1:19426 - - [26/Apr/2025 17:47:18] "HTTP/1.1 OPTIONS /" - 204 No Content
{'action': 'execFunc', 'param': 'function1', 'pyParams': []}
::1:19426 - - [26/Apr/2025 17:47:18] "HTTP/1.1 POST /" - 200 OK
......