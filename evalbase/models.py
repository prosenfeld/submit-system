from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT)
    street_address = models.CharField(
        max_length=150)
    city_state = models.CharField(
        max_length=150)
    postal_code = models.CharField(
        max_length=10)
    country = models.CharField(
        max_length=50)
    created_at = models.DateField(
        auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return reverse('profile')
    
class Organization(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='org_owner_of')
    shortname = models.CharField(
        max_length=15,
        verbose_name='Short name',
        help_text='A short (max 15 chars) acronym or abbreviation.')
    longname = models.CharField(
        max_length=50,
        verbose_name='Long name',
        help_text='The full name of your organization.')
    contact_person = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='org_contact_for')
    passphrase = models.CharField(
        max_length=20,
        editable=False)
    members = models.ManyToManyField(
        User,
        related_name='member_of')

    def __str__(self):
        return self.shortname
    
    def get_absolute_url(self):
        return reverse('org-detail', args=[str(self.shortname)])

