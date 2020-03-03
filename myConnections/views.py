from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
from django.shortcuts import redirect
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

class PersonDetailView(DetailView):
    model = Person

class OrganisationDetailView(DetailView):
    model = Organisation
