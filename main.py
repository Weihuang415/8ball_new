import asyncio
import random
import glob
import os

# from pynput.keyboard import Key, Controller
from pynput import keyboard

import requests
import multiprocessing
from time import sleep, time

import yt_dlp
from base64 import b64encode
from googleapiclient.discovery import build

from mpu6050 import mpu6050
sensor = mpu6050(0x68)

prefix = ['IMG ', 'IMG_', 'IMG-', 'DSC ']
postfix = [' MOV', '.MOV', ' .MOV']
DEVELOPER_KEY = 'AIzaSyCGp2bkWFADc2zcHr_VPMl6W8CVbbs1IJc'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

pickedVid = ''
cachedVids = glob.glob('VideoDL/*.mp4')
# cachedVids = [os.path.basename(file) for file in glob.glob('VideoDL/*.mp4')] #good-looking filename without VideoDL/

print("cachedVids:", cachedVids)
output_dir = 'VideoDL'

played = False
playing = False
screenUp = False
canFlip = False

searchResult = []
i_search = 0


# YouTube Search
def youtube_search():
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    videos_search = []

    while len(videos_search) < 5:  # once it has 5 searching results
        try:
            search_response = youtube.search().list(
                q=random.choice(prefix) + str(random.randint(999, 9999)) + random.choice(postfix),
                part='snippet',
                type="video",
                videoDefinition="standard",
                videoDimension="2d",
                videoDuration="short",
                maxResults=10
            ).execute()

            for search_result in search_response.get('items', []):
                videos_search.append(search_result['id']['videoId'])

        except Exception as e:
            print(e)
    print('videos_search:', videos_search)
    return videos_search


# Download
async def download_vid():
    global searchResult
    print("S", searchResult)
    # searchResult = youtube_search()

    video_id = searchResult[i_search]
    if video_id:
        url = "https://www.youtube.com/watch?v=" + video_id
        print(url)
        print("i", i_search)

        ydl_opts = {
            'format': 'mp4[height<540]',
            'logger': MyLogger(),
            'nocheckcertificate': True,
            'progress_hooks': [my_hook],
            # 'outtmpl': + str(int(time.time()))[-4:] + '_'+ video_id + '.mp4'
            'outtmpl': os.path.join(output_dir, 'yt_' + str(int(time.time()))[-6:] + '_' + str(video_id)[4:] + '.mp4')
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            global cachedVids
            cachedVids = sorted(glob.glob('VideoDL/*.mp4'))

    else:
        print("No suitable videos found.")


class MyLogger(object):
    def debug(self, msg):
        print(msg)
        pass

    def warning(self, msg):
        print(msg)
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        global cachedVids
        cachedVids = sorted(glob.glob('*.mp4'))
        print('Done downloading, now converting ...')
        # print("vids: " + str(cachedVids))


# VLC player opens (multiprocess)
def vlc_open():
    global playing
    video_process = multiprocessing.Process(target=play_video_process, args=(pickedVid,))
    video_process.start()


def play_video_process(pickedVid):  # VideoDefault/default2.mp4 #VideoDL/{pickedVid}
    vlc_cmd = f'"C:/Program Files (x86)/VideoLAN/VLC/vlc.exe" --repeat --extraintf=http --http-host=127.0.0.1 --http-port=8080 --http-password=asdf {os.path.abspath(pickedVid)}'
    os.system(vlc_cmd)
    # vlc_cmd = f"cvlc {os.path.abspath(pickedVid)} --fullscreen --repeat --extraintf=http --http-host=127.0.0.1 --http-port=8080 --http-password=asdf"
    print("Video_process", pickedVid)


# Http setting
def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'


# Play a Video
def play_next():
    global playing
    global played
    global pickedVid
    cachedVids = glob.glob('VideoDL/*.mp4')

    if cachedVids:
        playing = True
        # Playthe First one
        pickedVid = cachedVids[0]
        play_url = f'http://127.0.0.1:8080/requests/status.json'
        headers = {'Authorization': basic_auth("", "asdf")}
        params = {'command': 'in_play', 'input': os.path.abspath(pickedVid)}
        response = requests.get(play_url, headers=headers, params=params)
        if response.status_code == 200:
            print(f'VLC is now playing the picked video: {pickedVid}')
            os.system("cls")
        else:
            print(f'Failed to play the picked video. Status code: {response.status_code}')
    else:
        print("No videos available.")


# Stop the Video
def stop_playing():
    global played
    global playing
    global pickedVid

    if playing:

        play_url = f'http://127.0.0.1:8080/requests/status.json'
        headers = {'Authorization': basic_auth("", "asdf")}

        # Stop Video
        params = {'command': 'pl_stop', 'input': os.path.abspath(pickedVid)}
        response = requests.get(play_url, headers=headers, params=params)
        if response.status_code == 200:
            print(f'VLC stoped the picked video: {pickedVid}')
        else:
            print(f'Failed to stop the picked video. Status code: {response.status_code}')

        # Play default video
        defaultVid = 'VideoDefault\Default2.mp4'
        params = {'command': 'in_play', 'input': os.path.abspath(defaultVid)}
        response = requests.get(play_url, headers=headers, params=params)
        if response.status_code == 200:
            print(f'VLC is now playing the default video: {defaultVid}')
        else:
            print(f'Failed to play the default video. Status code: {response.status_code}')

        sleep(2)  # delay between default video and picked video

        played = True

    else:
        print("No videos playing.")


def delete_video():
    cachedVids = glob.glob('VideoDL/*.mp4')
    if played:
        print(f"{cachedVids[0]} --- Removing the played video.")

        os.remove(cachedVids[0])  # remove the file in VideoDL folder
        print(f"{cachedVids[0]} --- Removed.")

        cachedVids.pop(0)  # remove from the list
        print(f"{cachedVids[0]} --- first video in cachedVids.")


def sensor_detect(key):
    global screenUp
    kalAngleZ = angle_read()
    # if key == 'u':
    #     screenUp = True
    # elif key == 'd':
    #     screenUp = False

    if 30 > kalAngleZ > -30:
        screenUp = True
    else:
        screenUp = False
    # return kalAngleZ


async def main_loop():
    global canFlip, screenUp, i_search, searchResult
    background_tasks = set()

    while True:
        # sensorDetect()
        if screenUp is False:  # it's down
            if canFlip is False:
                print('---Down---')
                stop_playing()
                delete_video()

                loop = asyncio.get_event_loop()
                task = loop.create_task(download_vid())
                background_tasks.add(task)

                # asyncio.run(Tasks())
                canFlip = True

        else:  # It's up
            if canFlip is True:
                print('up')

                play_next()

                i_search += 1
                print("index:", i_search)
                if i_search >= 3:
                    i_search = 0
                    searchResult = youtube_search()
                canFlip = False  # Set it to False after playing the videos
        await asyncio.sleep(0.04)


def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
        sensor_detect(key.char)
    except AttributeError:
        print('special key {0} pressed'.format(
            key))


def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


if __name__ == '__main__':
    vlc_open()
    searchResult = youtube_search()

    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()

    asyncio.run(main_loop())
