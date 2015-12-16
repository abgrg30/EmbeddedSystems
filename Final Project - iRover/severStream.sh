## This is meant to run on the beaglebone to capture video
gst-launch v4l2src ! image/jpeg,framerate=30/1,width=320,height=240 ! udpsink host=192.168.43.198 port=2000
