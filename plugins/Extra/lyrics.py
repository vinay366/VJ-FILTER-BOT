from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from info import CHNL_LNK
import requests 

import os

GENIUS_API_KEY = "VNcYSYtcNHWiE8TuUF3E6LqiwqtEZeBUmMvcj5En7UzX-xx-MZZOerYpzEoHbMsA"  # Replace with your Genius API key
GENIUS_API_URL = "https://api.genius.com/search"

@Client.on_message(filters.text & filters.command(["lyrics"]))
async def sng(bot, message):
    vj = await bot.ask(chat_id=message.from_user.id, text="Now send me your song name.")
    if vj.text:
        mee = await vj.reply_text("`Searching 🔎`")
        song = vj.text.strip()
        chat_id = message.from_user.id

        try:
            # Fetch full lyrics
            rpl = lyrics(song)
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

def fetch_lyrics_url(song):
    """
    Extract the Genius URL for the song.
    """
    data = search(song)
    hits = data.get("response", {}).get("hits", [])

    if not hits:
        raise ValueError("No results found.")

    # Extract details of the first result
    song_info = hits[0].get("result", {})
    song_url = song_info.get("url", "")

    if not song_url:
        raise ValueError("No URL found for the song.")

    return song_url

def scrape_lyrics(song_url):
    """
    Scrape the lyrics text from the Genius song page.
    """
    response = requests.get(song_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the lyrics container
    lyrics_div = soup.find("div", class_="Lyrics__Container-sc-1ynbvzw-6")
    if not lyrics_div:
        raise ValueError("Couldn't extract lyrics from the page.")

    # Extract and clean up the lyrics text
    lyrics = "\n".join([line.get_text(separator="\n") for line in lyrics_div.find_all("p")])
    return lyrics.strip()

def lyrics(song):
    """
    Get full lyrics text by scraping Genius page.
    """
    song_url = fetch_lyrics_url(song)
    full_lyrics = scrape_lyrics(song_url)

    return (
        f"**🎶 Successfully Found Lyrics for {song}:**\n\n"
        f"`{full_lyrics}`\n\n"
        "**Made By Artificial Intelligence**"
    )
