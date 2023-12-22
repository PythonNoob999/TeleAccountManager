from pyrogram import Client, errors
from pyrogram.errors import (
BadRequest,
Unauthorized,
FloodWait,
SessionPasswordNeeded
)
from .info import db, api_id, api_hash, logger
from .parser import parse_kwargs, lnk, process_links, process_ref_link
import json
import asyncio

r,g,w = "\033[1;31;40m", "\033[1;32;40m>> ", "\033[0;40m"

async def binput(text):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, text)


async def create_account():
    password=""
    print(f"{r}Type phone number with +\nExample: +2018421981{w}")
    phone_number = await binput(g)
    if phone_number == "":
        exit()
    if not db.check_exist(phone_number):
        app = Client(phone_number,api_id, api_hash, device_model="AccountManagerV2", in_memory=True)
        try:
            await app.connect()
            sent_code = await app.send_code(phone_number)
            print(f"{r}Type the code that has been sent to you✉️{w}")
            code = await binput(g)
            do_it = True
            try:
    	        await app.sign_in(phone_number=phone_number, phone_code_hash=sent_code.phone_code_hash, phone_code=code)
            except BadRequest:
    	        print("\033[1;31;40mCode Invalid!!, type it again\033[0;40m")
    	        code = await binput(g)
    	        while True:
    	            try:
    	                print("\033[1;31;40mChecking Code💬\033[0;40m")
    	                await app.sign_in(phone_number=phone_number, phone_code_hash=sent_code.phone_code_hash, phone_code=code)
    	                print('\033[1;31;40mCorrect Code✅\033[0;40m')
    	                break
    	            except BadRequest:
    	                print("\033[1;31;40mCode Invalid!!, type it again")
    	                code = await binput(g)
    	            except SessionPasswordNeeded:
    	                break
    	            except Exception as e:
    	                log(e)
    	                do_it=False
    	                break

            except SessionPasswordNeeded:
    	        while True:
        	       try:
        	           print('\033[1;31;40mChecking Password🔑\033[0;40m')
        	           await app.check_password(password)
        	           break
        	       except BadRequest as e:
        	            if e.ID == "PASSWORD_HASH_INVALID":
        	                print(f"{r}Password Invalid🔑❌ Send Password:{w}")
        	                password = await binput(g)
        	            else:
        	                log(e.ID)
        	                do_it=False
        	                break
        	       except Exception as e:
        	            do_it=False
        	            break

            if do_it:
                 session_string = ""
                 if not db.check_exist(phone_number):
                     session_string = await app.export_session_string()
                 try:
                     await app.disconnect()
                 except:
                     pass
                 db.add_account(phone_number, session_string, password)
                 print(f"\033[1;32;40mSigned in to {phone_number} Successfully✅\033[0;40m")
            else:
                 print("\033[1;31;40mFailed to login❗\033[0;40m")
        except Exception as e:
            logger.exception(e)
            print(f"{r}Phone number Invalid{w}")
    else:
    	print(f"{r}Account Already In DB!{w}")


atb = (lambda x: True if x.upper()=="Y" else False)

def send_message_dialog(console):
    console.print("[bold yellow]Enter the [italic]username[/italic]")

    username = console.input("[bold green]>> ")

    console.print("[bold yellow]Type the number of accounts\n[bold red]max by default")

    count = console.input("[bold green]>> ")

    while not count.isdigit() and count != "":
        console.print("[bold red]Wrong number, please type correct number or empty string for default settings")
        count = console.input("[bold green]>> ")
    count = "max" if count == "" else int(count)

    console.print("[bold yellow]Please, type the message that you want to send to the user/bot")

    message = console.input("[bold green]>> ")

    console.print("[bold yellow]Type the wait time for each account, in seconds\n[bold red]0 by default")

    hold = console.input("[bold green]>> ")

    while not hold.isdigit() and hold != "":
        console.print("[bold red]Wrong number, please type correct number or empty string for default settings")
        hold = console.input("[bold green]>> ")

    hold = 0 if hold=="" else int(hold)

    console.print("[bold yellow]do you want to run at maximum speed? AKA max_perf=True?\n[Y/N]")

    max_perf = atb(console.input("[bold green]>> "))

    task = {
        "command": "send_message",
        "count": count,
        "max_perf": max_perf,
        "username": lnk(username),
        "hold": hold,
        "message": message
    }

    return task

