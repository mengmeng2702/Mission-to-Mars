# import splinter and beautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

#path to chromedriver
#!which chromedriver

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)

#visit the mars nasa news site
url = "https://mars.nasa.gov/news/"
browser.visit(url)
#optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time = 1)

#set up the html parser
html = browser.html
news_soup = soup(html,"html.parser")
slide_elem = news_soup.select_one("ul.item_list li.slide")

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div",class_="content_title").get_text()
news_title

# use the parent element to find the paragrph text
news_p = slide_elem.find("div",class_="article_teaser_body").get_text()
news_p

#space images url retrieve the images
# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)

#find and click the full image button
full_image_elem = browser.find_by_tag("button")[1]
full_image_elem.click()

#parse the resulting html with soup
html = browser.html
img_soup = soup(html,"html.parser")

# Find the relative image url
img_url_rel = img_soup.find("img", class_="fancybox-image").get("src")
img_url_rel

# Use the base URL to create an absolute URL
img_url = f"https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}"
img_url

df = pd.read_html("https://space-facts.com/mars/")[0]
df.columns =["description","value"]
df.set_index("description",inplace =True)


# return the values back to html format
df.to_html()

browser.quit()

