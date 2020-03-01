from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.urls import reverse

# Create your models here.


class User(AbstractUser):
    is_person = models.BooleanField(default=False)
    is_organisation = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('my_connections:index')


class Organisation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    company_site = models.URLField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("index", kwargs={"pk": self.pk})
    

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    relationships = models.ManyToManyField(Organisation, related_name='accounts')

    def get_absolute_url(self):
        return reverse("index", kwargs={"pk": self.pk})

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

class Entry(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='entries', default=None)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='entries', default=None)
    date_confirmed = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        if self.organisation:
            return '{} entered {}'.format(self.person.user.username, self.organisation.name)
        else:
            return '{} requesting entry'.format(self.person.user.username)

class AccessCode(models.Model):
    entry = models.OneToOneField(Entry, on_delete=models.CASCADE, related_name='access_code')
    code =  models.UUIDField(default=uuid.uuid4().hex[:6], editable=False, unique=True) # Create 6 digit code
    date_attempted = models.DateTimeField(blank=True, null=True, default=timezone.now)

