import requests
from bs4 import BeautifulSoup
import csv23

with open('D:\\datafrom.csv', 'w', newline='') as file:
    writer = csv23.writer(file)
    writer.writerow(["Title", "textdata"])
    for i in range(1,16):
        url="https://www.thegazette.co.uk/all-notices/notice?text=&categorycode-all=all&noticetypes=&location-postcode-1=&location-distance-1=1&location-local-authority-1=&numberOfLocationSearches=1&start-publish-date=&end-publish-date=&edition=&london-issue=&edinburgh-issue=&belfast-issue=&sort-by=&results-page-size=10"+str(i)
        # url="https://www.w3schools.com/"

        headers={
        'user-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        response=requests.get(url,headers=headers)
        print(response)
        soup=BeautifulSoup(response.content,"html")
        getpoint=soup.find_all('div',class_="feed-item")
        
        for getpoint in getpoint:
            alink=getpoint.find('h3',class_='title').text.strip()
                # print(alink)
            data_from=""
            if getpoint.find('p'):
                plink=getpoint.find('p').text.strip().replace('\n','').replace(' ','')
                    # print(plink)
                data_from=plink
            else:
                dlist_element=getpoint.find_all('dl')
                for dlt in dlist_element:
                    dlist=dlt.text.strip().replace('\n','').replace(' ','')
                    # dlist = ' '.join(dlt.stripped_strings)
                    # print(dlist)
                    # data_from=dlist
                    data_from += dlist
                    # print(data_from)
                
            writer.writerow([alink,data_from])
print("Done")



