from django.db import models

# Create your models here.
class Submission(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    information = models.OneToOneField('Information', on_delete=models.CASCADE)
    need_flight = models.BooleanField()
    flight = models.OneToOneField('Flights', on_delete=models.CASCADE, blank=True, null=True)
    gh_name = models.CharField(max_length=100)
    question1 = models.TextField()
    question2 = models.TextField()
    question3 = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    submitted = models.BooleanField(default=False)

class Information(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    birth_date = models.DateField()
    address_street1 = models.CharField(max_length=300)
    address_street2 = models.CharField(max_length=200, blank=True, null=True)
    address_city = models.CharField(max_length=100)
    address_postal_code = models.CharField(max_length=10)
    address_state = models.CharField(max_length=100)
    address_country = models.CharField(max_length=100)
    address_geo = models.JSONField()
    distance = models.DecimalField(max_digits=10, decimal_places=2)

class Flights(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    departure_airport = models.CharField(max_length=4)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    flights = models.JSONField(blank=True, null=True)