from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import CreateView, DetailView
from myConnections.models import User,Person,Organisation
from myConnections.forms import PersonSignUpForm, OrganisationSignUpForm

# Create your views here.

def index(request):
    if (not request.user.is_authenticated) :
        return render(request, 'index.html')
    elif (request.user.is_person):
        return redirect(reverse('my_connections:person', kwargs= {'pk': request.user.person.pk}))
    elif (request.user.is_organisation):
        return redirect(reverse('my_connections:organisation', kwargs= {'pk': request.user.organisation.pk}))

class PersonSignUpView(CreateView):
    model = User
    form_class = PersonSignUpForm
    template_name = 'registration/signup_form.html'
    success_url = reverse_lazy('my_connections:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_type"] = 'Person'
        return context

class OrganisationSignUpView(CreateView):
    model = User
    form_class = OrganisationSignUpForm
    template_name = 'registration/signup_form.html'
    success_url = reverse_lazy('my_connections:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_type"] = 'Organisation'
        return context
    
def logout_message(request):
    return render(request, 'registration/logout_message.html')

class PersonDetailView(UserPassesTestMixin, DetailView):
    model = Person
    login_url = reverse_lazy('my_connections:login')

    def test_func(self):
        # if not logged, go to login page
        if not self.request.user:
            return False

        # If logged in but has no access, show "Forbidden" page
        self.raise_exception = True

        # A person can view only their own profile
        if self.request.user.is_person:
            return self.request.user.person.pk == self.kwargs['pk']
        
        # An organisation can only see the profiles of their accounts
        if self.request.user.is_organisation:
            return self.request.user.organisation.accounts.filter(pk=self.kwargs['pk'])
class OrganisationDetailView(UserPassesTestMixin, DetailView):
    model = Organisation
    login_url = reverse_lazy('my_connections:login')

    def test_func(self):
        # if not logged, go to login page
        if not self.request.user:
            return False

        # If logged in but has no access, show "Forbidden" page
        self.raise_exception = True

        # A person can view only their related organisations
        if self.request.user.is_person:
            return self.request.user.person.relationships.filter(pk=self.kwargs['pk'])
        
        # An organisation can only see their own profile
        if self.request.user.is_organisation:
            return self.request.user.organisation.pk == self.kwargs['pk']
