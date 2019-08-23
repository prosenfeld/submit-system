import uuid
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from .models import *

class SignUp(generic.edit.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('profile-create')
    template_name = 'signup.html'

class ProfileDetail(generic.detail.DetailView):
    model = UserProfile
    template_name = 'evalbase/profile_view.html'

    # You can only see your own profile.
    def get_object(self):
        try:
            return UserProfile.objects.get(user=self.request.user)
        except:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.request.user.id)
        return context

class ProfileCreate(generic.edit.CreateView):
    model = UserProfile
    fields = ['street_address', 'city_state', 'country', 'postal_code']
    template_name = 'evalbase/profile_form.html'
    
    # The profile is always for the current user.
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProfileEdit(generic.edit.UpdateView):
    model = UserProfile
    fields = ['street_address', 'city_state', 'country', 'postal_code']
    template_name = 'evalbase/profile_form.html'

    # You can only see your own profile.
    def get_object(self):
        try:
            return UserProfile.objects.get(user=self.request.user)
        except:
            return None

class OrganizationList(generic.ListView):
    model = Organization
    template_name = 'evalbase/my-orgs.html'

    def get_queryset(self):
        # return orgs I own or I am a member of.
        return Organization.objects \
                .filter(members=self.request.user) \
                .filter(owner=self.request.user)

class OrganizationDetail(generic.DetailView):
    model = Organization
    template_name = 'evalbase/org-detail.html'
    slug_field = 'shortname'
    slug_url_kwarg = 'shortname'

class OrganizationCreate(generic.edit.CreateView):
    model = Organization
    template_name = 'evalbase/org-create.html'
    fields = ['shortname', 'longname']

    def form_valid(self, form):
        form.instance.contact_person = self.request.user
        form.instance.owner = self.request.user
        form.instance.passphrase = uuid.uuid4()
        return super().form_valid(form)
            
    
class OrganizationJoin(generic.TemplateView):
    pass
class OrganizationEdit(generic.TemplateView):
    pass

        
class HomeView(generic.base.TemplateView):
    template_name = 'evalbase/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['open_evals'] = Conference.objects.filter(open_signup=True)
        context['my_evals'] = Conference.objects.filter(participants__members__id=self.request.user.id)
        return context

