Для мониторинга Cisco Stack потребуются следующие mib:\
    - CISCO-SMI.mib\
    - CISCO-STACKWISE-MIB.mib\
    - CISCO-TC.mib\
    - ENTITY-MIB.mib


Эти файлы необходимо разместить в директории /usr/share/snmp/mibs 
на сервере с которого выполняется запрос (zabbix server или proxy)


В сам zabbix необходимо добавить шаблон и привязать его к стекирумому коммутатору.
