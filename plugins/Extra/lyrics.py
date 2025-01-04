from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from info import CHNL_LNK
import requests 
from xml.etree import ElementTree as ET

import os


API_URL = "http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect"

@Client.on_message(filters.text & filters.command(["lyrics"]))
async def sng(bot, message):
    # Ask user for the song name
    vj = await bot.ask(chat_id=message.from_user.id, text="Now send me the song name.")
    if vj.text:
        mee = await vj.reply_text("`Searching 🔎`")
        song = vj.text.strip()
        chat_id = message.from_user.id

        try:
            # Fetch lyrics using the song name
            rpl = fetch_lyrics(song)

            await mee.delete()
            await bot.send_message(
                chat_id,
                text=rpl,
                reply_to_message_id=message.id,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇꜱ", url=CHNL_LNK)]])
            )
        except Exception as e:
            await mee.delete()
            await vj.reply_text(
                f"I couldn't find lyrics for `{song}`.\n\nError: {str(e)}",
                quote=True,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇꜱ", url=CHNL_LNK)]])
            )
    else:
        await vj.reply_text("Send me only text Buddy.")

def fetch_lyrics(song):
    """
    Fetch lyrics from the ChartLyrics API using only the song name.
    """
    params = {
        "artist": "",  # Empty since we're only using the song name
        "song": song
    }
    response = requests.get(API_URL, params=params)
    if response.status_code != 200:
        raise ValueError("Lyrics not found. Please check the song title.")

    # Parse XML response
    root = ET.fromstring(response.content)
    lyrics = root.find(".//Lyric")
    if lyrics is None or not lyrics.text:
        raise ValueError("Lyrics not found.")

    return (
        f"**🎶 Successfully Found Lyrics for {song}:**\n\n"
        f"`{lyrics.text}`\n\n"
        "**Made By Artificial Intelligence**"
    )
