def isfloat(string):
    try:
        float(string)
        return True
    except:
        return False

stb = (lambda x: True if x.lower() == "true" else False)
soi = (lambda x: x if not isfloat(x) else int(x))

KWARGS_TYPES = {
    "count": str,
    "link": str,
    "message": str,
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
    "username": soi,
    "force_find": stb,
    "max_perf": stb,
    "button": stb,
    "mute": stb,
    "archive": stb
}


def lnk(x):
    if x.isdigit(): return int(x)
    try:
        return x.replace("https://t.me/","").replace("http://t.me/","").replace("https://telegram.me/","").replace("http://telegram.me/","").replace("@","")
    except:
        return x

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
        elif link.isdigit():
            result.append(int(link))
        else:
            result.append(lnk(link))
    return result

def process_post_link(link):
    if "/c/" in link:
        indexes = [1,2]
    else:
        indexes = [0,1]
    link = lnk(link).split("/")
    return {"chat": soi(link[indexes[0]]), "id": int(link[indexes[1]])}

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
            kwarg = kwg.split("=",1)[0].strip()
            value = kwg.split("=",1)[1].strip()
            kwgs[kwarg]= KWARGS_TYPES[kwarg](value)
    return kwgs

