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



import random
from ..logging import LOGGER
from asyncio import sleep


import config
from EdenBot import app, botusername, time_date_india
from EdenBot.modules.private import channel_button
from EdenBot.database import (set_channel, get_channel,
    is_set_channel, is_elector,
    add_vote, create_elector,
    count_votes, add_served_channel, add_one_poll
    )

from pyrogram import filters
from pyrogram.types import Message, ChatMember, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import (ChatAdminRequired,
    UsernameNotOccupied,
    UsernameInvalid,
    PeerIdInvalid,
    UserNotParticipant,
    ChannelPrivate,
    RightForbidden
    )




emojis = ['🔸','🔷','💚','❤️','💘','💜','💛','💖']



# Channel Setup & Time Settings

async def check_admin(chat_id, user_id):
    try:
        member = await app.get_chat_member(chat_id=chat_id, user_id=user_id)
    except UserNotParticipant:
        return False
    statusmember = member.status
    if str(statusmember) in ["ChatMemberStatus.ADMINISTRATOR", "ChatMemberStatus.OWNER"]:
        return True
    else:
        return False


async def check_user(chat_id, user_id):
    try:
        member = await app.get_chat_member(chat_id=chat_id, user_id=user_id)
    except UserNotParticipant:
        return False
    statusmember = member.status
    if str(statusmember) in ["ChatMemberStatus.MEMBER", "ChatMemberStatus.ADMINISTRATOR", "ChatMemberStatus.OWNER"]:
        return True
    else:
        return False



