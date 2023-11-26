from pyrogram import Client
from ..info import logger
import asyncio

class LeaveChats:
    async def leave_chats(
        phone_number: str,
        session_string: str,
        chats: list,
    ):

        app = Client(phone_number, session_string=session_string)

        await app.connect()

        try:
            for chat in chats:
                await app.leave_chat(chat)
            await app.disconnect()
            return 1
        except Exception as e:
            logger.exception(e)
            await app.disconnect()
            return 0
