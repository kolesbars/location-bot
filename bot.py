import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.utils import executor
from geopy.geocoders import Nominatim
import asyncio

TOKEN = "YOUR_BOT_TOKEN"
GROUP_ID = -1001234567890  # Замените на ID вашей группы

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

geolocator = Nominatim(user_agent="geo_bot")
user_locations = {}

async def update_group_title():
    if len(user_locations) == 0:
        return
    
    cities = set()
    for user_id, location in user_locations.items():
        latitude, longitude = location
        location_info = geolocator.reverse((latitude, longitude), language="en")
        if location_info and "address" in location_info.raw:
            city = location_info.raw["address"].get("city") or location_info.raw["address"].get("town")
            if city:
                cities.add(city)
    
    if cities:
        new_title = " & ".join(sorted(cities)) + " team"
        await bot.set_chat_title(GROUP_ID, new_title)
        logging.info(f"Updated group title to: {new_title}")

@dp.message_handler(content_types=ContentType.LOCATION)
async def handle_location(message: types.Message):
    user_id = message.from_user.id
    latitude = message.location.latitude
    longitude = message.location.longitude
    user_locations[user_id] = (latitude, longitude)
    await update_group_title()
    await message.reply("Геолокация обновлена!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
