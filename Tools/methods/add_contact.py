from pyrogram import Client
from ..info import logger
import asyncio

class AddContact:
    async def add_contact(
        phone_number: str,
        session_string: str,
        username: str,
        first_name: str,
        contact_number = None,
        last_name = None
    ):

        app = Client(phone_number, session_string=session_string)

        await app.connect()

        try:
            if contact_number is not None:
                await app.add_contact(
                    user_id=username,
                    phone_number=contact_number,
                    first_name=first_name,
                    last_name=last_name
                )
            else:
                await app.add_contact(
                    user_id=username,
                    first_name=first_name
                )
            await app.disconnect()
            return 1
        except Exception as e:
            logger.exception(e)
            await app.disconnect()
            return 0
