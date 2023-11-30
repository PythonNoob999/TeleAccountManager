from pyrogram import Client
from ..info import logger
import re

class Captcha:
    async def captcha(
        phone_number: str,
        session_string: str,
        username: str,
        force_find: bool = False,
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

            await app.send_message(username, str(solve))
            await app.disconnect()

            return 1


        except Exception as e:
            await app.disconnect()
            logger.exception(e)
            return 0

    def get_math_captcha(text):
        pattern = r"\b\d+\s*[-+*/]\s*\d+\b"

        equations = re.findall(pattern,text)

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
