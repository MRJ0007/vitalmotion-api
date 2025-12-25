import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI not set in environment")

client = MongoClient(MONGO_URI)

# 🔑 Main database
db = client["vitalmotion"]

# 🔑 Collections used across app
sensor_collection = db.sensors
alerts_collection = db.alerts
users_collection = db.users
doctors_collection = db.doctors
# ✅ ADD THIS
doctors = db["doctors"]
users = db["users"]