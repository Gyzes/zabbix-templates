Для обнаружения сенсоров используется скрипт powershell.
Для работы шаблона на хосте должен быть запущен [openhardwaremonitor](https://github.com/openhardwaremonitor/openhardwaremonitor)

В папку `C:\Program Files\Zabbix Agent\zabbix_agentd.conf.d` поместить файл
`zabbix_agentd.conf.d\sensors.conf`

В папку` C:\Program Files\Zabbix Agent\scripts\` положить скрипт `scripts\sensors.ps1`

В Zabbix добавить шаблон и привязать его к хосту.

У шаблона или хоста прописать макросы
| Имя макроса        | Значение по умолчанию |
| ------------------ | --------------------- |
| {$ZABBIX_HOST}     | zabbix                | 
| {$ZABBIX_PORT}     | 10051                 |
| {$TEMP_HIGH}       | 70                    |
