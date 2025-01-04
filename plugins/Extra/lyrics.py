from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import CHNL_LNK
import os

API_URL = "https://api.genius.com/search"
GENIUS_API_KEY = "ZSXjn8OAKM669PrE2Lo1QjZC5dFd3j3K5AbZ4kAHex3sIH_rWvwTv6PhXlAY9iqh"

# Configure Selenium WebDriver
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver_service = Service('/path/to/chromedriver')  # Replace with the path to your ChromeDriver

@Client.on_message(filters.text & filters.command(["lyrics"]))
async def sng(bot, message):
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
    lyrics = fetch_lyrics_from_url_with_selenium(song_url)
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

def fetch_lyrics_from_url_with_selenium(url):
    """
    Fetch lyrics using Selenium for JavaScript-rendered content.
    """
    driver = webdriver.Chrome(service=driver_service, options=options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    lyrics_divs = soup.find_all("div", class_="Lyrics__Container-sc-1ynbvzw-6")
    if not lyrics_divs:
        raise ValueError("Lyrics not found on the page.")

    lyrics = "\n".join([div.get_text(separator="\n").strip() for div in lyrics_divs])
    return lyrics.strip()
