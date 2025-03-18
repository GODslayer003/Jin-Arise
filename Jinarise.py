import enum
import math
import pyrogram
import time
import asyncio
from asyncio import gather
import json
from telegram import ChatPermissions, InputFile
import os
import aiohttp
import parso
import requests
import shutil
from PIL import Image
import tgcrypto
import openai
import pathlib
from pathlib import Path
import glob
import pytz
import imghdr
import PIL
from PIL import Image
import re
from googletrans import Translator
import mimetypes
import imghdr
from collections import deque
import logging
from pyrogram.errors import RPCError
import random
from random import choice
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from pyrogram.errors import UserNotParticipant
from pyrogram.filters import new_chat_members_filter
from pyrogram.raw.types.messages import StickerSet
from pyrogram.raw.functions.messages import GetStickerSet
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client, filters
from pyrogram.filters import chat
from pyrogram.filters import new_chat_members, new_chat_members_filter
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler, Updater
from datetime import datetime, timedelta
from pyrogram.enums import ChatMembersFilter
from pyrogram.enums import ChatMemberStatus
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pyrogram.errors import ChatAdminRequired
import pyrogram.types
from pyrogram.types import Message, Sticker, Photo
from pyrogram.enums import MessageMediaType
from pyrogram import raw
from pyrogram.raw.functions.stickers import CreateStickerSet, AddStickerToSet
from pyrogram.raw.types import InputStickerSetShortName, InputStickerSetItem
from pyrogram.types import InputMediaPhoto
from pyrogram.errors import FloodWait, BadRequest
from pyrogram.raw import functions, types
from pyrogram.types import InputMediaDocument, InputMedia, input_media, InputTextMessageContent
from pyrogram.types import ChatPermissions
import traceback
from pyrogram.raw.functions.messages import GetStickerSet
from pyrogram.raw.types import InputStickerSetShortName, InputStickerSetItem
from pyrogram.errors import UserNotParticipant, PeerIdInvalid, StickersetInvalid
from pyrogram import filters as tg_filters 
from traceback import format_exc
from pyrogram.raw.functions import stickers
import os
import random
import time
import asyncio
from datetime import datetime, timedelta
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import (  # To handle Telegram-specific errors gracefully
    PeerIdInvalid,
    ShortnameOccupyFailed,
    StickerEmojiInvalid,
    StickerPngDimensions,
    StickerPngNopng,
    UserBannedInChannel,
    UserDeactivated,
    UserBlocked,
    StickersetInvalid,
    UserIsBlocked
)
from pyrogram.errors import (
    RPCError, 
    BadRequest, 
    Forbidden, 
    FloodWait, 
    StickersetInvalid, 
    PeerIdInvalid
)

load_dotenv()

# Replace with your actual API credentials
API_ID = 28109322 # Replace with your actual API ID
API_HASH = "93e79f71020f32c3fc78eb85a013515a"
API_TOKEN = "7680103909:AAF4pAGERtFqIr9uu4USVN0dNgFI9SjAYp0" 
BOT_USERNAME = "@JinArisedBot"
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=API_TOKEN)

GEMINI_API_TOKEN = "AIzaSyDdBvqeAkLkOBK53JGenbunDh8Gy4RjwMI"  # Replace with your actual API token
# Gemini API endpoint
GEMINI_API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_TOKEN}'

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of best dialogues from Jin Sung Woo
dialogues = [
    "The Weaker You Are, the Faster You Get Thrown Away, but if You’re Strong, People Will Seek That Strength.",
    "I Will Protect My Family Even if It Means Turning All the Hunters in the World Against Me",
    "You Sure Had a Lot to Say for Someone Who’s About to Die",
    "Frost Monarch. Do Not Assume the Position of the King With Only That Much Power",
    "If the Pain Doesn’t Kill Me, It Will Only Make Me Stronger",
    "If You Guys Are Hunters, I’m Saying You Should Be Ready to Become Hunted",
    "The System Uses Me, and I Use the System",
    "I Feel Like Something Within Me Is Lost Every Time I Get Stronger"
]

# Folder containing GIFs
GIF_FOLDER = "D:\WORKS\ARISE JIN\Starting"
BATTLE_GIF_FOLDER = "d:/WORKS/ARISE JIN/Battle"
# Battle folders and probabilities
LEVELS = {
    "Low Level": (1, "D:\WORKS\ARISE JIN\Low Level"),
    "Mid Level": (2, "D:\WORKS\ARISE JIN\Mid Level"),
    "Top Level": (3, "D:\WORKS\ARISE JIN\Top Level"),
    "Legend Level": (4, "D:\WORKS\ARISE JIN\Legend Level"),
    "Ultra Level": (5, r"D:\WORKS\ARISE JIN\Ultra Level")
}

# Cooldown dictionary
cooldowns = {}

# Group rankings dictionary
group_rankings = {}

# Cooldown time in seconds
WEB_COOLDOWN = 1200  # Example: 5 minutes

team_cooldowns = {}  # Store user cooldowns and their teammates
TEAM_COOLDOWN = timedelta(hours=24)

# User data dictionary
user_data = {}
# Dictionary to store Sukuna mode states
jin_mode = {}

# In-memory storage
user_hp = {}
user_points = {}
user_cooldowns = {}
user_barrier_status = {}
user_protect_status={}
reverse_cooldowns={}
medical_cooldowns={}
counter_cooldowns = {}
hospital_cooldowns = {}  # New cooldown dictionary for users with 0 HP
# Initialize user data
user_hp = {}
user_cooldowns = {}
user_barrier_status = {}
user_points = {}
counter_cooldowns = {}

def get_random_image(folder):
    if not os.path.exists(folder) or not os.listdir(folder):
        return None
    return os.path.join(folder, random.choice(os.listdir(folder)))

