В папке /usr/lib/zabbix/externalscripts на zabbix сервере разместить файл zoom.py

В zabbix сервере создать хост (без разницы с каким интерфейсом) и привязать шаблон

В макросах хоста прописать актуальные параметры:

          macro: '{$TOKEN}'
          value: '12345'

Токен необходимо получить в маркетплейсе Zoom (jwe app).
Подробная информация тут: https://marketplace.zoom.us/docs/guides/auth/jwt
