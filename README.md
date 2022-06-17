# asyncronous port scanner with aiohttp

## requirements:
- python=3.10+
- aiohttp==3.8.1
- loguru==0.6.0

## testing requirements:
- pytest==7.1.2
- pytest-aiohttp==1.0.4

## starting:
```sh
python app.py
```

## testing:
```sh
pytest tests.py
```
## using:
server starts on http://127.0.0.1:5462

## GET requests format:
```
/scan/{ip}/{begin_port}/{end_port}
```
ports are non-negative integers
## output format:
[{"port":begin_port, "state": ("open"|"close")}, ..., {"port":end_port, "state": ("open"|"close")}]
