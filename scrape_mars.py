
# coding: utf-8

# # Mission to Mars

# # WebScraping
# -------
# ## NASA Mars News
# -------
# - Get the latest  [NASA Mars News](https://mars.nasa.gov/news/) by scraping the website and collect the latest news title and paragragh text.


# Dependencies
import time
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from selenium import webdriver
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Create a dictionary for all of the scraped data
    mars_data = {}

    # Visit the Mars news page. 
    mars_news_url = "https://mars.nasa.gov/news/"
    browser.visit(mars_news_url)
 

    # Search for news
    # Scrape page into soup
    html = browser.html
    mars_news = bs(html, 'html.parser')

    # Find the latest Mars news title.
    news_title = mars_news.find('div', class_='content_title').text


    # Find the latest Mars news summary.
    news_p = mars_news.find('div', class_="rollover_description_inner").text

    # Add the news title and summary to the dictionary
    mars_data["news_title"] = news_title
    mars_data["summary"] = news_p


    # ## JPL Mars Space Images - Featured Image
    # ------
    # - Visit the url for JPL's Featured Space [Image](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    # - Use splinter to navigate the site and find the full size jpg image url for the current Featured Mars Image.
    # - Save a complete url string for this image


    # While chromedriver is open go to JPL's Featured Space Image page. 
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    # Scrape the browser into soup and use soup to find the full resolution image of mars
    # Save the image url to a variable called `featured_image_url`
    html = browser.html
    jpl_soup = bs(html, 'html.parser')
    image_url = jpl_soup.find('a', {'id': 'full_image', 'data-fancybox-href': True}).get('data-fancybox-href')

    # Get the base url from the href of the website 
    jpl_logo_href = jpl_soup.find_all('div', class_='jpl_logo')

    # Retrieve page with the requests module
    response = requests.get(jpl_url)

    # Create BeautifulSoup object; parse with 'html.parser'
    html_page = browser.html
    JPL_soup = bs(html_page, "html.parser")

    # Get all the hrefs of the url
    links = []
    for link in JPL_soup.find_all('a'):
        links.append(link.get('href'))


    # Retrieve the 2nd href in the list 
    jpl_link = links[1].strip('/')

    # Concatenate to get the featured image url.
    featured_image_url = "https://"+jpl_link + image_url

    # Add the featured image url to the dictionary
    mars_data["featured_image_url"] = featured_image_url


    # ## Mars Weather 
    # ------
    # - From the [Mars Weather twitter](https://twitter.com/marswxreport?lang=en) account scrape the latest Mars weather tweet from the page.
    # - Save the tweet text for the weather report.


    # While chromedriver is open go to Mars weather twitter page. 
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    time.sleep(10)
  

    # Search for the twitter weather news and scrape page into soup
    html = browser.html
    twitter_news = bs(html, 'html.parser')

    # Get the first tweet by using 'find' on the p element with 
    # the class = 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'.
    tweet = twitter_news.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')

    # Extract the unwanted a tag with the following class. 
    #unwanted = tweet.find('a', class_="twitter-timeline-link u-hidden")
    #unwanted.extract()

    mars_weather = tweet.text

    # Add the weather to the dictionary
    mars_data["mars_weather"] = mars_weather

    # ## Mars Facts
    # ---- 
    # - Visit the [Mars Facts webpage](https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # - Use Pandas to convert the data to a HTML table string.


    #  While chromedriver is open go to Mars facts url using chrome from the excuteable command above. 
    mars_facts_url = "https://space-facts.com/mars/"
    browser.visit(mars_facts_url)

    # Conver the url to a pandas df
    mars_df = pd.read_html(mars_facts_url)
    mars_facts_df = pd.DataFrame(mars_df[0])

    mars_facts_df.columns = ['Characteristic','Data']
    mars_df_table = mars_facts_df.set_index("Characteristic")

     # Convert the pd df to HTML table and clean up. 
    mars_html_table = mars_df_table.to_html(classes='marsdata')
    mars_table = mars_html_table.replace('\n', ' ')

    # Add the Mars facts table to the dictionary
    mars_data["mars_table"] = mars_table


    # ## Mars Hemispheres
    # ----
    # - Visit the [USGS Astrogeology site](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
    # - Get the image url to the full resolution image for each hemisphere.
    # - Save both the image url string as a Python dictionary for the full resolution hemipshere image, and the Hemisphere title containing the hemisphere name.
    # - Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

    #  While chromedriver is open go to USGS Astr ogeologyurl using chrome from the excuteable command above. 
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)


    # Search for the Mars hemispheres page and scrape page into soup
    html = browser.html
    mars_hemispheres = bs(html, 'html.parser')

    # Get the div element that holds the images. 
    images = mars_hemispheres.find('div', class_='collapsible results')
    
    #Loop through the class="item" by clicking the h3 tag and getting the title and url. 

    hemispheres_image_urls = []

    for i in range(len(images.find_all("div", class_="item"))):
        time.sleep(5)
        image = browser.find_by_tag('h3')
        image[i].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        title = soup.find("h2", class_="title").text
        div = soup.find("div", class_="downloads")
        for li in div:
            link = div.find('a')
        url = link.attrs['href']
        hemispheres = {
                'title' : title,
                'img_url' : url
            }
        hemispheres_image_urls.append(hemispheres)
        browser.back()

        # Add the hemispheres data to the  dictionary
        mars_data["hemispheres_image_urls"] = hemispheres_image_urls

        # Return the dictionary
        return mars_data



   # Test scrape_mars 
# if __name__ == "__main__":
 #    scrape()
