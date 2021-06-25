#!/usr/bin/env python
# coding: utf-8
# The above are typically optional. Most environments use utf-8 coding,
# and we can specify python on the command line when execute the code, 
# but it doesn't hurt to be explicit, and might occasionally help. 

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# ### Initialize the browser, Create a data dictionary, and End the WebDriver returning the scraped data.
# Declare the function:
def scrape_all():
    # Initiate headless driver for deployment (Set up Splinter).
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # Run all scraping functions and store results in a dictionary.
    # Where did this come from?
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Set our news title and paragraph variables 
    news_title, news_paragraph = mars_news(browser)
    # Stop webdriver and return data
    browser.quit()
    return data

# ### News Titles and Paragraph Summary
# Declare the function:
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page. Wait for div.list_text to load but not more than 1 second.
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    return news_title, news_p

# ### Featured Images
# Declare the function:
# Visit URL
def featured_image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url <- Where is this coming from?
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

        # Find the relative image url <- This makes more sense to me.
        # img_url_rel2 = img_soup.find('img', class_='headerimage fade-in').get('src')

    except AttributeError:
        return None

     # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


# ### Mars Facts
# Define the function
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns = ['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

    # browser.quit() <- This is no longer needed. 
