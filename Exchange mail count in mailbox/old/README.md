Используется для мониторинга выборки почты у сервисдесков. 
Если много писем в ящике, то есть проблемы с порталом или почтой.

Для отправки на Zabbix server используется скрипт powershell:\
Переменная $users может быть заполнена либо из OU, либо из CSV. 
В данном примере данные обновляются из OU при добавлении нового портала.

В файле C:\Program Files\Zabbix Agent\zabbix_agentd.conf.d\zbx-exchange.conf добавить строки:
```
UserParameter=mailboxitems.discovery,powershell -NoLogo -NoProfile -File "C:\Program Files\Zabbix Agent\scripts\mailbox_item.ps1"
UserParameter=mailboxitems[*],powershell -NoLogo -NoProfile -File "C:\Program Files\Zabbix Agent\scripts\mailbox_item.ps1" -Mailbox "$1"
```

Скопировать файл mailbox_item.ps1 в директорию C:\Program Files\Zabbix Agent\scripts\
В файле указать путь до OU в переменной OU.
