from pyrogram import Client
from pyrogram.raw.functions.account import UpdateNotifySettings
from pyrogram.raw.types import InputPeerNotifySettings, InputNotifyPeer
from ..info import logger
from ..parser import process_links
from typing import Union

class ExportChats:
    async def export_chats(
        phone_number: str,
        session_string: str,
        username: Union[str,int],
        force_find: bool = False,
        mute: bool = False,
        archive: bool = False
    ):
        app = Client(phone_number, session_string=session_string)

        await app.connect()

        try:
            if not force_find:
                message = await ExportChats.get_last_message(app,username)
            else:
                message = await ExportChats.find(app,username)

            chats = ExportChats.export(message.reply_markup.inline_keyboard)
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
            await app.disconnect()
            logger.exception(e)
            return 0

    def export(keyboard):
        links = []

        for row in keyboard:
            for button in row:
                if button.url:
                    links.append(button.url)
        return process_links('|'.join(links))

    async def find(app,username):
        async for m in app.get_chat_history(username, limit=10):
            if m.reply_markup is not None:
                return m

    async def get_last_message(app, username):
        async for m in app.get_chat_history(username,limit=1):
            return m