TOTAL_HP = 1000
BARRIER_COOLDOWN = timedelta(hours=5)
RESET_COOLDOWN = timedelta(minutes=5)
# Constants
TOTAL_HP = 1000  # Total health points for users
COOLDOWN_CURSE = timedelta(minutes=5)  # 10 minutes cooldown for curse
BARRIER_COOLDOWN = timedelta(hours=5)  # Barrier cooldown
RESET_COOLDOWN = timedelta(minutes=10)  # Reset cooldown
COUNTER_COOLDOWN = timedelta(minutes=5)  # Cooldown for COUNTER action
HOSPITAL_COOLDOWN = timedelta(hours=5)
PROTECT_COOLDOWN= timedelta(minutes=45)
REVERSE_COOLDOWN= timedelta(minutes=8)
MEDICAL_COOLDOWN= timedelta(hours=10)
COOLDOWN_SOUL = timedelta(minutes=8)

# File paths
user_data_file = "user_data.json"
domain_folder = "DOMAIN"
cursed_folder = "CURSE"
counter_folder = "BLOCKED"


def select_random_image():
    level, folder = random.choices(list(LEVELS.items()), weights=[level[0] for level in LEVELS.values()])[0]
    image_file = random.choice(os.listdir(folder))
    image_path = os.path.join(folder, image_file)
    return image_path, level


# Utility functions
def get_random_image(folder):
    """Return a random image path from the specified folder."""
    images = [f for f in os.listdir(folder) if f.endswith('.jpg')]
    if images:
        return os.path.join(folder, random.choice(images))
    return None

# Function to format remaining time
def format_remaining_time(cooldown_end_time):
    remaining_time = cooldown_end_time - datetime.now()
    minutes, seconds = divmod(remaining_time.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def is_on_cooldown(user_id, command):
    """Check if the user is on cooldown for a specific command."""
    cooldowns = user_cooldowns.get(user_id, {})
    if isinstance(cooldowns, dict):  # Ensure cooldowns is a dictionary
        command_cooldown = cooldowns.get(command, None)
        if command_cooldown is not None and datetime.now().timestamp() < command_cooldown:
            return True
    return False

async def get_sticker_set_by_name(client, pack_name):
    try:
        return await client.get_sticker_set(pack_name)
    except Exception as e:
        logger.error(f"Failed to get sticker set: {str(e)}")
        return None
    
async def create_sticker_set(client, user_id, title, short_name, stickers):
    try:
        await client.create_sticker_set(user_id, title, short_name, stickers)
        return True
    except Exception as e:
        logger.error(f"Failed to create sticker set: {str(e)}")
        return False

async def add_sticker_to_set(client, stickerset, sticker):
    try:
        await client.add_sticker_to_set(stickerset, sticker)
    except Exception as e:
        logger.error(f"Failed to add sticker to set: {str(e)}")
        raise        

def get_image_type(file_path):
    try:
        with Image.open(file_path) as img:
            return img.format.lower()  # Return 'png', 'jpeg', etc.
    except Exception as e:
        logger.error(f"Failed to identify image type: {str(e)}")
        return None


def activate_barrier(user_id):
    if user_id not in user_barrier_status:
        user_barrier_status[user_id] = {"barrier_active": False, "last_barrier_use": None}
    
    user_barrier_status[user_id]["barrier_active"] = True
    user_barrier_status[user_id]["last_barrier_use"] = datetime.now()



def set_hospital_cooldown(user_id):
    hospital_cooldowns[user_id] = (datetime.now() + HOSPITAL_COOLDOWN).timestamp()

def is_in_hospital(user_id):
    if user_id in hospital_cooldowns:
        cooldown_end = datetime.fromtimestamp(hospital_cooldowns[user_id])
        if datetime.now() < cooldown_end:
            return True, cooldown_end
    return False, None


def set_cooldown(user_id, command, duration):
    if user_id not in user_cooldowns:
        user_cooldowns[user_id] = {}  # Initialize as a dictionary
    user_cooldowns[user_id][command] = (datetime.now() + duration).timestamp()



# Get remaining cooldown time
def get_cooldown_remaining_time(user_id, command):
    cooldown_end = user_cooldowns.get(user_id, {}).get(command, None)
    if cooldown_end:
        remaining_time = cooldown_end - datetime.now()
        if remaining_time.total_seconds() > 0:
            return remaining_time
    return None


def set_counter_cooldown(user_id):
    counter_cooldowns[user_id] = (datetime.now() + COUNTER_COOLDOWN).timestamp()

def is_on_counter_cooldown(user_id):
    if user_id in counter_cooldowns:
        cooldown_end = datetime.fromtimestamp(counter_cooldowns[user_id])
        if datetime.now() < cooldown_end:
            return True
    return False


# Protect (formerly Barrier) activation logic
def activate_protect(user_id):
    if user_id not in user_protect_status:
        user_protect_status[user_id] = {"protect_active": False, "last_protect_use": None}
    
    user_protect_status[user_id]["protect_active"] = True
    user_protect_status[user_id]["last_protect_use"] = datetime.now()

# Medical cooldown management
def set_medical_cooldown(user_id):
    medical_cooldowns[user_id] = (datetime.now() + MEDICAL_COOLDOWN).timestamp()

def is_in_medical_cooldown(user_id):
    if user_id in medical_cooldowns:
        cooldown_end = datetime.fromtimestamp(medical_cooldowns[user_id])
        if datetime.now() < cooldown_end:
            return True, cooldown_end
    return False, None

# General cooldown management for commands
def set_cooldown(user_id, command, duration):
    if user_id not in user_cooldowns:
        user_cooldowns[user_id] = {}  # Initialize as a dictionary
    user_cooldowns[user_id][command] = (datetime.now() + duration).timestamp()

# Get remaining cooldown time for a command
def get_cooldown_remaining_time(user_id, command):
    cooldown_end = user_cooldowns.get(user_id, {}).get(command, None)
    if cooldown_end:
        remaining_time = cooldown_end - datetime.now()
        if remaining_time.total_seconds() > 0:
            return remaining_time
    return None

# Reverse cooldown management
def set_reverse_cooldown(user_id):
    reverse_cooldowns[user_id] = (datetime.now() + COUNTER_COOLDOWN).timestamp()

def is_on_reverse_cooldown(user_id):
    if user_id in reverse_cooldowns:
        cooldown_end = datetime.fromtimestamp(reverse_cooldowns[user_id])
        if datetime.now() < cooldown_end:
            return True
    return False


# Function to load JSON data
def load_json_data(file_path, default_data=None):
    """Load JSON data from a file or return default data if the file is missing or empty."""
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print(f"Error: JSON file {file_path} is corrupted. Initializing empty data.")
                return default_data if default_data is not None else {}
    return default_data if default_data is not None else {}

# Function to save JSON data
def save_json_data(file_path, data):
    """Save JSON data to a file."""
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# Define the path to the user data file
user_data_file = "user_data.json"

# Load data from JSON files
def load_data():
    global user_data
    user_data = load_json_data(user_data_file, default_data={})

# Get a random image from the specified folder
def get_random_image(folder):
    """Get a random image from the specified folder."""
    images = [f for f in os.listdir(folder) if f.endswith('.jpg')]
    return os.path.join(folder, random.choice(images)) if images else None

def initialize_user_data(user_id):
    if user_id not in user_hp:
        user_hp[user_id] = TOTAL_HP
    if user_id not in user_points:
        user_points[user_id] = 0
    if user_id not in user_cooldowns:
        user_cooldowns[user_id] = {}  # Initialize as an empty dictionary
    if user_id not in user_barrier_status:
        user_barrier_status[user_id] = {"barrier_active": False, "barrier_lift_time": None, "last_barrier_use": None}



# Check if a user is an admin in the group
async def is_admin(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    except Exception as e:
        print(f"Error checking admin status: {e}")
        return False


# Start a 26-hour cooldown
def start_26_hour_cooldown(user_id):
    user_cooldowns[user_id] = datetime.now() + timedelta(hours=26)  # 26 hours


# Function to reset the rankings and send announcements
def reset_rankings():
    global group_rankings
    if not group_rankings:
        return
    
    # Sort rankings
    sorted_rankings = sorted(group_rankings.items(), key=lambda x: x[1], reverse=True)
    
    # Top 3 users
    top_users = sorted_rankings[:3]
    announcement = ["🎖️ **Daily Rankings** 🎖️\n"]
    
    for rank, (user_id, stars) in enumerate(top_users, start=1):
        try:
            user = app.get_users(user_id)  # Fetch user details
            user_mention = f"[{user.first_name}](tg://user?id={user_id})"  # Clickable mention
        except:
            user_mention = f"User {user_id}"  # Fallback if user info can't be fetched
        announcement.append(f"{rank}. {user_mention} - **{stars} Stars**")

    announcement.append("\n⭐ Rankings have been reset. Start earning stars again!")
    
    # Send announcement to the group
    app.send_message("@BleachGc+", "\n".join(announcement))

    # Reset rankings
    group_rankings.clear()

    # Reset home command (this can be customized further based on your implementation)
    user_data.clear()  # Assuming user_data holds home data for users

# Function to calculate time to next reset (3rd day at 12:00 AM IST)
async def schedule_reset():
    while True:
        now = datetime.now()
        
        # Calculate the next reset time (3rd day at 12:00 AM IST)
        # IST is UTC +5:30, so adjust accordingly
        ist_now = now + timedelta(hours=5, minutes=30)
        next_reset = ist_now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=(3 - (ist_now.day % 3)))
        
        # Wait until next reset time
        time_to_wait = (next_reset - ist_now).total_seconds()
        if time_to_wait > 0:
            await asyncio.sleep(time_to_wait)
        
        # Trigger the reset every 3rd day
        reset_rankings()
# Initialize the scheduler
scheduler = AsyncIOScheduler()
scheduler.start()

# Schedule the reset at 12:00 AM IST daily
scheduler.add_job(reset_rankings, trigger="cron", hour=0, minute=0)  # 18:30 UTC = 12:00 AM IST


def get_random_mp4(folder_path):
    """Get a random .mp4 file from a given folder."""
    mp4_files = [f for f in os.listdir(folder_path) if f.endswith('.mp4')]
    if not mp4_files:
        return None
    return os.path.join(folder_path, random.choice(mp4_files))


def merge_images(image1_path, image2_path):
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)
    merged_image = Image.new("RGB", (image1.width + image2.width, max(image1.height, image2.height)))
    merged_image.paste(image1, (0, 0))
    merged_image.paste(image2, (image1.width, 0))
    merged_image_path = "d:/WORKS/ARISE JIN/merged_image.jpg"
    merged_image.save(merged_image_path)
    return merged_image_path

