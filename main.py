from pyrogram import Client, filters
from Tools.client import Execute, Run
from Tools.parser import parse_kwargs
from Tools.info import logger
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

    if command in ["send_message", "join_chats","leave_chats", "ref","click","send_contact", "add_contact", "send_reaction","send_vote", "unsend_vote"]:
        kwargs = parse_kwargs(m.text, txt[0])
        await m.reply("Executing⏰")
        try:
            count = pc()
            result = await Execute(command, kwargs)
            return await m.reply(f"Done {result['done']}/{result['total']}\nDone in {pc() - count} Seconds")
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

client.run()
