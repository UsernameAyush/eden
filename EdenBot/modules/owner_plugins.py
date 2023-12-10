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
import psutil
import asyncio
from datetime import datetime


from config import PING_IMG_URL, SUPPORT_CHAT, OWNER_ID, START_IMG_URL, STATS_IMG_URL,SUPPORT_CHANNEL
from EdenBot.modules.voting import check_user
from EdenBot import app, botusername as Bot_Username, boot, botid, time_date_india, votedb
from EdenBot.modules.private import close_button
from EdenBot.database.database import (add_served_channel,
    get_served_channels,
    add_served_chat,
    get_served_chats,
    get_served_users,
    total_polls, live_polls,
    live_polls_inList)

from EdenBot.logging import LOGGER
from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.enums import ChatType
from pyrogram.types import Message, ChatMember, InlineKeyboardMarkup, InlineKeyboardButton






async def get_channel_id():
    channel_link = SUPPORT_CHANNEL
    if channel_link.startswith("https://t.me/"):
        splited_link = channel_link.split("/")
        chat = await app.get_chat(f"@{splited_link[-1]}")
        return chat.id
    elif channel_link.startswith("@"):
        chat = await app.get_chat(channel_link)
        return chat.id
    elif channel_link.isnumeric():
        return channel_link




@app.on_message(filters.command(["id"]))
async def id_info(app, message):
	if message.reply_to_message:
		chat_id = message.reply_to_message.forward_from_chat
		return await message.reply_text(f"💡 {chat_id.title}'s ID : <code>{chat_id.id}</code>")

	splited_cmd = message.text.split(" ")

	if len(splited_cmd) == 1:
		if message.chat:
			return await message.reply_text(f"💡 {message.chat.title}'s ID : <code>{message.chat.id}</code>")
		else:
			return await message.reply_text(f"💡 {message.from_user.first_name}'s ID : <code>{message.from_user.id}</code>")
	
	if splited_cmd[0] in ['id','/id']:
		if splited_cmd[1].startswith("https://t.me/"):
			if splited_cmd[1].startswith("https://t.me/+"):
				return message.reply_text(f"This link is a private link that can't be access by bots from outside of chat's. Please send this /id command to your channel/group after making me admin there.")
		try:
			baby_chat = await app.get_chat(splited_cmd[1])
			return await message.reply_text(f"💡 {baby_chat.title}'s ID : <code>{baby_chat.id}</code>")
		except:
			return await message.reply_text(f"Did you gave me a valid chat's link ?? Check the link and try again.")

		if splited_cmd[1].startswith("@"):
			try:
				baby_chat = await app.get_chat(splited_cmd[1])
				return await message.reply_text(f"💡 {baby_chat.title}'s ID : <code>{baby_chat.id}</code>")
			except:
				return await message.reply_text(f"Did you gave me a valid chat's link ?? Check the link and try again.")



def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "ᴍ", "ʜ", "ᴅᴀʏs"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time


async def bot_sys_stats():
	bot_uptime = int(time.time() - boot)
	UP = f"{get_readable_time(bot_uptime)}"
	CPU = f"{psutil.cpu_percent(interval=0.5)}%"
	RAM = f"{psutil.virtual_memory().percent}%"
	DISK = f"{psutil.disk_usage('/').percent}%"
	return UP, CPU, RAM, DISK



@app.on_message(filters.command(["ping","alive"]))
async def pingi_pongi(_, message):
    response = await message.reply_photo(photo=PING_IMG_URL, caption="Loading...")
    UP, CPU, RAM, DISK = await bot_sys_stats()
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(f'🔷 Close 🔷', callback_data='delete_now')]])
    text_ping = f"""╔══          » Aʟɪᴠᴇ «         ══╗

      ⏰ Uᴘᴛɪᴍᴇ : {UP}

      💻  Cᴘᴜ      : {CPU}

      📼  Rᴀᴍ      : {RAM}

      💾  Dɪsᴋ     : {DISK}

      🚹  Oᴡɴᴇʀ : {SUPPORT_CHAT}

╚══             ⊱⭕️⊰              ══╝

♨️ Bot Username :
 @{Bot_Username}"""
    return await response.edit_text(text_ping, reply_markup=close_button)



