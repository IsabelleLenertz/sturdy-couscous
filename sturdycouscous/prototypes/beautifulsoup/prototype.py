from bs4 import BeautifulSoup
import requests
#Target web page
url = "https://projects.fivethirtyeight.com/trump-approval-ratings/"
response = request.get(url)
if response.status_code == 200:
    links = BeautifulSoup(response.content, 'lxml').soup.find_all('a')
    #Get all headers from the latest section of the web site
    for link in links:
        print(link.attrs['href'])
