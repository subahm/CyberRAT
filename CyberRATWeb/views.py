import json

import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.generic import CreateView
from django.http import Http404

from CyberRATWeb.scrapers.scrappers import *
from CyberRATWeb.services.timeline_analyzer import TimeLineAnalysisResults
from CyberRATWeb.forms import SearchForm
from CyberRATWeb.models import Search
from CyberRATWeb.services.email_service import EmailService


class Entity():

    def __init__(self, name, breachNumber, breachedSites, facebook_data, time_line_data, threatLevel, profilePhoto,
                 twitter_data, twitter_posts):
        self.name = name
        self.breachNumber = breachNumber
        self.breachedSites = breachedSites
        self.facebook_data = facebook_data
        self.time_line_data = time_line_data
        self.threatLevel = threatLevel
        self.profilePhoto = profilePhoto
        self.twitter_data = twitter_data
        self.twitter_posts = twitter_posts


class HomeView(CreateView):
    form_class = SearchForm
    model = Search
    redirect_field_name = 'results.html'


def results(request, uuid):
    try:
        search = get_object_or_404(Search, uuid=uuid)
    except ValueError:
        raise Http404

    entity = get_search_result_entity(search)

    return render(request, 'CyberRATWeb/results.html', {'entity': entity, 'uuid': uuid})


def generateEmail(request, uuid, entity):
    try:
        search = get_object_or_404(Search, uuid=uuid)
    except ValueError:
        raise Http404

    email = search.email
    entity = get_search_result_entity(search)

    site_html = render_to_string('CyberRATWeb/results.html', {'entity': entity, 'uuid': uuid})

    email_service = EmailService.getInstance()
    email_service.send_results(request, uuid, email, site_html)

    return render(request, 'CyberRATWeb/results.html', {'entity': entity, 'uuid': uuid})


def get_search_result_entity(search):
    name = search.name
    email = search.email
    profile_link = search.facebook_link
    instagram_link = search.instagram_link
    twitter_link = search.twitter_link

    entity = Entity('', '', '', '', '', '', '', '', '')

    entity.name = name
    entity.breachNumber = checkHIBP(email)
    entity.breachedSites = checkHIBP(email)
    entity.facebook_data = Facebook(profile_link)

    entity.threatLevel = (len(entity.facebook_data) - 1) * 3
    if (entity.threatLevel > 50):
        entity.threatLevel = 50

    if (instagram_link != ""):
        time_line_data = get_instagram_posts(instagram_link)
        entity.time_line_data = TimeLineAnalysisResults(time_line_data)
    else:
        entity.time_line_data = None

    entity.profilePhoto = ProfilePhoto(profile_link)
    entity.twitter_posts = []
    if (twitter_link != ""):
        twitter_results = TwitterData(twitter_link)
        entity.twitter_data = twitter_results[0]
        entity.twitter_posts = twitter_results[1]
    else:
        entity.twitter_data = None

    """if (len(entity.breachNumber) <= 0):
        entity.threatLevel = '0%'
    elif (len(entity.breachNumber) < 3):
        entity.threatLevel = '25%'
    elif (len(entity.breachNumber) < 5):
        entity.threatLevel = '50%'
    else:
        entity.threatLevel = '100%'"""
    threat = len(entity.breachNumber) * 8
    if (threat > 50):
        threat = 50
    entity.threatLevel = entity.threatLevel + threat
    if (entity.threatLevel > 85):
        entity.threatLevel = 80

    return entity