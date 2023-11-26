from .database import DB
import json
import logging


data = json.load(open("auth.json", "r"))
api_id = data["api_id"]
api_hash = data["api_hash"]
db = DB()
logger = logging.getLogger("TAM")

error_format = """{
    "time": %(asctime)s,
    "name": %(name)s,
    "levelname": %(levelname)s,
    "error": %(message)s,
}"""

info_format = "[%(asctime)s] %(message)s"


shandler = logging.StreamHandler()
fhandler = logging.FileHandler("errors.log")
shandler.setLevel(logging.INFO)
fhandler.setLevel(logging.ERROR)
shandler.setFormatter(logging.Formatter(info_format))
fhandler.setFormatter(logging.Formatter(error_format))

logger.addHandler(shandler)
logger.addHandler(fhandler)
