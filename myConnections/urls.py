from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from myConnections import views


app_name='my_connections'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/person', views.PersonSignUpView.as_view(), name='person_signup'),
    path('signup/organisation', views.OrganisationSignUpView.as_view(), name='organisation_signup'),
    path('login', LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True), name='login'),
    path('person/<int:pk>/', views.PersonDetailView.as_view(), name='person'),
    path('organisation/<int:pk>/', views.OrganisationDetailView.as_view(), name='organisation'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout_message/', views.logout_message, name='logout_message'),
    path('connections', views.connections, name='connections'),
    path('register_prompt/', views.register_prompt, name='register_prompt'),
]

