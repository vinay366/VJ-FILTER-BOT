from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

from info import CHNL_LNK  # Ensure CHNL_LNK is defined in the info module

GENIUS_API_KEY = "VAFbg5jQr-dBB3zPO_fq2x6hxxQh3aJjCim2ti6IF0ixOgunSwyHCjT7b4yXt3oq"  # Replace with your Genius API key
GENIUS_API_URL = "https://api.genius.com/search"

@Client.on_message(filters.text & filters.command(["lyrics"]))
async def sng(bot, message):
    vj = await bot.ask(chat_id=message.from_user.id, text="Now send me your song name.")
    if vj.text:
        mee = await vj.reply_text("`Searching 🔎`")
        song = vj.text.strip()
        chat_id = message.from_user.id
        rpl = lyrics(song)

        try:
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
                f"I couldn't find lyrics for `{song}`.",
                quote=True,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇꜱ", url=CHNL_LNK)]])
            )
    else:
        await vj.reply_text("Send me only text Buddy.")

def search(song):
    """
    Search for the song using the Genius API.
    """
    headers = {"Authorization": f"Bearer {GENIUS_API_KEY}"}
    params = {"q": song}
    response = requests.get(GENIUS_API_URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def lyrics(song):
    """
    Extract lyrics details from the Genius API response.
    """
    data = search(song)
    hits = data.get("response", {}).get("hits", [])

    if not hits:
        raise ValueError("No results found.")

    # Extract details of the first result
    song_info = hits[0].get("result", {})
    song_title = song_info.get("title", "Unknown Title")
    song_artist = song_info.get("primary_artist", {}).get("name", "Unknown Artist")
    song_url = song_info.get("url", "")

    return (
        f"**🎶 Successfully Found Lyrics for {song_title} by {song_artist}:**\n\n"
        f"🔗 [View Full Lyrics]({song_url})\n\n"
        "**Made By Artificial Intelligence**"
    )
