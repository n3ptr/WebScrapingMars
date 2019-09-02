from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_data():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(4)

    i=0
    MarsData = []
    headlines = []
    paragraphs = []
    nwsDates = []
    hemisphere_image_urls = []

    html = browser.html
    soup = bs(html, "html.parser")

    # titleCards = soup.find('li', class_='slide')
    totalPar = len(soup.find_all('div', class_='article_teaser_body'))
    # aPar = soup.find_all('div', class_='article_teaser_body')[0].text

    while i < totalPar:
        aTitle = soup.find_all('div', class_='content_title')[i].text
        aPar = soup.find_all('div', class_='article_teaser_body')[i].text
        nwsDate = soup.find_all('div', class_='list_date')[i].text
        clnTitle = aTitle.replace('\n', ' ').replace('\r', '').strip()
        clnPar = aPar.replace('\n', ' ').replace('\r', '').strip()
        headlines.append(clnTitle)
        paragraphs.append(clnPar)
        nwsDates.append(nwsDate)
        i += 1

    print(headlines[0])
    hl = headlines[0]
    print(paragraphs[0])
    pg = paragraphs[0]
    print(nwsDates[0])
    dt = nwsDates[0]

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(3)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)

    browser.click_link_by_partial_text('more info')
    time.sleep(3)

    html = browser.html
    soup = bs(html, "html.parser")
    full_res = soup.find_all(class_='download_tiff')[1].a['href']
    # image_string = 'https:' + full_res

    url = 'https://twitter.com/MarsWxReport'
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    Mars_Weather = soup.find_all(class_='js-tweet-text-container')
    MarsWeather = Mars_Weather[1].text

    # mars facts
    url = 'https://space-facts.com/mars/'
    res = requests.get(url)
    soup = bs(res.content,"html.parser")
    table = soup.find_all('table')[1]
    table_rows = table.find_all('tr')

    res = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text.strip() for tr in td if tr.text.strip()]
        if row:
            res.append(row)


    df = pd.DataFrame(res, columns=["Stat", "Value"])
    # print(df)
    tblMars = df.to_html()

    print(tblMars)

    #hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(5)

    html = browser.html
    soup = bs(html, "html.parser")
    #get the most recent tweet text
    hemi = soup.find_all('div', class_='item')
    # hemiTitle = soup.find_all(class_='itemLink product-item')
    time.sleep(2)

    # loop and visit each full image page, pull full image URL
    for item in hemi:
        linkTxt = item.a['href']
        titleTxt =  item.h3.text
        url = 'https://astrogeology.usgs.gov/' + linkTxt
        browser.visit(url)
        time.sleep(2)
        html = browser.html
        soup = bs(html, "html.parser")
        img = soup.find(class_='downloads')
        img_url = img.a['href']
        hemisphere_image_urls.append({"title": titleTxt, "img_url": img_url})

    print(hemisphere_image_urls)

    browser.quit()

    # marsData = {
    #     "Headline": hl,
    #     "newPara": pg,
    #     "nwsDate": dt,
    #     'MarsWeather': MarsWeather,
    #     'MarsFacts': tblMars,
    #     'hemi': hemisphere_image_urls
    # }
        marsData = {
        "Headline": hl,
        "newPara": pg,
        "nwsDate": dt,
        'MarsWeather': MarsWeather,
        'MarsFacts': tblMars,
        'hemi': hemisphere_image_urls
    }

    return marsData
