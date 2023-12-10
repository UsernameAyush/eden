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

import time
import random

from config import SUDO_USER, START_IMG_URL, SUPPORT_CHAT, SUPPORT_CHANNEL, FORCE_JOIN

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import MessageNotModified

from EdenBot.database.database import add_served_user

from EdenBot import app, boot, botname, botusername
from EdenBot.helpers import get_readable_time,settings_markup, RANDOM, HELP_TEXT


help_text = """As We Promised you to keep bot very simple & Easy-to-Use, So we did only 3 commands. 🤝


<b>FOR USERS 👬</b>:
•━━━━━━━━━━━━━━━━•

<b>/channel [ channel ID or Link ]</b> : __set a channel before first vote/poll.__

<b>/vote [ Name Of The Voter ]</b> : __This will create poll & will send this to your selected channel.__

<b>/id</b> : __get id of your channel/group or yourself.__"""

help_text_owner = """As We Promised you to keep bot very simple & Easy-to-Use, So we did only 2 commands. 🤝


<b>FOR USERS 👬</b>:
•━━━━━━━━━━━━━━━━•

<b>/channel [ channel ID or Link ]</b> : __set a channel before first vote/poll.__

<b>/vote [ Name Of The Voter ]</b> : __This will create poll & will send this to your selected channel.__

<b>/id</b> : __get id of your channel/group or yourself.__


<b>FOR OWNER 🤴🏻</b>:
•━━━━━━━━━━━━━━━━•

<b>/broadcast</b> __(reply or text)__
<b>/stats</b> : __Get stats of bot__
<b>/ping</b> : __Get pinging information__
"""


upl = InlineKeyboardMarkup(
    [
    [
    InlineKeyboardButton(text="➕ Add me to a Group", url=f"https://t.me/{botusername}?startgroup=true"),
    ],
    [
    InlineKeyboardButton(text="🔰 • Help • 🔰", callback_data="help_command"),
    InlineKeyboardButton(text="🕵 • Owner • 🕵", url=f"{SUPPORT_CHAT}"),
    ],
    [
    InlineKeyboardButton(text="❇️ • Channel • ❇️", url=f"{SUPPORT_CHANNEL}"),
    ],
    ],
    )



close_button = InlineKeyboardMarkup([[InlineKeyboardButton(text=f'❌ • Close • ❌', callback_data="close")]])
home_button = InlineKeyboardMarkup([[InlineKeyboardButton(text=f'🌴🏠 • Home • 🏠🌴', callback_data="home_now")]])
channel_button = InlineKeyboardMarkup([[InlineKeyboardButton(text=f'📢 Click Me 📢', url=SUPPORT_CHANNEL)]])





@app.on_message(filters.command(["start"]) & filters.private)
async def on_private_start(_, message: Message):
    if FORCE_JOIN is True:
        from EdenBot.modules.owner_plugins import get_channel_id
        chat_id_channel = await get_channel_id()
        from EdenBot.modules.voting import check_user
        if await check_user(chat_id_channel, message.from_user.id) is False:
            return await message.reply_text("<b>Please Join Our Channel Before Using The Bot.</b>", reply_markup=channel_button)
    await add_served_user(message.from_user.id)
    start_text = f"""Hii {message.from_user.first_name} ♥️


Welcome To {botname} 🌷

This is a great and Easy-to-Use bot for creating polls in your channel and groups too. Just setup your channel/group and create a poll via /vote Ayush 🏖


Click <b>"Help"</b> Button for getting help command lists 👩🏻‍💻"""
    return await message.reply_photo(START_IMG_URL, caption=start_text, reply_markup=upl)

@app.on_message(filters.command(["help"]) & filters.private)
async def on_private_help(_, message: Message):
    await add_served_user(message.from_user.id)
    if message.from_user.id in SUDO_USER:
        return await message.reply_photo(START_IMG_URL, caption=help_text_owner, reply_markup=home_button)
    else:
        return await message.reply_photo(START_IMG_URL, caption=help_text, reply_markup=home_button)

        

@app.on_callback_query(filters.regex("help"))
async def on_help_button(client, CallbackQuery):
    if CallbackQuery.from_user.id in SUDO_USER:
        await CallbackQuery.message.edit_text(help_text_owner, reply_markup=home_button)
        return
    else:
        await CallbackQuery.message.edit_text(help_text, reply_markup=home_button)
        return



@app.on_callback_query(filters.regex("home_now"))
async def on_home_button(client, CallbackQuery):
    start_text = f"""Hii {CallbackQuery.from_user.first_name} ♥️

Welcome To {botname} 🌷

This is a great and Easy-to-Use bot for creating polls in your channel and groups too. Just setup your channel/group and create a poll via /vote Ayush 🏖


Click <b>"Help"</b> Button for getting help command lists 👩🏻‍💻"""
    await CallbackQuery.message.edit_text(start_text, reply_markup=upl)
    return


@app.on_callback_query(filters.regex("close"))
async def on_close_button(client, CallbackQuery):
    await CallbackQuery.message.delete()


