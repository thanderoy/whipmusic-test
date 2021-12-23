### import datetime
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class CreateUserForm(UserCreationForm):
    free_membership, created = Membership.objects.get_or_create(slug='free_membership', price=0 ,membership_type='Free')
    class Meta(UserCreationForm.Meta):
       model = User
       fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self):
      user = super().save(commit=False)
      user.save()
      
      user_membership = UserMembership.objects.create(user=user, membership=self.free_membership)
      user_membership.save()
      
      user_subscription = Subscription()
      user_subscription.user_membership = user_membership
      user_subscription.save()
      return user

class PaymentForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(required=False)
    phone = forms.CharField( max_length=15, required=False)
    # amount = forms.FloatField()