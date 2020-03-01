from django.urls import path
from myConnections import views

app_name='my_connections'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/student', views.PersonSignUpView.as_view(), name='student_signup'),
    path('signup/organisation', views.OrganisationSignUpView.as_view(), name='organisation_signup'),
]