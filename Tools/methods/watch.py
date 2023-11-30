from pyrogram import Client
from pyrogram.raw.functions.messages import GetMessagesViews
from ..info import logger
from ..parser import process_post_link

class Watch:
    async def watch(
        phone_number: str,
        session_string: str,
        link: str
    ):
        link = process_post_link(link)

        app = Client(phone_number, session_string=session_string)

        await app.connect()

        try:
            peer = await app.resolve_peer(link["chat"])

            await app.invoke(GetMessagesViews(
                peer=peer,
                id=[link["id"]],
                increment=True
            ))
            await app.disconnect()
            return 1

        except Exception as e:
            await app.disconnect()
            logger.exception(e)
            return 0
