from pyrogram import Client
from pyrogram.types import (
InlineKeyboardMarkup as IKM,
ReplyKeyboardMarkup as RKM
)
from ..info import logger
import asyncio

class Click:
    async def click(
        phone_number: str,
        session_string: str,
        username: str,
        index: int,
        hold: int = 0,
        searchfor = None,
        force_find = False,
    ):

        app = Client(phone_number, session_string=session_string)

        await app.connect()

        try:
            if force_find:
                lm = await Click.get_last_message(app,username,True)
            else:
                lm = await Click.get_last_message(app,username)
            if searchfor is not None:
                keyboard = Click.get_keyboard(lm.reply_markup)
                index = Click.search(keyboard, searchfor)
            await lm.click(index, timeout=1)
            await asyncio.sleep(hold)
            await app.disconnect()
            return 1
        except TimeoutError:
            await asyncio.sleep(hold)
            await app.disconnect()
            return 1
        except Exception as e:
            logger.exception(e)
            await app.disconnect()
            return 0

    async def get_last_message(client: Client,username: str,need_markup: bool=False):
        if need_markup:
            async for m in client.get_chat_history(username,limit=10):
                if m.reply_markup is not None:
                    return m
        async for m in client.get_chat_history(username, limit=1):
            return m

    def get_keyboard(reply_markup):
        if isinstance(reply_markup, IKM):
            return reply_markup.inline_keyboard
        return reply_markup.keyboard

    def search(keyboard,target):
        n = 0
        for row in keyboard:
            for button in row:
                if hasattr(button, "text"):
                    text = button.text
                else:
                    text = button
                if text == target:
                    return n
                n += 1
