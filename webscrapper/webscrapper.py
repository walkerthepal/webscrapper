from pathlib import Path
import sys
import re
import json
import requests
import pandas as pd
import  bs4


def main():

    sweetwater = {
        "url" : "https://www.sweetwater.com/store/search?s=",
        "headers" : { 
                    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
                    "Referer" : "https://www.sweetwater.com/"
                    }
                }
    reverb = {        
        "url" : "https://reverb.com/marketplace?query=big muff",
        "headers" : { 
                    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"
                    }
                }
    
    #Get query object
    with open(Path("./webscrapper/test_input.json")) as file:
        query = json.load(file)
    
    print(query)
    
    #Reverb setup
    if query["website"] == "reverb":

        headers = reverb["headers"]

        url = reverb["url"] + query["item"]

    #Sweetwater setup
    elif query["website"] == "sweetwater":

        headers = sweetwater["headers"]

        item = re.split(r'\s', query["item"])
        for word in item:
            if word == item[0]:
                url = sweetwater["url"] + f'{word}'
            else:
                url = sweetwater["url"] + f'+{word}'
    else:
        sys.exit("JSON doesn't contain 'reverb' or 'sweetwater' for 'website'.")

    #https request
    page = requests.get(url,headers=headers)
    
    if page.status_code != 200:
        sys.exit(page.status_code)

    soup = bs4.BeautifulSoup(page.content, "html5lib")
    print(soup.prettify())
    prices = soup.findAll("price-display")
    print(prices)

#<div class="grid-card__price"><span class="price-display">$70.99</span></div>
#-------------------------# 
if __name__ == '__main__':
    main()