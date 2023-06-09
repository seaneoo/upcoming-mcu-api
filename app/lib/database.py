
import certifi
import motor.motor_asyncio

from config import config

_connection_uri = config['MONGO_CONNECTION_URI']

client = motor.motor_asyncio.AsyncIOMotorClient(
    _connection_uri, tlsCAFile=certifi.where())

database = client['upcomingmcu']
collection = database['productions']
