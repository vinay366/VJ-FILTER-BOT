from __future__ import unicode_literals

import os, requests, asyncio, math, time, wget
from pyrogram import filters, Client
from pyrogram.types import Message
from info import CHNL_LNK
from youtube_search import YoutubeSearch
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL

from __future__ import unicode_literals
import os
import requests
import json
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL
from info import CHNL_LNK  # Your channel link or any other info

# Function to load cookies from the cookies.json file
def load_cookies(cookies_path="cookies.json"):
    if os.path.exists(cookies_path):
        with open(cookies_path, "r") as f:
            cookies = json.load(f)
        print("Cookies loaded successfully.")
        return cookies
    else:
        raise FileNotFoundError(f"Cookies file {cookies_path} not found.")

# Function to handle rate-limiting, retrying after flood waits
async def rate_limit_retry(func, *args, **kwargs):
    while True:
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if "FLOOD_WAIT" in str(e):
                wait_time = int(str(e).split()[-1])  # Get the wait time from error
                print(f"Rate-limited, retrying after {wait_time} seconds.")
                await asyncio.sleep(wait_time + 1)  # Wait for the specified time
            else:
                raise e  # Raise other exceptions

# Search YouTube and get the best result
def get_video_info(query):
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"]
        thumbnail = results[0]["thumbnails"][0]
        duration = results[0]["duration"]
        thumbnail_name = f'thumb_{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumbnail_name, 'wb').write(thumb.content)
        return link, title, duration, thumbnail_name
    except Exception as e:
        print(f"Error fetching video info: {str(e)}")
        return None, None, None, None

# Function to download audio (MP3 format)
def download_audio(url, output_path="audio.mp3"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegAudioConvertor',
            'preferredformat': 'mp3',
        }],
        'quiet': True,
        'nocheckcertificate': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            print(f"Error downloading audio: {str(e)}")

# Function to download video (MP4 format)
def download_video(url, output_path="video.mp4"):
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
        'quiet': True,
        'nocheckcertificate': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            print(f"Error downloading video: {str(e)}")

# Define the Pyrogram bot
app = Client("my_bot")

# Command for downloading audio
@app.on_message(filters.command('song', prefixes='/'))
async def song(client, message: Message):
    query = ' '.join(message.command[1:])
    if not query:
        await message.reply("Please provide a song name.")
        return
    
    await message.reply(f"Searching for {query} on YouTube...")
    
    link, title, duration, thumbnail_name = get_video_info(query)
    if not link:
        await message.reply("Couldn't find the song.")
        return

    await message.reply(f"Found: {title}\nDownloading audio...")

    # Download audio
    audio_file = f"{title}.mp3"
    download_audio(link, audio_file)

    await message.reply_audio(
        audio=open(audio_file, 'rb'),
        title=title,
        performer='Artist',  # You can change this if needed
        duration=duration,
        thumb=thumbnail_name,
        caption=f"Download link: {CHNL_LNK}"
    )

    # Cleanup
    os.remove(audio_file)
    os.remove(thumbnail_name)
    print("Audio sent and cleaned up.")

# Command for downloading video
@app.on_message(filters.command('video', prefixes='/'))
async def video(client, message: Message):
    query = ' '.join(message.command[1:])
    if not query:
        await message.reply("Please provide a video name.")
        return
    
    await message.reply(f"Searching for {query} on YouTube...")
    
    link, title, duration, thumbnail_name = get_video_info(query)
    if not link:
        await message.reply("Couldn't find the video.")
        return

    await message.reply(f"Found: {title}\nDownloading video...")

    # Download video
    video_file = f"{title}.mp4"
    download_video(link, video_file)

    await message.reply_video(
        video=open(video_file, 'rb'),
        caption=f"Download link: {CHNL_LNK}",
        thumb=thumbnail_name,
        title=title,
        duration=int(duration.split(':')[0])*60 + int(duration.split(':')[1]),
    )

    # Cleanup
    os.remove(video_file)
    os.remove(thumbnail_name)
    print("Video sent and cleaned up.")

