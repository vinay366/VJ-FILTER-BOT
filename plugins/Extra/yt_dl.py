from __future__ import unicode_literals

import os, requests, asyncio, math, time, wget
from pyrogram import filters, Client
from pyrogram.types import Message
from info import CHNL_LNK
from youtube_search import YoutubeSearch
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL

from yt_dlp import YoutubeDL
import os
import requests

# Path to the cookies.json file
cookies_file = 'https://github.com/Partik1165/UMESH-BOT/blob/6f3ea46d1bbc47e9a60992bc72ffbe78dac93b23/cookies.json'  # Replace with your actual path

# yt-dlp options with cookie file
ydl_opts = {
    "format": "bestaudio[ext=m4a]",
    "cookiefile": cookies_file  # Pass the cookies file here
}

# Example search query (song title)
query = "Shape of You Ed Sheeran"

# Search for the song using yt-dlp
with YoutubeDL(ydl_opts) as ydl:
    # Extract video information without downloading it
    try:
        info_dict = ydl.extract_info(f"ytsearch:{query}", download=False)
        # Choose the first result (if available)
        video_url = info_dict['entries'][0]['url']
        
        # Download the audio
        print("Downloading audio...")
        ydl.download([video_url])
    except Exception as e:
        print(f"Error: {str(e)}")

                os.remove(thumb_name)
        except Exception as e:
            print(f"Error deleting temporary files: {e}")


