from pyrogram import Client
from ..info import logger
from ..parser import process_post_link
from typing import Union

class SendVote:
    async def send_vote(
        phone_number: str,
        session_string: str,
        link: str,
        choices: Union[int,list],
        button: bool = False,
    ):
        link = process_post_link(link)

        app = Client(phone_number, session_string=session_string)

        await app.connect()

        try:
            if button:
                msg = await SendVote.get_message(app,link["chat"],link["id"])
                await msg.click(choices)
            else:
                await app.vote_poll(link["chat"],link["id"],choices)
            await app.disconnect()
            return 1
        except Exception as e:
            logger.exception(e)
            await app.disconnect()
            return 0

    async def get_message(app,chat_id,message_id):
        message = await app.get_messages(
            chat_id=chat_id,
            message_ids=message_id
        )
        return message
