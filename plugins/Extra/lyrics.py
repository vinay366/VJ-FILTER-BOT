from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from info import CHNL_LNK
import requests 

import os


GENIUS_API_TOKEN = 'VNcYSYtcNHWiE8TuUF3E6LqiwqtEZeBUmMvcj5En7UzX-xx-MZZOerYpzEoHbMsA'

BASE_URL = "https://api.genius.com"


@Client.on_message(filters.text & filters.command(["lyrics"]))
async def sng(bot, message):
    vj = await bot.ask(chat_id=message.from_user.id, text="Now send me your song name.")
    if vj.text:
        mee = await vj.reply_text("`Searching 🔎`")
        song = vj.text
        chat_id = message.from_user.id
        rpl = lyrics(song)
        await mee.delete()
        try:
            await mee.delete()
            await bot.send_message(chat_id, text = rpl, reply_to_message_id = message.id, reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs ", url = CHNL_LNK)]]))
        except Exception as e:                            
            await vj.reply_text(f"I Can't Find A Song With `{song}`", quote = True, reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url = CHNL_LNK)]]))
    else:
        await vj.reply_text("Send me only text Buddy.")

# Function to search for the song and get the song page URL
def search(song):
    headers = {'Authorization': f'Bearer {GENIUS_API_TOKEN}'}
    search_url = BASE_URL + "/search"
    
    # Make a request to Genius' search endpoint with the song name
    params = {'q': song}
    response = requests.get(search_url, headers=headers, params=params)
    
    if response.status_code == 200:
        json_data = response.json()
        # Get the first song result (usually the most relevant)
        hit = json_data['response']['hits'][0]['result']
        song_url = hit['url']
        # Fetch lyrics from the song's page
        lyrics = get_lyrics_from_url(song_url)
        return {"lyrics": lyrics}
    else:
        return {"lyrics": "Song not found or error occurred."}

# Function to scrape lyrics from the Genius song page
def get_lyrics_from_url(song_url):
    response = requests.get(song_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        lyrics_div = soup.find('div', class_='lyrics')
        
        if lyrics_div:
            return lyrics_div.get_text(strip=True)
        else:
            return "Lyrics not found."
    else:
        return "Could not retrieve the song page."

# Function to extract and format lyrics
def lyrics(song):
    fin = search(song)
    text = f'**🎶 Sᴜᴄᴄᴇꜱꜰᴜʟʟy Exᴛʀᴀᴄᴛᴇᴅ Lyɪʀɪᴄꜱ Oꜰ {song}**\n\n'
    text += f'`{fin["lyrics"]}`'
    text += '\n\n\n**Made By Artificial Intelligence**'
    return text



