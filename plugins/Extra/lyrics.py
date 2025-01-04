from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from info import CHNL_LNK
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
            # Fetch lyrics and song URL using the song name
            rpl, song_url = fetch_lyrics_and_url(song)

            await mee.delete()
            await bot.send_message(
                chat_id,
                text=rpl,
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
    Fetch lyrics and the Genius URL using the song name.
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
    )

def fetch_lyrics_from_url(url):
    """
    Fetch lyrics directly from the Genius song page.
    """
    # You can use libraries like BeautifulSoup to scrape lyrics from the Genius page.
    # Here is a simplified placeholder for demonstration.
    # Replace this with scraping logic if needed.
    return "This is a placeholder for lyrics. Add scraping logic to fetch actual lyrics."


