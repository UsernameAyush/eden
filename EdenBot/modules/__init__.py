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

import glob
from os.path import basename, dirname, isfile


def __list_all_modules():
    mod_paths = glob.glob(dirname(__file__) + "/*.py")

    all_modules = [
        basename(f)[:-3]
        for f in mod_paths
        if isfile(f)
        and f.endswith(".py")
        and not f.endswith("__init__.py")
    ]

    return all_modules


ALL_MODULES = sorted(__list_all_modules())
__all__ = ALL_MODULES + ["ALL_MODULES"]
