import os
import re
import json
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

def clearFileName(file_name): # Removes special chars from file name
    return re.sub('[?\/\\ ].+', '', file_name)

def clearUrl(url): # Changes / to - in url
    url = re.sub('\/(?=$)', '', url)
    return re.sub('\/', '-', url)

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

                    data = s.get(urljoin(start_url, inn), cookies=cookies)


                    if os.path.isfile(file_path):
                        continue

                    with open(file_path, "wb") as f:
                        f.write(data.content)
                elif dw_from_other:
                    if not inn_p.scheme:
                        inn = f'http:{inn}'

                    file_name = inn_p.netloc + clearUrl(inn_p.path)
                    file_path = os.path.join(files_folder, file_name)

                    res[inner] = file_name


                    if os.path.isfile(file_path):
                        continue

                    data = s.get(inn, cookies=cookies)

                    with open(file_path, "wb") as f:
                        f.write(data.content)

    def findLinks(depth: int):
        for res in soup.find_all('a'):
            if res.has_attr('href'):
                href = res['href']
                href_p = urlparse(href)
                if not href_p.netloc:
                    href_full_url = urljoin(start_url, href)
                    file_name = start_url_p.netloc + clearUrl(href_p.path) + '.html'
                    file_path = os.path.join(files_folder, file_name)

                    res['href'] = file_name


                    if os.path.isfile(file_path):
                        continue

                    downloadPage(href_full_url, file_path, depth-1)

    print(f'Downloading {url} and its content...')

    response = s.get(url, cookies=cookies)
    soup = BeautifulSoup(response.text, "html.parser")

    findAndDownload('img', 'src')
    findAndDownload('link', 'href')
    findAndDownload('script', 'src')

    if depth > 0:
        findLinks(depth)

    with open(file_path, "wb") as f:
        f.write(soup.prettify('utf-8'))


with open('config.json') as f:
    cfg = json.load(f)

start_url = cfg['url']
cookies = cfg['cookies']
depth = cfg['depth']
dw_from_other = cfg['dw_from_other']

start_url_p = urlparse(start_url)

files_folder = start_url_p.netloc + '_files'
if not os.path.exists(files_folder):
    os.mkdir(files_folder)


file_name = start_url_p.netloc + clearUrl(start_url_p.path) + '.html'
file_path = os.path.join(files_folder, file_name)

s = requests.Session()
downloadPage(start_url, file_path, depth=depth)