async def get_user_profile_photo(client, user_id):
    photos = client.get_chat_photos(user_id)
    async for photo in photos:
        return photo.file_id
    return None

def get_exp_gained(level):
    exp_gains = {
        "Low Level": 100,
        "Mid Level": 200,
        "Top Level": 300,
        "Legend Level": 400,
        "Ultra Level": 500
    }
    return exp_gains[level]

def get_user_level(exp):
    if exp >= 1500:
        return 4
    elif exp >= 1000:
        return 3
    elif exp >= 500:
        return 2
    else:
        return 1

@app.on_message(filters.command("start"))
async def start(client, message):
    # Select a random GIF from the folder
    gif_file = random.choice(os.listdir(GIF_FOLDER))
    gif_path = os.path.join(GIF_FOLDER, gif_file)
    
    # Select a random dialogue
    dialogue = random.choice(dialogues)
    
    # Send the GIF with the dialogue as caption
    await client.send_animation(
        chat_id=message.chat.id,
        animation=gif_path,
        caption=dialogue
    )

@app.on_message(filters.command("arise"))
async def battle(client, message: Message):
    global group_rankings
    user_id = message.from_user.id
    user_mention = f"[{message.from_user.first_name}](tg://user?id={user_id})"

    # Check cooldown for the battle command
    last_used = user_data.get(user_id, {}).get("last_battle", 0)
    if time.time() - last_used < WEB_COOLDOWN:
        remaining_time = WEB_COOLDOWN - (time.time() - last_used)
        await message.reply_text(
            f"⏳ {user_mention}, you need to wait {int(remaining_time // 60)} minutes and {int(remaining_time % 60)} seconds to use /arise again."
        )
        return

    # Define level folder and emoji mapping
    level_probabilities = [50, 40, 35, 30, 20]
    level_names = ["Low Level", "Mid Level", "Top Level", "Legend Level", "Ultra Level"]
    level = random.choices(level_names, weights=level_probabilities, k=1)[0]
    level_folder = LEVELS[level][1]
    level_emojis = {
        "Low Level": "🟢",  # Green Emoji
        "Mid Level": "🔵",  # Blue Emoji
        "Top Level": "⚫",  # Black Emoji
        "Legend Level": "🟣",  # Purple Emoji
        "Ultra Level": "🟡",  # Golden Emoji
    }
    emoji = level_emojis.get(level, "⭐")  # Default to star emoji

    # Select random character 
    if not os.listdir(level_folder):
        await message.reply_text(f"No characters available in the {level} folder.")
        return

    character_file = random.choice(os.listdir(level_folder))
    character_name = os.path.splitext(character_file)[0]

    # Store character
    user_store = user_data.setdefault(user_id, {}).setdefault("store", [])
    user_store.append((character_name, level))
    user_data[user_id]["last_battle"] = time.time()

    # Update rankings
    group_rankings[user_id] = group_rankings.get(user_id, 0) + LEVELS[level][0]

    # Send a random GIF from BATTLE folder with text
    gif_file = random.choice(os.listdir(BATTLE_GIF_FOLDER))
    gif_path = os.path.join(BATTLE_GIF_FOLDER, gif_file)

    try:
        # Send the GIF with the text message
        gif_message = await message.reply_animation(gif_path, caption="𝗜𝗳 𝘁𝗵𝗲 𝘀𝘆𝘀𝘁𝗲𝗺 𝘂𝘀𝗲𝘀 𝗺𝗲, 𝗜 𝘂𝘀𝗲 𝘁𝗵𝗲 𝗦𝘆𝘀𝘁𝗲𝗺... 𝐁𝐀𝐓𝐓𝐋𝐄!")
        
        # Wait for 3 seconds before deleting the GIF and text
        await asyncio.sleep(5)
        
        # Delete the GIF and text message
        await gif_message.delete()
        
    except Exception as e:
        await message.reply_text(f"⚠️ Failed to send GIF: {e}")
        return

    # Define star mapping
    level_stars = {
        "Low Level": "⭐",
        "Mid Level": "⭐⭐",
        "Top Level": "⭐⭐⭐",
        "Legend Level": "⭐⭐⭐⭐",
        "Ultra Level": "⭐⭐⭐⭐⭐"
    }
    stars = level_stars.get(level, "⭐")  # Default to 1 star

    # Send character image
    character_path = os.path.join(level_folder, character_file)
    with open(character_path, "rb") as character_image:
        await message.reply_photo(
            character_image,
            caption=(f"🎉 Congratulations {user_mention}!\n\n"
                     f"{emoji} You managed to Arise {emoji}\n**{character_name}**\n\n{stars}")
        )



