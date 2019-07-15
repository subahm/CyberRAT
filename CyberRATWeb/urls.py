from django.conf.urls import url

from CyberRATWeb.services.email_service import EmailService
from . import views

urlpatterns = [
    url('^$', views.HomeView.as_view(), name='search_form'),
    url('^results/(?P<uuid>.+)$', views.results, name='results'),
    url('^results/email/(?P<uuid>.+)/(?P<entity>.+)/$', views.generateEmail, name='generate_email')
]

# instantiate email service singleton
email_service = EmailService()