@app.on_message(filters.command(["channel"]) & filters.private)
async def select_channel(_, message):
    user_id = None
    try:
        if message.text:
            channel_link = message.text.split(" ")[1]
        else:
            channel_link = message.caption.split(" ")[1]
    except:
        return await message.reply_text("<b>💡 Usage:</b>\n • /channel [ Channel ID or Channel Link ]\n\nYou Can Get Your channel id by sending /id command in your channel.")
    
    if channel_link.isnumeric():
        channel_split = str(channel_link)
        if channel_link[0:4] == "-100":
            channel_blink = str(channel_split[1:])
            channel_link = int("-"+"channel_blink")
        elif channel_link[0:3] == "100":
            channel_link = int("-"+f"{channel_split}")
        else:
            return await message.reply_text("<b>Wrong Channel ID 🔴</b> . Please try with channel's link or give me full channel ID like -100123456789")
        
        try:
            try:
                channel_detect = await app.get_chat(channel_link)
            except:
                return await message.reply_text("<b>Wrong Channel ID 🔴</b> . Please try with channel's link or give me full channel ID like -100123456789")
            channel_owned = message.from_user.id
            if await check_admin(channel_detect.id, channel_owned) == False:
                return await message.reply(f"🤚 You are not an Owner or Admin in {channel_link} ")

            try:
                setting = await set_channel(channel_owned, channel_detect.id)
                await add_served_channel(channel_detect.id)
                if setting is True:
                    return await message.reply_text("<b>Channel Selected ✅</b>. You can Create Votes now!\n\n#Note - Whenever you wanna change your voting channel, Just use /channel again.")
                elif setting == "updated":
                    return await message.reply_text("<b>New Channel Updated ✅</b>. You can Create Votes now!")
                elif setting == "already":
                    return await message.reply_text("<b>This Channel Is Already Selected ✅</b>. You can Create Votes now!")
                elif setting is False:
                    return await message.reply_text(f"<b>Something Went Wrong 🔴</b>.\n\nTry again with link.")
                else:
                    return await message.reply_text("<b>Channel Selected ✅</b>. You can Create Votes now!\n\n#Note - Whenever you wanna change your voting channel, Just use /channel again.")
            except Exception as err:
                LOGGER(__name__).info(f"ERRORRRRRRRRRRRRR >> \n\n{err}")
                return
        except Exception as err:
            print(err)
            LOGGER(__name__).info(f"ERRORRRRRRRRRRRRR >> \n\n{err}")
            return

    else:
        if channel_link.startswith("https://t.me/"):
            if channel_link.startswith("https://t.me/+"):
                try:
                    channel_detect = await app.get_chat(channel_link)
                    channel_owned = message.from_user.id
                    if await check_admin(channel_detect.id, channel_owned) == False:
                        return await message.reply(f"🤚 You are not an Owner or Admin in {channel_link} ")
                    setting = await set_channel(channel_owned, channel_detect.id)
                    await add_served_channel(channel_detect.id)
                    if setting:
                        return await message.reply_text("<b>Channel Selected ✅</b>. You can Create Votes now!\n\n#Note - Whenever you wanna change your voting channel, Just use /channel again.")
                    elif setting == "updated":
                        return await message.reply_text("<b>New Channel Updated ✅</b>. You can Create Votes now!")
                    elif setting == "already":
                        return await message.reply_text("<b>This Channel Is Already Selected ✅</b>. You can Create Votes now!")
                    else:
                        return await message.reply_text("<b>Channel Selected ✅</b>. You can Create Votes now!\n\n#Note - Whenever you wanna change your voting channel, Just use /channel again.")
                except Exception as err:
                    return await message.reply_text("<b>⚠ CHANNEL PRIVATE : </b>\nPlease Add me in your channel then send /id command in your channel. then copy your channel ID and send here by /channel [ Channel ID ]")
            else:
                channel_link = channel_link.split("/")[-1]
                try:
                    channel_detect = await app.get_chat(channel_link)
                except:
                    return await message.reply_text("<b>Wrong Channel Link 🔴</b> . Check Link or Give Channel ID by sending /id in your channel.")
                channel_owned = message.from_user.id
                if await check_admin(channel_detect.id, channel_owned) == False:
                    return await message.reply(f"🤚 You are not an Owner or Admin in {channel_link} ")

                try:
                    setting = await set_channel(channel_owned, channel_detect.id)
                    await add_served_channel(channel_detect.id)
                    if setting:
                        return await message.reply_text("<b>Channel Selected ✅</b>. You can Create Votes now!\n\n#Note - Whenever you wanna change your voting channel, Just use /channel again.")
                    elif setting == "updated":
                        return await message.reply_text("<b>New Channel Updated ✅</b>. You can Create Votes now!")
                    elif setting == "already":
                        return await message.reply_text("<b>This Channel Is Already Selected ✅</b>. You can Create Votes now!")
                    else:
                        return await message.reply_text("<b>Channel Selected ✅</b>. You can Create Votes now!\n\n#Note - Whenever you wanna change your voting channel, Just use /channel again.")
                except Exception as err:
                    return await message.reply_text(f"<b>Something Went Wrong 🔴</b>. Please try again after sometime waiting (Due to database server busy) or report this issue to my owner.\n\n{err}")
        elif channel_link.startswith("@"):
            channel_link = channel_link[1:]
            try:
                channel_detect = await app.get_chat(channel_link)
            except:
                return await message.reply_text("<b>Wrong Channel Username 🔴</b> . Check Link or Give Channel ID by sending /id in your channel.")
            channel_owned = message.from_user.id
            if await check_admin(channel_detect.id, channel_owned) == False:
                return await message.reply(f"🤚 You are not an Owner or Admin in {channel_link} ")

            try:
                setting = await set_channel(channel_owned, channel_detect.id)
                await add_served_channel(channel_detect.id)
                if setting:
                    return await message.reply_text("<b>Channel Selected ✅</b>. You can Create Votes now!\n\n#Note - Whenever you wanna change your voting channel, Just use /channel again.")
                elif setting == "updated":
                    return await message.reply_text("<b>New Channel Updated ✅</b>. You can Create Votes now!")
                elif setting == "already":
                    return await message.reply_text("<b>This Channel Is Already Selected ✅</b>. You can Create Votes now!")
                else:
                    return await message.reply_text("<b>Channel Selected ✅</b>. You can Create Votes now!\n\n#Note - Whenever you wanna change your voting channel, Just use /channel again.")
            except Exception as err:
                return await message.reply_text(f"<b>Something Went Wrong 🔴</b>. Please try again after sometime waiting (Due to database server busy) or report this issue to my owner.\n\n\n{err}")


