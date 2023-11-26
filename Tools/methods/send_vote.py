from pyrogram import Client
from ..info import logger
from ..parser import process_post_link
from typing import Union

class SendVote:
    async def send_vote(
        phone_number: str,
        session_string: str,
        link: str,
        choices: Union[int,list]
    ):
        link = process_post_link(link)

        app = Client(phone_number, session_string=session_string)

        await app.connect()

        try:
            await app.vote_poll(link["chat"],link["id"],choices)
            await app.disconnect()
            return 1
        except Exception as e:
            logger.exception(e)
            await app.disconnect()
            return 0