# Define star mapping
level_stars = {
    "Low Level": "⭐",
    "Mid Level": "⭐⭐",
    "Top Level": "⭐⭐⭐",
    "Legend Level": "⭐⭐⭐⭐",
    "Ultra Level": "⭐⭐⭐⭐⭐"
}

@app.on_message(filters.command("shadow"))
async def shadow(client, message):
    user_id = message.from_user.id
    user_mention = f"[{message.from_user.first_name}](tg://user?id={user_id})"

    # Get user characters
    user_store = user_data.get(user_id, {}).get("store", [])
    if not user_store:
        await message.reply_text(
            f"🏠 {user_mention}, your shadow is empty. Use /arise to build characters!"
        )
        return

    # Define emoji mapping
    level_emojis = {
        "Low Level": "🟢",  # Green Emoji
        "Mid Level": "🔵",  # Blue Emoji
        "Top Level": "⚫",  # Black Emoji
        "Legend Level": "🟣",  # Purple Emoji
        "Ultra Level": "🟡",  # Golden Emoji
    }

    # Display characters and total levels
    total_levels = sum(LEVELS[level][0] for _, level in user_store)
    response = [f"🏠 {user_mention}, here are your characters:\n"]
    for idx, (character_name, level) in enumerate(user_store, start=1):
        stars = level_stars.get(level, "⭐")  # Default to 1 star
        response.append(f"{idx}. **{character_name}** {stars}")

    response.append(f"\n✨ Total Levels: {total_levels}")

    # Get user's profile photo
    profile_photo_id = await get_user_profile_photo(client, user_id)
    if profile_photo_id:
        await message.reply_photo(
            photo=profile_photo_id,
            caption="\n".join(response),
            reply_to_message_id=message.id
        )
    else:
        await message.reply_text(
            "\n".join(response),
            reply_to_message_id=message.id
        )



