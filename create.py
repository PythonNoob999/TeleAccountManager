from rich.console import Console
from rich.table import Table
from Tools.dialogs import (
send_message_dialog,
chats_dialog,
click_dialog,
ref_dialog
)
import json

cl = Console()

choices = Table(title="Options")

choices.add_column("Code", justify="right")
choices.add_column("Function", justify="left")

choices.add_row("1","send_message")
choices.add_row("2","join_chats")
choices.add_row("3","leave_chats")
choices.add_row("4","click")
choices.add_row("5","ref")
choices.add_row("6", "export script")

tasks = []

while True:
    cl.print(choices)
    code = cl.input("[bold green]>> ")

    if code == "1":
        tasks.append(send_message_dialog(cl))

    elif code == "2":
        tasks.append(chats_dialog("join_chats",cl))

    elif code == "3":
        tasks.append(chats_dialog("leave_chats", cl))

    elif code == "4":
        tasks.append(click_dialog("click", cl))

    elif code == "5":
        tasks.append(ref_dialog("ref",cl))

    elif code == "6":

        cl.print("[bold yellow]Type script name:")
        name = cl.input("[bold green]>> ")

        if tasks != []:
            with open(f"scripts/{name}.json", "w+") as f:
                f.write(json.dumps(tasks, indent=4, ensure_ascii=False))
                f.close()

        cl.print(f"[bold green]Saved {name} to scripts folder")
        exit()

