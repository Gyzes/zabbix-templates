$Path = "D:\BD"

function convertto-encoding ([string]$from, [string]$to){
    begin{
        $encfrom = [system.text.encoding]::getencoding($from)
        $encto = [system.text.encoding]::getencoding($to)
    }
    process{
        $bytes = $encto.getbytes($_)
        $bytes = [system.text.encoding]::convert($encfrom, $encto, $bytes)
        $encto.getstring($bytes)
    }
}

#Create list for JSON array.
$jsonlist = "{`n"
$jsonlist += " `"data`":[`n"

#Получили список баз. Записываем в переменную. / We get a list of databases. Write to the variable.
$basename = Get-ChildItem $Path

foreach ($name in $basename)
{
	if ($name.name -like "*.mdf") {
    	$jsonlist+= "{ `"{#DBNAME}`" : `"" + $name.name.replace(".mdf","") + "`", `"{#INST}`" : `"SQLServer" `
                    + $i + "`" }," | convertto-encoding "cp866" "utf-8"
	}
}


$jsonlist += "]"
$jsonlist += "}"

$jsonlist = $jsonlist.replace("},]}","}]}")

#Output array.
write-host $jsonlist
