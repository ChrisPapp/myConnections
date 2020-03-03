from django import forms
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from .models import User, Person, Organisation
from django.db import transaction

class PersonSignUpForm(UserCreationForm):

    profile_image = forms.ImageField()
    birth_date = forms.DateField()
    city = forms.CharField(max_length=128)

    class Meta(UserCreationForm.Meta):
        model=User
        fields=('username', 'password1', 'password2', 'first_name', 'last_name')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_person = True
        user.save()
        person = Person.objects.create(user=user, profile_pic=self.cleaned_data.get('profile_image'), birth_date=self.cleaned_data.get('birth_date'), city=self.cleaned_data.get('city'))
        return user

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('my_connections:index')

class OrganisationSignUpForm(UserCreationForm):

    name = forms.CharField(max_length=128, required=True)
    company_site = forms.URLField(required=False)
    logo = forms.ImageField()

    class Meta(UserCreationForm.Meta):
        model=User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_organisation = True
        user.save()
        user.refresh_from_db()
        organisation = Organisation.objects.create(user=user, name=self.cleaned_data.get('name'), company_site=self.cleaned_data.get('company_site'), logo=self.cleaned_data.get('logo'))
        return user

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('my_connections:index')