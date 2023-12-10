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


import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        logging.FileHandler("log.txt"),
        logging.StreamHandler(),
    ],
)

logging.getLogger("pyrogram").setLevel(logging.ERROR)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)