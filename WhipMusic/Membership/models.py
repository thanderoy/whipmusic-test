from django.db import models
from django.conf import settings

# import datetime
# from datetime import date

# Create your models here.
MEMBERSHIP_TYPES = (
    ('Premium', 'Premium'),
    ('Free', 'Free')
)



class Membership(models.Model):
    slug = models.SlugField(null=True, blank=True)
    price = models.FloatField(default=0)
    membership_type = models.CharField(choices=MEMBERSHIP_TYPES, default='Free', max_length=30)

    def __str__(self):
        return self.membership_type

class UserMembership(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user_membership', on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, related_name='user_membership', null=True, on_delete=models.SET_NULL)
    # paid_until = models.DateField( null=True, blank=True)

    # def set_paid_until(self, date_or_timestamp):
    #     if isinstance(date_or_timestamp, int):
    #         paid_until = date.fromtimestamp(date_or_timestamp)
    #     elif isinstance(date_or_timestamp, str):
    #         paid_until = date.fromtimestamp(int(date_or_timestamp))
    #     else:
    #         paid_until = date_or_timestamp

    #     self.paid_until = paid_until
    #     self.save()

    # def has_paid(self, current_date = datetime.date.today()):

    #     if self.paid_until is None:
    #         return False
        
    #     return current_date < self.paid_until

    # def is_premium(self):

    #     if self.subscription_type != 'Premium':
    #         return 

    def __str__(self):
        return self.user.username

class Subscription(models.Model):
    user_membership = models.ForeignKey(UserMembership, related_name='subscription', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_membership.user.username
    