@app.on_message(filters.command("arisers"))
async def hunters(client, message):
    global group_rankings
    user_id = message.from_user.id

    if not group_rankings:
        await message.reply_text("📜 Rankings are empty. Be the first to start earning levels with /arise!")
        return

    # Sort rankings by level count in descending order
    sorted_rankings = sorted(group_rankings.items(), key=lambda x: x[1], reverse=True)
    response = ["📜 **Current Rankings** 📜\n"]

    # Initialize rank categories with emojis
    categories = {
        "**Z+ Rank** 🏆": (1, 3),         # Trophy Emoji
        "**SSS+ Rank** 🔥": (4, 7),      # Fire Emoji
        "**SS Rank** 🌟": (8, 12),       # Star Emoji
        "**S Rank** 💎": (13, 16),       # Gem Emoji
        "**A Rank** 🥇": (17, 20),       # Gold Medal Emoji
        "**B Rank** 🥈": (21, 24),       # Silver Medal Emoji
        "**C Rank** 🥉": (25, 28),       # Bronze Medal Emoji
        "**D Rank** ⚙️": (29, 30),       # Gear Emoji
        "**Newbie Rank** 🌱": (31, float("inf")),  # Seedling Emoji
    }

    # Group users into ranks
    for category, (start, end) in categories.items():
        rank_group = [
            (rank, uid, levels)
            for rank, (uid, levels) in enumerate(sorted_rankings, start=1)
            if start <= rank <= end
        ]
        if rank_group:
            response.append(f"**{category}**")
            for rank, uid, levels in rank_group:
                try:
                    user = await client.get_users(uid)
                    user_name = user.first_name
                except:
                    user_name = f"User {uid}"
                response.append(f"{rank}. {user_name} - **{levels} Rank**")
            response.append("")  # Add spacing between categories

    # Find and append the current user's rank
    user_rank = next((rank for rank, (uid, _) in enumerate(sorted_rankings, start=1) if uid == user_id), None)
    if user_rank:
        user_levels = group_rankings.get(user_id, 0)
        user_mention = f"[{message.from_user.first_name}](tg://user?id={user_id})"
        response.append(
            f"\n🧑‍🎓 {user_mention}, you are ranked **#{user_rank}** with **{user_levels} Lvl**.\n\nJoin @BleachGC for more cmds."
        )
 # Send the response message
    await message.reply_text("\n".join(response))




@app.on_message(filters.command("shelter"))
async def barrier_command(client, message):
    user_id = message.from_user.id
    initialize_user_data(user_id)

    # Check if the user is under cooldown
    if user_id in user_cooldowns and user_cooldowns[user_id] is not None and datetime.now().timestamp() < user_cooldowns[user_id]:
        remaining_time = int(user_cooldowns[user_id] - datetime.now().timestamp())
        hours, seconds = divmod(remaining_time, 3600)
        minutes, seconds = divmod(seconds, 60)
        await message.reply_text(
            f"{message.from_user.first_name}, you are still under cooldown. You can use the **Shelter** command again in {hours} hour(s), {minutes} minute(s), and {seconds} second(s)."
        )
        return

    # Ensure user data is initialized in user_barrier_status
    if user_id not in user_barrier_status:
        user_barrier_status[user_id] = {"barrier_active": False, "barrier_lift_time": None, "last_barrier_use": None}

    # Activate Barrier for the user
    user_barrier_status[user_id]["barrier_active"] = True
    user_barrier_status[user_id]["last_barrier_use"] = datetime.now()
    await message.reply_text("Barrier activated! You are now protected from curses.")

    # Set the cooldown for 3 hours
    user_cooldowns[user_id] = (datetime.now() + BARRIER_COOLDOWN).timestamp()






@app.on_message(filters.command("come"))
async def domain_command(client, message):
    user_id = message.from_user.id
    now = datetime.now()
    initialize_user_data(user_id)

    # Check if the user has an active barrier
    barrier_active = user_barrier_status.get(user_id, {}).get("barrier_active", False)
    if not barrier_active:
        await message.reply_text("No active barrier to lift.")
        return

    # Lift the barrier immediately
    user_barrier_status[user_id]["barrier_active"] = False
    user_barrier_status[user_id]["barrier_lift_time"] = None
    user_barrier_status[user_id]["last_barrier_use"] = now
    await message.reply_text("Barrier has been lifted early!")

    # Reset the cooldown for the Barrier command to 30 minutes
    user_cooldowns[user_id] = (now + RESET_COOLDOWN).timestamp()

    remaining_time = int(user_cooldowns[user_id] - now.timestamp())
    hours, seconds = divmod(remaining_time, 3600)
    minutes, seconds = divmod(seconds, 60)
    await message.reply_text(
        f"You cannot use the **Shelter** command again for {hours} hour(s), {minutes} minute(s), and {seconds} second(s)."
    )




def create_health_bar(current_hp):
    full_blocks = int(current_hp / TOTAL_HP * 20)
    empty_blocks = 20 - full_blocks
    return f"[{'█' * full_blocks}{'░' * empty_blocks}] {current_hp}/{TOTAL_HP} HP"

def initialize_user_data(user_id):
    if user_id not in user_hp:
        user_hp[user_id] = TOTAL_HP
    if user_id not in user_points:
        user_points[user_id] = 0

@app.on_message(filters.command(["health", "hp"]))
async def show_health(client, message):
    user_id = message.from_user.id
    initialize_user_data(user_id)
    hp_bar = create_health_bar(user_hp[user_id])
    await message.reply_text(f"Your Health: {hp_bar}")

