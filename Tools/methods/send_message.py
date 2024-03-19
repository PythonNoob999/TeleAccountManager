from pyrogram import Client
from ..info import logger
from ..parser import lnk
from typing import Union
import asyncio, random

class SendMessage:
    async def send_message(
        phone_number: str,
        session_string: str,
        username: Union[str,int],
        message: Union[str, list],
        reply_to: int = None
    ):
        app = Client(phone_number, session_string=session_string)

        await app.connect()
        message = random.choice(message) if isinstance(message, list) else message

        try:
            if reply_to is not None:
                msg = await app.get_messages(lnk(username), reply_to)
                await msg.reply(message)
            else:
                await app.send_message(lnk(username), message)
            await app.disconnect()
            return 1
        except Exception as e:
            logger.exception(e)
            await app.disconnect()
            return 0

