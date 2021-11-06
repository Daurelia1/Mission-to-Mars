# Import Dependencies
import pandas as pd
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
import shutil
from IPython.display import Image
from webdriver_manager.chrome import ChromeDriverManager
import scrape_mars

# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit redplanetscience.com 
url ="https://redplanetscience.com/"
browser.visit(url)

html = browser.html
soup = bs(browser.html, 'lxml')

Latest_title = soup.find_all('div', class_='content_title')[0].text
Latest_paragraph = soup.find_all('div', class_='article_teaser_body')[0].text
print(f"Latest Title:{Latest_title}")
print(f"Latest Paragraph:{Latest_paragraph}")

url = 'https://spaceimages-mars.com'
browser.visit(url)
soup = bs(browser.html, 'lxml')

for div in soup.find_all('div', class_='floating_text_area'):
    a = div.find('a')
    image = a['href']
    print(image)
Featured_image_url = 'https://spaceimages-mars.com/'+ image
print(f"Featured_image_url = {Featured_image_url}")

response = requests.get(Featured_image_url, stream=True)
with open('Images/Featuredimage.png', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)

Image(url='Images/Featuredimage.png')

url = 'https://galaxyfacts-mars.com'
table = pd.read_html(url)[0]
header = table.iloc[0]
table = table[1:]
ind=table[0].tolist()
marsList = table[1].tolist()
earthList = table[2].tolist()
marsDict = {'Mars':marsList,
            'Earth':earthList}
table=pd.DataFrame(marsDict,index=ind)
table

html_table= table.to_html()
html_table=html_table.replace('\n', '')
html_table

url = 'https://marshemispheres.com/'
response = requests.get(url)
soup = bs(response.text, 'lxml')
results = soup.find_all('div', class_='description')

hemisphere_image_urls=[]
for each in results:
    title = each.h3.text    
    response = requests.get(f'https://marshemispheres.com/{each.a["href"]}')
    soup = bs(response.text,'lxml')
    hemiResult=soup.find_all('li')[0].a['href']
    hemisphere_image_urls.append({
        "title":title[0:-9],
        "img_url":f'https://marshemispheres.com/{hemiResult}'
        })
print(hemisphere_image_urls)