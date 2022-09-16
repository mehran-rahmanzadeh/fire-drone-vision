sudo modprobe v4l2loopback devices=5

echo 'mod done'

sudo /home/pi/flirone-v4l2/flirone /home/pi/flirone-v4l2/palettes/Iron2.raw &

echo 'flir done'

sleep 5

echo 'sleep done'

python3 /home/pi/fire-drone-vision/scripts/show_flir.py
