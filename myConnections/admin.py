from django.contrib import admin
from .models import Person, Organisation, Entry, User, Invite

# Register your models here.

admin.site.register(User)
admin.site.register(Person)
admin.site.register(Organisation)
admin.site.register(Entry)
admin.site.register(Invite)