@app.on_message(filters.command(["sys", "system"]))
async def curse_command(client, message):
    user_id = message.from_user.id
    target_user_id = None
    
    # Check if the command was a reply to a message
    if message.reply_to_message and message.reply_to_message.from_user:
        target_user = message.reply_to_message.from_user

        # Check if the target is a bot
        if target_user.is_bot:
            await message.reply_text("**Don't be this WEAK!** \nReply to other user, rather then stealing points from a Bot.")
            return

    else:
        await message.reply_text("Reply to a user's message to target them with a curse.")
        return
    
    # Initialize user data for the attacker
    initialize_user_data(user_id)

    # Check if the user is currently in the hospital
    in_hospital, cooldown_end = is_in_hospital(user_id)
    if in_hospital:
        remaining_time = int(cooldown_end.timestamp() - datetime.now().timestamp())
        hours, seconds = divmod(remaining_time, 3600)
        minutes, seconds = divmod(seconds, 60)
        await message.reply_text(
            f"You have been taken down, now recover.\n\nTime needed - {hours} hour(s), {minutes} minute(s), and {seconds} second(s)."
        )
        return

    # If user's HP is 0, set the hospital cooldown and reset their HP and points
    if user_hp[user_id] <= 0:
        set_hospital_cooldown(user_id)
        user_hp[user_id] = TOTAL_HP
        user_points[user_id] = 0
        await message.reply_text("You have been taken down and are being sent for recovery. Your HP and Mana have been reset.")
        return

    # Check if the user is currently on cooldown due to a COUNTER action
    if is_on_counter_cooldown(user_id):
        remaining_time = int(counter_cooldowns[user_id] - datetime.now().timestamp())
        hours, seconds = divmod(remaining_time, 3600)
        minutes, seconds = divmod(seconds, 60)
        await message.reply_text(
            f"Your **Your system was BLOCKED**. You can use it back under {hours} hour(s), {minutes} minute(s), and {seconds} second(s)."
        )
        return

    # Check if the user issuing the command has an active barrier
    if user_id in user_barrier_status and user_barrier_status[user_id].get("barrier_active", False):
        await message.reply_text(f"You are currently protected by a Shelter and cannot use the **system** command.")
        return

    # Check if the user is in the hospital and trying to use the Shelter command
    if message.text.lower() == "/shelter" and in_hospital:
        await message.reply_text("You are resting in Hospital, come back and I shall provide you Shelter.")
        return

    # Check if the command was a reply to another user's message
    if message.reply_to_message and message.reply_to_message.from_user:
        target_user_id = message.reply_to_message.from_user.id
    else:
        await message.reply_text("Reply to a user's message to target them with a curse.")
        return

    # Initialize target user data
    initialize_user_data(target_user_id)

    # Check if the target user has an active barrier
    if user_barrier_status.get(target_user_id, {}).get("barrier_active", False):
        await message.reply_text(f"{message.reply_to_message.from_user.first_name} is protected by a Shelter. You cannot use system against them.")
        return

    # Fetch target user details
    target_user = message.reply_to_message.from_user
    if not target_user:
        await message.reply_text("Target user not found.")
        return

    target_user_id = target_user.id
    target_user_name = target_user.first_name

    # Ensure user HP is initialized
    if target_user_id not in user_hp:
        user_hp[target_user_id] = TOTAL_HP

    if user_id not in user_hp:
        user_hp[user_id] = TOTAL_HP

    # If user's HP is 0, set the hospital cooldown
    if user_hp[user_id] <= 0:
        set_hospital_cooldown(user_id)
        await message.reply_text("You have been taken down and are being sent for recovery.")
        return

    # Random selection for action (DOMAIN, CURSED, COUNTER)
    random_choice = random.choices(
        ["DOMAIN", "CURSE", "BLOCKED"], 
        [0.2, 0.7, 0.1]
    )[0]

    if random_choice == "DOMAIN":
        image_path = get_random_image(domain_folder)
        user_hp[target_user_id] -= 100
        user_points[user_id] = user_points.get(user_id, 0) + 5
        action_message = f"**MONARCH LEVEL** used by [{message.from_user.first_name}](tg://user?id={user_id}) against [{target_user_name}](tg://user?id={target_user_id}). \n -100 Health is Vanished!!"
        # Remove Barrier if target user had it
        if target_user_id in user_barrier_status:
            user_barrier_status[target_user_id]["barrier_active"] = False

    elif random_choice == "CURSE":
        image_path = get_random_image(cursed_folder)
        user_hp[target_user_id] -= 50
        user_points[user_id] = user_points.get(user_id, 0) + 1
        action_message = f"**SS RANK** used by [{message.from_user.first_name}](tg://user?id={user_id}) against [{target_user_name}](tg://user?id={target_user_id}). \n -50 Health is Vanished!!"

    else:  # COUNTER
        image_path = get_random_image(counter_folder)
        user_hp[user_id] += 5
        user_points[user_id] = user_points.get(user_id, 0) - 3
        action_message = f"**BLOCKED** [{message.from_user.first_name}](tg://user?id={user_id}) from [{target_user_name}](tg://user?id={target_user_id}). \n +5 Health is REPLENISHED!!"
        
        # Set cooldown for COUNTER action
        set_counter_cooldown(user_id)

    # Ensure HP is within bounds
    user_hp[target_user_id] = max(0, user_hp[target_user_id])
    user_hp[user_id] = min(TOTAL_HP, user_hp[user_id])

    # If target user's HP reaches 0, they go on a 5-hour cooldown and reset
    if user_hp[target_user_id] == 0:
        set_hospital_cooldown(target_user_id)
        user_hp[target_user_id] = TOTAL_HP
        user_points[target_user_id] = 0
        await message.reply_text(
            f"[{target_user_name}](tg://user?id={target_user_id}) has been taken down successfully and is now recovering for 5 hours."
        )
        return

    # Create health bars for both users
    target_hp_bar = create_health_bar(user_hp[target_user_id])
    user_hp_bar = create_health_bar(user_hp[user_id])

    # Send the image and action message
    if image_path:
        await message.reply_photo(
            photo=image_path,
            caption=f"{action_message}\n\nTarget's Health: {target_hp_bar}\n\nYour Health: {user_hp_bar}"
        )
    else:
        await message.reply_text(action_message)
        return

    # Check if the user issuing the command has an active barrier
    if user_id in user_barrier_status and user_barrier_status[user_id].get("barrier_active", False):
        await message.reply_text(f"You are currently protected by a Shelter and cannot use the **system** command.")
        return

    # Check if the command was a reply to another user's message
    if message.reply_to_message and message.reply_to_message.from_user:
        target_user_id = message.reply_to_message.from_user.id
    else:
        await message.reply_text("Reply to a user's message to target them with a curse.")
        return

    # Initialize target user data
    initialize_user_data(target_user_id)

    # Check if the target user has an active barrier
    if user_barrier_status.get(target_user_id, {}).get("barrier_active", False):
        await message.reply_text(f"{message.reply_to_message.from_user.first_name} is protected by a Shelter. You cannot use system against them.")
        return

    # Fetch target user details
    target_user = message.reply_to_message.from_user
    if not target_user:
        await message.reply_text("Target user not found.")
        return

    target_user_id = target_user.id
    target_user_name = target_user.first_name

    # Ensure user HP is initialized
    if target_user_id not in user_hp:
        user_hp[target_user_id] = TOTAL_HP

    if user_id not in user_hp:
        user_hp[user_id] = TOTAL_HP

    # If user's HP is 0, set the hospital cooldown
    if user_hp[user_id] <= 0:
        set_hospital_cooldown(user_id)
        await message.reply_text("You have been taken down and are being sent for recovery.")
        return

    # Random selection for action (DOMAIN, CURSED, COUNTER)
    random_choice = random.choices(
        ["DOMAIN", "CURSE", "BLOCKED"], 
        [0.2, 0.7, 0.1]
    )[0]

    if random_choice == "DOMAIN":
        image_path = get_random_image(domain_folder)
        user_hp[target_user_id] -= 100
        user_points[user_id] = user_points.get(user_id, 0) + 5
        action_message = f"**MONARCH LEVEL** used by [{message.from_user.first_name}](tg://user?id={user_id}) against [{target_user_name}](tg://user?id={target_user_id}). \n -100 Health is Vanished!!"
        # Remove Barrier if target user had it
        if target_user_id in user_barrier_status:
            user_barrier_status[target_user_id]["barrier_active"] = False

    elif random_choice == "CURSE":
        image_path = get_random_image(cursed_folder)
        user_hp[target_user_id] -= 50
        user_points[user_id] = user_points.get(user_id, 0) + 1
        action_message = f"**SS RANK** used by [{message.from_user.first_name}](tg://user?id={user_id}) against [{target_user_name}](tg://user?id={target_user_id}). \n -50 Health is Vanished!!"

    else:  # COUNTER
        image_path = get_random_image(counter_folder)
        user_hp[user_id] += 5
        user_points[user_id] = user_points.get(user_id, 0) - 3
        action_message = f"**BLOCKED** [{message.from_user.first_name}](tg://user?id={user_id}) from [{target_user_name}](tg://user?id={target_user_id}). \n +5 Health is REPLENISHED!!"
        
        # Set cooldown for COUNTER action
        set_counter_cooldown(user_id)

    # Ensure HP is within bounds
    user_hp[target_user_id] = max(0, user_hp[target_user_id])
    user_hp[user_id] = min(TOTAL_HP, user_hp[user_id])

    # If target user's HP reaches 0, they go on a 26-hour cooldown
    if user_hp[target_user_id] == 0:
        start_26_hour_cooldown(target_user_id)
        await message.reply_text(
            f"[{target_user_name}](tg://user?id={target_user_id}) has been taken down successfully!!"
        )
        return

    # Create health bars for both users
    target_hp_bar = create_health_bar(user_hp[target_user_id])
    user_hp_bar = create_health_bar(user_hp[user_id])

    # Send the image and action message
    if image_path:
        await message.reply_photo(
            photo=image_path,
            caption=f"{action_message}\n\nTarget's Health: {target_hp_bar}\n\nYour Health: {user_hp_bar}"
        )
    else:
        await message.reply_text(action_message)





