from amadeus import Client, ResponseError
from datetime import datetime
from fastapi.responses import JSONResponse
import os
import logging
import requests
from dotenv import load_dotenv

from fastapi import APIRouter, Depends, Response,Request, HTTPException
import typing as t
flight_router = r = APIRouter()


from app.db.schemas import FlightDataBase

load_dotenv()




BASE_URL = "https://api.amadeus.com/v1"
BASE_URL1 = "https://api.amadeus.com/v2"

def get_city_name(amadeus, airport_code: str):
    try:
        # Call the Amadeus API to get the location information for a given airport code
        response = amadeus.reference_data.locations.get(
            keyword=airport_code,
            subType='AIRPORT'
        ).data
        # print("Returned data:", response)

        # Extract the city name from the address field in the response
        if response and 'address' in response[0]:
            city_name = response[0]['address']['cityName']
            country_name = response[0]['address']['countryName']
            city_country = f"{city_name}, {country_name}"
            return city_country
        return airport_code  # Fallback if city name is not found
    except ResponseError as error:
        print(f"Error occurred: {error}")
        return airport_code  # Fallback in case of an error










def get_access_token():
    """Retrieve access token from Amadeus API."""
    client_id = 'GAiV9ZBkjGaaOFnBJoug5C8ommSSG92V'
    client_secret = 'HeB0zuLPQpfyyOld'
    token_url = f"{BASE_URL}/security/oauth2/token"

    response = requests.post(
        token_url,
        data={
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret
        }
    )

    if response.status_code == 200:
        token = response.json().get('access_token')
        print("Access token retrieved successfully.")
        return token
    else:
        print("Failed to retrieve access token: %s", response.text)
        return None

def validate_departure_code(departure):
    # Validate the departure code (should be 3 characters)
    if len(departure) != 3 or not departure.isalpha():
        print("Invalid departure code: %s. It must be 3 alphabetical characters.", departure)
        return False
    return True
















def flight_search(departure, budget=None):
    if not validate_departure_code(departure):
        return {"success": False, "message": "Invalid departure code."}

    token = get_access_token()
    if not token:
        return {"success": False, "message": "Unable to retrieve access token."}

    try:
        # Call the flight_destinations API to search for destinations from the origin
        destinations_url = f"{BASE_URL}/shopping/flight-destinations?origin={departure}"
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = requests.get(destinations_url, headers=headers)
        if response.status_code == 200:
           
            limited_responses = response.json().get('data', [])[0]
            print(limited_responses)
            flight_offers_url = f"{BASE_URL1}/shopping/flight-offers"
            params = {
                'originLocationCode': limited_responses['origin'],
                'destinationLocationCode': limited_responses['destination'],
                'departureDate': limited_responses['departureDate'],
                'returnDate': limited_responses['returnDate'],
                'adults': '1',
                'nonStop': 'false'
            }
            response = requests.get(flight_offers_url, headers=headers, params=params)
            airline_url = f"{BASE_URL}/reference-data/airlines"
            params = {
                'airlineCodes': response.json()['data'][0]['itineraries'][0]['segments'][0]['carrierCode']
            }
            response = requests.get(airline_url, headers=headers, params=params)
            print(response.json()['data'])
            import pdb
            pdb.set_trace()
            if not limited_responses:
                print("No destinations found for the departure code: %s", departure)
                return {"success": False, "message": "No destinations found."}

            print("Limited responses retrieved successfully.")
            return {"success": True, "data": limited_responses}
        else:
            print("API call failed: %s", response.text)
            return {
                "success": False,
                "message": f"Error occurred: {response.status_code}",
                "details": response.text
            }

    except Exception as e:
        print("An unexpected error occurred: %s", str(e))
        return {"success": False, "message": "An unexpected error occurred."}




















# def flight_search(departure,budget):
#     global custom_id
#     try:
#         # Initialize Amadeus client
#         amadeus = Client(
#             client_id='GAiV9ZBkjGaaOFnBJoug5C8ommSSG92V',
#             client_secret='HeB0zuLPQpfyyOld'
#         )

#         # Get the origin from the request, defaulting to 'LON'
       
#         # origin_location =  'LON'
#         formatted_response = []
#         # Call the flight_destinations API to search for destinations from the origin
#         response = amadeus.shopping.flight_destinations.get(origin=departure).data
#         limited_responses = response[:15]
        
#         for flight in limited_responses:
#                 # print("flight info",flight)
#                 departure_date = flight.get("departureDate")
#                 return_date = flight.get("returnDate")
            
#                 origin_code =  flight["origin"]
#                 destination_code = flight["destination"]
#                 origin = get_city_name(amadeus, origin_code)
#                 destination = get_city_name(amadeus, destination_code)
#                 fare_amount = float(flight["price"]["total"])
#                 if fare_amount <= float(budget):
#                     flight_data = {
#                         "fromCity": origin,  # Replace origin airport with city name
#                         "toCity": destination,  # Replace destination airport with city name
#                         "departureDate": departure_date,
#                         "returnDate": return_date,
#                         "fareAmount": fare_amount,
#                     }
#                     formatted_response.append(flight_data)
              
              

            
#         return JSONResponse(content=formatted_response)
#     except ResponseError as error:
#         # Handle error responses and raise an HTTP 500 exception
#         raise HTTPException(status_code=500, detail=str(error))



def travel_deals(request):
    try:
        import pdb
        pdb.set_trace()
        amadeus = Client(
            client_id='UAbyH4HXarnNVr07CCYtnNEZYuM4MFdr',
            client_secret='BD8cuKGP0bvJPZgi'
        )

        destination = request.GET.get('destination', 'LON')  # Example: London

        response = amadeus.shopping.hotel_offers_search.get(
            cityCode=destination,
            checkInDate="2024-09-06",
            checkOutDate="2024-09-08",
            adults=1,
        ).data

        return JSONResponse(response, safe=False)
    except ResponseError as error:
        return JSONResponse({'error': str(error)}, status=500)



@r.get(
    "/flight-search",
    
    response_model_exclude_none=True,
)
async def flights_search(
  departure: str, budget: str 
):
    """
    Get Nearby tickets
    """
    budget_value = 123  # Specify your budget value
#     result = flight_search("LON", budget_value)
    flights = flight_search('LON',budget_value)
    # This is necessary for react-admin to work
    
    return flights





































# Example usage
# if _name_ == "_main_":
#     budget_value = 123  # Specify your budget value
#     result = flight_search("LON", budget_value)
#     if result["success"]:
#         print("Flight search results:", result["data"])
#     else:
#         print("Error:", result["message"])



