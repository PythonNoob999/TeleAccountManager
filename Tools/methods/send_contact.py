from pyrogram import Client
from ..info import logger
from typing import Union
import asyncio

class SendContact:
    async def send_contact(
        phone_number: str,
        session_string: str,
        username: Union[str,int],
        contact_number: str,
        first_name: str,
        last_name = None
    ):

        app = Client(phone_number, session_string=session_string)

        await app.connect()

        app.me = await app.get_me()

        if contact_number == "self":
            contact_number = app.me.phone_number
        if first_name == "self":
            first_name = app.me.first_name
        if last_name == "self":
            last_name = app.me.last_name

        try:
            await app.send_contact(username,phone_number=contact_number,first_name=first_name,last_name=last_name)
            await app.disconnect()
            return 1
        except Exception as e:
            logger.exception(e)
            await app.disconnect()
            return 0
