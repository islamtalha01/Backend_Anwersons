from amadeus import Client, ResponseError
from datetime import datetime
from fastapi.responses import JSONResponse

from fastapi import APIRouter, Depends, Response,Request, HTTPException
import typing as t
flight_router = r = APIRouter()


from app.db.schemas import FlightDataBase



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


def flight_search(departure,budget):
    global custom_id
    try:
        # Initialize Amadeus client
        amadeus = Client(
            client_id='UAbyH4HXarnNVr07CCYtnNEZYuM4MFdr',
            client_secret='BD8cuKGP0bvJPZgi'
        )

        # Get the origin from the request, defaulting to 'LON'
       
        # origin_location =  'LON'
        formatted_response = []
        # Call the flight_destinations API to search for destinations from the origin
        response = amadeus.shopping.flight_destinations.get(origin=departure).data
        limited_responses = response[:15]
        
        for flight in limited_responses:
                # print("flight info",flight)
                departure_date = flight.get("departureDate")
                return_date = flight.get("returnDate")
            
                origin_code =  flight["origin"]
                destination_code = flight["destination"]
                origin = get_city_name(amadeus, origin_code)
                destination = get_city_name(amadeus, destination_code)
                fare_amount = float(flight["price"]["total"])
                if fare_amount <= float(budget):
                    flight_data = {
                        "fromCity": origin,  # Replace origin airport with city name
                        "toCity": destination,  # Replace destination airport with city name
                        "departureDate": departure_date,
                        "returnDate": return_date,
                        "fareAmount": fare_amount,
                    }
                    formatted_response.append(flight_data)
              
              

            
        return JSONResponse(content=formatted_response)
    except ResponseError as error:
        # Handle error responses and raise an HTTP 500 exception
        raise HTTPException(status_code=500, detail=str(error))


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
    response_model=t.List[FlightDataBase],
    response_model_exclude_none=True,
)
async def flights_search(
  departure: str, budget: str 
):
    """
    Get Nearby tickets
    """
    flights = flight_search(departure,budget)
    # This is necessary for react-admin to work
    
    return flights