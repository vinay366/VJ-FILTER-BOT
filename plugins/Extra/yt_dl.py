from __future__ import unicode_literals

import os, requests, asyncio, math, time, wget
from pyrogram import filters, Client
from pyrogram.types import Message
from info import CHNL_LNK
from youtube_search import YoutubeSearch
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL

# Function to load cookies from the cookies.json file
def load_cookies(cookies_path="cookies.json"):
    if os.path.exists(cookies_path):
        with open(cookies_path, "r") as f:
            cookies = json.load(f)
        print("Cookies loaded successfully.")
        return cookies
    else:
        raise FileNotFoundError(f"Cookies file {cookies_path} not found.")

# Function to download the video or audio using cookies for authentication
def download_media_with_cookies(url, cookies_path="cookies.json", audio_only=False):
    cookies = load_cookies(cookies_path)
    
    ydl_opts = {
        "cookiefile": cookies_path,  # Use the cookies file for authentication
        "quiet": False,  # Enable verbosity to see logs
        "writeinfojson": True,  # Write metadata to a .json file
        "outtmpl": "%(title)s.%(ext)s",  # Output file name format
        "postprocessors": [],  # Default postprocessors
        "format": "bestaudio/best" if audio_only else "best",  # Download audio only if requested
        "geo_bypass": True,  # To bypass geo-restrictions
        "nocheckcertificate": True,  # To ignore SSL certificate errors
    }

    if audio_only:
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegAudioConvertor",  # Converts to the best audio format available
            "preferredformat": "mp3",  # Converts the audio to MP3
        }]
        ydl_opts["format"] = "bestaudio/best"

    with YoutubeDL(ydl_opts) as ydl:
        try:
            # Start downloading the video or audio
            ydl.download([url])
        except Exception as e:
            print(f"Error downloading video: {str(e)}")

# Function to extract the video URL or search query from the user's message
def get_video_url(message):
    text = message.strip()
    if text.startswith("http"):
        return text
    else:
        return f"https://www.youtube.com/results?search_query={message}"

# Function to get video information (metadata)
def get_video_info(url, cookies_path="cookies.json"):
    cookies = load_cookies(cookies_path)
    ydl_opts = {
        "cookiefile": cookies_path,
        "quiet": True,
        "writeinfojson": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=False)
            return info_dict
        except Exception as e:
            print(f"Error fetching video info: {str(e)}")
            return None

# Function to save video metadata to a JSON file
def save_metadata_to_json(info_dict, filename="video_metadata.json"):
    with open(filename, 'w') as f:
        json.dump(info_dict, f, indent=4)
    print(f"Metadata saved to {filename}.")

# The main bot code using Pyrogram
@Client.on_message(filters.command(['song', 'mp3']) & filters.private)
async def song(client, message):
    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"
    
    query = ' '.join(message.command[1:])
    print(f"Searching for song: {query}")
    
    m = await message.reply(f"**Searching your song...!\n{query}**")
    
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb_{title}.jpg'
        
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)
        
        performer = "[NETWORKS™]"
        duration = results[0]["duration"]
        
    except Exception as e:
        print(str(e))
        return await m.edit("Example: /song vaa vaathi song")
    
    await m.edit("**Downloading your song...!**")
    
    try:
        # Downloading using yt-dlp
        ydl_opts = {"format": "bestaudio[ext=m4a]"}
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        
        # Converting duration to seconds
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        
        cap = f"**BY›› [UPDATE]({CHNL_LNK})**"
        
        await message.reply_audio(
            audio_file,
            caption=cap,
            quote=False,
            title=title,
            duration=dur,
            performer=performer,
            thumb=thumb_name
        )
        
        await m.delete()

    except Exception as e:
        await m.edit("**🚫 Error downloading the song 🚫**")
        print(e)
    
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)


@Client.on_message(filters.command(["video", "mp4"]))
async def vsong(client, message: Message):
    urlissed = message.text.split(None, 1)[1] if len(message.text.split(None, 1)) > 1 else None
    if not urlissed:
        return await message.reply("Example: /video [Your video link]")
    
    pablo = await client.send_message(message.chat.id, f"**Finding your video...** `{urlissed}`")
    
    try:
        search = SearchVideos(urlissed, offset=1, mode="dict", max_results=1)
        video = search.result()["search_result"][0]
        
        video_url = video["link"]
        video_title = video["title"]
        video_id = video["id"]
        video_thumbnail = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        
        # Downloading the video thumbnail
        thumb_file = wget.download(video_thumbnail)
        
        # Video download options
        opts = {
            "format": "best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
            "outtmpl": f"{video_id}.mp4",
            "logtostderr": False,
            "quiet": True,
        }
        
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(video_url, download=True)
        
        file_stark = f"{ytdl_data['id']}.mp4"
        capy = f"""**TITLE :** [{video_title}]({video_url})\n**REQUESTED BY :** {message.from_user.mention}"""
        
        await client.send_video(
            message.chat.id,
            video=open(file_stark, "rb"),
            duration=int(ytdl_data["duration"]),
            file_name=str(ytdl_data["title"]),
            thumb=thumb_file,
            caption=capy,
            supports_streaming=True,        
            reply_to_message_id=message.id
        )
        
        await pablo.delete()
        os.remove(thumb_file)
        os.remove(file_stark)
    
    except Exception as e:
        await pablo.edit_text(f"**Download Failed, Try Again Later**\n**Error:** `{str(e)}`")
        print(f"Error: {e}")
