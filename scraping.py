# import splinter and beautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

#path to chromedriver
#!which chromedriver

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
def scrape_all():
    #initiate headless driver for deployment
    browser = Browser('chrome', executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)

    #run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "last_modified": dt.datetime.now()
    }

    #stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    #visit the mars nasa news site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    #optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time = 1)

    #set up the html parser
    html = browser.html
    news_soup = soup(html,"html.parser")

    #add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div",class_="content_title").get_text()

        # use the parent element to find the paragrph text
        news_p = slide_elem.find("div",class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

#space images url retrieve the images
def featured_image(browser):

    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    #find and click the full image button
    full_image_elem = browser.find_by_tag("button")[1]
    full_image_elem.click()

    #parse the resulting html with soup
    html = browser.html
    img_soup = soup(html,"html.parser")

    try:

        # Find the relative image url
        img_url_rel = img_soup.find("img", class_="fancybox-image").get("src")
    except AttributeError:
        return None
    # Use the base URL to create an absolute URL
    img_url = f"https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}"
    
    return img_url

def mars_facts():
    try:
        #use "read_html" to scrape the facts table into a dataframe
        df = pd.read_html("https://space-facts.com/mars/")[0]
    except BaseException:
        return None

    #assign columns and set index of dataframe
    df.columns =["description","value"]
    df.set_index("description",inplace =True)

    #convert dataframe into HTML format, add bootstrap
    # return the values back to html format
    return df.to_html()

if __name__ == "__main__":
    #if running as script, print scraped data
    print(scrape_all())