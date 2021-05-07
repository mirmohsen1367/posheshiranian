from django.urls import path
from user.views import user
from user.views import login

urlpatterns = [
    path('evaluation/', user.EvaluationExpert.as_view()),
    path('insurser/', user.InsurserView.as_view()),
    path('login/', login.UserLogIn.as_view()),
    path('companies/', user.CompaniView.as_view()),
    path('companis/user', user. CompanyUSerView.as_view()),
    path('permission/', user.PermissionView.as_view()),
    path('permission/user/',user.UserPermissionView.as_view())
    ]