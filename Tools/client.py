from .info import db
from pyrogram import Client
from .methods import Methods
import asyncio

methods = {
    "send_message": Methods.send_message,
    "join_chats": Methods.join_chats,
    "leave_chats": Methods.leave_chats,
    "ref": Methods.ref,
    "click": Methods.click,
    "send_contact": Methods.send_contact,
    "add_contact": Methods.add_contact,
    "send_reaction": Methods.send_reaction
}

async def Execute(method,kwargs):
    start = 0; stop=-1
    if "count" in kwargs.keys():
        count = kwargs["count"]
        kwargs.pop("count")

        if "-" in count:
            start = int(count.split("-")[0])-1
            stop = int(count.split("-")[1])
        else:
            if count == "max":
                stop = -1
            else:
                stop = int(count)

    accs = db.get_accounts()
    s = 0
    t = 0

    func = methods[method]
    keys = [k for k in accs.keys()]
    if start == 0 and stop == -1:
        keys = keys[start:]
    else:
        keys = keys[start:stop]

    stack = False
    stack = kwargs["max_perf"]
    kwargs.pop("max_perf")

    tasks = []

    for acc in keys:
        t += 1
        if stack:
            tasks.append(func(acc,accs[acc],**kwargs))
        else:
            s += await func(acc, accs[acc], **kwargs)

    if tasks != []:
        s = sum(await asyncio.gather(*tasks))

    return {
        "total": t,
        "done": s
    }

