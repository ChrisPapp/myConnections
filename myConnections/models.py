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
    logo = models.ImageField(upload_to='profiles')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("index", kwargs={"pk": self.pk})
    

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    relationships = models.ManyToManyField(Organisation, related_name='accounts')
    profile_pic = models.ImageField(upload_to='profiles')
    birth_date = models.DateField()
    city = models.CharField(max_length=128)

    def get_absolute_url(self):
        return reverse("index", kwargs={"pk": self.pk})
    
    def get_full_name(self):
        return self.user.first_name + ' ' + self.user.last_name

    def __str__(self):
        return self.get_full_name()

class Entry(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='entries', default=None)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='entries', default=None)
    date_confirmed = models.DateTimeField(blank=True, null=True, default=timezone.now)

    def __str__(self):
        if self.organisation:
            return '{} entered {}'.format(self.person.user.username, self.organisation.name)
        else:
            return '{} requesting entry'.format(self.person.user.username)

class Invite(models.Model):
    by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invites')
    code =  models.UUIDField(default=uuid.uuid4, editable=False, unique=True) # Create 6 digit code
    date_attempted = models.DateTimeField(blank=True, null=True, default=timezone.now)

    def is_expired(self):
        now = timezone.now()
        diff = now - self.date_attempted
        # Codes created by person expire in 5 minutes (300 seconds)
        if self.by.is_person:
            return diff.seconds > 300
        # Codes created by organisations expire in 1 day
        else:
            return diff.days >= 1
