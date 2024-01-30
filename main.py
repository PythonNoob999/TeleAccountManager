from pyrogram import Client, filters
from Tools.client import Execute, Run
from Tools.parser import parse_kwargs
from Tools.info import logger, db
from Tools.methods.refresh import Refresh
from time import perf_counter as pc

client = Client(
    "MainAccount"
)

def is_me(filter,cli,update):
    try:
        return update.from_user.id == cli.me.id
    except:
        return False

IsMe = filters.create(is_me, "IsMe")

@client.on_message(filters.text & IsMe)
async def main_handler(bot, m):
    user = m.from_user
    txt = m.text.split()
    command = txt[0].replace("/", "")

    if command in ["send_message", "join_chats","leave_chats", "ref","click","send_contact", "add_contact", "send_reaction","send_vote", "unsend_vote", "export_chats","captcha", "watch"]:
        kwargs = parse_kwargs(m.text, txt[0])
        await m.reply("Executing⏰")
        try:
            count = pc()
            result = await Execute(command, kwargs)
            return await m.reply(f"Done {result['done']}/{result['total']}\nDone in {pc() - count} Seconds\n\n[devoloper]('https://t.me/kerolis55463')")
        except Exception as e:
            logger.error(e)
            return await m.reply("Invalid Arguments")

    elif command == "run":
        if m.reply_to_message is not None:
            if m.reply_to_message.document is not None:
                script = m.reply_to_message.document
                await m.reply_to_message.download(script.file_name)

                await m.reply(f"Executing {script.file_name.replace('.json','')}⏰")
                count = pc()
                result = await Run(bot,m,f"downloads/{script.file_name}")
                return await m.reply(f"Finished {script.file_name.replace('.json', '')} in {pc() - count} Seconds✅")


        return await m.reply('Please reply to a message that has a script')

    elif command == "delete":
        try:
            account = txt[1]
            if db.check_exist(account):
                ss = db.get_account_info(account)["session_string"]
                db.delete_account(account)
                app = Client(account, session_string=ss)
                try:
                    await app.connect()
                    await app.log_out()
                except:
                    pass
                return await m.reply(f"Deleted {account}✅")
            return await m.reply("This phone number is not in the DB")
        except:
            return await m.reply("Please but a phone number to delete")

    elif command == "refresh":
        await m.reply("Refreshing📟")
        inf = await Refresh.refresh()
        text = f'''
Scan complete!
Results:
  total accounts: {inf["total"]}
  banned: {inf["banned"]}
  revoked: {inf["revoked"]}
  remaining accounts: {inf["remain"]}
        '''
        return await m.reply(text)

client.run()
