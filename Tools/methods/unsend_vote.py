from pyrogram import Client
from ..info import logger
from ..parser import process_post_link
from typing import Union

class UnsendVote:
    async def unsend_vote(
        phone_number: str,
        session_string: str,
        link: str,
    ):
        link = process_post_link(link)

        app = Client(phone_number, session_string=session_string)

        await app.connect()

        try:
            await app.retract_vote(link["chat"],link["id"])
            await app.disconnect()
            return 1
        except Exception as e:
            logger.exception(e)
            await app.disconnect()
            return 0

