from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import time
from urllib.request import urlopen
import json
from .timeline_post import TimelinePost
from webdriver_manager.chrome import ChromeDriverManager

def get_instagram_posts(profile_link):
    c = webdriver.Chrome(ChromeDriverManager().install())

    try:
        c.get(profile_link)
    except:
        print('failed to obtain posts from instagram timeline')
        c.close()
        return []

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