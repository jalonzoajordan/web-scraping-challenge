from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    #Set up scrape utilities
    #Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #Scrape the Mars News Site and collect the latest News Title and Paragraph Text. (https://redplanetscience.com/)
    #Assign the text to variables that you can reference later.

    #visit the website
    url_MarsSite = "https://redplanetscience.com/"
    browser.visit(url_MarsSite)

    #scrape xml data into BeautifulSoup
    html = browser.html
    soup = bs(html, "html.parser")

    #get latest news title
    latest_NewsTitle = soup.find('div', {'class':'content_title'}).text

    #get latest paragraph text
    latest_NewsTest = soup.find('div', {'class':'article_teaser_body'}).text

    #visit the url for the image (https://spaceimages-mars.com/)
    url_Image = "https://spaceimages-mars.com/"
    browser.visit(url_Image)

    #scrape xml data into BeautifulSoup
    html = browser.html
    soup = bs(html, "html.parser")

    #Find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    featured_image_path = soup.find('img', {'class':'headerimage'})['src']
    featured_image_url = url_Image + featured_image_path

    #Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet including Diameter, 
    #Mass, etc. (https://galaxyfacts-mars.com/)
    url_Facts = "https://galaxyfacts-mars.com/"

    #Since this is a table we can use pandas
    table_Facts = pd.read_html(url_Facts)

    #First table is about comparisons to Earth. Mars data is on second table
    facts_df = table_Facts[1]

    #Use Pandas to convert the data to a HTML table string.
    html_table = facts_df.to_html()

    #Visit the astrogeology site to obtain high resolution images for each of Mar's hemispheres. (https://marshemispheres.com/)
    url_hemImages = "https://marshemispheres.com/"
    browser.visit(url_hemImages)

    #scrape xml data into BeautifulSoup
    html = browser.html
    soup = bs(html, "html.parser")

    #get all of the image sources
    hemImage_sources = soup.findAll('a',{'class':'itemLink'})

    image_url_list = []
    for image in hemImage_sources:
        image_string = image['href']
        image_dict = {"title": f'{image_string[:-5]} Hemisphere',
                    "img_url": url_hemImages + image['href']}
        if image_dict not in image_url_list:
            image_url_list.append(image_dict)
    
    #Create a full dictionary of data to return
    mars_data_compiled = {
        "Latest_title" : latest_NewsTitle,
        "Latest_desc" : latest_NewsTest,
        "Featured_image" : featured_image_url,
        "Mars_stats_table": html_table,
        "hd_images" : image_url_list
    }

    #close the browser
    browser.quit()

    return mars_data_compiled