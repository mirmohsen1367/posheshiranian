from django.urls import path
from user.views import views
from  user.views import login

urlpatterns = [
    path('evaluation/', views.EvaluationExpert.as_view()),
    path('insurser/', views.InsurserView.as_view()),
    path('login/', login.UserLogIn.as_view()),
    ]