import uuid
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from .models import *

class SignUp(generic.edit.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'evalbase/signup.html'

class EvalBaseLoginReqdMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')
    
class ProfileDetail(EvalBaseLoginReqdMixin, generic.detail.DetailView):
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

class ProfileCreate(EvalBaseLoginReqdMixin, generic.edit.CreateView):
    model = UserProfile
    fields = ['street_address', 'city_state', 'country', 'postal_code']
    template_name = 'evalbase/profile_form.html'
    
    # The profile is always for the current user.
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProfileEdit(EvalBaseLoginReqdMixin, generic.edit.UpdateView):
    model = UserProfile
    fields = ['street_address', 'city_state', 'country', 'postal_code']
    template_name = 'evalbase/profile_form.html'

    # You can only see your own profile.
    def get_object(self):
        try:
            return UserProfile.objects.get(user=self.request.user)
        except:
            return None

class OrganizationList(EvalBaseLoginReqdMixin, generic.ListView):
    model = Organization
    template_name = 'evalbase/my-orgs.html'

    def get_queryset(self):
        # return orgs I own or I am a member of.
        rs = Organization.objects.filter(members__pk=self.request.user.pk)
        rs = rs.union(Organization.objects.filter(owner=self.request.user))
        return rs

class OrganizationDetail(EvalBaseLoginReqdMixin, generic.DetailView):
    model = Organization
    template_name = 'evalbase/org-detail.html'
    slug_field = 'shortname'
    slub_url_kwarg = 'shortname'

    def get_object(self):
        try:
            org = Organization.objects.get(shortname=self.kwargs['shortname'])
            if org.members.filter(pk=self.request.user.pk).exists():
                return org
            else:
                raise PermissionDenied()
        except:
            raise PermissionDenied()

class OrganizationCreate(EvalBaseLoginReqdMixin, generic.edit.CreateView):
    model = Organization
    template_name = 'evalbase/org-create.html'
    fields = ['shortname', 'longname']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.conf = Conference.objects.get(shortname=self.kwargs['conf'])
        context['conf'] = self.conf
        return context
    
    def form_valid(self, form):
        form.instance.contact_person = self.request.user
        form.instance.owner = self.request.user
        confname = self.kwargs['conf']
        form.instance.conference = Conference.objects.get(shortname=confname)
        form.instance.passphrase = uuid.uuid4()
        return super().form_valid(form)
            
    
class OrganizationJoin(EvalBaseLoginReqdMixin, generic.TemplateView):
    template_name='evalbase/join.html'

    def get_context_data(self, **kwargs):
        org = Organization.objects.get(passphrase=self.kwargs['key'])
        context = super().get_context_data(**kwargs)
        context['org'] = org
        context['key'] = self.kwargs['key']
        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user
        org = Organization.objects.get(passphrase=self.kwargs['key'])
        org.members.add(user)
        return HttpResponseRedirect(reverse_lazy('home'))
        
class OrganizationEdit(EvalBaseLoginReqdMixin, generic.TemplateView):
    pass

        
class HomeView(generic.base.TemplateView):
    template_name = 'evalbase/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['open_evals'] = Conference.objects.filter(open_signup=True)
        context['my_orgs'] = Organization.objects.filter(members__pk=self.request.user.pk).filter(conference__complete=False)
        return context

class ConferenceTasks(EvalBaseLoginReqdMixin, generic.ListView):
    model = Task
    template_name = 'evalbase/tasks.html'
    
    def get_queryset(self):
        return Task.objects.filter(conference__shortname=self.kwargs['conf']).filter(task_open=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conf'] = Conference.objects.get(shortname=self.kwargs['conf'])
        return context

class SubmitTask(EvalBaseLoginReqdMixin, generic.TemplateView):
    template_name = 'evalbase/submit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = Task.objects.get(shortname=kwargs['task'], conference__shortname=kwargs['conf'])
        submitform = SubmitForm.objects.get(task=task)
        fields = SubmitFormField.objects.filter(submit_form=submitform)
        choices = {}

        for field in fields:
            if field.question_type == SubmitFormField.QuestionType.RADIO or field.question_type == SubmitFormField.QuestionType.CHECKBOX:
                choices[field.meta_key] = field.choices.split(',')

        context['orgs'] = Organization.objects.filter(members__pk=self.request.user.pk).filter(conference__shortname=kwargs['conf'])
        context['conf'] = Conference.objects.get(shortname=kwargs['conf'])
        context['task'] = task
        context['form'] = submitform
        context['fields'] = fields
        context['choices'] = choices
        return context

    def post(self, request, *args, **kwargs):
        form = request.POST
        return render(request, 'evalbase/foo.html', context={'form': form})
