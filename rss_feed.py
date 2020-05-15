import requests
import pandas as pd
import random
from bs4 import BeautifulSoup
from time import sleep
from fake_useragent import UserAgent

ua = UserAgent()

sleep_time=[4,5]
#proxies=[
'http://185.200.178.243:3128',
'http://185.198.247.59:3128',
'http://194.38.29.135:3128',
'http://194.38.29.33:3128',
'http://185.198.247.190:3128',
'http://194.38.29.168:3128',
'http://192.144.25.170:3128',
'http://185.200.178.25:3128',
'http://192.144.25.114:3128',
'http://194.38.29.150:3128'
#]
#proxies=['http://194.38.29.150:3128']
if __name__ == '__main__':
    df=pd.read_csv('invalid-rss.csv',encoding = "ISO-8859-1")
    df['RSS']=df['RSS'].astype(str)
    print(df['RSS'].dtype)
    for index,row in df.iloc[316:].iterrows():
        itunes_id=row['Itunes-Link']
        headers={'User-Agent': ua.random}
        with requests.Session() as s:
            r=s.post('http://getrssfeed.com/',data={'url':itunes_id},headers=headers)
            soup=BeautifulSoup(r.content,'lxml')
            danger=soup.select_one('.label.label-danger')
            if danger:
                df.at[index,'RSS']='Unknown podcast'
                print('Unknown podcast')
                with open('links.txt','a') as f:
                    f.write("Unknown podcast"+"\n")
                sleep(random.choice(sleep_time))
                continue

            rss_url=soup.select_one('.btn-primary')['href']
            print(rss_url)
            df.at[index,'RSS']=rss_url
            with open('links.txt','a') as f:
                f.write(rss_url+"\n")
            sleep(random.choice(sleep_time))
                 
    df.to_csv('new-rss.csv')

