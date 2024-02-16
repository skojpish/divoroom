from os import getenv
from aiogram import Bot
from dotenv import load_dotenv


load_dotenv('bot/.env')

token = getenv("TOKEN")
bot = Bot(token, parse_mode="HTML")
master_id = getenv("MASTER_ID")
master_username = getenv("MASTER_USERNAME")

