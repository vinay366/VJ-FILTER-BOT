# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

# Clone Code Credit : YT - @Tech_VJ / TG - @VJ_Bots / GitHub - @VJBots

import sys, glob, importlib, logging, logging.config, pytz, asyncio
from pathlib import Path

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("cinemagoer").setLevel(logging.ERROR)

from pyrogram import Client, idle
from database.users_chats_db import db
from info import *
from utils import temp
from typing import Union, Optional, AsyncGenerator
from Script import script 
from datetime import date, datetime 
from aiohttp import web
from plugins import web_server
from plugins.clone import restart_bots

from TechVJ.bot import TechVJBot
from TechVJ.util.keepalive import ping_server
from TechVJ.bot.clients import initialize_clients

ppath = "plugins/*.py"
files = glob.glob(ppath)

# Create and set event loop before starting the bot
loop = asyncio.get_event_loop()

async def start():
    print('\n')
    print('Initializing Your Bot')
    bot_info = await TechVJBot.get_me()
    await initialize_clients()
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"plugins/{plugin_name}.py")
            import_path = f"plugins.{plugin_name}"
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules[import_path] = load
            print("Tech VJ Imported => " + plugin_name)

    if ON_HEROKU:
        asyncio.create_task(ping_server())

    # Fetch banned users and chats
    b_users, b_chats = await db.get_banned()
    temp.BANNED_USERS = b_users
    temp.BANNED_CHATS = b_chats

    me = await TechVJBot.get_me()
    temp.BOT = TechVJBot
    temp.ME = me.id
    temp.U_NAME = me.username
    temp.B_NAME = me.first_name

    logging.info(script.LOGO)

    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time = now.strftime("%H:%M:%S %p")

    try:
        await TechVJBot.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))
    except Exception as e:
        logging.error(f"Failed to notify in log channel: {e}")

    for ch in CHANNELS:
        try:
            k = await TechVJBot.send_message(chat_id=ch, text="**Bot Restarted**")
            await k.delete()
        except Exception as e:
            logging.error(f"Failed to notify in channel {ch}: {e}")

    try:
        k = await TechVJBot.send_message(chat_id=AUTH_CHANNEL, text="**Bot Restarted**")
        await k.delete()
    except Exception as e:
        logging.error(f"Failed to notify in auth channel: {e}")

    if CLONE_MODE:
        print("Restarting All Clone Bots.......")
        await restart_bots()
        print("Restarted All Clone Bots.")

    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()
    await idle()

if __name__ == '__main__':
    try:
        loop.run_until_complete(start())
    except KeyboardInterrupt:
        logging.info('Service Stopped. Bye 👋')
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
