import requests
from bs4 import BeautifulSoup
import subprocess

def find_link(soup, substring):
    for a in soup.find_all('a', href=True):
        if substring not in a["href"]:
            continue
        
        return a['href']

the_input_for_search = input("Search: ")

URL = f"https://1337x.to/category-search/{the_input_for_search}/Movies/1/"
h = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0"
}

r = requests.get(URL, headers=h)
soup = BeautifulSoup(r.content, "html.parser")

link = f"https://1337x.to{find_link(soup, '/torrent/')}"
print(link)

r = requests.get(link, headers=h)
soup = BeautifulSoup(r.content, "html.parser")

magnet_link = find_link(soup, "magnet:")

print(magnet_link)

process = subprocess.Popen(["webtorrent", magnet_link, "--vlc"],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
stdout, stderr

print(stdout)
print(stderr)