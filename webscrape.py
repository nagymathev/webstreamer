import requests
from bs4 import BeautifulSoup
import subprocess

def find_link(soup, substring):
    links = []
    for a in soup.find_all('a', href=True):
        if substring not in a["href"]:
            continue
        
        links.append(a['href'])
    return links

the_input_for_search = input("Search: ")

URL = f"https://1337x.to/category-search/{the_input_for_search}/Movies/1/"
h = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0"
}

r = requests.get(URL, headers=h)
soup = BeautifulSoup(r.content, "html.parser")

link = []
stripped_links = []
link.append(find_link(soup, "/torrent/"))
for i in link:
    for string in i:
        string = string.split("/")
        for x in range(3):
            string.pop(0)
        string.pop(1)
        stripped_links.append(string)

first10_title = stripped_links[0:10]
for i, x in enumerate(first10_title):
    print('{0}. {1}'.format(i, repr(x)))

movie_select = int(input("Select the index of the movie you would like to watch: "))
selected_movie = link[0][movie_select]

r = requests.get(f"https://1337x.to{selected_movie}", headers=h)
soup = BeautifulSoup(r.content, "html.parser")

magnet_link = find_link(soup, "magnet:")
magnet_link.pop()
magnet_link = magnet_link[0]

process = subprocess.Popen(["webtorrent", magnet_link, "--vlc"],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
stdout, stderr