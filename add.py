from Tools.info import db
from Tools.dialogs import create_account
import asyncio

async def loop():
    while True:
        print('''\033[1;32;40m
1- Add
2/q/exit- Quit
\033[0;40m''')
        choice = input("\033[1;33;40m>> \033[0;40m")

        if choice.strip() == "1":
            await create_account()
        elif choice.strip().lower() in ["2", "q", "exit"]:
            quit()

asyncio.run(loop())
