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




import asyncio
import random
from typing import Dict, List, Union
from EdenBot import mongodb, votedb
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio



# First Database In MongoDB For Storing Hard Copy Of Basic Information.
chatsdb = mongodb.groups
channelsdb = mongodb.channels # Ab sudo users ke liye banana hai check/add/delete
usersbase = mongodb.userbase
polls_count = mongodb.polls


channel_setting = mongodb.channelsetting

async def live_polls_inList():
    existing_electors = await votedb.list_collection_names()
    Currently_On_Going_Polls = existing_electors
    str_list = []
    for i in Currently_On_Going_Polls:
        str_list.append(str(i))
    return str_list


async def live_polls():
    existing_electors = await votedb.list_collection_names()
    Currently_On_Going_Polls = len(existing_electors)
    return Currently_On_Going_Polls


async def total_polls():
    polls_countt = await polls_count.count_documents({})
    return polls_countt


async def add_one_poll():
    try:
        await polls_count.insert_one({"DummyPoll": "DummyPoll"})
    except:
        return



# Channel Setting Databse

async def is_set_channel(channel_owner_id):
    channel_get = await channel_setting.find_one({"Owner_ID": channel_owner_id})
    if not channel_get:
        return False
    return True

async def set_channel(channel_owner_id, channel_id):
    is_set = await is_set_channel(channel_owner_id)
    if is_set:
        get_owner = await channel_setting.find_one({"Owner_ID": channel_owner_id})
        old_channel_id = get_owner["channel_id"]
        if str(old_channel_id) == str(channel_id):
            return "already"
        else:
            New_Channel = await channel_setting.update_one({"Owner_ID": channel_owner_id}, {"$set": {"channel_id": channel_id}})
            return "updated"
    channel_setting.insert_one({"Owner_ID": channel_owner_id, "channel_id": channel_id})
    return True

async def get_channel(channel_owner_id):
    is_set = await is_set_channel(channel_owner_id)
    if is_set:
        get_owner = await channel_setting.find_one({"Owner_ID": channel_owner_id})
        channel_id = get_owner["channel_id"]
        return int(channel_id)
    return False




# Elector (Poll) Creating & getting
async def is_elector(elector_id):
    elector = str(elector_id)
    existing_electors = await votedb.list_collection_names()
    if elector not in existing_electors:
        return False
    else:
        return True

async def create_elector(elector_id, voter_id, channel_id):
    elector = str(elector_id)
    checking = await is_elector(elector)
    if checking:
        return
    else:
        New_Elector = votedb[elector]
        justPro = await New_Elector.insert_one({"_id": f"{voter_id}", "Channel": channel_id})
        return True


# adding, checking, deleting vote at the same time
async def add_vote(elector_id, voter_id, channel_id):
    Elector =  str(elector_id)
    try:
        vote_info = await votedb[Elector].find_one({"_id": f"{voter_id}", "Channel": channel_id})
        if vote_info:
            await votedb[Elector].delete_one({"_id": f"{voter_id}", "Channel": channel_id})
            return False
            #await votedb[Elector].insert_one({"_id": f"{voter_id}", "Channel": channel_id})
            #return True
        else:
            await votedb[Elector].insert_one({"_id": f"{voter_id}", "Channel": channel_id})
            return True
    except Exception as lol:
        print(lol)
        #await votedb[Elector].delete_one({"_id": f"{voter_id}", "Channel": channel_id})
        return False



async def count_votes(elector_id):
    New_Elector = votedb[elector_id]
    total_documents = await New_Elector.count_documents({})
    return total_documents





async def get_served_chats() -> list:
    chats = chatsdb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return []
    chats_list = []
    for chat in await chats.to_list(length=1000000000):
        chats_list.append(chat)
    return chats_list


async def is_served_chat(chat_id: int) -> bool:
    chat = await chatsdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True


async def add_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if is_served:
        return
    return await chatsdb.insert_one({"chat_id": chat_id})



async def get_served_users() -> list:
    #served_users = await usersbase.find({"user_id": {"$lt": 0}}).to_list(length=1000000000)
    chats = usersbase.find({"user_id": {"$gt": 0}})
    if not chats:
        return []
    chats_list = []
    for chat in await chats.to_list(length=1000000000):
        chats_list.append(chat)
    return chats_list


async def is_served_user(user_id: int) -> bool:
    chat = await usersbase.find_one({"user_id": user_id})
    if not chat:
        return False
    return True


async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await usersbase.insert_one({"user_id": user_id})





async def get_served_channels() -> list:
    chats = channelsdb.find({"channel_id": {"$lt": 0}})
    if not chats:
        return []
    chats_list = []
    for chat in await chats.to_list(length=1000000000):
        chats_list.append(chat)
    return chats_list


async def is_served_channel(channel_id: int) -> bool:
    chat = await channelsdb.find_one({"channel_id": channel_id})
    if not chat:
        return False
    return True


async def add_served_channel(channel_id):
    is_served = await is_served_channel(channel_id)
    if is_served:
        return
    return await channelsdb.insert_one({"channel_id": channel_id})
