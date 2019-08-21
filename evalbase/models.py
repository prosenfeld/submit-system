from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.urls import reverse

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    street_address = models.CharField(max_length=150)
    city_state = models.CharField(max_length=150)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('profile')
    
