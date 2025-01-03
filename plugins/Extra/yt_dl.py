from __future__ import unicode_literals

import os, requests, asyncio, math, time, wget
from pyrogram import filters, Client
from pyrogram.types import Message
from info import CHNL_LNK
from youtube_search import YoutubeSearch
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL

# Function to load cookies from the cookies.json file (if required for authentication)
def load_cookies(cookies_path="cookies.json"):
    if os.path.exists(cookies_path):
        with open(cookies_path, "r") as f:
            cookies = json.load(f)
        print("Cookies loaded successfully.")
        return cookies
    else:
        print(f"No cookies file found at {cookies_path}. Proceeding without it.")
        return {}

# Search for the video or audio using yt-dlp and return the URL
def search_and_get_url(query):
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(f"ytsearch:{query}", download=False)
            if 'entries' in result:
                video = result['entries'][0]  # Get the first video result
                return video['url'], video['title'], video['duration']
            else:
                return None, None, None
        except Exception as e:
            print(f"Error in search: {str(e)}")
            return None, None, None

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

# Initialize the bot
app = Client("my_bot")

# Command for downloading audio
@app.on_message(filters.command('song', prefixes='/'))
async def song(client, message: Message):
    query = ' '.join(message.command[1:])
    if not query:
        await message.reply("Please provide a song name.")
        return
    
    await message.reply(f"Searching for {query} on YouTube...")
    
    # Get video URL, title, and duration from yt-dlp
    link, title, duration = search_and_get_url(query)
    if not link:
        await message.reply("Couldn't find the song.")
        return

    await message.reply(f"Found: {title}\nDownloading audio...")

    # Download audio (MP3 format)
    audio_file = f"{title}.mp3"
    download_audio(link, audio_file)

    # Send audio to the user
    await message.reply_audio(
        audio=open(audio_file, 'rb'),
        title=title,
        performer='Artist',  # You can change this if needed
        duration=duration,
        caption=f"Here is your song: {title}"
    )

    # Cleanup the files
    os.remove(audio_file)
    print("Audio sent and cleaned up.")

# Command for downloading video
@app.on_message(filters.command('video', prefixes='/'))
async def video(client, message: Message):
    query = ' '.join(message.command[1:])
    if not query:
        await message.reply("Please provide a video name.")
        return
    
    await message.reply(f"Searching for {query} on YouTube...")
    
    # Get video URL, title, and duration from yt-dlp
    link, title, duration = search_and_get_url(query)
    if not link:
        await message.reply("Couldn't find the video.")
        return

    await message.reply(f"Found: {title}\nDownloading video...")

    # Download video (MP4 format)
    video_file = f"{title}.mp4"
    download_video(link, video_file)

    # Send video to the user
    await message.reply_video(
        video=open(video_file, 'rb'),
        caption=f"Here is your video: {title}",
        duration=duration,
    )

    # Cleanup the files
    os.remove(video_file)
    print("Video sent and cleaned up.")

# Run the bot
if __name__ == "__main__":
    app.run()
