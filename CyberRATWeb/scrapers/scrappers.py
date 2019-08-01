from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import time
from urllib.request import urlopen
import json
from .timeline_post import TimelinePost
from webdriver_manager.chrome import ChromeDriverManager

def checkHIBP(email):
    result = []
    headers = {
        'hibp-api-key': '4d56711edb2c4b72b8a418ea2c558d41',
        'user-agent': 'CyberRat'
    }

    url = 'https://haveibeenpwned.com/api/v3/breachedaccount/' + email + '?truncateResponse=False'

    resp = requests.get(url=url, headers=headers)
    try:
        data = resp.json()
        for i in range(len(data)):
            result.append(data[i]['Name'] + " on " + data[i]['BreachDate'])
    except:
        result = []
    return result

def Facebook(profile_link):
    result = []

    try:
        r = requests.get(url=profile_link)
        soup = BeautifulSoup(r.text, "html.parser")
        data = json.loads(soup.find('script', type='application/ld+json').text)
        data1 = [element.text for element in soup.find_all("div", class_="_2lzr _50f5 _50f7")]
        data2 = [element.text for element in soup.find_all("div", class_="fsm fwn fcg")]

        try:
            result.append('Lives in ' + data['address']['addressLocality'])
        except:
            result
        if (data1):
            result.append('Affiliations with')
            for i in range(len(data1)):
                result.append('<b>' + data1[i] + '</b>' + ': ' + data2[i])
    except:
        result = []

    return result

def get_instagram_posts(profile_link):
    c = webdriver.Chrome(ChromeDriverManager().install())

    try:
        c.get(profile_link)
    except:
        print('failed to obtain posts from instagram timeline')
        c.close()
        return "account unreachable"

    try:
        privacy_status = c.find_element_by_xpath("//*[contains(text(),'This Account is Private')]")
        if privacy_status:
            c.close()
            return "account private"
    except:
        print("account not private")

    element = c.find_element_by_tag_name('body') # or whatever tag you're looking to scrape from

    for i in range(10):
        element.send_keys(Keys.END)
        time.sleep(0.5)

    soup = BeautifulSoup(c.page_source, 'html.parser')

    post_urls = []
    for a in soup.find_all('a'):
        if '/p/' in a['href']:
            post_urls.append(profile_link + a['href'][1:])

    result = []
    for post_url in post_urls:
        try:
            page = urlopen(post_url).read()
            data = BeautifulSoup(page, 'html.parser')
            body = data.find('body')
            script = body.find('script')
            raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')
            json_data = json.loads(raw)
            posts = json_data['entry_data']['PostPage'][0]['graphql']
            posts = json.dumps(posts)
            posts = json.loads(posts)
            result.append(
                TimelinePost(
                    posts['shortcode_media']['edge_media_to_caption']['edges'][0]['node']['text'],
                    posts['shortcode_media']['display_url']
                )
            )
        except:
            print("post url no accessible\n")
            pass

    c.close()

    return result

def ProfilePhoto(profile_link):
    result = ''
    try:
        r = requests.get(url=profile_link)
        soup = BeautifulSoup(r.text, "html.parser")
        images = soup.find('img', class_="_11kf img")
        result = images['src']
    except:
        result = ''
    return result

def TwitterData(twitter_link):
    result = []
    twitter_posts = []

    try:
        r = requests.get(url=twitter_link)
        soup = BeautifulSoup(r.text, "html.parser")
        bio = soup.find('p', class_="ProfileHeaderCard-bio u-dir")
        if (bio.text):
            result.append(bio.text)
        bio1 = soup.find('span', class_="ProfileHeaderCard-locationText u-dir")
        if (bio1.text):
            result.append(bio1.text)
        bio2 = soup.find('span', class_="ProfileHeaderCard-urlText u-dir")
        if (bio2.text):
            result.append(bio2.text)
        bio3 = soup.find('span', class_="ProfileHeaderCard-joinDateText js-tooltip u-dir")
        if (bio3.text):
            result.append(bio3.text)
        bio4 = soup.find('span', class_="ProfileHeaderCard-birthdateText u-dir")
        if (bio4.text):
            result.append(bio4.text)
        posts = soup.findAll('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
        if(posts):
            for i in range(10):
                twitter_posts.append(posts[i].text)

    except:
        result = ''

    return (result, twitter_posts)