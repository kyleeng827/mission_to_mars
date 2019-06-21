from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=True)

def news_scrape():
    browser = init_browser()
    # URL of news page to be scraped
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(news_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # title of first article in feed
    news = soup.select_one('ul.item_list li.slide')
    news_title = news.find('div', class_="content_title").get_text()

    # description of first article in feed
    news_p = news.find('div', class_="article_teaser_body").get_text()

    # store into dictionary
    mars_news_title = {
        "news_title": news_title,
        "news_p": news_p
        }
    
    browser.quit()

    return mars_news_title

def img_scrape():
    browser = init_browser()
    # URL of gallery of images when query = 'Mars' to be scraped
    images_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(images_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    base_image_url = 'https://www.jpl.nasa.gov'
    # returns partial url of featured image
    partial_image_url = soup.find("a", class_='button fancybox')['data-link']
    # Concat partial and base URL
    featured_image_url = base_image_url + partial_image_url

    # store into dictionary
    mars_img = {
        "featured_image_url": featured_image_url
    }

    browser.quit()

    return mars_img

def weather_scrape():
    browser = init_browser()
    # URL of twitter page to be scraped
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # weather
    weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    # store into dictionary
    mars_weather = {
        "weather": weather
    }

    browser.quit()

    return mars_weather

def facts_scrape():
    browser = init_browser()
    # URL of webpage containing table
    table_url='https://space-facts.com/mars/'
    browser.visit(table_url)

    # read table from webpage using Pandas
    tables = pd.read_html(table_url , encoding= "utf-8")

    # Convert table into dataframe
    df = tables[0]
    df.columns = ['Characteristic', 'Description']
    
    # import df into html
    facts_html = df.to_html()

    # store into dictionary
    mars_facts = {
        "facts_html": facts_html
    }

    browser.quit()

    return mars_facts

def hemisphere_img():
    browser = init_browser()

    # Create empty list to store imgs later
    hemisphere_imgs = []

    for x in range(4):
        url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url)
        
        browser.find_by_css("a.product-item h3")[x].click()
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        base_url = "https://astrogeology.usgs.gov"

        # hemisphere name and image
        hemisphere_name = soup.find('h2', {"class":"title"}).text
        hemisphere_img_urls = soup.find('img', {"class":"wide-image"})["src"]
        
        # Store data into dictionary
        hemisphere_dict ={
            "title": hemisphere_name,
            "img_url": base_url + hemisphere_img_urls 
        }

        # append to empty list above
        hemisphere_imgs.append(hemisphere_dict)

        browser.back()

    return hemisphere_imgs

def scrape_all():
    browser = init_browser()

    scrape_data = {
        "News Scrape": news_scrape(),
        "Image Scrape": img_scrape(),
        "Weather Scrape": weather_scrape(),
        "Facts Scrape": facts_scrape(),
        "Hemisphere Scrape": hemisphere_img()
    }
    browser.quit()

    return scrape_data