#! /usr/bin/bash


sudo rfkill unblock bluetooth
sleep 1

bluetoothctl <<EOF
power on
EOF

sleep 1

bluetoothctl <<EOF
pair mac address
EOF

sudo rfcomm bind 0 mac address

pipenv run python yacm_cli.py /dev/rfcomm0

sudo rfcomm release 0

bluetoothctl <<EOF
power off
EOF
