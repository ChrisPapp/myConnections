from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
from myConnections.models import User
from myConnections.forms import PersonSignUpForm, OrganisationSignUpForm

# Create your views here.

def index(request):
    return render(request, 'index.html')

class PersonSignUpView(CreateView):
    model = User
    form_class = PersonSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_type"] = 'Person'
        return context

class OrganisationSignUpView(CreateView):
    model = User
    form_class = OrganisationSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_type"] = 'Organisation'
        return context
    
def logout_message(request):
    return render(request, 'registration/logout_message.html')