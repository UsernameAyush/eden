# A Vote Bot Made by Ayush and owned by Raichu
#
# Copyright (C) 2023-2024 by JustAyu@Github, < https://github.com/Justayu >.
#
# This file is part of < https://github.com/JustAyu/EdenBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/JustAyu/EdenBot/blob/master/LICENSE >
#
# All rights reserved.
#
from pymongo import MongoClient

import sys
import asyncio
import time
from datetime import datetime
import pytz

from config import MONGO_DB_URI, LOGGER_ID
from .logging import LOGGER
from motor.motor_asyncio import AsyncIOMotorClient


from pyrogram import Client
import config


loop = asyncio.get_event_loop()
boot = time.time()



try:
    LOGGER(__name__).info("Database Initializing...")
    _mongo_async_ = AsyncIOMotorClient(MONGO_DB_URI)
    mongodb = _mongo_async_.AyushBot
    votedb = _mongo_async_.VotingDatabase
    LOGGER(__name__).info("DFV & BID Database Created!")
except:
    LOGGER(__name__).error("Failed to connect to your Mongo Database.")
    exit()


botid = 0
botname = ""
botusername = ""


SUDOERS = config.SUDO_USER

app = Client(
    "RVB",
    config.API_ID,
    config.API_HASH,
    bot_token=config.BOT_TOKEN,
)


async def initiate_bot():
    global botid, botname, botusername
    await app.start()
    getme = await app.get_me()
    botid = getme.id
    botusername = (getme.username).lower()
    if getme.last_name:
        botname = getme.first_name + " " + getme.last_name
    else:
        botname = getme.first_name
    try:
        await app.send_message(LOGGER_ID, f"{botname} Started 🍟")
    except Exception as lol:
        print("Please Make Bot An Admin In The Logger Group.")
        LOGGER(__name__).info("Please Make Bot An Admin In The Logger Group.")



loop.run_until_complete(initiate_bot())


def time_date_india():
    india_tz = pytz.timezone('Asia/Kolkata')
    india_datetime = datetime.now(india_tz)
    today_datee = india_datetime.strftime('%d')
    today_hour = india_datetime.strftime('%H')
    baby = str(today_datee)
    baby2 = str(today_hour)
    today_date = baby.zfill(2)
    today_hour = baby2.zfill(2)
    return today_date, today_hour

