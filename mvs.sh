#!/bin/bash
# This script will copy the config file, edit it and move dasd
# to the /config and /dasd volume if they don't already exist
# Then it will boot MVS/CE

# Does the hercules config file exist?
# If not, copy the config from MVS/CE
# and replace the folder location with
# volume names
if [ ! -f /config/local.cnf ]; then
    echo "[*] /config/local.cnf does not exist... generating"
    sed 's_DASD/_/dasd/_g' MVSCE/conf/local.cnf > /config/local.cnf
    sed -i 's_punchcards/_/punchcards/_g' /config/local.cnf
    sed -i 's_printers/_/printers/_g' /config/local.cnf
    sed -i 's_mvslog.txt_/logs/mvslog.txt_g' /config/local.cnf
    sed -i 's_localhost_0.0.0.0_g' /config/local.cnf
    sed -i 's_localhost_0.0.0.0_g' /config/local.cnf
    sed -i 's_conf/local/_/config/local/_g' /config/local.cnf
    echo "" >> /config/local.cnf
    echo "#################################" >> /config/local.cnf
    echo "# Adding HTTP server for Docker" >> /config/local.cnf
    echo 'HTTP   PORT 8888 AUTH ${HUSER:=hercules} ${HPASS:=hercules}' >> /config/local.cnf
    echo "HTTP   START" >> /config/local.cnf
fi

if [ ! -f /config/local/custom.cnf ]; then
    echo "[*] /config/local/custom.cnf does not exist... generating"
    mkdir -p /config/local/
    sed 's_conf/local/_/config/local/_g' MVSCE/conf/local/custom.cnf > /config/local/custom.cnf
fi

for conf in MVSCE/conf/local/*; do 
    if  cmp -s "$conf" "/config/local/$(basename $conf)" ; then 
        echo "[*] /config/local/$(basename $conf) no changes"
    else 
        # Check which file is newer
        if [ "$conf" -nt "/config/local/$(basename $conf)" ]; then
            # backup the previous config if it exists
            cp "/config/local/$(basename $conf)" "/config/local/$(basename $conf).bak" 2>/dev/null
            cp "$conf" "/config/local/$(basename $conf)"
            sed 's_conf/local/_/config/local/_g' -i "/config/local/$(basename $conf)"
            # check to make sure the config exists in custom.cnf
            if $(grep -L "/config/local/$(basename $conf)" /config/local/custom.cnf) ; then
                # if not then we add it   
                echo "INCLUDE /config/local/$(basename $conf)" >> /config/local/custom.cnf
            fi
        fi
    fi
done 



for disk in MVSCE/DASD/*; do
    if [ ! -f /dasd/$(basename $disk) ]; then
        echo "[*] Copying $disk"
        cp -v $disk /dasd/
    fi
done

if [ ! -f /certs/ftp.pem ]; then
    echo "[*] /certs/ftp.pem does not exist... generating"
    openssl req -x509 -nodes -days 365 \
    -subj  "/C=CA/ST=QC/O=FTPD Inc/CN=hercules.ftp" \
     -newkey rsa:2048 -keyout /certs/ftp.key \
     -out /certs/ftp.crt
     cat /certs/ftp.key /certs/ftp.crt > /certs/ftp.pem

fi


if [ ! -f /certs/3270.pem ]; then
    echo "[*] /certs/3270.pem does not exist... generating"
    openssl req -x509 -nodes -days 365 \
    -subj  "/C=CA/ST=QC/O=TN3270 Inc/CN=hercules.3270" \
     -newkey rsa:2048 -keyout /certs/3270.key \
     -out /certs/3270.crt
     cat /certs/3270.key /certs/3270.crt > /certs/3270.pem

fi

echo "[*] Starting encrypted FTP listener on port 3221"
( socat openssl-listen:3221,cert=/certs/ftp.pem,verify=0,reuseaddr,fork tcp4:127.0.0.1:2121 ) &
echo "[*] Starting encrypted TN3270 listener on port 3223"
( socat openssl-listen:3223,cert=/certs/3270.pem,verify=0,reuseaddr,fork tcp4:127.0.0.1:3270 ) &

echo "[*] Starting Unencrypted TN3270 listener on port 21021"
socat -v TCP4-LISTEN:21021,reuseaddr,fork tcp4:127.0.0.1:2121 &

echo "[*] Launching web3270"
cd /web3270
python3 -u /web3270/server.py --config /config --certs /certs &
cd /MVSCE
echo "[*] Starting Hercules"
hercules -f /config/local.cnf -r conf/mvsce.rc --daemon > /logs/hercules.log