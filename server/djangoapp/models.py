from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return "Name: " + self.name


class CarModel(models.Model):
    SEDAN = 'SEDAN'
    SUV = 'SUV'
    WAGON = 'WAGON'

    CAR_TYPE_CHOICES = (
        (SEDAN, 'SEDAN'),
        (SUV, 'SUV'),
        (WAGON, 'WAGON')
    )

    carmakes = models.ManyToManyField(CarMake)
    name = models.CharField(max_length=100)
    dealer_id = models.IntegerField()
    cartype = models.CharField(max_length=20,choices=CAR_TYPE_CHOICES)
    year = models.DateField()

    def __str__(self):
        return "Name: " + self.name

class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name + "\n" + "Dealer ID: " + str(self.id) + "\n" + "Dealer address: " + self.address

class DealerReview:

    sentiment = ""

    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.id = id

    def __str__(self):
        return "Dealer name: " + self.name


# <HINT> Create a plain Python class `DealerReview` to hold review data
