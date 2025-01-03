from __future__ import unicode_literals

import os, requests, asyncio, math, time, wget
from pyrogram import filters, Client
from pyrogram.types import Message
from info import CHNL_LNK
from youtube_search import YoutubeSearch
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL

# Define a custom User-Agent (you can copy one from your browser)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"

@Client.on_message(filters.command(['song', 'mp3']) & filters.private)
async def song(client, message):
    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    query = ' '.join(message.command[1:])
    print(query)

    m = await message.reply(f"**ѕєαrchíng чσur ѕσng...!\n {query}**")

    # Custom yt-dlp options with User-Agent
    ydl_opts = {
        "format": "bestaudio[ext=m4a]",
        "headers": {
            "User-Agent": USER_AGENT  # Setting the custom User-Agent here
        }
    }

    try:
        # Use youtube-search to search for the song
        results = YoutubeSearch(query, max_results=1).to_dict()
        if not results:
            await m.edit("**No results found for the search query.**")
            return

        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb_{title}.jpg'

        # Download thumbnail
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)
        performer = "[NETWORKS™]"
        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]

        await m.edit("**dσwnlσαdíng чσur ѕσng...!**")

        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)

        cap = f"**BY›› [UPDATE]({CHNL_LNK})**"
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        
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
        print(f"Error in song download: {str(e)}")
        await m.edit("**🚫 𝙴𝚁𝚁𝙾𝚁 🚫**")
    finally:
        try:
            if os.path.exists(audio_file):
                os.remove(audio_file)
            if os.path.exists(thumb_name):
                os.remove(thumb_name)
        except Exception as e:
            print(f"Error deleting temporary files: {e}")


