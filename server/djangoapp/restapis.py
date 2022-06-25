import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, CategoriesOptions, ClassificationsOptions, SentimentOptions


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))

    try:
        # Basic authentication GET
        response = requests.get(url,
                                headers={'Content-Type': 'application/json'},
                                params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url,
                                 json=json_payload
                                 )
    except:
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)

    return json_data



def get_dealers_from_cf(**kwargs):
    results = []
    # Call get_request with a URL parameter
    url = "https://c3e33bcc.us-south.apigw.appdomain.cloud/api/dealership"
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["entries"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"],
                zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_reviews_from_cf(**kwargs):
    results = []
    # Call get_request with a URL parameter
    url = "https://c3e33bcc.us-south.apigw.appdomain.cloud/api/review"
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["entries"]
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(
                dealership=review_doc["dealership"],
                name=review_doc["name"],
                purchase=review_doc["purchase"],
                review=review_doc["review"],
                purchase_date=review_doc["purchase_date"],
                car_make=review_doc["car_make"],
                car_model=review_doc["car_model"],
                car_year=review_doc["car_year"],
                id=review_doc["id"]
            )
            results.append(review_obj)

    return results

def analyze_review_sentiments(dealerreview):
    try:
        apikey = "T3x3Dfnmio1VBl5pKYMmwUjiXiAkKfBtTrKlzfywvDys"
        url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/7881185c-2632-4842-a05f-69d1283507d0"

        authenticator = IAMAuthenticator(apikey)
        natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2022-04-07',
            authenticator=authenticator
        )

        natural_language_understanding.set_service_url(url)

        response = natural_language_understanding.analyze(
            text=dealerreview,
            features=Features(sentiment=SentimentOptions())).get_result()

        print(response)

        sentiment = response['sentiment']['document']['label']

        return sentiment
    except:
        return "insufficient Text for sentiment"


def get_dealer_reviews_from_cf(dealer_id, **kwargs):
    all_reviews = get_reviews_from_cf(**kwargs)
    list_of_reviews_for_dealer = list()
    for review_obj in all_reviews:
        if review_obj.dealership == dealer_id:
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            list_of_reviews_for_dealer.append(review_obj)

    return list_of_reviews_for_dealer

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



