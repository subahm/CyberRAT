import json

import requests
from bs4 import BeautifulSoup


def Linkedin(linkedin_profile_link):
    result = []

    try:
        r = requests.get(url=linkedin_profile_link)
        soup = BeautifulSoup(r.text, "html.parser")
        data = json.loads(soup.find('script', type='application/ld+json').text)
        data1 = [element.text for element in soup.find_all("div", class_="result-card__title experience-item__title")]

        result.append('Lives in ' + data['address']['addressLocality'])
        if (data1):
            result.append('Affiliations include')
            for i in range(len(data1)):
                result.append(str(i + 1) + ': ' + data1[i])
    except:
        result.append('Could not retrieve anything')
    print (*result)
    print ("sfs")

Linkedin("https://ca.linkedin.com/in/subah-mehrotra-b71484132")