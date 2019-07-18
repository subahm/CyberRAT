import json

import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.generic import CreateView
from django.http import Http404

from CyberRATWeb.scrapers.instagram_scrapper import get_instagram_posts
from CyberRATWeb.services.timeline_analyzer import TimeLineAnalysisResults
from CyberRATWeb.forms import SearchForm
from CyberRATWeb.models import Search
from CyberRATWeb.services.email_service import EmailService


class Entity():

    def __init__(self, name, breachNumber, breachedSites, facebook_data, time_line_data, threatLevel):
        self.name=name
        self.breachNumber = breachNumber
        self.breachedSites = breachedSites
        self.facebook_data = facebook_data
        self.time_line_data = time_line_data
        self.threatLevel = threatLevel


class HomeView(CreateView):
    form_class = SearchForm
    model = Search
    redirect_field_name = 'results.html'


def results(request, uuid):

    try:
        search = get_object_or_404(Search, uuid=uuid)
    except ValueError:
        raise Http404

    name = search.name
    email = search.email
    profile_link = search.facebook_link
    instagram_link = search.instagram_link

    def checkHIBP(email):
        result=[]
        headers = {
                 'hibp-api-key': '4d56711edb2c4b72b8a418ea2c558d41',
                 'user-agent': 'CyberRat'
        }
        
        url = 'https://haveibeenpwned.com/api/v3/breachedaccount/'+email+'?truncateResponse=False'

        resp = requests.get(url=url,headers=headers)
        try:
            data = resp.json()
            for i in range(len(data)):
                result.append(data[i]['Name'] + " on " + data[i]['BreachDate'] )
        except:
            result=[]
        return result


    def Facebook(profile_link):
        result = []

        try:
            r=requests.get(url=profile_link)
            soup = BeautifulSoup(r.text, "html.parser")
            data = json.loads(soup.find('script', type='application/ld+json').text)
            data1 = [element.text for element in soup.find_all("div", class_="_2lzr _50f5 _50f7")]

            result.append('Lives in ' + data['address']['addressLocality'])
            if(data1):
                result.append('Affiliations include')
                for i in range(len(data1)):
                    result.append(str(i+1) + ': ' + data1[i])
        except:
             result.append('Could not retrieve anything')
        return result

    # def Linkedin(linkedin_profile_link):
    #     result = []
    #
    #     try:
    #         r=requests.get(url=linkedin_profile_link)
    #         soup = BeautifulSoup(r.text, "html.parser")
    #         data = json.loads(soup.find('script', type='application/ld+json').text)
    #         data1 = [element.text for element in soup.find_all("div", class_="result-card__title experience-item__title")]
    #
    #         result.append('Lives in ' + data['address']['addressLocality'])
    #         if(data1):
    #             result.append('Affiliations include')
    #             for i in range(len(data1)):
    #                 result.append(str(i+1) + ': ' + data1[i])
    #     except:
    #          result.append('Could not retrieve anything')
    #     return result

    time_line_data = get_instagram_posts(instagram_link)

    entity = Entity('', '', '','','','')

    entity.name = name
    entity.breachNumber = checkHIBP(email)
    entity.breachedSites = checkHIBP(email)
    entity.facebook_data = Facebook(profile_link)
    entity.time_line_data = TimeLineAnalysisResults(time_line_data)

    print("THIS IS THING")
    print(entity.time_line_data.post_containing_dog_name)
    print(entity.time_line_data.post_containing_mothers_maiden)


    if (len(entity.breachNumber) <= 0):
        entity.threatLevel = '0%'
    elif (len(entity.breachNumber) < 3):
        entity.threatLevel = '25%'
    elif (len(entity.breachNumber) < 5):
        entity.threatLevel = '50%'
    else:
        entity.threatLevel = '100%'

    return render(request, 'CyberRATWeb/results.html', {'entity': entity, 'uuid': uuid})


def generateEmail(request, uuid, entity):
    try:
        search = get_object_or_404(Search, uuid=uuid)
    except ValueError:
        raise Http404

    email = search.email

    site_html = render_to_string('CyberRATWeb/results.html', {'entity': entity, 'uuid': uuid})

    email_service = EmailService.getInstance()
    email_service.send_results(request, uuid, email, site_html)

    return redirect(request.META['HTTP_REFERER'])
