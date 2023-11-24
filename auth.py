import subprocess
subprocess.run("pip install -r require.txt",shell=True)
from pyrogram import Client
from rich.console import Console
import os
import json

console = Console()

if os.path.isfile("auth.json"):
    console.print("YOU ALREADY HAVE YOUR CREDINTALS!!",style="bold red")
    exit()



console.print("Hi, welcome to the TeleAccountManager-V2 Tool, aka [i]TAM-V2[/i]", style="bold green")

api_id = console.input("What is your API_ID :id_button:\n")

api_hash = console.input("What is your API_HASH :japanese_bargain_button:\n")

with open("auth.json", "w") as f:
    data = {
        "api_id": int(api_id),
        "api_hash": api_hash
    }
    f.write(json.dumps(data, indent=4, ensure_ascii=False))
    f.close()

app = Client("MainAccount", int(api_id), api_hash)

app.start()

app.stop()
