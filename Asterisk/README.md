На сервере АТС выполняем следующие команды:

1. Создаем папку \
`mkdir /etc/zabbix/scripts`
  
 
2. Копируем файл на VOIP сервер в следующее раположение
`/etc/zabbix/scripts/asterisk_trunk_discovery.sh`

   
3. Назначаем права 
    ```shell
    chown zabbix.zabbix /etc/zabbix/scripts/asterisk_trunk_discovery.sh
    chmod 500 /etc/zabbix/scripts/asterisk_trunk_discovery.sh
    ```
   
4. Настраиваем sudo \
`echo -ne "\nzabbix ALL = NOPASSWD: /usr/sbin/asterisk\n" >> /etc/sudoers`
   

5. Настраиваем Zabbix агент
    ```shell
    echo -ne "UserParameter=asterisk_trunk_discovery[*],/etc/zabbix/scripts/asterisk_trunk_discovery.sh $1\n" \
    >> /etc/zabbix/zabbix_agentd.d/userparameter.conf
    ```


6. Перезапустить Zabbix агент
`systemctl restart zabbix-agent`
   

7. На сервере Zabbix установить шаблон zbx_export_templates.yaml и привязать к необходимому узлу
