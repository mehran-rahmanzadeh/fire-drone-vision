# Fire Drone Vision Setup

### Setup HD & thermal cameras on raspberry pi

### Requirements

clone `v412loopback` repository
```shell
git clone https://github.com/umlaeute/v4l2loopback.git
```
build `v4l2loopback`
```shell
cd v4l2loopback
make
```
NOTE: if error occurs, try to run `sudo make install`
```shell
git clone https://github.com/fnoop/flirone-v4l2.git
```
build `flirone-v4l2`
```shell
cd flirone-v4l2
make
```
Now you can use implemented scripts to run cameras
```shell
sudo modprobe v4l2loopback devices=5
```
```shell
# in flirone-v4l2/
sudo ./flirone palettes/Iron2.raw
```
```shell
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

```
or simply run
```shell
sudo bash ./scripts/start_webcam.sh
```
Now you can access cameras throw these ways:
- HD: `udp://@:8554`
- Thermal: `/dev/video3`

Or you can use the given script:
```shell
bash ./scripts/show_all_cams.sh
```