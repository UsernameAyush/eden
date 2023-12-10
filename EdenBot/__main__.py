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
import importlib

from EdenBot import botusername
from pyrogram import idle
from .logging import LOGGER
from EdenBot.modules import ALL_MODULES

loop = asyncio.get_event_loop()


async def initiate_bot():
    LOGGER("EdenBot.Modules").info("Modules Imported!")
    for all_module in ALL_MODULES:
        importlib.import_module("EdenBot.modules." + all_module)
    LOGGER("EdenBot.Modules").info("Starting Bot...")
    LOGGER("Bot Status").info(f"{botusername} Started!")
    await idle()
    print("Stoped Bot.")


if __name__ == "__main__":
    loop.run_until_complete(initiate_bot())
