from django.shortcuts import redirect, render
from django.views.generic import ListView
from django import forms
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from random import random
import math
import requests

from .forms import PaymentForm, CreateUserForm


from .models import UserMembership, Membership, Subscription
from decouple import config

# Create your views here.

@login_required(login_url='login')
def HomePage(request):
    user_details = UserMembership.objects.get(user=request.user)

    context = {
        'user_details': user_details
    }

    return render(request, 'index.html', context)

def RegisterPage(request):
    if request.user.is_authenticated:
        return redirect('index')

    else:

        if request.method == 'POST':
            form = CreateUserForm(request.POST)

            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Acount for ' + user + ' created successfully')

                return redirect ('login')


        else:
            form = CreateUserForm()

        context = {'form':form}
        return render(request, 'accounts/register.html', context)

def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Username or Password is incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)

def LogoutPage(request):
    logout(request)
    return redirect ('login')

@login_required(login_url='login')
def SubscribePage(request):

    if request.method == 'POST':
        form = PaymentForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            amount = '20'
    
            return redirect(str(process_payment(name, email, phone, amount)))
    else:
        form = PaymentForm()

    context = {'form': form}

    return render(request, 'subscribe.html', context)


def process_payment(name, email, phone, amount):
    auth_token = config('SEC_KEY', default='FLWSECK_TEST-cb3ba17d5ad7637d0f509ecf1b5fe820-X')
    hed = {'Authorization': 'Bearer ' + auth_token}
    data = {
        "tx_ref":''+str(math.floor(1000000 + random()*9000000)),
        "amount":amount,
        "currency":"USD",
        "redirect_url":"https://whipmusic-test.herokuapp.com/callback",
        "payment_options":"card",
        "meta":{
            "consumer_id":23,
            "consumer_mac":"92a3-912ba-1192a"
        },
        "customer":{
            "email":email,
            "phonenumber":phone,
            "name":name
        },
        "customizations":{
            "title":"WHIPMUSIC",
            "description":"Monthly Sub",
        }
        }
    url = ' https://api.flutterwave.com/v3/payments'
    response = requests.post(url, json=data, headers=hed)
    response=response.json()
    link=response['data']['link']

    return link

@require_http_methods(['GET', 'POST'])
def payment_response(request):
    status=request.GET.get('status', None)
    tx_ref=request.GET.get('tx_ref', None)
    print(status)
    print(tx_ref)

    if status == 'successful':
        user = request.user

        user_membership = UserMembership.objects.get(user=user)
        user_membership.membership = 'Premium'
        user_membership.save()
        
        user_subscription = Subscription()
        user_subscription.user_membership = user_membership
        user_subscription.save()
        
        return render(request, 'txn_success.html')
    else:
        return render(request, 'txn_fail.html')
    
