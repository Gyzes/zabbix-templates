В папке /usr/lib/zabbix/externalscripts на zabbix сервере разместить файл certs_check.py

Для работы скрипта понадобится установить дополнительную библиотеку:
```shell
pip3 install bs4
```

В zabbix сервере создать хост (без разницы с каким интерфейсом) и привязать шаблон

В макросах хоста прописать актуальные параметры:

          macro: '{$PAGEID}'
          value: '12345'

          macro: '{$PASSWORD}'
          value: password

          macro: '{$URL}'
          value: 'https://confluence.example.com'

          macro: '{$USERNAME}'
          value: username
