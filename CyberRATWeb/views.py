from django.http import HttpResponse
from django.shortcuts import render
import requests

from CyberRATWeb.forms import EmailForm

class Entity():
    def __init__(self, name, breachNumber, breachedSites, threatLevel):
        self.name=name
        self.breachNumber = breachNumber
        self.breachedSites = breachedSites
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

    entity = Entity('', '', '', '')

    entity.name = name
    entity.breachNumber = checkHIBP(email)
    entity.breachedSites = checkHIBP(email)

    if (len(entity.breachNumber) <= 0):
        entity.threatLevel = '0%'
    elif (len(entity.breachNumber) < 3):
        entity.threatLevel = '25%'
    elif (len(entity.breachNumber) < 5):
        entity.threatLevel = '50%'
    else:
        entity.threatLevel = '100%'

    return render(request,'results.html', {'entity':entity})
