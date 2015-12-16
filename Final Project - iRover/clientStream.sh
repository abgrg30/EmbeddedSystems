rm -rf fifo
mkfifo fifo
gst-launch -v udpsrc port=2000 !  jpegdec ! ffmpegcolorspace ! 'video/x-raw-yuv,format=(fourcc)I420' ! ffenc_mpeg4 ! filesink location=fifo
