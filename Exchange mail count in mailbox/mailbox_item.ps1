$OU = "ou=servicedesks,ou=_services,ou=_accounts,ou=_it,ou=open,dc=open-com,dc=ru"

#Add Exchange management shell
$SnapinName = "Microsoft.Exchange.Management.PowerShell.SnapIn"
try {
    Add-PSSnapin -Name $SnapinName -ErrorAction Stop
} catch [Exception] {
    return -1
}

#Read users
$users = Get-ADUser -SearchBase $OU -filter { mail -ge 0 }

For ($i=1; $i -le $($users.samaccountname | measure-object).Count; $i++) {
    $Mailbox = $users.samaccountname | Select-Object -first $i | Select-Object -last 1
    $itemvalue = Get-MailboxfolderStatistics $Mailbox -FolderScope Inbox -ErrorAction Silent
    $itemvalue = $itemvalue.ItemsInFolder
    $data = '{\"data\":[{\"{#MAILBOXNAME}\":\"'+$mailbox+'\"}]}'
    C:\"Program Files"\"Zabbix Agent"\zabbix_sender.exe -z SRV-ZBX01 -p 10051 -s $env:COMPUTERNAME `
        -k "mailboxitems.discovery" -o $data --tls-connect psk  --tls-psk-identity Agent `
        --tls-psk-file C:\"Program Files"\"Zabbix Agent"\key.psk
    C:\"Program Files"\"Zabbix Agent"\zabbix_sender.exe -z SRV-ZBX01 -p 10051 -s $env:COMPUTERNAME `
        -k "mailboxitems[$mailbox]"  -o "$itemvalue" --tls-connect psk  --tls-psk-identity Agent `
        --tls-psk-file C:\"Program Files"\"Zabbix Agent"\key.psk
    }
