#!/bin/bash

fun_error1(){
  echo "Ошибка! Отсутствуют параметры (trunks или ips или registration_monitoring)"
}
fun_error2(){
  echo "Ошибка! Отсутствуют параметры (название_транка)"
}

if [ $# -ne 0 ]
then
  case $1 in
    trunks_sip)
      /usr/bin/sudo asterisk -rx "sip show registry" | sed -e 1d -e '$d' | \
        awk -v ORS="" 'BEGIN { print "{\"data\":["} { print "{\"{#TRUNKNAME}\":\""$3"\"}," } END { print "]}" }' | \
        sed 's/,]}$/]}\n/' ;;

    trunks_iax)
      /usr/bin/sudo asterisk -rx "iax2 show registry" | sed -e 1d -e '$d' | \
        awk -v ORS="" 'BEGIN { print "{\"data\":["} { print "{\"{#TRUNKNAME}\":\""$3"\"}," } END { print "]}" }' | \
        sed 's/,]}$/]}\n/' ;;
    ips)
      (/usr/bin/sudo asterisk -rx "sip show registry" && /usr/bin/sudo asterisk -rx "iax2 show registry") | \
        sed -e 1d -e '$d' | grep '.*:.*' | awk ' BEGIN { print "{\"data\":[" } !seen[$1]++ { gsub(/:.+/, "", $1);
        print "{\"{#TRUNKIP}\":\""$1"\"}," } END { print "]}" }' | tr -d '\n' | sed 's/,]}$/]}\n/' ;;

    registration_monitoring_sip)
      if [ $# -eq 2 ]
      then
        stat=`/usr/bin/sudo asterisk -rx "sip show registry" | grep -w $2 | awk '{print $5}'`
        if [ $stat == 'Registered' ] || [ $stat == 'Request' ] ; then echo 1; else echo 0; fi;
      else
        fun_error2
      fi ;;

    registration_monitoring_iax)
      if [ $# -eq 2 ]
        then
          stat=`/usr/bin/sudo asterisk -rx "iax2 show registry" | grep -w $2 | awk '{print $6}'`
          if [ $stat == 'Rejected' ] || [ $stat == 'Request' ] ; then echo 1; else echo 0; fi;
          #/usr/bin/sudo asterisk -rx "iax2 show peers" | grep -w $2 | awk '{print $7}'
        else
          fun_error2
        fi ;;
      *)
        fun_error1 ;;
    esac
else
  fun_error1
fi
