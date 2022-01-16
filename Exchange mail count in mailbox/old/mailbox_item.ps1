<#
    .PARAMETER Mailbox
    Mailboxname (login in AD).
#>

Param (
    [Parameter(Position=0,Mandatory=$False)]$Mailbox
)

$OU = "ou=Servicedesk,ou=_Service,ou=_IT,ou=ORGSTAFF,dc=orgstaff,dc=com"

#Add Exchange management shell
$SnapinName = "Microsoft.Exchange.Management.PowerShell.SnapIn"
try {
    Add-PSSnapin -Name $SnapinName -ErrorAction Stop
} catch [Exception] {
    return -1
}

#Read users
$users = Get-ADUser -SearchBase $OU -filter 'Enabled -eq $true'

if ($Mailbox)
{
    #Return items in Inbox
    $itemvalue = Get-MailboxfolderStatistics $Mailbox -FolderScope Inbox -ErrorAction Silent #| fl ItemsInFolder
    $itemvalue = $itemvalue.ItemsInFolder
    Write-Output $itemvalue
}
else
{
    #Generate LLD
    $dict =  New-Object System.Collections.ArrayList
    For ($i=1; $i -le $($users.samaccountname | measure-object).Count; $i++) {
        $mailboxname = $users.samaccountname | Select-Object -first $i | Select-Object -last 1
        $dict.Add(@{"{#MAILBOXNAME}"=$mailboxname}) > $null
        }
    $res = @{"data"=$dict} | ConvertTo-Json
    Write-Output $res
}
