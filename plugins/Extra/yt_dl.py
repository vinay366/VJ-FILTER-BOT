from __future__ import unicode_literals

import os, requests, asyncio, math, time, wget
from pyrogram import filters, Client
from pyrogram.types import Message
from info import CHNL_LNK
from youtube_search import YoutubeSearch
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL

# Replace with the actual path to your cookies.json file
COOKIES_FILE = "https://github.com/Partik1165/UMESH-BOT/blob/6f3ea46d1bbc47e9a60992bc72ffbe78dac93b23/cookies.json"

# Function to download song using yt-dlp
@Client.on_message(filters.command(['song', 'mp3']) & filters.private)
async def song(client, message):
    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    
    # Extract query from message
    query = ' '.join(message.command[1:])
    print(query)
    
    # Sending initial message to user
    m = await message.reply(f"**Searching for your song...!**\n{query}")
    
    # yt-dlp options
    ydl_opts = {
        "format": "bestaudio[ext=m4a]",
        "cookiefile": COOKIES_FILE  # Load cookies from file
    }

    try:
        # Search for the song using YoutubeSearch
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb_{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)
        performer = "[NETWORKS™]"
        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]
    except Exception as e:
        print(str(e))
        return await m.edit("**Error while searching for the song**")

    await m.edit("**Downloading your song...!**")

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)

        cap = f"**BY›› [UPDATE]({CHNL_LNK})**"
        
        # Convert duration to seconds
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        
        # Send the audio file
        await message.reply_audio(
            audio_file,
            caption=cap,
            quote=False,
            title=title,
            duration=dur,
            performer=performer,
            thumb=thumb_name
        )

        # Delete temporary files
        os.remove(audio_file)
        os.remove(thumb_name)
        await m.delete()
    except Exception as e:
        await m.edit("**Error during download**")
        print(e)

# Function to handle cookie-based authentication for video download
@Client.on_message(filters.command(["video", "mp4"]))
async def vsong(client, message):
    urlissed = message.text.split(None, 1)[1] if len(message.text.split(None, 1)) > 1 else None
    if not urlissed:
        return await message.reply("Example: /video <Your video URL>")
    
    pablo = await message.reply(f"**Finding your video...** `{urlissed}`")

    # yt-dlp options for downloading videos
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "cookiefile": COOKIES_FILE,  # Add cookies here
        "outtmpl": "%(id)s.mp4",  # Specify output template
    }

    try:
        with YoutubeDL(opts) as ytdl:
            # Extract video information and download
            ytdl_data = ytdl.extract_info(urlissed, download=True)

        # Get file path and video details
        file_stark = f"{ytdl_data['id']}.mp4"
        thum = f"https://img.youtube.com/vi/{ytdl_data['id']}/hqdefault.jpg"
        capy = f"**TITLE:** [{ytdl_data['title']}]({urlissed})\n**Requested by:** {message.from_user.mention}"

        # Send the downloaded video
        await client.send_video(
            message.chat.id,
            video=open(file_stark, "rb"),
            caption=capy,
            duration=int(ytdl_data["duration"]),
            thumb=thum,
            supports_streaming=True,
            reply_to_message_id=message.id
        )

        # Clean up the temporary files
        os.remove(file_stark)
        await pablo.delete()
    except Exception as e:
        await pablo.edit(f"**Download Failed!**\n**Error:** {str(e)}")


