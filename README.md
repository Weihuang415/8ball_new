# 8ball

## Requirements ##
**python packages:**
- google-api-python-client
- yt-dlp
- python-vlc
- pmpu6050-raspberrypi
- requests
- pynput
- python3-smbus (apt install)
  
**Install python packages using *apt & pip* install:**

    pip install -r requirements.txt
    sudo apt install python3-smbus
    
### MPU 6050 ###
- enable I2C in raspberry config
- check your smbus (mine is 11)
- install the example python file
  - be careful about the file path of the mpu6050 module --> from mpu6050 import mpu6050

**Install *mpu 6050 accelerometer* library:**

    sudo apt install python3-smbus
    pip install mpu6050-raspberrypi


### youtube API ###

**Install the googleapiclient package:** 

    pip install google-api-python-client


### yoututbe download video ###

**Install the youtube_dlp package:**

    pip install yt-dlp


### VLC media player ###

**Install the vlc package (32 bits):**

    pip install python-vlc

