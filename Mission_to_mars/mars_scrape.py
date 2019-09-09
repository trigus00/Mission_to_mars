from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests



def init_bowser():
    
    
    #@NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    
    return Browser("chrome", **executable_path, headless=False)
mars = {} 

def mars_article():
    
    try:
        browser = init_bowser()
        url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup( html,'html.parser')

        mars['titles'] = soup.find('div', class_='content_title').find('a').text
        mars['paragraph'] = soup.find('div', class_='rollover_description_inner').text

        return mars

    finally:
        browser.quit()
        
def mars_image():
    try:
        browser=init_bowser()
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')
        
        #scraping the image
        featured_image = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')
        #scraping the image 
        featured_image = featured_image[1:-1]
        
        # url main website and image website 
        main_url = 'http://www.jpl.nasa.gov'
        image_url= main_url + featured_image
        mars['Mars_Image'] = image_url
        return mars
    finally:
        browser.quit()

def mars_twitter():
    try:
        #twitter scraping 
        browser = init_bowser()
        mars_weather_twitter = 'https://twitter.com/marswxreport?lang=en' 
        browser.visit(mars_weather_twitter)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        #finding latest tweets on Mars Twitter acount 
        latest_tweet = soup.find_all('div', class_='js-tweet-text-container')
        for tweet in latest_tweet:
            weather_tweets = tweet.find('p').text
            if 'sol' and 'pressure' in weather_tweets:
                mars['twitter']= weather_tweets[:-23]
            else: 
                pass
        return mars
    finally:
        browser.quit()
def mars_facts():
    try:
        #image scraping 
        browser = init_bowser()
        mars_facts = 'https://space-facts.com/mars/'
        browser.visit(mars_facts)
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')
    
    
        my_table = soup.find('table',{'class':'tablepress tablepress-id-p-mars'})
        info = my_table.find_all('tr')
        mars_facts = [] 
        for i in info:
            row = i 
            mars_facts.append(row.get_text('').split(':'))
        row = 0
        columns = []
    
        while row < 9:
            columns.append(mars_facts[row][0])
            row = row + 1 
        row = 0
    
        columns_1 = []

        while row < 9:
            columns_1.append(mars_facts[row][1])
            row = row + 1 

        mars_df =pd.DataFrame()
        mars_df['Description'] = columns
        mars_df['Values']=columns_1

        mars_df.set_index('Description')

        facts = mars_df.to_dict(orient='record')
        
    
        mars['facts']= facts
        return mars
    finally:
        browser.quit()

def mars_hemespheres():
    try:
        #image scraping 
        browser = init_bowser()
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')

        #hempisphere URLS 
        hemisphere_image_urls = []
        main_url = 'https://astrogeology.usgs.gov'

        image_items = soup.find_all('div',class_='item')
        for link in image_items:
            image_name = link.find('h3').get_text
            image_find = link.find('a', class_='itemLink product-item')['href']
            link_to_image = main_url + image_find 
    
        #opening another website using link to image 
    
            browser.visit(link_to_image)
            image_html = browser.html
            soup = BeautifulSoup(image_html, 'html.parser')
            image_url = main_url + soup.find('img', class_='wide-image')['src']
    
    
    
            hemisphere_image_urls.append({"title": image_name , "image_url": image_url})
            mars['hemesphere']=hemisphere_image_urls
        
        return mars
    
    finally:
        browser.quit()

