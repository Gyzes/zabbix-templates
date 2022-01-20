
PARAM (
    [String]$ZABBIXSERVER,
    [Int]$ZABBIXPORT
)

$HWS = Get-WmiObject -Namespace root\openhardwaremonitor -class hardware
$SensorsTypes = ('load', 'voltage', 'power', 'fan', 'control', 'temperature', 'clock', 'data', 'smallData', 'throughput' )

ForEach ( $HW in $HWS ) {
    ForEach ( $Type in $SensorsTypes ) {
        $Filter = "SensorType='" + $Type + "' And Parent='" + $HW.Identifier + "'"
        $Sensors = Get-WmiObject -Namespace root\openhardwaremonitor -class sensor -Filter $Filter
        ForEach ( $Sensor in $Sensors ) {
            $data = ('{"data":[{"{#IDENTIFIER}":"'+$Sensor.Identifier+'","{#HWNAME}":"'+$HW.Name+'","{#NAME}":"'+$Sensor.Name+'"}]}').Replace(" ","_") | ConvertTo-Json
            $key = "hardware.sensors." + $Type
            C:\"Program Files"\"Zabbix Agent"\zabbix_sender.exe -z $ZABBIXSERVER -p $ZABBIXPORT -s $HW.__SERVER -k $key -o $data
            
            $key = "hardware.sensor." + $Type + '[' + $Sensor.Identifier + ']'
            C:\"Program Files"\"Zabbix Agent"\zabbix_sender.exe -z $ZABBIXSERVER -p $ZABBIXPORT -s $HW.__SERVER -k $key -o $Sensor.Value
        }
    }
}
