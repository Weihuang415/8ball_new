# 8ball_new
Organized folder! compared to the old 8ball

pip install -r requirements.txt
pip3 install --upgrade yt-dlp

## Requirements ##
- google-api-python-client
- yt-dlp
- python-vlc
- pmpu6050-raspberrypi
- requests
- pynput

> pip install -r requirements.txt

> sudo apt install python3-smbus


### MPU 6050 ###
- enable I2C in raspberry config
- check your smbus (mine is 11)
- install the example package

  > sudo apt install python3-smbus
   
   > pip install mpu6050-raspberrypi

! be careful about the file path of the mpu6050 module #from mpu6050 import mpu6050


### youtube API ###
- Install the googleapiclient package** 

  > pip install google-api-python-client


### yt_dlp ###
- Install the youtube_dlp package**

  > pip install yt-dlp


### VLC media player ###
- install the vlc package (32 bits)

  > using 'pip install python-vlc'

