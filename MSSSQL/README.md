Для обнаружения баз используется скрипт powershell.

В папку C:\Program Files\Zabbix Agent\zabbix_agentd.conf.d поместить файл
zabbix_agentd.conf.d\userparameter_mssql.conf

В папку C:\Program Files\Zabbix Agent\scripts\ положить скрипт 
scripts\mssql_basename.ps1 (В переменную $Path прописать путь до файлов баз данных)

В Zabbix добавить шаблон и привязать его к хосту.
