Используется для мониторинга выборки почты у сервисдесков. 
Если много писем в ящике, то есть проблемы с порталом или почтой.

Для отправки на Zabbix server используется скрипт powershell:\
Переменная $users может быть заполнена либо из OU, либо из CSV. 
В данном примере данные обновляются из OU при добавлении нового портала.

В файле C:\Program Files\Zabbix Agent\zabbix_agentd.conf.d\zbx-exchange.conf добавить строки:
```
UserParameter=mailboxitems.check,powershell -NoLogo -NoProfile -File "C:\Program Files\Zabbix Agent\scripts\mailbox_check.ps1"
```

Скопировать файл mailbox_item.ps1 и mailbox_check.ps1 в директорию C:\Program Files\Zabbix Agent\scripts\.
В файле указать путь до OU в переменной OU.

На сервере Exchange создать в планировщике задачу:
1) Имя задания "mailbox items"
2) Запуск от пользователя "СИСТЕМА";
3) Запуск программы "powershell" с параметрами "-File 'C:\Program Files\Zabbix Agent\scripts\mailbox_item.ps1'"