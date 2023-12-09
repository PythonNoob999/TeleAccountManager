from pyrogram import Client, errors
from ..info import logger, db

class Refresh:
    async def refresh():
        accounts = db.get_accounts()
        banned = 0
        revoked = 0

        for account in accounts:
            app = Client(account, session_string=accounts[account])

            try:
                await app.connect()
                await app.send_message("me", "Ping")
                await app.disconnect()
            except errors.SessionRevoked:
                revoked += 1
                db.delete_account(account)
            except errors.AuthKeyUnregistered:
                revoked +=1
                db.delete_account(account)
            except errors.UserDeactivatedBan:
                banned += 1
                db.delete_account(account)
            except errors.UserDeactivated:
                banned += 1
                db.delete_account(account)
        return {
            "total": len(accounts),
            "banned": banned,
            "revoked": revoked,
            "remain": len(accounts)-(banned+revoked)
        }