@app.on_message(filters.command("hunters"))
async def show_rankings(client, message):
    if not user_points:
        await message.reply_text("No records found of your System!")
        return

    # Sort users by points in descending order
    sorted_users = sorted(user_points.items(), key=lambda x: x[1], reverse=True)

    # Initialize ranking categories
    categories = {
        "𝑺𝑺𝑹 𝒓𝒂𝒏𝒌": (1, 1),
        "𝘚𝘚 𝘳𝘢𝘯𝘬": (2, 5),
        "𝘚 𝘳𝘢𝘯𝘬": (6, 10),
        "𝘈 𝘳𝘢𝘯𝘬": (11, 15),
        "𝘉 𝘳𝘢𝘯𝘬": (16, 20),
        "𝘊 𝘳𝘢𝘯𝘬": (21, 30),
        "𝘋 𝘳𝘢𝘯𝘬": (31, 35),
        "𝘊𝘰𝘮𝘮𝘰𝘯𝘦𝘳𝘴": (36, float("inf")),
    }

    # Determine user's rank and build filtered rankings
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    user_rank_category = None
    user_rank_position = None
    user_points_display = None
    ranking_message = "**Here is the List, of Best HUNTERS**\n"
    ranking_message += "**************************************\n"

    for category, (start, end) in categories.items():
        category_users = [
            (idx, user_id, points)
            for idx, (user_id, points) in enumerate(sorted_users, start=1)
            if start <= idx <= end
        ]

        # If category has no users, skip it
        if not category_users:
            continue

        # Add this category to the message
        ranking_message += f"**{category}**\n"

        for idx, uid, points in category_users:
            if uid == user_id:
                user_rank_category = category
                user_rank_position = idx
                user_points_display = points
                ranking_message += f"{idx}. {message.from_user.mention} - {points} **Mana Energy**\n"  # Mention user
            else:
                try:
                    user = await client.get_users(uid)
                    user_name = user.first_name
                    ranking_message += f"{idx}. {user_name} - {points} **Mana Energy**\n"
                except Exception as e:
                    print(f"Error retrieving user info: {e}")
                    ranking_message += f"{idx}. User with ID {uid} - {points} **Mana Energy**\n"

        # Add a border after each category
        ranking_message += "----------------------------------------\n"

        # Break if the user's rank has already been displayed
        if user_rank_category:
            break

    # Add the user's rank to the message
    if user_rank_category:
        ranking_message += f"\n**{message.from_user.mention}, your Official Rank is {user_rank_position}.**"
    else:
        ranking_message += f"\n**{message.from_user.mention}, YOU ARE IN COMMONERS.**"

    # Send the message
    await message.reply_text(ranking_message)


