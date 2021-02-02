#!/usr/bin/env python
# coding: utf-8

# In[13]:


from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

# In[14]:

def scrape_all():
# Windows users
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)

    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now()
    }

# In[15]:

def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


    # In[16]:


    html = browser.html
    news_soup = soup(html, 'html.parser')


    # Add try/except for error handling
    try:

        slide_elem = news_soup.select_one('ul.item_list li.slide')


        # In[17]:


        #slide_elem.find("div", class_='content_title')


        # In[18]:


        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        #news_title


    # In[19]:


    # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None    

    return news_title, news_p


# ### 10.3.4 Featured Images 

# In[20]:

def featured_image(browser):
# Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)


    # In[21]:


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # In[23]:


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')


# In[24]:

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        #img_url_rel

    except AttributeError:
        return None


# In[25]:


    # Use the base URL to create an absolute URL
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    return img_url


# In[32]:

def mars_facts():
    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]
#df.head()
    except BaseException:
        return None

    df.columns=['description', 'Mars']
    df.set_index('description', inplace=True)
    #df


# In[34]:


    return df.to_html()


# In[35]:


    browser.quit()
    return data


# In[ ]:
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())



