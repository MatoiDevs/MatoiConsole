import os
import sys
import requests
from datetime import datetime
from colored import stylize

class Main:
    @staticmethod
    def format_console_date(date):
        return f"[{date.strftime('%Y-%m-%d-%H:%M:%S')}]"

    @staticmethod
    def get_args():
        return sys.argv

class Resolver:
    @staticmethod
    def solve_link(target_id):
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        }
        response = requests.get(f"https://servers-frontend.fivem.net/api/servers/single/{target_id}", headers=headers)
        data = response.json()
        return {
            "ip": data["Data"]["connectEndPoints"][0],
            "hostname": data["Data"]["hostname"]
        }

def resolve_cfx_url(url):
    target_id = os.path.basename(url)
    target_data = Resolver.solve_link(target_id)
    return target_data

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(stylize("[ERROR] bad command usage", 'red'))
        print(stylize("Usage Scheme:", '#ffe900') + " - user@some_name:~# python3 main.py <cfx.re-link>")
        sys.exit()

    target_link = sys.argv[1]
    target_data = resolve_cfx_url(target_link)
    
    print(stylize(Main.format_console_date(datetime.today()), 'yellow') + stylize(" Target info :", 'green'))
    print(stylize(f"+-----------------------------------------------------+\n"
                   f"|                  Target Info                        |\n"
                   f"+-----------------------------------------------------+\n"
                   f"|  Server IP: {target_data['ip']}\n"
                   f"+-----------------------------------------------------+", 'yellow'))
