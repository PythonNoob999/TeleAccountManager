from pyrogram import Client, errors
from pyrogram.errors import (
BadRequest,
Unauthorized,
FloodWait,
SessionPasswordNeeded
)
from .info import db, api_id, api_hash, logger
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

