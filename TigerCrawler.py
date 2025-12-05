
print("\033[92m")
print(r"""

$$$$$$$$\ $$\                  $$$$$$\                                   $$\                     
\__$$  __|$$ |                $$  __$$\                                  $$ |                    
   $$ |   $$$$$$$\   $$$$$$\  $$ /  \__| $$$$$$\  $$$$$$\  $$\  $$\  $$\ $$ | $$$$$$\   $$$$$$\  
   $$ |   $$  __$$\ $$  __$$\ $$ |      $$  __$$\ \____$$\ $$ | $$ | $$ |$$ |$$  __$$\ $$  __$$\ 
   $$ |   $$ |  $$ |$$$$$$$$ |$$ |      $$ |  \__|$$$$$$$ |$$ | $$ | $$ |$$ |$$$$$$$$ |$$ |  \__|
   $$ |   $$ |  $$ |$$   ____|$$ |  $$\ $$ |     $$  __$$ |$$ | $$ | $$ |$$ |$$   ____|$$ |      
   $$ |   $$ |  $$ |\$$$$$$$\ \$$$$$$  |$$ |     \$$$$$$$ |\$$$$$\$$$$  |$$ |\$$$$$$$\ $$ |      
   \__|   \__|  \__| \_______| \______/ \__|      \_______| \_____\____/ \__| \_______|\__|      
                                                                                                 
                                                                                                                                                                 
 """)

print("\033[0m")
import threading
import queue
import re
import urllib.parse
import requests
from bs4 import BeautifulSoup

MAX_URLS    = 100
MAX_THREADS = 20
TIMEOUT     = 5


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", re.I)
BAD_EXTS = (".png", ".jpg", ".jpeg", ".webp")


to_visit = queue.Queue()
visited  = set()
queued   = set()
emails   = set()
count    = 0
lock     = threading.Lock()
session  = requests.Session()
session.headers.update({"User-Agent": "TigerMailCrawler/1.0"})

def enqueue(url):
    
    with lock:
        if url not in visited and url not in queued and len(visited) + to_visit.qsize() < MAX_URLS:
            queued.add(url)
            to_visit.put(url)

def worker():
    global count
    while True:
        url = to_visit.get()
        if url is None:
            to_visit.task_done()
            return

        with lock:
            queued.remove(url)
            visited.add(url)
            count += 1
            idx = count

        print(f"[{idx}] Processing: {url}")

        try:
            resp = session.get(url, timeout=TIMEOUT)
            html = resp.text

            found = set(EMAIL_RE.findall(html))
            found = {e for e in found if not e.lower().endswith(BAD_EXTS)}
            with lock:
                emails.update(found)

          
            parts = urllib.parse.urlsplit(url)
            base  = f"{parts.scheme}://{parts.netloc}"
            path  = url[:url.rfind("/")+1] if "/" in parts.path else url

            soup = BeautifulSoup(html, "lxml")
            for a in soup.find_all("a", href=True):
                href = a["href"].strip()
                if href.startswith(("mailto:", "tel:", "#", "javascript:", "ftp:")):
                    continue
                if href.startswith("/"):
                    link = base + href
                elif href.startswith("http"):
                    link = href
                else:
                    link = urllib.parse.urljoin(path, href)
                enqueue(link)

        except Exception:
            pass

        to_visit.task_done()

def main():
    start = input("[+] Enter your target URL to scan: ").strip()
    if not start.startswith(("http://","https://")):
        print("[-] Include http:// or https://")
        return

    
    enqueue(start)

 
    threads = []
    for _ in range(MAX_THREADS):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        threads.append(t)

    
    to_visit.join()

 
    for _ in threads:
        to_visit.put(None)
    for t in threads:
        t.join()

 
    print("\n[+] Emails found:")
    for e in sorted(emails):
        print(" -", e)

if __name__ == "__main__":
    main()
