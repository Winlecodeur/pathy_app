from django.urls import path
from account import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('reset_password/', views.request_reset_password, name="request_reset_password"),
    path('verify_reset_code/', views.verify_reset_code, name="verify_reset_code"),
    path('reset_code/', views.reset_password, name="reset_password"),
]