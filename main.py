import yaml
import os
from colorama import Fore, Style, init
from colorama import Fore, Back, Style
from pystyle import Colors, Colorate
import importlib.util
import threading
import os
import pwinput
from libs.fivem import resolve_cfx_url
import subprocess
import requests
import time
import sys

COLOR_MAPPING = {
    "{black}": Fore.BLACK,
    "{red}": Fore.RED,
    "{green}": Fore.GREEN,
    "{yellow}": Fore.YELLOW,
    "{blue}": Fore.BLUE,
    "{magenta}": Fore.MAGENTA,
    "{cyan}": Fore.CYAN,
    "{lightmagenta}": Fore.LIGHTMAGENTA_EX,
    "{lightgreen}": Fore.LIGHTGREEN_EX,
    "{lightred}": Fore.LIGHTRED_EX,
    "{white}": Fore.WHITE,
    "{reset}": Style.RESET_ALL,
}

init(autoreset=True)

version_url = "https://raw.githubusercontent.com/MatoiDevs/MatoiConsole/refs/heads/main/version"
local_version = "2.1"


def replace_color_placeholders(text):
    """Replace color placeholders in the text with actual color codes."""
    for placeholder, color_code in COLOR_MAPPING.items():
        text = text.replace(placeholder, color_code)
    return text

