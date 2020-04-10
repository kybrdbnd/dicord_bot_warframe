import os
import pytz
from pymongo import MongoClient

TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')
GENERAL_CHANNEL_ID = os.getenv('GENERAL_CHANNEL_ID')
GIVEAWAY_CHANNEL_ID = os.getenv('GIVEAWAY_CHANNEL_ID')
USER_ID = os.getenv('USER_ID')
MONGO_URL = os.getenv('MONGO_URL')
INTRODUCTION_CHANNEL_ID = os.getenv('INTRODUCTION_CHANNEL_ID')
timeZone = pytz.timezone('Asia/Kolkata')
REACTIONS_LIST = ['🇦', '🇧', '🇨', '🇩', '🇪']
relics_tiers = ['Axi', 'Lith', 'Neo', 'Meso', 'Requiem']
mission_type = ['Capture', 'Mobile Defense', 'Defense', 'Rescue', 'Sabotage', 'Exterminate', 'All', 'Survival',
                'Assault', 'Spy', 'Excavation']
DEFAULT_MISSION_TYPE = 'Capture'
IGN_COLLECTION_NAME = 'ign'
GIVEAWAY_COLLECTION_NAME = 'Giveaway'

conn = MongoClient(MONGO_URL)
db = conn['warframe_india']
