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


    # <HINT> Create a plain Python class `CarDealer` to hold dealer data

    # <HINT> Create a plain Python class `DealerReview` to hold review data
