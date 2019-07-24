from django.db import models
from django.urls import reverse
import uuid

class Search(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    facebook_link = models.CharField(max_length=200)
    linkedin_link = models.CharField(max_length=200, default='')
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def get_absolute_url(self):
        return reverse("results", kwargs={'uuid':self.uuid})

    def __str__(self):
        return self.name + self.email + self.facebook_link + self.linkedin_link + self.uuid
