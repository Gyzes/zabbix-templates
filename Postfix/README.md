Для мониторинга postfix понадобится установить на почтовом сервере следующие пакеты:

**logcheck** - позволяет просматривать лог с того места, где остановился в прошлый раз
**postfix-perl-scripts** - содержит скрипты для анализа файла логов

`yum install logcheck postfix-perl-scripts`

Скопировать файл postfix-zabbix-stats.sh в директорию /etc/zabbix/zabbix_scripts/

В файл /etc/crontab добавить строчку:\
`*/10 * * * * root bash /etc/zabbix/zabbix_scripts/postfix-zabbix-stats.sh`

В файле /etc/sudoers добавить строчку:\
`zabbix ALL = NOPASSWD: /usr/sbin/pflogsumm, /usr/sbin/logtail`

В файле /etc/zabbix/zabbix_agentd.d/userparameter.conf добавить текст:
```
UserParameter=postfix[*],/etc/zabbix/zabbix_scripts/postfix-zabbix-stats.sh $1
UserParameter=postfix.queue,mailq | grep -v "Mail queue is empty" | grep -c '^[0-9A-Z]'
```

На zabbix сервере загрузить шаблон и привязать его к хосту:
