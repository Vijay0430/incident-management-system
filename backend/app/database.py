import redis
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# REDIS
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)
# MONGODB
mongo_client = MongoClient(
    "mongodb://localhost:27017"
)

mongo_db = mongo_client["ims"]

signals_collection = mongo_db["signals"]

# POSTGRESQL
DATABASE_URL = "postgresql://admin:admin@localhost:5432/ims"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine
)
