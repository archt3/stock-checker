import requests
import os
from twilio.rest import Client
url = 'https://www.costco.com/xbox-series-s-with-additional-controller.product.100699182.html'
def html_get(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"}
    page = requests.get(url, headers=headers)
    return page.content
from bs4 import BeautifulSoup
def check_item_in_stock(url):
    soup = BeautifulSoup(html_get(url), 'html.parser')
    out_of_stock_divs = soup.findAll("img", {"class": "oos-overlay hide"})
    return len(out_of_stock_divs) != 0

def send_message(words):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    message = client.messages \
                    .create(
                         body=words,
                         from_='+15865718624',
                         to='+15108960949'
                     )
    print(message.sid)

import time
times=0
in_stock = check_item_in_stock(url)
print(in_stock)
while not in_stock:
    print(times)
    if(times%60==0):
        print('checking')
        send_message("still checking")
        times=0
    time.sleep(60)
    in_stock = check_item_in_stock(url)
    if(in_stock):
        send_message("in stock")
    times+=1
