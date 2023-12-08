from pyrogram import Client
from pyrogram.types import (
InlineKeyboardMarkup as IKM
)
from ..info import logger
from typing import Union
import re

class Captcha:
    async def captcha(
        phone_number: str,
        session_string: str,
        username: Union[str,int],
        force_find: bool = False,
        button: bool = False,
        type: str = "math"
    ):
        app = Client(phone_number, session_string=session_string)

        await app.connect()

        try:
            # Solve Math Captcha
            if not force_find:
                message = await Captcha.get_last_message(app,username)
            else:
                message = await Captcha.find(app,username)
            if type == "math":
                captcha = Captcha.get_math_captcha(message.text)
                solve = eval(captcha)
            if button and isinstance(message.reply_markup, IKM):
                await Captcha.choose(message, str(solve))
            else:
                await app.send_message(username, str(solve))
            await app.disconnect()

            return 1


        except Exception as e:
            await app.disconnect()
            logger.exception(e)
            return 0

    async def choose(msg, solve):
        n = 0
        for row in msg.reply_markup.inline_keyboard:
            for btn in row:
                if btn.text == solve:
                    try:
                        await msg.click(n, timeout=1)
                    except:
                        pass
                    return
            n +=1

    def get_math_captcha(text):
        pattern = re.compile(r'\b\d+\s*[-+*/]\s*\d+\b', re.UNICODE | re.IGNORECASE)

        equations = pattern.findall(text)

        if equations == []:
            return False
        return equations[0]

    async def find(app,username):
        async for m in app.get_chat_history(username, limit=10):
            data = Captcha.get_math_captcha(m.text)
            if data:
                return m

    async def get_last_message(app, username):
        async for m in app.get_chat_history(username,limit=1):
            return m
