import os
import json
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import ssl
import re
import csv

fields = ['image', 'explication', 'tomove', 'figure']
rows = []

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

ua = UserAgent()

url = 'https://www.chesstactics.org/the-double-attack/the-knight-fork/introduction/2_1_1_1.html'
headers = {'User-Agent':str(ua.random)}

i=0

while True:
    i+=1
    print(i)

    req = requests.get(url, headers=headers)
    req.encoding = req.apparent_encoding
    soup = BeautifulSoup(req.text, 'html.parser')

    url2 = soup.find("a", {"class": "next"})['href']

    imdivs = soup.find_all("div", {"class": "tactics"})
    img = imdivs[0].find('img')['src']

    #figure
    figure = imdivs[0].find('span', {"class": "figure-label"}).getText()

    #to-move
    tomove = '[' + imdivs[0].find('span', {"class": "to-move"}).getText() + ']'

    namer = re.search('(\d)+\.(\d)+\.(\d)+\.(\d)+', figure)
    imgname = re.sub('\.', '_', namer.group()) + '.svg'

    #image
    image = f'<img src="{imgname}">'

    #downloading image
    imglink = 'https://www.chesstactics.org' + img
    with open(imgname, 'wb') as handle:
        response = requests.get(imglink, stream=True)
        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)

    paras = soup.find_all("p")
    explication = ''
    for para in paras:
        if explication:
            explication += '\n' + para.getText()
        else:
            explication = para.getText()
    #explication
    re.sub(' +', ' ', explication)

    adder = [image, explication, tomove, figure]
    rows.append(adder)

    if url == url2:
        break
    url = url2


with open('anki.csv', 'w', encoding="utf-8", newline='') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)
      
    # writing the fields
    csvwriter.writerow(fields)
      
    # writing the data rows
    csvwriter.writerows(rows)