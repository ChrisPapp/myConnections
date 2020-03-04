from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.views.generic import CreateView, DetailView, View, TemplateView, FormView
from myConnections.models import User,Person,Organisation, Invite, Entry
from myConnections.forms import PersonSignUpForm, OrganisationSignUpForm, EnterCodeForm
from myConnections.decorators import person_required

# Create your views here.

def index(request):
    if (not request.user.is_authenticated) :
        return redirect(reverse('my_connections:register_prompt'))
    elif (request.user.is_person):
        return redirect(reverse('my_connections:person', kwargs= {'pk': request.user.person.pk}))
    elif (request.user.is_organisation):
        return redirect(reverse('my_connections:organisation', kwargs= {'pk': request.user.organisation.pk}))
    else:
        return redirect('my_connections:logout')


def register_prompt(request):
    return render(request, 'register_prompt.html')

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


@login_required
@person_required
def connections(request):
    return render(request, 'connections.html')


class InviteCreateView(LoginRequiredMixin, View):
    model = Invite
    login_url = reverse_lazy('my_connections:login')
    def get(self, request, *args, **kwargs):
        invite = Invite(by=request.user)
        self.uuid = invite.code
        invite.save()
        return redirect(reverse_lazy('my_connections:invite_success', kwargs={'uuid': self.uuid}))
    

class InviteSuccessView(LoginRequiredMixin, DetailView):
    template_name = 'myConnections/invite_success.html'
    login_url = reverse_lazy('my_connections:login')

    def get_object(self):
        invite = get_object_or_404(Invite, code=self.kwargs['uuid'])
        if invite and invite.by != self.request.user:
            raise Http404()
        return invite

class EnterCodeView(LoginRequiredMixin, FormView):
    template_name ='myConnections/enter_code.html'
    form_class = EnterCodeForm
    success_url = reverse_lazy('my_connections:code_success')

    def form_valid(self, form):
        code = form.cleaned_data.get('code')
        try:
            invite = Invite.objects.get(code=code)
            by_user = invite.by

            # Invides should be sent between person and organisations
            if (self.request.user.is_person and by_user.is_person) or (self.request.user.is_organisation and by_user.is_organisation):
                raise Http404()
            if (invite.is_expired()):
                # We are done with this invite
                invite.delete()
                return redirect(reverse_lazy('my_connections:code_expired'))
            # Organisation invites person to create connection
            if (by_user.is_organisation):
                by_user.organisation.accounts.add(self.request.user.person)
            else: # Person wants to be identified
                if (by_user.person in self.request.user.organisation.accounts.all()):
                    Entry.objects.create(person=by_user.person, organisation=self.request.user.organisation)
                else:
                    raise Http404()
            # We are done with this invite
            invite.delete()
        except Invite.DoesNotExist:
            raise Http404()
        return super().form_valid(form)

class SuccessCodeView(LoginRequiredMixin, TemplateView):
    template_name='myConnections/code_success.html'

class ExpiredCodeView(LoginRequiredMixin, TemplateView):
    template_name='myConnections/code_expired.html'