@app.on_message(filters.command(["vote"]) & filters.private)
async def create_polls(_, message):
    user_idd = message.from_user.id
    if config.FORCE_JOIN is True:
        from EdenBot.modules.owner_plugins import get_channel_id
        chat_id_channel = await get_channel_id()
        if await check_user(chat_id_channel, user_idd) is False:
            return await message.reply_text("<b>Please Join Our Channel Before Using The Bot.</b>", reply_markup=channel_button)
    #if await get_channel(user_idd):
    try:
        try:
            send_to_channel = await get_channel(user_idd)
        except (KeyError, ValueError):
            return await message.reply_text("<b>You Didn't Setup any channel</b>. Setup your channel by /channel [Channle link or ID]")
        except:
            return await message.reply_text("<b>You Didn't Setup any channel</b>. Setup your channel by /channel [Channle link or ID]")
    except:
        return await message.reply_text("<b>You Didn't Setup any channel</b>. Setup your channel by /channel [Channle link or ID]")

    if len(message.text.split(" ")) > 1:
        noughty_text = message.text.split(" ")[1:]
    else:
        return await message.reply_text("use this command like /vote ayush to create a vote")

    if await is_set_channel(user_idd):
        if await check_admin(send_to_channel, user_idd) == False:
            return await message.reply(f"You are not Owner or Admin in {send_to_channel}. Please be an admin or setup your own channel using /channel [Channle ID or Link]")
    else:
        return await message.reply_text("<b>You Didn't Setup any channel</b>. Setup your channel by /channel [Channle link or ID]")


    try:
        Noughty_text = ' '.join(noughty_text)
        textung = f"📮 Name : <b>{Noughty_text}</b>\n\n⛱ __Created By__ : {message.from_user.first_name}"
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text=f'🔷 0 Votes 🔷', callback_data="vote_now")]])
        
        await app.send_message(chat_id = send_to_channel, text= textung, reply_markup=keyboard)
        await add_one_poll()
        return await message.reply_text(f"<b>Vote Poll Created</b> ✅\nCreated In : {send_to_channel}")
    except ChatAdminRequired:
        return message.reply_text(f"⚠ I can't detect your channel.\n maybe I am not an admin in your channel. Please make me admin there then try again.")
    except RightForbidden:
        return message.reply_text(f"⚠ I have no rights in your channel. Please give me at lease delete and posting's rights to work.")
    except Exception as err:
        return await message.reply_text(f"<b>Something Went Wrong 🔴</b>. Please try again after waiting sometime (Due to database server busy) or report this issue to my owner.")




@app.on_callback_query(filters.regex("vote_now"))
async def votingg(_, query):
    user_di = query.from_user.id
    chat_id = query.message.chat.id
    message_id = query.message.id
    msg = await app.get_messages(chat_id, message_id)
    message_date = str(msg.date)[8:10]
    message_time = str(msg.date)[11:13]
    today_date = int(time_date_india()[0])
    current_hour = int(time_date_india()[1])
    elector_id = str(str(chat_id) + "/" + str(message_id) + "/" + str(message_date))

    """if (int(message_time) + 6) <= current_hour:
        await query.answer("Poll Ended Few Moments Ago 🍟")
        total_votes = await count_votes(elector_id)
        new_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text=f'🗳 {total_votes} Voted 🗳', url=f"@{botusername}")]])
        await query.edit_message_reply_markup(new_markup)
        return"""


    if int(message_date) != today_date:
        await query.answer("Poll Ended Long Time Ago 🍟")
        total_votes = await count_votes(elector_id)
        new_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text=f'🗳 {total_votes} Voted 🗳', url=f"@{botusername}")]])
        await query.edit_message_reply_markup(new_markup)
        return


    if await check_user(chat_id, user_di) is False:
        return await query.answer("JOIN THE CHANNEL FOR VOTING 🟥")
    if await is_elector(elector_id) is True:
        try:
            processing_vote = await add_vote(elector_id, user_di, chat_id)
            if processing_vote is True:
                em = random.choices(emojis)
                await query.answer("You Voted ✅")
                await sleep(0.7)
                total_votes = await count_votes(elector_id)
                new_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text=f'{em[0]}  {total_votes}  {em[0]}', callback_data="vote_now")]])
                await query.edit_message_reply_markup(new_markup)
                #return
            else:
                em = random.choices(emojis)
                await query.answer("You Took Your Vote Back 🔻")
                await sleep(0.7)
                total_votes = await count_votes(elector_id)
                new_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text=f'{em[0]}  {total_votes}  {em[0]}', callback_data="vote_now")]])
                await query.edit_message_reply_markup(new_markup)
                return
        except Exception as err:
            return
    else:
        try:
            creation = await create_elector(elector_id, user_di, chat_id)
            if creation is True:
                em = random.choices(emojis)
                await query.answer("You Voted ✅")
                await sleep(0.7)
                total_votes = await count_votes(elector_id)
                new_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text=f'{em[0]}  {total_votes}  {em[0]}', callback_data="vote_now")]])
                await query.edit_message_reply_markup(new_markup)
                return
            else:
                return print("Creation not completed due to database error.")
        except Exception as err:
            return print(err)
    return
