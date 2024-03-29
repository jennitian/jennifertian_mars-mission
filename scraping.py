#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    # convert browser html to soup object
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    
    return news_title, news_p

###image scraping
# Visit URL
def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    try: 
        # Find the relative image url inside <figure/> <a/> <img/>
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        # Adds base url
    except AttributeError:
        return None

    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    return img_url

def hemispheres(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    #find full image buttom
    high_res_images = []
    i = 0
    for i in range(0,4):
        image_link = browser.find_link_by_partial_text('Hemisphere Enhanced')[i]
        image_link.click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        #get url
        img_url = soup.select_one('div.downloads a').get('href')
        #get title
        img_title = soup.find("h2", class_= 'title').get_text()
        #append list with title: url
        high_res_images.append({img_title: img_url})
        #start from front page again
        browser.visit(url)
        i += 1
    return high_res_images

    

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Value']
    df.set_index('Description', inplace=True)
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="/usr/local/bin/chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)
    hemispheres_list = hemispheres(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres_list}
    return data

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
