import os, re, requests, time, random
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from http.cookies import SimpleCookie
from __config__ import *

def clearFileName(file_name): # Removes special chars from file name
    return re.sub('[?\/\\ ].+', '', file_name)

def clearUrl(url): # Changes / to - in url
    url = re.sub('\/(?=$)', '', url)
    return re.sub('\/', '-', url)

def randomWait(): # Random wait between two set values
    time.sleep(random.uniform(min_sleep, max_sleep))

def isPathAllowed(path): # Check if path is in allowed urls list
    for x in allowed_paths:
        if re.search(x, path):
            return True
    return False

def downloadPage(url: str, file_path: str, depth: int):
    def findAndDownload(tag: str, inner: str):
        for res in soup.find_all(tag):
            if res.has_attr(inner):
                inn = res[inner]
                inn_p = urlparse(inn)
                if not inn_p.netloc:
                    file_name = clearFileName(os.path.basename(inn))
                    file_path = os.path.join(files_folder, file_name)

                    res[inner] = file_name

                    randomWait()
                    data = s.get(urljoin(start_url, inn))


                    if os.path.isfile(file_path):
                        continue

                    with open(file_path, "wb") as f:
                        f.write(data.content)
                elif dw_other:
                    if not inn_p.scheme:
                        inn = f'http:{inn}'

                    file_name = inn_p.netloc + clearUrl(inn_p.path)
                    file_path = os.path.join(files_folder, file_name)

                    res[inner] = file_name


                    if os.path.isfile(file_path):
                        continue

                    randomWait()
                    data = s.get(inn)

                    with open(file_path, "wb") as f:
                        f.write(data.content)

    def findLinks(depth: int):
        for res in soup.find_all('a'):
            if res.has_attr('href'):
                href = res['href']
                href_p = urlparse(href)

                if href_p.netloc == start_url_p.netloc or not href_p.netloc and isPathAllowed(href_p.path):
                    href_full_url = urljoin(start_url, href)
                    file_name = start_url_p.netloc + clearUrl(href_p.path) + '.html'
                    file_path = os.path.join(files_folder, file_name)

                    res['href'] = file_name


                    if os.path.isfile(file_path):
                        continue

                    downloadPage(href_full_url, file_path, depth-1)


    print(f'Downloading {url} and its content...')

    with open(file_path, "w") as f:
        f.write('')

    randomWait()
    response = s.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    findAndDownload('img', 'src')
    findAndDownload('link', 'href')
    findAndDownload('script', 'src')

    if depth > 0:
        findLinks(depth)

    with open(file_path, "wb") as f:
        f.write(soup.prettify('utf-8'))



simple_cookie = SimpleCookie()
with open('cookies.txt') as f:
    simple_cookie.load(f.read())

cookies = {k: v.value for k, v in simple_cookie.items()}


start_url_p = urlparse(start_url)

files_folder = start_url_p.netloc + '_files'
if not os.path.exists(files_folder):
    os.mkdir(files_folder)


file_name = start_url_p.netloc + clearUrl(start_url_p.path) + '.html'
file_path = os.path.join(files_folder, file_name)

s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'})
s.cookies.update(cookies)

downloadPage(start_url, file_path, depth=depth)
