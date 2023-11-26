from pyrogram import Client
from ..info import logger
from ..parser import lnk
import asyncio

class SendMessage:
    async def send_message(
        phone_number: str,
        session_string: str,
        username: str,
        message: str,
    ):

        app = Client(phone_number, session_string=session_string)

        await app.connect()

        try:
            await app.send_message(lnk(username), message)
            await app.disconnect()
            return 1
        except Exception as e:
            logger.exception(e)
            await app.disconnect()
            return 0

