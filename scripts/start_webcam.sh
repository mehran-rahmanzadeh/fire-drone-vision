#!/bin/bash

START_PATH="/gp/gpWebcam/START?res="
STOP_PATH="/gp/gpWebcam/STOP"
FOV_PATH="/gp/gpWebcam/SETTINGS?fov="

GOPRO_RESOLUTION=1080
GOPRO_FOV_ID=0
GOPRO_FOV=wide

echo
echo activating webcam
echo

dev=$(ip -4 --oneline link | grep -v "state DOWN" | grep -v LOOPBACK | grep -v "NO-CARRIER" | cut -f2 -d":" | tail -1 | xargs)
GOPRO_DEVICE=${dev}

ip=$(ip -4 addr show dev ${GOPRO_DEVICE} | grep -Po '(?<=inet )[\d.]+')
GOPRO_IP=${ip}

mangled_ip=$(echo ${GOPRO_IP} | awk -F"." '{print $1"."$2"."$3".51"}')
GOPRO_INTERFACE_IP=$mangled_ip

echo GOPRO_INTERFACE_IP: ${GOPRO_INTERFACE_IP}


# Switching to the GoPro Webcam mode
response=$(curl -s ${GOPRO_INTERFACE_IP}${START_PATH}${GOPRO_RESOLUTION})
if [ $? -ne 0 ]; then
    echo "Error while starting the Webcam mode. ."
    exit 1
fi
echo $response
if [[ -z "${response}" ]]; then
    echo "Did not receive a valid response from your GoPro. Please try again to run this script, timing is sometimes crucial."
    exit 1
fi
response=$(curl -s ${GOPRO_INTERFACE_IP}${FOV_PATH}${GOPRO_FOV_ID})
echo $response
if [[ -z "${response}" ]]; then
    echo "Did not receive a valid response from your GoPro. Please try again to run this script, timing is sometimes crucial."
    exit 1
fi

echo "Successfully started the GoPro Webcam mode. (The icon on the Camera should have changed)"
