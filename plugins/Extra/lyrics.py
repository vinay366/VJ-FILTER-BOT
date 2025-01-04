from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from info import CHNL_LNK
import requests 

API_URL = "https://api.lyrics.ovh/v1"

@Client.on_message(filters.text & filters.command(["lyrics"]))
async def sng(bot, message):
    vj = await bot.ask(chat_id=message.from_user.id, text="Now send me the artist and song name in the format:\n`Artist - Song Title`")
    if vj.text:
        mee = await vj.reply_text("`Searching 🔎`")
        input_text = vj.text.strip()
        chat_id = message.from_user.id

        try:
            # Extract artist and song title
            if " - " not in input_text:
                raise ValueError("Invalid format. Use `Artist - Song Title`.")

            artist, song = map(str.strip, input_text.split(" - ", 1))
            rpl = fetch_lyrics(artist, song)

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
                f"I couldn't find lyrics for `{input_text}`.\n\nError: {str(e)}",
                quote=True,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇꜱ", url=CHNL_LNK)]])
            )
    else:
        await vj.reply_text("Send me only text Buddy.")

def fetch_lyrics(artist, song):
    """
    Fetch lyrics from the Lyrics.ovh API.
    """
    response = requests.get(f"https://api.lyrics.ovh/v1/{artist}/{song}")
    if response.status_code != 200:
        raise ValueError("Lyrics not found. Please check the artist and song title.")

    data = response.json()
    lyrics = data.get("lyrics", None)
    if not lyrics:
        raise ValueError("Lyrics not found in the response.")

    return (
        f"**🎶 Successfully Found Lyrics for {song} by {artist}:**\n\n"
        f"`{lyrics}`\n\n"
        "**Made By Artificial Intelligence**"
    )
