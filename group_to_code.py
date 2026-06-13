import os
import re
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

def group_scrape():
    username = os.getenv("UEK_LOGIN")
    password = os.getenv("UEK_PASSWORD")
    session = requests.Session()
    session.auth = (username, password)
    url='https://planzajec.uek.krakow.pl/index.php'
    base_url='https://planzajec.uek.krakow.pl/'
    response = session.get(url)
    if response.status_code == 401:
        print('problem')
    response.encoding = 'utf-8-sig' 
    soup = BeautifulSoup(response.text, 'html.parser')
    kategorie_divs = soup.find_all('div', class_='kategorie')   #'a', class_="kategorie"
    all_between_links=[]
    all_groups=[]
    for div in kategorie_divs:
        links = div.find_all('a')
        all_between_links.extend(links)
    for link in all_between_links:
        subpage_path = link.get('href')
        #text = link.text
        full_url = base_url + subpage_path.lstrip('/')
        subpage_response = session.get(full_url)
        
        if subpage_response.status_code == 200:
            subpage_response.encoding = 'utf-8-sig'
            subpage_soup = BeautifulSoup(subpage_response.text, 'html.parser')
            div_forgroup=subpage_soup.find_all('div', class_="kolumna")
            subbetween=[]
            for sub_div in div_forgroup:
                sublinks=sub_div.find_all('a')
                subbetween.extend(sublinks)
            #group_names = [{"name":link.text,"link":re.findall(r'id=(\d+)',link['href'])[0]} for link in subbetween]
            
            for link in subbetween:
                match = re.search(r'id=(\d+)', link['href'])
                if match:
                    all_groups.append({
                        "name": link.text.strip(),
                        "link": match.group(1)
                    })
        else:print(f"Failed to load. Status: {subpage_response.status_code}")
    
    with open('dic.json', 'w', encoding="utf-8-sig") as f:
        json.dump(all_groups, f, ensure_ascii=False, indent=4)
    print("Saved file 'dic.json' succesfully!")
        # 3. Be polite to the server! Pause for half a second between requests


group_scrape()