def chats_dialog(command, console):
    console.print("[bold yellow]Please type each chat link separated with |\n[bold yellow]Example:\n[bold green]@chat1|https://t.me/chat2|https://t.me/+chat3")

    chats = process_links(console.input("[bold green]>> "))

    console.print("[bold yellow]Type the number of accounts\n[bold red]max by default")

    count = console.input("[bold green]>> ")

    while not count.isdigit() and count != "":
        console.print("[bold red]Wrong number, please type correct number or empty string for default settings")
        count = console.input("[bold green]>> ")
    count = "max" if count == "" else int(count)

    console.print("[bold yellow]Type the wait time between each account, in seconds\n[bold red]0 by default")

    hold = console.input("[bold green]>> ")

    while not hold.isdigit() and hold != "":
        console.print("[bold red]Wrong number, please type correct number or empty string for default settings")
        hold = console.input("[bold green]>> ")

    hold = 0 if hold == "" else int(hold)

    console.print("[bold yellow]do you want to run at maximum speed? AKA max_perf=True?\n[Y/N]")

    max_perf = atb(console.input("[bold green]>> "))

    task = {
        "command": command,
        "count": count,
        "max_perf": max_perf,
        "hold": hold,
        "chats": chats
    }

    return task

def click_dialog(command, console):
    console.print("[bold yellow]Type bot username to click the message in")

    username = lnk(console.input("[bold green]>> "))

    console.print("[bold yellow]Type the button index, starting from 0 which is the first button")

    index = console.input("[bold green]>> ")

    while not index.isdigit():
        console.print("[bold red]Wrong number, please type correct number or empty string for default settings")
        index = console.input("[bold green]>> ")

    index = int(index)

    console.print("[bold yellow]Do you want to enable force_find option?\n[bold green]force_find let the account check every last message from the bot,until it finds a keyboard, and click it")

    force_find = console.input("[bold green][Y/N] ")
    force_find = True if force_find.lower()=="Y" else False

    console.print("[bold yellow]Type a button name to find, instead of using index, type a button name to search for or empty string for default settings")

    searchfor = console.input("[bold green]>> ")

    searchfor = False if searchfor=="" else searchfor

    console.print("[bold yellow]Type the number of accounts\n[bold red]max by default")

    count = console.input("[bold green]>> ")

    while not count.isdigit() and count != "":
        console.print("[bold red]Wrong number, please type correct number or empty string for default settings")
        count = console.input("[bold green]>> ")
    count = "max" if count == "" else int(count)

    console.print("[bold yellow]Type the wait time between each account, in seconds\n[bold red]0 by default")

    hold = console.input("[bold green]>> ")

    while not hold.isdigit() and hold != "":
        console.print("[bold red]Wrong number, please type correct number or empty string for default settings")
        hold = console.input("[bold green]>> ")

    hold = 0 if hold == "" else int(hold)

    console.print("[bold yellow]do you want to run at maximum speed? AKA max_perf=True?\n[Y/N]")

    max_perf = atb(console.input("[bold green]>> "))

    task = {
        "command": command,
        "count": count,
        "max_perf": max_perf,
        "hold": hold,
        "username": username,
        "index": index,
        "force_find": force_find,
        "searchfor": searchfor
    }

    return task

def ref_dialog(command, console):
    console.print("[bold yellow]Type your refferal link")

    link = console.input("[bold green]>> ")
    while True:
        try:
            process_ref_link(link)
            break
        except:
            console.print("[bold red]Invalid Refferal Link :warning:\n[bold yellow]try again")

            link = console.input("[bold green]>> ")

    console.print("[bold yellow]Type the number of accounts\n[bold red]max by default")

    count = console.input("[bold green]>> ")

    while not count.isdigit() and count != "":
        console.print("[bold red]Wrong number, please type correct number or empty string for default settings")
        count = console.input("[bold green]>> ")
    count = "max" if count == "" else int(count)

    console.print("[bold yellow]Type the wait time between each account, in seconds\n[bold red]0 by default")

    hold = console.input("[bold green]>> ")

    while not hold.isdigit() and hold != "":
        console.print("[bold red]Wrong number, please type correct number or empty string for default settings")
        hold = console.input("[bold green]>> ")

    hold = 0 if hold == "" else int(hold)

    console.print("[bold yellow]do you want to run at maximum speed? AKA max_perf=True?\n[Y/N]")

    max_perf = atb(console.input("[bold green]>> "))

    task = {
        "command": command,
        "count": count,
        "max_perf": max_perf,
        "hold": hold,
        "link": link
    }

    return task