IS_BROADCASTING = None
# Broadcasting By Owner

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def braodcast_message(app, message):
    global IS_BROADCASTING
    if message.reply_to_message:
        x = message.reply_to_message.id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text("Empty broadcasting? Reply or give something to broadcast...Fuck-Off")
        query = message.text.split(None, 1)[1]
        if "-pin" in query:
            query = query.replace("-pin", "")
        if "-pinloud" in query:
            query = query.replace("-pinloud", "")
        if "-user" in query:
            query = query.replace("-user", "")
        if "-nobot" in query:
        	query = query.replace("-nobot", "")
        if query == "":
            return await message.reply_text("Broadcast for groups ??")

    IS_BROADCASTING = True
    await message.reply_text("Broadcasting Started!")

    if "-nobot" not in message.text:
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = (
                    await app.forward_messages(i, y, x)
                    if message.reply_to_message
                    else await app.send_message(i, text=query)
                )
                if "-pin" in message.text:
                    try:
                        await m.pin(disable_notification=True)
                        pin += 1
                    except:
                        continue
                elif "-pinloud" in message.text:
                    try:
                        await m.pin(disable_notification=False)
                        pin += 1
                    except:
                        continue
                sent += 1
                await asyncio.sleep(0.2)
            except FloodWait as fw:
                flood_time = int(fw.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except:
                continue
        try:
            await message.reply_text(f"Broadcasted in {sent} Chats with {pin} pins ✅")
        except:
            pass

    if "-user" in message.text:
        susr = 0
        served_users = []
        susers = await get_served_users()
        for user in susers:
            served_users.append(int(user["user_id"]))
        for i in served_users:
            try:
                m = (
                    await app.forward_messages(i, y, x)
                    if message.reply_to_message
                    else await app.send_message(i, text=query)
                )
                susr += 1
                await asyncio.sleep(0.2)
            except FloodWait as fw:
                flood_time = int(fw.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except:
                pass
        try:
            await message.reply_text(f"Broadcasted To {susr} ✅")
        except:
            pass

    IS_BROADCASTING = False




@app.on_message(filters.command(["polls", "live","av"]) & filters.user(OWNER_ID))
async def livePollsss(app, message):
    try:
        today_date = int(time_date_india()[0])
        live_polls_pure_list = await live_polls_inList()
        channel_ids = []

        for polling in live_polls_pure_list:
            splited_part_of_polls = polling.split("/")
            poll_channel_id = splited_part_of_polls[0]
            date_of_polls = int(splited_part_of_polls[2])
            if date_of_polls != today_date:
                await votedb[polling].drop()
            else:
                channel_ids.append(int(poll_channel_id))

        names_of_channel = []

        try:
            for channel_idd in channel_ids:
                try:
                    get_chat = await app.get_chat(channel_idd)
                    titli = get_chat.title
                    if titli not in names_of_channel:
                        names_of_channel.append(titli)
                except Exception as ok:
                    LOGGER("PEER_ID INVALID").info(f"Raised By LPW Module\n\n {ok}")
                    if channel_idd not in names_of_channel:
                        names_of_channel.append(str(channel_idd))

            if len(live_polls_pure_list) == 0:
                return await message.reply_text(f'No Active Poll Currently ❌')
            elif len(names_of_channel) > 20:
                return await message.reply_text(f"<b>💡 LIVE POLLS</b> >> {len(live_polls_pure_list)}\n\n<b>🔷 IN CHANNELS</b> >> {len(names_of_channel)}")
            else:
                return await message.reply_text(f"<b>💡 LIVE POLLS</b> >> {len(live_polls_pure_list)}\n\n<b>🔷 LIST OF CHANNELS WHERE POLLS ARE</b> >> \n{names_of_channel}\nTotal Channels >> {len(names_of_channel)}")
        except Exception as err:
            LOGGER("LPW Module").info(f"Raised By LPW Module\n\n {err}")
            return
    except Exception as err:
        LOGGER("LPW Module").info(f"Raised By LPW Module\n\n {err}")





@app.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def states(app, message):
    total_groups = len(await get_served_chats())
    total_users = len(await get_served_users())
    total_channels = len(await get_served_channels())
    total_pollss = await total_polls()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    LIVE_POLLSs = int(await live_polls())
    return await message.reply_photo(photo=STATS_IMG_URL, caption=f"<b>@{Bot_Username} Stats 📊</b>\n<━━━━━━━━━━━━━━━━>\n\n<b>BASIC INFORMATION :</b>\n━━━━━━━━━━━━━━━•\n<b>Total Groups</b> : {total_groups}\n<b>Total Channel</b> : {total_channels}\n<b>Total Users</b> : {total_users}\n\n<b>SYSTEM INFORMATION</b> :\n━━━━━━━━━━━━━━━━━•\n<b>UP-TIME</b> : {UP}\n<b>CPU</b> : {CPU}\n<b>RAM</b> : {RAM}\n<b>STORAGE</b> : {DISK}\n<b>LIVE POLLS</b> : {LIVE_POLLSs}\n<b>TOTAL POLLS</b> : {total_pollss}", reply_markup=close_button)








"""
@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message):
    for member in message.new_chat_members:
        if str(member.id) == f"{botid}":
            if message.chat.type == ChatType.CHANNEL:
                await add_served_channel(message.chat.id)
                return await app.send_message(message.chat.id, f"Thank You For Adding @{Bot_Username} in {message.chat.title} 🏡.")
            else:
                await add_served_chat(message.chat.id)
                return await app.send_message(message.chat.id, f"Thank You For Adding @{Bot_Username} in {message.chat.title} 🏡.")
"""


