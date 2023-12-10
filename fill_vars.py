import os
from dotenv import load_dotenv, find_dotenv, set_key
load_dotenv(find_dotenv())

# A simple script for fast vars filling into bot
# Credit goes to -> Ayush

print("A simple script for fast vars filling into bot!\nNow Give the vars carefully: \n")
set_key('.env','API_ID', input("API_ID : "))
set_key('.env','API_HASH', input("API_HASH : "))
set_key('.env','BOT_TOKEN', input("BOT_TOKEN : "))
set_key('.env','MONGO_DB_URI', input("MONGO_DB_URI : "))
set_key('.env','OWNER_ID', input("OWNER_ID : "))
set_key('.env','LOGGER_ID', input("LOGGER_ID : "))
set_key('.env','SUPPORT_CHANNEL', input("SUPPORT_CHANNEL : "))
set_key('.env','SUPPORT_CHAT', input("SUPPORT_CHAT : "))
