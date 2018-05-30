from __future__ import print_function
from bs4 import BeautifulSoup
import requests
import re
import urllib
import http.cookiejar
import sys
import time

login_url = 'http://www.neopets.com/login.phtml'
found_count = 0
login_attempt_count = 0

username = input('Username: ')
password = input('Password: ')

with requests.Session() as s:
    while(login_attempt_count < 3):
        r = s.get(login_url)
        Text = r.content.decode()
        soup = BeautifulSoup(Text, 'html.parser')
        payload = {'destination': '', 'username': username, 'password': password}
        print('Logging in to the site.')
        r = s.post(login_url, data=payload)
        while(True):
            r = s.get('http://www.neopets.com/magma/pool.phtml')
            Text = r.content.decode()
            soup = BeautifulSoup(Text, 'html.parser')
            if str(soup.find(id="npanchor")) == 'None':
                print('Signed out. Attempting to sign in...', flush=True)
                login_attempt_count += 1
                break
            neopoints = re.search(r'\>(.*?)\<',str(soup.find(id="npanchor"))).group(1)
            time_str = re.search(r'\>(.*?)\<',str(soup.find(id="nst"))).group(1)
            if "Moltara are permitted to enter the Pool" in Text:
                print("Not now ", time_str + ' ' + neopoints, flush=True)
                time_txt = open('X:\\User\\Documents\\magma-time-checker\\magma_times.txt', 'a')
                time_txt.write('NOT found at ' + time_str + '\n')
                time_txt.close()
                f = open('X:\\User\\Documents\\magma-time-checker\\magma.html', 'w')
                f.write(str(r.content))
                f.close()
            else:
                print("FOUND!!!!!!!!!!!!!!!!")
                found_count += 1
                f = open('X:\\User\\Documents\\magma-time-checker\\MAGMATIMEFOUND' + str(found_count) + '.html', 'w')
                f.write(str(r.content))
                f.close()
                time_txt = open('X:\\User\\Documents\\magma-time-checker\\magma_times.txt', 'a')
                time_txt.write('FOUND AT ' + time_str + '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
                time_txt.close()
            time.sleep(60)