@app.on_message(filters.command("team"))
async def team_up(_, message: Message):
    """
    Finds a random teammate for a battle against Sukuna with 24-hour cooldown.
    Shows team info for replied user if command is replied to someone.
    """
    # Determine whose team info to show
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name
    else:
        user_id = message.from_user.id
        user_name = message.from_user.first_name

    current_time = datetime.now()

    # Generate random percentages with Sukuna having upper hand
    sukuna_percentage = random.randint(50, 100)  # Sukuna gets 75-98%
    team_percentage = 100 - sukuna_percentage   # Team gets remaining percentage

    # Check if user is on cooldown and has an existing teammate
    if user_id in team_cooldowns:
        cooldown_data = team_cooldowns[user_id]
        if current_time < cooldown_data['expire_time']:
            # Get the existing teammate data
            teammate_data = cooldown_data['teammate']
            remaining_time = cooldown_data['expire_time'] - current_time
            hours = int(remaining_time.total_seconds() // 3600)
            minutes = int((remaining_time.total_seconds() % 3600) // 60)

            try:
                # Get teammate's info
                teammate = await app.get_users(teammate_data['id'])
                
                caption = (
                    f"🤝 **Current Team Information for {user_name}**\n\n"
                    f"👥 **Teammate:** {teammate_data['first_name']}\n\n"
                    f"⏳ Team cooldown: **{hours}h {minutes}m** remaining\n\n"
                    f"🎯 **Battle Odds:**\n"
                    f"👹 MONARCH: {sukuna_percentage}%\n"
                    f"💪 {user_name} & {teammate_data['first_name']}: {team_percentage}%\n\n"
                    f"{'🔥 *Even the odds seem against you, your determination burns bright!*' if team_percentage <= 10 else '⚔️ *The battle will be legendary!*'}"
                )

                try:
                    photos = []
                    async for photo in app.get_chat_photos(teammate.id, limit=1):
                        photos.append(photo)
                    
                    if photos:
                        await message.reply_photo(
                            photo=photos[0].file_id,
                            caption=caption
                        )
                    else:
                        await message.reply_text(caption)
                except Exception:
                    await message.reply_text(caption)

            except Exception as e:
                await message.reply_text(f"Error displaying team info: {e}")
            return

    try:
        # Get all chat members
        members = []
        async for member in app.get_chat_members(message.chat.id):
            if (member.user.id != app.me.id and  # Not the bot
                member.user.id != user_id and    # Not the command user
                not member.user.is_bot):         # Not other bots
                members.append(member.user)

        if not members:
            await message.reply_text("❌ No eligible teammates found in this chat!")
            return

        # Choose random teammate
        teammate = random.choice(members)

        # Store teammate data and cooldown
        team_cooldowns[user_id] = {
            'teammate': {
                'id': teammate.id,
                'first_name': teammate.first_name
            },
            'expire_time': current_time + TEAM_COOLDOWN
        }

        # Add different messages based on team percentage
        team_message = (
            "😱 **The odds are terrifying, but heroes never back down!**" if team_percentage <= 5 else
            "💫 **Against all odds, your spirit remains unbroken!**" if team_percentage <= 10 else
            "✨ **Together you might stand a chance!**" if team_percentage <= 15 else
            "🌟 **The power of teamwork knows no bounds!**"
        )

        caption = (
            f"🌟 **New Team Formed for {user_name}!**\n\n"
            f"🤝 **Teammate:** {teammate.first_name}\n\n"
            f"🎯 **Battle Odds:**\n"
            f"👹 MONARCH: {sukuna_percentage}%\n"
            f"💪 {user_name} & {teammate.first_name}: {team_percentage}%\n\n"
            f"{team_message}\n\n"
            f"⏳ Team locked for 24 hours!"
        )

        try:
            photos = []
            async for photo in app.get_chat_photos(teammate.id, limit=1):
                photos.append(photo)
            
            if photos:
                await message.reply_photo(
                    photo=photos[0].file_id,
                    caption=caption
                )
            else:
                await message.reply_text(caption)
        except Exception:
            await message.reply_text(caption)

    except UserNotParticipant:
        await message.reply_text("❌ I need to be a member of this chat first!")
    except Exception as e:
        await message.reply_text(f"❌ Error finding a teammate: {e}")


async def get_jin_response(prompt):
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(GEMINI_API_URL, headers=headers, json=data) as response:
            result = await response.json()
            
            # Debugging: print the entire response to see its structure
            print(result)
            
            # Extract the response text from the API
            try:
                return result['candidates'][0]['content']['parts'][0]['text']
            except (KeyError, IndexError) as e:
                return "I couldn't understand that, try asking something else."

@app.on_message(filters.text)
async def handle_message(client, message):
    user_id = message.from_user.id
    
    # Handle SUKUNA ON and SUKUNA OFF commands
    if message.text.lower() == 'jin on':
        jin_mode[user_id] = 'ON'
        await message.reply_text("Jin mode is now ON. Arise your questions.")
        return  # Exit the function to avoid further processing

    elif message.text.lower() == 'jin off':
        jin_mode[user_id] = 'OFF'
        await message.reply_text("Jin mode is now OFF. I will not respond with my true form.")
        return  # Exit the function to avoid further processing

    # If Sukuna mode is OFF, do not generate a Sukuna response
    if jin_mode.get(user_id, 'OFF') == 'OFF':
        # Simply do nothing or respond with a default message
        # Example: await message.reply_text("Sukuna mode is OFF. No responses will be given.")
        return  # Do nothing

    # Process message with Sukuna's response if Sukuna mode is ON
    if jin_mode.get(user_id, 'OFF') == 'ON':
        try:
            prompt = message.text
            jin_response = await get_jin_response(prompt)
            await message.reply_text(jin_response)
        except Exception as e:
            await message.reply_text(f"An error occurred: {e}")




def convert_time_to_seconds(time_value):
    """Convert a time string (e.g., '1h', '30m') to seconds."""
    unit = time_value[-1]
    value = int(time_value[:-1])
    if unit == 'h':
        return value * 3600
    elif unit == 'm':
        return value * 60
    elif unit == 's':
        return value
    else:
        raise ValueError("Invalid time format. Use 'h', 'm', or 's'.")

async def get_warn(chat_id, user_id):
    # Dummy implementation, replace with actual logic
    return {"warns": 0}

def int_to_alpha(user_id):
    """Convert an integer user ID to an alphabetic string."""
    alpha = ""
    while user_id > 0:
        user_id, remainder = divmod(user_id - 1, 26)
        alpha = chr(65 + remainder) + alpha
    return alpha




if __name__ == "__main__":  
    app.run() 