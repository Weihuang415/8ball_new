# 8ball

**Operating System:** 
- Debian GNU/Linux 11 (bullseye)
  - Rapberry Pi OS (64-bit)
- Raspberry Pi Zero W 2
  
  - username: pi
  - password: new8ball
  - hostname: new8ball

**Notion**

- [NightLight Labs Notion](https://www.notion.so/nightlight/Divin8tion-4ac8bdd7f42d4dee9b319b0bb917112e)

**Install git and python3:**

    sudo apt-get update
    sudo apt-get install git
    sudo apt install python3 (raspberry pi os buster version is python2.7 default)


## HyperPixel 2.0" Round Drivers for Raspberry Pi 4 ##
- **HyperPixel Product Page:** [HyperPixel 2.0" Round](https://shop.pimoroni.com/products/hyperpixel-round?variant=39381081882707)  
- **HyperPixel Drivers Original Github:** [HyperPixel 2.0" Round Drivers for Raspberry Pi 4](https://github.com/pimoroni/hyperpixel2r)
- **Official Tutorial:** [Getting Started with HyperPixel 4.0](https://learn.pimoroni.com/article/getting-started-with-hyperpixel-4)

- Installing / Uninstalling
First, clone this GitHub repository branch to your Pi:

		git clone https://github.com/pimoroni/hyperpixel2r
- Then run the installer to install:

		cd hyperpixel2r
		sudo ./install.sh
  
> **NOTE:** In the [this YouTube tutorial](https://youtu.be/OkNh8wXZtR0), he said, "The Pimoroni HyperPixel2r display drivers are for **Raspberry Pi OS Buster** only", but Raspberry Pi OS Buster doesn’t work with newest vlc player version(3.0.18)!!


## Requirements ##
**python packages:**
- google-api-python-client
- yt-dlp
- python-vlc 
- mpu6050-raspberrypi
- requests
- pynput (python3 & X server required)
- python3-smbus (apt install)
  
**Install python packages using *apt & pip***

    pip install -r requirements.txt
    sudo apt install python3-smbus
    sudo apt install vlc

    
### MPU 6050 accelerometer ###
- enable I2C in raspberry config
- check your smbus (mine is 11)
- install the example python file
 > **NOTE:** be careful about the file path of the mpu6050 module --> from mpu6050 import mpu6050


**Install mpu 6050 library:**

    sudo apt install python3-smbus
    pip install mpu6050-raspberrypi


### Kalman Filter ###

- **[Kalman Filter for mpu6050 Library:](https://github.com/rocheparadox/Kalman-Filter-Python-for-mpu6050/tree/master)** Since the detected value is "angular velocity", I use Kalman Filter to get the "angle" value.

> **NOTE:** The Kalman Filter Library is modified as no while loop in 8ball.



### Enable I2C ###

**Interface Option:**

    sudo raspi-congif
    
**To do an I2C scan on a Raspberry Pi:**  

    sudo apt-get install i2c-tools

**Test if you get the i2c:**  

*0 —> I2C is on*  
*1 —> I2C is off*  
    
    sudo raspi-config nonint get_i2c

**detect i2c address:**

> [**How to Scan and Detect I2C Addresses**](https://learn.adafruit.com/scanning-i2c-addresses/raspberry-pi)

> Run the following command to list all available I2C buses:

    ls /dev/i2c-*
    
**Here use bus 11**
    
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



### YouTube API ###

**Install the googleapiclient package:** 

    pip install google-api-python-client
    
> [YouTube Data API | Videos: list](https://developers.google.com/youtube/v3/docs/videos/list)




### YouTube download video ###

**Install the youtube_dlp package:**

    pip install yt-dlp

> **[yt-dlp Official Github](https://github.com/yt-dlp/yt-dlp)**

> **Options:** https://github.com/yt-dlp/yt-dlp#download-options

> **[Filtering Formats:](https://github.com/yt-dlp/yt-dlp#filtering-formats)**
You can filter the video formats by putting a condition in brackets, as in `-f "best[height=720]"` (or `-f "[filesize>10M]"` since filters without a selector are interpreted as `best`).

>**NOTE:** Downloading (yt-dlp) is separate from Searching(YouTube API). 
The yt-dlp filter will not apply to API searching but only downloading part. The filter finds the videos that have been searched and see if that satisfy the filter



### VLC media player ###

**Install the vlc package:**

    pip install python-vlc
    sudo apt install vlc

- Set up the password before connecting to the server
  - User name: None
  - Password: asdf



## Save log in txt file ##
    
**Redirections for both standard error (stderr) and standard output (stdout):**
    
    python main.py > output.log 2>&1
    
**Create a file named output.log**
    
    touch output.log




