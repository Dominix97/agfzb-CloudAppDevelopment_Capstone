from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_reviews_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        # Get dealers from the URL
        dealerships = get_dealers_from_cf()
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealerships)

def get_reviews(request):
    if request.method == "GET":
        # Get dealers from the URL
        reviews = get_reviews_from_cf()
        # Return a list of dealer short name
        return HttpResponse(reviews)

def get_dealer_details(request, dealer_id):
    context = {}
    dealer_reviews = get_dealer_reviews_from_cf(dealer_id)
    reviews_output = ' '.join([review_obj.review for review_obj in dealer_reviews]).join([review_obj.sentiment for review_obj in dealer_reviews])
    return HttpResponse(reviews_output)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    # user_exist = False
    # try:
    #     username = request.POST['username']
    #     User.objects.get(username=username)
    #     user_exist = True
    # except:
    #     return "User not logged in"
    #
    # if user_exist:

    review = dict()
    review["id"] = 101
    review["name"] = "Test Name"
    review["purchase"] = True
    review["purchase_date"] = "2000-01-01"
    review["car_make"] = "Honda"
    review["car_model"] = "Civic"
    review["car_year"] = datetime.utcnow().isoformat()
    review["dealership"] = dealer_id
    review["review"] = "This is a great car dealer, awesome work and great customer satisfaction"

    json_payload = dict()
    json_payload["review"] = review

    url = "https://c3e33bcc.us-south.apigw.appdomain.cloud/api/review"

    result = post_request(url, json_payload)

    return HttpResponse(result)




