from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from myConnections import views


app_name='my_connections'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/student', views.PersonSignUpView.as_view(), name='student_signup'),
    path('signup/organisation', views.OrganisationSignUpView.as_view(), name='organisation_signup'),
    path('login', LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout_message/', views.logout_message, name='logout_message'),
]