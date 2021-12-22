from django.urls.conf import path

from . import views

urlpatterns = [
    path('', views.HomePage, name='index'),
    path('register/', views.RegisterPage, name='register'),
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.LogoutPage, name='logout'),
    path('buy-premium/', views.SubscribePage, name='subscribe'),
    path('callback/', views.payment_response, name='payment_response'),
    path('subscription/', views.SubscribePage, name='subscription'),


    
]