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

from os import getenv
from dotenv import load_dotenv

load_dotenv()

OWNER_ID = int(getenv("OWNER_ID"))
LOGGER_ID = int(getenv("LOGGER_ID", None))


API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")


BOT_TOKEN = getenv("BOT_TOKEN")


MONGO_DB_URI = getenv("MONGO_DB_URI", None)


SUDO_USER = list(
    map(int, getenv("SUDO_USER", "").split())
)  # Input type must be interger


FORCE_JOIN = True

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/BestForAlways")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/Life_Codes")



START_IMG_URL = "https://i.pinimg.com/236x/57/ec/22/57ec223ee51d8753168de1af3ede1aeb.jpg"
PING_IMG_URL = "https://i.pinimg.com/564x/d9/b5/46/d9b5464b3de60b9b1df325e41cf22fd3.jpg"
STATS_IMG_URL = "https://i.pinimg.com/originals/2f/b8/d3/2fb8d33c12f3816e5bfed7fe614d447a.jpg"


# This Bot Is Made For Raichu