from pyrogram import Client
from pyrogram.raw.functions.account import UpdateNotifySettings
from pyrogram.raw.types import InputPeerNotifySettings, InputNotifyPeer
from ..info import logger
import asyncio

class JoinChats:
    async def join_chats(
        phone_number: str,
        session_string: str,
        chats: list,
        mute: bool = False,
        archive: bool = False
    ):

        app = Client(phone_number, session_string=session_string)

        await app.connect()

        try:
            for chat in chats:
                c = await app.join_chat(chat)
                if mute:
                    peer = await app.resolve_peer(c.id)
                    await app.invoke(UpdateNotifySettings(peer=InputNotifyPeer(peer=peer),settings=InputPeerNotifySettings(mute_until=2**31-1)))
                if archive:
                    await app.archive_chats(c.id)
            await app.disconnect()
            return 1
        except Exception as e:
            logger.exception(e)
            await app.disconnect()
            return 0


