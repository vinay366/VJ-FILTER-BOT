from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from info import CHNL_LNK
from bs4 import BeautifulSoup
import requests 
import os

GENIUS_API_KEY = "ZSXjn8OAKM669PrE2Lo1QjZC5dFd3j3K5AbZ4kAHex3sIH_rWvwTv6PhXlAY9iqh"
API_URL = "https://api.genius.com/search"

@Client.on_message(filters.text & filters.command(["lyrics"]))
async def sng(bot, message):
    # Ask user for the song name
    vj = await bot.ask(chat_id=message.from_user.id, text="Now send me the song name.")
    if vj.text:
        mee = await vj.reply_text("`Searching 🔎`")
        song = vj.text.strip()
        chat_id = message.from_user.id

        try:
            # Fetch lyrics, song URL, and artist image using the song name
            rpl, song_url, artist_image = fetch_lyrics_and_url(song)

            await mee.delete()
            # Send the artist's photo
            await bot.send_photo(
                chat_id,
                photo=artist_image,
                caption=rpl,
                reply_to_message_id=message.id,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("🎵 View Song on Genius", url=song_url)],
                        [InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇꜱ", url=CHNL_LNK)],
                    ]
                ),
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

def fetch_lyrics_and_url(song):
    """
    Fetch lyrics, Genius URL, and artist image using the song name.
    """
    headers = {"Authorization": f"Bearer {GENIUS_API_KEY}"}
    params = {"q": song}
    response = requests.get(API_URL, headers=headers, params=params)
    if response.status_code != 200:
        raise ValueError("Lyrics not found. Please check the song title.")

    data = response.json()
    hits = data.get("response", {}).get("hits", [])
    if not hits:
        raise ValueError("Lyrics not found.")

    # Get the first result
    song_data = hits[0]["result"]
    song_title = song_data["title"]
    song_artist = song_data["primary_artist"]["name"]
    song_url = song_data["url"]
    artist_image = song_data["primary_artist"]["image_url"]

    # Fetch lyrics from the song page
    lyrics = fetch_lyrics_from_url(song_url)
    if not lyrics:
        raise ValueError("Lyrics not found.")

    return (
        f"**🎶 Successfully Found Lyrics:**\n\n"
        f"**Song:** {song_title}\n"
        f"**Artist:** {song_artist}\n\n"
        f"`{lyrics.strip()}`\n\n"
        "**Made By Artificial Intelligence**",
        song_url,
        artist_image,
    )

def fetch_lyrics_from_url(url):
    """
    Fetch lyrics directly from the Genius song page using BeautifulSoup.
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("Failed to fetch lyrics page.")

    soup = BeautifulSoup(response.text, "html.parser")
    lyrics_div = soup.find("div", class_="Lyrics__Container-sc-1ynbvzw-6")
    if not lyrics_div:
        raise ValueError("Lyrics not found on the page.")

    # Extract text and clean up
    lyrics = "\n".join([line.get_text(separator="\n") for line in lyrics_div.find_all("p")])
    return lyrics.strip()



