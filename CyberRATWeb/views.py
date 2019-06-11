from django.http import HttpResponse
from django.shortcuts import render
import requests
import json
from bs4 import BeautifulSoup

from CyberRATWeb.forms import EmailForm

class Entity():

    def __init__(self, name, breachNumber, breachedSites, facebook_data, threatLevel):
        self.name=name
        self.breachNumber = breachNumber
        self.breachedSites = breachedSites
        self.facebook_data = facebook_data
        self.threatLevel = threatLevel

def home(request):
    form = EmailForm()
    return render(request, 'home.html', {'form': form})

def results(request):

    if request.method == "POST":
        dataForm = EmailForm(request.POST)
        if dataForm.is_valid():
            name = dataForm.cleaned_data['name']
            email = dataForm.cleaned_data['email']
            profile_link=dataForm.cleaned_data['facebook_link']
        else:
            dataForm = EmailForm()

    def checkHIBP(email):
        result= []
        url = 'https://haveibeenpwned.com/api/v2/breachedaccount/'+email

        resp = requests.get(url=url)
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



    entity = Entity('', '', '','','')


    entity.name = name
    entity.breachNumber = checkHIBP(email)
    entity.breachedSites = checkHIBP(email)
    entity.facebook_data = Facebook(profile_link)

    if (len(entity.breachNumber) <= 0):
        entity.threatLevel = '0%'
    elif (len(entity.breachNumber) < 3):
        entity.threatLevel = '25%'
    elif (len(entity.breachNumber) < 5):
        entity.threatLevel = '50%'
    else:
        entity.threatLevel = '100%'

    return render(request,'results.html', {'entity':entity})
