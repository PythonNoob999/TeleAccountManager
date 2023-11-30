stb = (lambda x: True if x == "True" else False)

KWARGS_TYPES = {
    "count": str,
    "link": str,
    "message": str,
    "username": str,
    "chats": str,
    "ref_link": str,
    "searchfor": str,
    "contact_number": str,
    "first_name": str,
    "last_name": str,
    "emoji": str,
    "chocies": str,
    "type": str,
    "hold": int,
    "index": int,
    "force_find": stb,
    "max_perf": stb,
    "button": stb
}


lnk = (lambda x: x.replace("https://t.me/","").replace("http://t.me/","").replace("https://telegram.me/","").replace("http://telegram.me/","").replace("@",""))

def process_ref_link(link):
    link = lnk(link).split("?")
    bot_user = link[0]
    command = link[1].split("=",1)[0]
    ref_code = link[1].split("=",1)[1]

    return {"user": bot_user, "msg": f"/{command} {ref_code}"}

def process_links(links):
    links = links.split("|")
    result = []

    for link in links:
        if link.isdigit():
            result.append(int(link))
        elif "+" in link:
            result.append(link)
        else:
            result.append(lnk(link))
    return result

def process_post_link(link):
    link = lnk(link).split("/")
    return {"chat": link[0], "id": int(link[1])}

# Parsing the arguments
def parse_kwargs(text: str,command: str) -> dict:
    # text.split()[0] == command, /ref, /etc
    kwargs = text.replace(command, "").strip().split("\n")
    # default Params
    kwgs = {
        "count": "max",
        "max_perf": False,
        "hold": 0
    }

    for kwg in kwargs:
        # key = message
        if "=" not in kwg:
            kwgs["message"] += f"\n{kwg}"
        elif "chats=" in kwg:
            kwgs["chats"] = process_links(kwg.split("=")[1].strip())
        elif "choices=" in kwg:
            choices = int(kwg.replace("choices=", "").strip())-1 if "-" not in kwg else [int(x)-1 for x in kwg.replace("choices=","").split("-")]
            kwgs["choices"] = choices
        else:
            kwgs[kwg.split("=",1)[0].strip()] = KWARGS_TYPES[kwg.split("=",1)[0].strip()](kwg.split("=",1)[1].strip())
    return kwgs

