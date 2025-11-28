# REPLACE HUMAN HEADS WITH CAT HEADS

In this project we aim to utilize the camera on 
a Raspberry Pi to detect human heads and substitute them
with cat heads.

## How to setup
- Install requirements
    - sudo apt install -y python3-opencv
    - sudo apt-get install python3-picamera2
    - pip3 install numpy --break-system-packages

- Download haarcascade (Remove after stable url)
    - wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml 


## Common Issues
- Window not appearing
    - Check display: echo $DISPLAY
    - Allow X11 forwarding over  SSH: ssh -X pi@raspberry

