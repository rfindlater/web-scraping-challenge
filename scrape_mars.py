
# Dependencies and Setup
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)



def scrape():
    browser = init_browser()


# Mars News
    # Scrape nasa mars webite
    url_news = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    # response = requests.get(url_news)
    browser.visit(url_news)
    time.sleep(2)

    html = browser.html


    soup = bs(html, 'html.parser')
    results = soup.find('div', class_="slide")

    news_title = results.find('div', class_="content_title").get_text()
    news_p = results.find('div', class_="rollover_description_inner").get_text()
    
    # Visit URL
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    time.sleep(3)
# JPL Image

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    relative_image_path = soup.find_all('img')[3]["src"]
    newurl = "https://www.jpl.nasa.gov"
    featured_image_url = newurl + relative_image_path
# Mars Weather

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # results = soup.find('div', class_="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-1mi0q7o")
    # results_nested = results.find_all('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    # mars_weather = results_nested[4].text
    mars_weather = None

# Mars Facts

    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)

    type(tables)

    facts_df = tables[0]
    facts_df.columns = ['Features', 'Facts']
    facts_df.set_index('Features', inplace=True)
    facts_df

    html_table = facts_df.to_html()

    html_table.replace('\n', '')

# Mars Hemisphere

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    time.sleep(2)

# Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    hemispheres = soup.find_all("div", class_="item")
    hemis_dict = []

    main_url = "https://astrogeology.usgs.gov"

    for i in hemispheres:
        title = i.find("h3").text
        img_src = i.find("a", class_="itemLink product-item")["href"]
        img_url = main_url + img_src
        
        browser.visit(img_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        full_image = soup.find('img', class_="wide-image")
        full_image_new = full_image.get('src')
        full_res_image = main_url + full_image_new
        hemis_dict.append({"title": title, "img_url": full_res_image})

    
    
    mars_info = {
        "title": news_title,
        "newsp": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": html_table,
        "hemispheres_info": hemis_dict
    }
    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_info