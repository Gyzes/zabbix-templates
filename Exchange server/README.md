Для обнаружения баз используется скрипт powershell.\ 
Так как подключение к Exchange занимает время, 
то в C:\Program Files\Zabbix Agent\zabbix_agentd.conf необходимо изменить таймаут:\
`Timeout=30`

В папку C:\Program Files\Zabbix Agent\zabbix_agentd.conf.d скопировать файл  zabbix_agentd.conf.d\zbx-exchange.conf

В папку C:\Program Files\Zabbix Agent\scripts\ скопировать файл scripts\zbx-exchange.ps1

В Zabbix добавить шаблон и привязать его к хосту.
