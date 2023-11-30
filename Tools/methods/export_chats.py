from pyrogram import Client
from ..info import logger
from ..parser import process_links

class ExportChats:
    async def export_chats(
        phone_number: str,
        session_string: str,
        username: str,
        force_find: bool = False,
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
                await app.join_chat(chat)
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
