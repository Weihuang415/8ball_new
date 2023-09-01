# 8ball

**Operating System:** 
- Debian GNU/Linux 11 (bullseye)
- Raspberry Pi Zero W 2
  - username: pi
  - password: new8ball
  - hostname: new8ball

**Install git and python3:**

	  sudo apt-get update
	  sudo apt-get install git
	  sudo apt install python3


## HyperPixel 2.0" Round Drivers for Raspberry Pi 4 ##
https://shop.pimoroni.com/products/hyperpixel-round?variant=39381081882707
- Installing / Uninstalling
First, clone this GitHub repository branch to your Pi:

		git clone https://github.com/pimoroni/hyperpixel2r
- Then run the installer to install:

		cd hyperpixel2r
		sudo ./install.sh


## Requirements ##
**python packages:**
- google-api-python-client
- yt-dlp
- python-vlc 
- mpu6050-raspberrypi
- requests
- pynput (python3 required)
- python3-smbus (apt install)
  
**Install python packages using *apt & pip* install:**

    pip install -r requirements.txt
    sudo apt install python3-smbus
		sudo apt install vlc
    
### MPU 6050 ###
- enable I2C in raspberry config
- check your smbus (mine is 11)
- install the example python file
 > **NOTE** be careful about the file path of the mpu6050 module --> from mpu6050 import mpu6050

**Install *mpu 6050 accelerometer* library:**

    sudo apt install python3-smbus
    pip install mpu6050-raspberrypi
    
### Enable I2C ###

Interface Option:

    sudo raspi-congif
    
test if you get the i2c:
    
    sudo raspi-config nonint get_i2c

detect i2c address:
    
    sudo i2cdetect -y 11
    
    /* Outcome
    0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    00:                         -- -- -- -- -- -- -- -- 
    10: -- -- -- -- -- UU -- -- -- -- -- -- -- -- -- -- 
    20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    60: -- -- -- -- -- -- -- -- 68 -- -- -- -- -- -- -- 
    70: -- -- -- -- -- -- -- --*/

### youtube API ###

**Install the googleapiclient package:** 

    pip install google-api-python-client


### yoututbe download video ###

**Install the youtube_dlp package:**
https://github.com/yt-dlp/yt-dlp#download-options
    
    pip install yt-dlp


### VLC media player ###

**Install the vlc package:**

    pip install python-vlc
		sudo apt install vlc

Set up the password before connecting to the server


Set up the password before connecting to the server
