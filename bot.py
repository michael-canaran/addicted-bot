# bot.py

import asyncio
import os
from datetime import datetime
from pymongo import MongoClient

import discord

from activity_check import get_game_activity

DISCORD_AUTH = os.environ.get('DISCORD_TOKEN')
DISCORD_SERVER = os.environ.get('SERVER_NAME')
CHANNEL = os.environ.get('GENERAL')
MONGODB_URI = os.environ.get('MONGODB_URI')

START_DATE = [int(info) for info in os.environ.get('START_DATE').split("/")]
END_DATE = [int(info) for info in os.environ.get('END_DATE').split("/")]

BEGIN = datetime(START_DATE[2], START_DATE[1], START_DATE[0])
END = datetime(END_DATE[2], END_DATE[1], END_DATE[0])

mongo_client = MongoClient(MONGODB_URI)
discord_client = discord.Client()


def valid_timeframe():
    return BEGIN <= datetime.now() <= END


@discord_client.event
async def on_ready():
    for guild in discord_client.guilds:
        print(f"{discord_client.user} is connected to the following server:\n{guild.name}(id: {guild.id})")
    general = discord_client.get_channel(int(CHANNEL))
    if mongo_client is not None:
        print("Connected to MongoDB successfully")
    else:
        print("Could not connect to MongoDB, exiting program")
        exit(-1)
    print(f"Checking for activity between the dates: {START_DATE[0]}/{START_DATE[1]}/{START_DATE[2]} - {END_DATE[0]}/"
          f"{END_DATE[1]}/{END_DATE[2]}")

    while True:
        if valid_timeframe():
            print("Grabbing initial data...")
            game_activity = get_game_activity()
            print("\nSTARTING GAME TRACKER")
            while valid_timeframe():
                print("Checking for game activity...")
                if game_activity != get_game_activity():
                    await general.send("PEDRO IS ADDICTED AND HAS PLAYED LEAGUE AS OF NOW AND OWES SERUNDER, "
                                       "INFUSIONAL, AND SUBARU $100 LUL")
                    print("Game has been played, shutting down.")
                    exit(0)
                print("Waiting 1 minute...")
                await asyncio.sleep(60)
        else:
            sleep_time = BEGIN - datetime.today()
            print("Not within timeframe, bot will be inactive for {} days, will begin monitoring then..."
                  .format(sleep_time.days))
            await asyncio.sleep(sleep_time.total_seconds())


if __name__ == "__main__":
    discord_client.run(DISCORD_AUTH)
