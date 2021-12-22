from logging import currentframe
from django.test import TestCase
from .models import User
 
from datetime import date, datetime, timedelta
# Create your tests here.

class PaymentUnitTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.save()

    def test_has_paid(self):
        self.assertFalse(self.user.has_paid(), "Initial user should have empty paid_until attr")

    def test_diff_date_values(self):
        current_date = date(2020,1,4) # 4th Jan 2020
        _30days = timedelta(days=30)

        self.user.set_paid_until(current_date + _30days)
        self.assertTrue(self.user.has_paid(current_date=current_date))
        
        self.user.set_paid_until(current_date - _30days)
        self.assertFalse(self.user.has_paid(current_date=current_date))

    def test_diff_input_types(self):
        current_date = date(2020,4,1) # 4th Jan 2020
        _30days = timedelta(days=30)

        ts_in_future = datetime.timestamp(current_date + _30days)

        self.user.set_paid_until(int(ts_in_future))
        self.user.set_paid_until('1212344545')

