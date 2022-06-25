from django.contrib import admin
from .models import CarModel, CarMake


# Register your models here.

# class CarModelInline(admin.StackedInline):
#     model = CarModel

class CarModelInline(admin.StackedInline):
     model = CarModel.carmakes.through


# class CarModelAdmin(admin.ModelAdmin):
#     # placeholder


class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]


# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel)
