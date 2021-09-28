import requests, re, queue, threading
from colorama import init, Fore

init()
lock = threading.Lock()

usernames = [word.rstrip().lower() for word in open('usernames.txt', 'r+').readlines()]
users = queue.Queue()

headers = {
        'Cookie': 'krul',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-AR,es;q=0.8,en-US;q=0.5,en;q=0.3'
        }

def scrape(text):
    if (scraped := re.findall('"nickname":"(.*?)"', text)) != []:
        return scraped[0]
    return False

def check():
    while not users.empty():
        name = users.get()
        r = requests.get(f"https://www.tiktok.com/@{name}?", headers=headers)
        scraped = scrape(r.text)
        
        if scraped != False:
            with lock:
                print(f"{Fore.MAGENTA}[{Fore.RESET}>{Fore.MAGENTA}]{Fore.RESET} {name}:{scraped}")
                with open("results.txt", "a", encoding="utf-8") as z:
                    z.write(f"{name}:{scraped}\n")
        else:
            if r.status_code == 404:
                with lock:
                    print(f"{Fore.RED}[{Fore.RESET}!{Fore.RED}]{Fore.RESET} {name} is available or banned")
            else:
                users.put(name)
                with lock:
                    print(f"{Fore.RED}[{Fore.RESET}!{Fore.RED}]{Fore.RESET} Error on {name}, retrying")

if __name__ == "__main__":
    print(f"{Fore.CYAN}[{Fore.RESET}?{Fore.CYAN}]{Fore.RESET} Tiktok Nickname Scraper")

    print(f"{Fore.CYAN}[{Fore.RESET}?{Fore.CYAN}]{Fore.RESET} Threads: ", end="")
    threads = int(input())

    loaded = 0
    for i in usernames:
        users.put(i)
        loaded += 1
    
    print(f"{Fore.CYAN}[{Fore.RESET}?{Fore.CYAN}]{Fore.RESET} Loaded {loaded} users, press enter to start")
    input()

    for i in range(threads):
        threading.Thread(target=check).start()
