from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify

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

class Conference(models.Model):
    shortname = models.CharField(
        max_length=15)
    longname = models.CharField(
        max_length=50)
    open_signup = models.BooleanField()
    tech_contact = models.EmailField()
    admin_contact = models.EmailField()
    complete = models.BooleanField()

    def __str__(self):
        return self.shortname
    

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
    conference = models.ForeignKey(
        Conference,
        on_delete=models.PROTECT)

    def __str__(self):
        return self.shortname
    
    def get_absolute_url(self):
        return reverse('org-detail', args=[str(self.shortname)])

class Task(models.Model):
    shortname = models.CharField(
        max_length=15)
    longname = models.CharField(
        max_length=50)
    conference = models.ForeignKey(
        Conference,
        on_delete=models.PROTECT)
    required = models.BooleanField()
    task_open = models.BooleanField()
    has_file = models.BooleanField()

    def __str__(self):
        return "/".join([self.conference.shortname, self.shortname])

class SubmitForm(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.PROTECT)
    header_template = models.CharField(
        max_length=30)

    def __str__(self):
        return self.task.shortname

class SubmitFormField(models.Model):
    class QuestionType(models.IntegerChoices):
        TEXT = 1
        NUMBER = 2
        RADIO = 3
        CHECKBOX = 4
        EMAIL = 5
        COMMENT = 6
        RUNTAG = 7

    submit_form = models.ForeignKey(
        SubmitForm,
        on_delete=models.PROTECT)
    question = models.CharField(
        max_length=100)
    choices = models.CharField(
        max_length=100,
        blank=True)
    meta_key = models.CharField(
        max_length=15)
    sequence = models.IntegerField()
    question_type = models.IntegerField(
        choices=QuestionType.choices,
        default=QuestionType.TEXT)
    def __str__(self):
        return self.meta_key
    
    class Meta:
        ordering = ['sequence']

class Submission(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.PROTECT)
    org = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT)
    date = models.DateField(
        auto_now_add=True)

class SubmitMeta(models.Model):
    submission = models.ForeignKey(
        Submission,
        on_delete=models.PROTECT)
    key = models.CharField(max_length=15)
    value = models.CharField(max_length=250)
