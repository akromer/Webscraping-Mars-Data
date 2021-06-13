#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import requests
from flask import Flask, render_template, redirect


# In[2]:


# Set up Splinter
def browser_start():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit site
def scrape():
    browser = browser_start()
    mars_dict={}

    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")


    # In[4]:


    news_title = soup.find('div' , class_='content_title').text
    news_p = soup.find('div' , class_='article_teaser_body').text
    f"{news_title}: {news_p}"


    # In[5]:


    #Image Site
    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")


    # In[6]:


    full_url = soup.find('a', class_='showimg fancybox-thumbs')['href']
    fullimage_url = image_url + full_url
    fullimage_url


    # In[7]:


    #Fact Site
    table_url = "https://galaxyfacts-mars.com/"


    # In[13]:


    facts = pd.read_html(table_url)
    facts = facts[1]
    facts = facts.rename(columns={0:"Metric", 1:"Values"})


    # In[23]:


    facts_html = facts.to_html()
    facts_html


    # In[25]:


    facts_html.replace('\n','')
    print(facts_html)


    # In[27]:


    #Hemispheres
    hemi_url = "https://marshemispheres.com/"
    browser.visit(hemi_url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")


    # In[28]:


    hemis_all = soup.find("div", class_="collapsible results")
    hemis = hemis_all.find_all("div", class_="item")


    # In[31]:


    hemis_sort = []

    for item in hemis:
        try:
            hemi = item.find("div", class_="description")
            title = hemi.h3.text
            hemisort_url = hemi.a["href"]
            browser.visit(hemi_url+hemisort_url)
            html = browser.html
            soup = bs(html, "html.parser")
            image_url=soup.find("li").a["href"]
            if (title and image_url):
                print(" ")
                print(title)
                print(image_url)
            hemi_dict={
                "title" : title,
                "image_url" : image_url
            }
            hemis_sort.append(hemi_dict)
            
        except Exception as ex:
            print(ex)


    # In[32]:


    mars_dict = {
        "news_title" : news_title,
        "news_p" : news_p,
        "fullimage_url" : fullimage_url,
        "facts_html" : facts_html,
        "hemis_sort" : hemis_sort
    }
    browser.quit()
    return mars_dict