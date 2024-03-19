from pyrogram import Client, errors
import re

class GetCode:
    async def get_code(
        phone_number: str,
        session_string: str
    ):
        app = Client(phone_number, session_string=session_string)

        await app.connect()

        try:
            async for m in app.get_chat_history(777000, limit=1):
                code = GetCode.extract(m.text)
            await app.disconnect()
            return code
        
        except (errors.UserDeactivated, errors.UserDeactivatedBan, errors.SessionRevoked, errors.AuthKeyInvalid):
            return False

        except Exception as e:
            await app.disconnect()
            return 1

    def extract(text):
        pattern = r"\b\d{5}\b"
        matches = re.findall(pattern, text)
        return matches[0] if matches else None