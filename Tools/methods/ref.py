from pyrogram import Client
from ..info import logger
from ..parser import process_ref_link
import asyncio

class Ref:
    async def ref(
        phone_number: str,
        session_string: str,
        ref_link: str,
    ):
        data = process_ref_link(ref_link)

        app = Client(phone_number, session_string=session_string)

        await app.connect()

        try:
            await app.send_message(data["user"], data["msg"])
            await app.disconnect()
            return 1
        except Exception as e:
            logger.exception(e)
            await app.disconnect()
            return 0