def load_ascii(file_path):
    """Load ASCII art from a file and replace color placeholders."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return replace_color_placeholders(content)


def replace_placeholders(template, values):
    """Replace placeholders in the template with actual colors and dynamic values."""
    for placeholder, color_code in COLOR_MAPPING.items():
        template = template.replace(placeholder, color_code)

    for key, value in values.items():
        template = template.replace(f"{{{key}}}", str(value))

    return template

def load_message(file_path, values):
    """Load a message template from a file and replace placeholders."""
    with open(file_path, 'r') as file:
        content = file.read()
    return replace_placeholders(content, values)

def load_messages(file_path):
    """Load messages from a YAML file and replace color placeholders."""
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    messages = data.get('messages', {})
    for key in messages:
        messages[key] = replace_color_placeholders(messages[key])
    return messages




def login(node, user=None, password=None):
    themedir = config.get("themedir", "theme")
    theme_dir = f"{themedir}"
    messages_file = os.path.join(theme_dir, 'messages.yml')
    messages = load_messages(messages_file)

    tor = "off"

    if os.path.exists('login.txt'):
        with open('login.txt', 'r') as file:
            credentials = file.read().strip().split(':')
            if len(credentials) == 2:
                user, password = credentials[0], credentials[1]
                os.system("cls")
                print(messages['saved-creds'])
            else:
                os.system("cls")
                print(messages['invalid-creds'])
                return

    if user is None or password is None:
        theme_dir = 'theme'
        ascii_file = os.path.join(theme_dir, 'ascii-login.txt')
        ascii_art = load_ascii(ascii_file)

        os.system("cls || clear")
        print(ascii_art)
        print(messages['login'])
        print("")
        user = input("Enter username: ")
        password = pwinput.pwinput(prompt = 'Enter the password: ', mask='*')

    api_url = f"https://api.failed.lol/matoi/auth?user={user}&password={password}"
    
    try:
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("code") == 200:
                print(messages['login-sucess'])
                with open('login.txt', 'w') as file:
                    file.write(f"{user}:{password}")
                clear(user, password, tor)
            else:
                print(messages['login-invalid'])
                if os.path.exists('login.txt'):
                    os.remove('login.txt')
        else:
            print(f"Error: Received status code {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def start_tor():
    tor_path = "tor.exe"
    tor_process = subprocess.Popen([tor_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)
    return tor_process

def tor_request(url):
    proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }
    try:
        response = requests.get(url, proxies=proxies, timeout=30)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def load_addon(addon_name):
    try:
        spec = importlib.util.spec_from_file_location(addon_name, f"addons/{addon_name}.py")
        addon_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(addon_module)

        if hasattr(addon_module, 'run'):
            threading.Thread(target=addon_module.run).start()
        else:
            print(f"{Fore.RED}Addon '{addon_name}' does not have a 'run' function.{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}Failed to load addon '{addon_name}': {e}{Fore.RESET}")

with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

def clear(user, password, tor):
    os.system("cls")
    startup(user, password, tor)

def startup(user, password, tor):
    program_title = config.get("title", "Matoi network attack system!")
    themedir = config.get("themedir", "theme")
    theme_dir = f"{themedir}"
    ascii_file = os.path.join(theme_dir, 'ascii-home.txt')
    homebanner = load_ascii(ascii_file)
    messages_file = os.path.join(theme_dir, 'messages.yml')
    messages = load_messages(messages_file)

    print(Style.RESET_ALL)
    os.system(f"title {program_title}")
    print(homebanner)
    print("")
    print(messages['welcome'])
    print("")
    main(user, password, tor)

def main(user, password, tor):
    command = input(f"{Back.MAGENTA}{user} </> Matoi {Back.RESET}{Fore.RESET} ")
    if command == "help":
        print("")
        print(f"{Fore.LIGHTMAGENTA_EX}attack{Fore.RESET}     - Stress test command          - {Fore.WHITE}D{Fore.RESET}")
        print(f"{Fore.LIGHTMAGENTA_EX}methods{Fore.RESET}    - Shows methods for network    - {Fore.WHITE}D{Fore.RESET}")
        print(f"{Fore.LIGHTMAGENTA_EX}tor{Fore.RESET}        - tor connection (on/off)      - {Fore.WHITE}D{Fore.RESET}")
        print(f"{Fore.LIGHTMAGENTA_EX}testtor{Fore.RESET}    - test tor connection          - {Fore.WHITE}D{Fore.RESET}")
        print(f"{Fore.LIGHTMAGENTA_EX}fivem{Fore.RESET}      - cfx resolve                  - {Fore.WHITE}D{Fore.RESET}")
        print(f"{Fore.LIGHTMAGENTA_EX}plans{Fore.RESET}      - List of Plans                - {Fore.WHITE}D{Fore.RESET}")
        print(f"{Fore.LIGHTMAGENTA_EX}addon{Fore.RESET}      - addons function              - {Fore.WHITE}D{Fore.RESET}")
        print(f"{Fore.LIGHTMAGENTA_EX}clear{Fore.RESET}      - clears console               - {Fore.WHITE}D{Fore.RESET}")
        print("")
        main(user, password, tor)

    if command.startswith("attack"):
        themedir = config.get("themedir", "theme")
        theme_dir = f"{themedir}"
        messages_file = os.path.join(theme_dir, 'messages.yml')
        messages = load_messages(messages_file)

        parts = command.split()

        if len(parts) != 6:
            print(messages['attack-invalid'])
            main(user, password, tor)
        else:
            attack, ip, port, time, network, method = parts
            theme_dir = 'theme'
            message_file = os.path.join(theme_dir, 'attack-messages.txt')
            ascii_file = os.path.join(theme_dir, 'ascii-attack.txt')
            attackbanner = load_ascii(ascii_file)

            os.system("cls")
            print("")
            print(attackbanner)
            print("")
            print(f"                     {Fore.LIGHTGREEN_EX}𝓪𝓽𝓽𝓪𝓬𝓴 𝓼𝓮𝓷𝓽!{Fore.RESET}")
            print(f"                     IP: {Fore.LIGHTRED_EX}{ip}{Fore.RESET}")
            print(f"                     PORT: {Fore.LIGHTRED_EX}{port}{Fore.RESET}")
            print(f"                     TIME: {Fore.LIGHTRED_EX}{time}s{Fore.RESET}")
            print(f"                     METHOD: {Fore.LIGHTRED_EX}{method}{Fore.RESET}")
            print("")

            if tor == "off":
                themedir = config.get("themedir", "theme")
                theme_dir = f"{themedir}"
                messages_file = os.path.join(theme_dir, 'messages.yml')
                messages = load_messages(messages_file)

                response = requests.get(f'https://api.failed.lol/matoi/start?user={user}&password={password}&network={network}&host={ip}&port={port}&method={method}&time={time}')

                if response.status_code == 200:
                    print(messages['attack-sent'])
                    main(user, password, tor)
                if response.status_code == 400:
                    print(messages['attack-sent'])
                    main(user, password, tor)
                if response.status_code == 508:
                    print(messages['attack-cooldown'])
                    main(user, password, tor)
                else:
                    print(messages['attack-fail'])
                    main(user, password, tor)
            if tor == "on":
                themedir = config.get("themedir", "theme")
                theme_dir = f"{themedir}"
                messages_file = os.path.join(theme_dir, 'messages.yml')
                messages = load_messages(messages_file)

                response = tor_request(f'https://api.failed.lol/matoi/start?user={user}&password={password}&network={network}&host={ip}&port={port}&method={method}&time={time}')

                if response.status_code == 200:
                    print(messages['attack-sent'])
                    main(user, password, tor)
                if response.status_code == 400:
                    print(messages['attack-sent'])
                    main(user, password, tor)
                if response.status_code == 508:
                    print(messages['attack-cooldown'])
                    main(user, password, tor)
                else:
                    print(messages['attack-fail'])
                    main(user, password, tor)


    elif command.startswith("addon "):
        addon_name = command.split()[1]
        load_addon(addon_name)
        main(user, password, tor)

    if command == "clear":
        clear(user, password, tor)

    if command.startswith("fivem"):
        parts = command.split()

        if len(parts) != 2:
            print(messages['fivem-invalid'])
            main(user, password, tor)
        else:
            fivem, cfx = parts
            url = f"{cfx}"
            target_info = resolve_cfx_url(url)
            print(target_info)
            main(user, password, tor)

    if command.startswith("tor"):
        themedir = config.get("themedir", "theme")
        theme_dir = f"{themedir}"
        messages_file = os.path.join(theme_dir, 'messages.yml')
        messages = load_messages(messages_file)

        parts = command.split()

        if len(parts) != 2:
            print(messages['tor-invalid'])
            main(user, password, tor)
        else:
            tor, status = parts
            if status == "on":
                tor = "on"
                print(messages['tor-connect'])
                main(user, password, tor)
            if status == "off":
                tor = "off"
                print(messages['tor-disconnect'])
                main(user, password, tor)

    if command.startswith("UserCreate"):
        themedir = config.get("themedir", "theme")
        theme_dir = f"{themedir}"
        messages_file = os.path.join(theme_dir, 'messages.yml')
        messages = load_messages(messages_file)

        parts = command.split()

        if len(parts) != 7:
            print(messages['UserCreate-invalid'])
            main(user, password, tor)
        else:
            UserCreate, username, password2, concurrents, maxTime, admin, allowedServers = parts

            url = f"https://api.failed.lol/matoi/admin/add?AdminUser={user}&AdminPassword={password}&username={username}&password={password2}&concurrents={concurrents}&maxTime={maxTime}&admin={admin}&allowedServers={allowedServers}"
            response = requests.get(url)

            if response.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}User {username} has been created{Fore.RESET}")
                main(user, password, tor)
            else:
                print(f"{Fore.LIGHTRED_EX}Error ocured or you dont have permissions for this!")
                print(url)
                main(user, password, tor)

    if command.startswith("UserDelete"):
        themedir = config.get("themedir", "theme")
        theme_dir = f"{themedir}"
        messages_file = os.path.join(theme_dir, 'messages.yml')
        messages = load_messages(messages_file)

        parts = command.split()

        if len(parts) != 2:
            print(messages['UserDelete-invalid'])
            main(user, password, tor)
        else:
            UserDelete, username = parts

            url = f"https://api.failed.lol/matoi/admin/delete?AdminUser={user}&AdminPassword={password}&username={username}"
            response = requests.get(url)

            if response.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}User {username} has been deleted{Fore.RESET}")
                main(user, password, tor)
            else:
                print(f"{Fore.LIGHTRED_EX}Error ocured or you dont have permissions for this!")
                print(url)
                main(user, password, tor)

    if command.startswith("UserEdit"):
        themedir = config.get("themedir", "theme")
        theme_dir = f"{themedir}"
        messages_file = os.path.join(theme_dir, 'messages.yml')
        messages = load_messages(messages_file)

        parts = command.split()

        if len(parts) != 6:
            print(messages['UserEdit-invalid'])
            main(user, password, tor)
        else:
            UserEdit, username, concurrents, maxTime, admin, allowedServers = parts

            url = f"https://api.failed.lol/matoi/admin/delete?AdminUser={user}&AdminPassword={password}&username={username}&concurrents={concurrents}&maxTime={maxTime}&allowedServers={allowedServers}"
            response = requests.get(url)

            if response.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}User {username} has been Edited{Fore.RESET}")
                main(user, password, tor)
            else:
                print(f"{Fore.LIGHTRED_EX}Error ocured or you dont have permissions for this!")
                print(url)
                main(user, password, tor)

    if command.startswith("methods"):
        url = f"https://api.failed.lol/matoi/methods?user={user}&password={password}"
        response = requests.get(url)

        if response.status_code == 200:
            network_methods = {network: [method.strip() for method in methods.split(',')]
                               for network, methods in response.json().items()}
        else:
            print(f"{Fore.RED}Failed to fetch data. Status code: {response.status_code}{Fore.RESET}")
            network_methods = {}

        parts = command.split()

        if len(parts) != 2:
            # Handle invalid command format correctly
            print(f"{Fore.RED}Invalid command format. Correct usage: 'methods <network>'{Fore.RESET}")
            main(user, password, tor)
            return

        _, network = parts

        # Check if the network exists in the network_methods
        if network.upper() in network_methods:
            methods = network_methods[network.upper()]
            print(f"{Fore.LIGHTGREEN_EX}Methods for network '{network.upper()}':{Fore.RESET}")
            for method in methods:
                print(f"- {method}")
        else:
            print(
                f"{Fore.RED}Unknown network '{network}'. Available networks: {', '.join(network_methods.keys())}{Fore.RESET}")
        main(user, password, tor)

    if command.startswith("ongoing"):
        # Send a GET request to check the attack status
        url = f"https://api.failed.lol/matoi/admin/status?AdminUser={user}&AdminPassword={password}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()  # Parse the JSON response

            # Check the status in the response
            status = data.get("status", "")

            if status == "":
                print(f"{Fore.GREEN}No attacks are currently running.{Fore.RESET}")
            else:
                # If there are active attacks, print them
                print(f"{Fore.YELLOW}Active attacks:{Fore.RESET}")
                attacks = status.split("\n")
                for attack in attacks:
                    print(f"{Fore.RED}{attack}{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}Error ocured or you dont have permissions for this!")

        main(user, password, tor)


    if command.startswith("test"):
        themedir = config.get("themedir", "theme")
        theme_dir = f"{themedir}"
        messages_file = os.path.join(theme_dir, 'messages.yml')
        messages = load_messages(messages_file)

        parts = command.split()

        if len(parts) != 2:
            print(messages['test-invalid'])
            main(user, password, tor)
        else:
            test, connection = parts
            if connection == "tor":
                url = "http://check.torproject.org"
                response = tor_request(url)
                if response:
                    if tor == "on": 
                        print(messages['tor-working'])
                        main(user, password, tor)
                    else:
                        print(messages['tor-notworking'])
                        main(user, password, tor)
                else:
                    print(messages['tor-notworking'])
                    main(user, password, tor)
            else:
                print(messages['connections'])
                main(user, password, tor)

    else:
        themedir = config.get("themedir", "theme")
        theme_dir = f"{themedir}"
        messages_file = os.path.join(theme_dir, 'messages.yml')
        messages = load_messages(messages_file)
        print(messages['unkcmd'])
        main(user, password, tor)
def startconsole():
    if sys.platform == "win32" or "cygwin" or "msys":
        os.system('chcp 65001')
        sys.stdout.reconfigure(encoding='utf-8')
        print(f"[MATOI-LOG] {Fore.GREEN}Pre-Starting tor client! This may take a while.")
        tor_process = start_tor()
        login("node1")
    else:
        sys.stdout.reconfigure(encoding='utf-8')
        login("node1")

def check_for_update():
    try:
        response = requests.get(version_url)
        response.raise_for_status()  
        remote_version = response.text.strip()

        if remote_version != local_version:
            print(f"Console is outdated. New version available: {remote_version}")
        else:
            print("Console is up to date.")
            startconsole()
    except requests.RequestException as e:
        print(f"Error checking for updates: {e}")

check_for_update()
