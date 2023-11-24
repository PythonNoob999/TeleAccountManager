from pyrogram import Client, filters
from Tools.client import Execute
from Tools.parser import parse_kwargs
from Tools.info import logger
from time import perf_counter as pc

client = Client(
    "MainAccount"
)

@client.on_message(filters.text, filters.me)
async def main_handler(bot, m):
    user = m.from_user
    txt = m.text.split()
    command = txt[0].replace("/", "")

    if command in ["send_message", "join_chats","leave_chats", "ref","click","send_contact", "add_contact", "send_reaction"]:
        kwargs = parse_kwargs(m.text, txt[0])
        await m.reply("Executing⏰")
        try:
            count = pc()
            result = await Execute(command, kwargs)
            return await m.reply(f"Done {result['done']}/{result['total']}\nDone in {pc() - count} Seconds")
        except Exception as e:
            logger.exception(e)
            return await m.reply("Invalid Arguments")

client.run()
