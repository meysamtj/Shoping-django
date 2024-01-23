from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('password/', views.Password.as_view(), name="password"),
]

