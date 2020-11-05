from bs4 import BeautifulSoup
import requests
#Target web page
url = "https://projects.fivethirtyeight.com/trump-approval-ratings/"

#Connection to web page
response = requests.get(url)
print(response.status_code)

# Convert the response HTLM string into a python string
html = response.text

soup = BeautifulSoup(response.content, 'lxml')

links = soup.find_all('a')

#Get all headers from the latest section of the web site
for link in links:
    print(link.attrs['href'])