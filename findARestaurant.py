import json
import requests

import sys
import codecs
# sys.stdout = codecs.getwriter('utf8')(sys.stdout)
# sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = ''
foursquare_client_secret = ''
google_api_key = ''

def getGeocodeLocation(inputString):

	#Replace Spaces with '+' in URL
	locationString = inputString.replace(" ", "+")
	url = f'https://maps.googleapis.com/maps/api/geocode/json?address={locationString}&key={google_api_key}'
	result = requests.get(url).json()
	latitude = result['results'][0]['geometry']['location']['lat']
	longitude = result['results'][0]['geometry']['location']['lng']
	return (latitude,longitude)

#This function takes in a string representation of a location and cuisine type, geocodes the location, and then pass in the latitude and longitude coordinates to the Foursquare API
def findARestaurant(mealType, location):

	latitude, longitude = getGeocodeLocation(location)
	
	url = f'https://api.foursquare.com/v2/venues/search?client_id={foursquare_client_id}&client_secret={foursquare_client_secret}&v=20130815&ll={latitude},{longitude}&query={mealType}'
	
	result = requests.get(url).json()
	
	if result['response']['venues']:
		#Grab the first restaurant
		restaurant = result['response']['venues'][0]
		venue_id = restaurant['id'] 
		restaurant_name = restaurant['name']
		restaurant_address = restaurant['location']['formattedAddress']
		#Format the Restaurant Address into one string
		address = ""
		for i in restaurant_address:
			address += i + " "
		restaurant_address = address
		
		#Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
		url = f'https://api.foursquare.com/v2/venues/{venue_id}/photos?client_id={foursquare_client_id}&v=20150603&client_secret={foursquare_client_secret}'
		result = requests.get(url)
		result = requests.get(url).json()
		#Grab the first image
		#if no image available, insert default image url
		if result['response']['photos']['items']:
			firstpic = result['response']['photos']['items'][0]
			prefix = firstpic['prefix']
			suffix = firstpic['suffix']
			imageURL = prefix + "300x300" + suffix
		else:
			imageURL = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"

		restaurantInfo = {'name':restaurant_name, 'address':restaurant_address, 'image':imageURL}
		print(f"Restaurant Name: {restaurantInfo['name']}")
		print(f"Restaurant Address: {restaurantInfo['address']}")
		print(f"Image: {restaurantInfo['image']}")
		import subprocess
		subprocess.Popen(f'python insert_data.py "{restaurant_name}" "{restaurant_address}" "{imageURL}"')
		return restaurantInfo
	else:
		print(f"No Restaurants Found for {location}")
		return "No Restaurants Found"


if __name__ == '__main__':
	findARestaurant("Momos", "Dehradoon")

	# findARestaurant("Pizza", "Tokyo, Japan")
	# print()
	# findARestaurant("Tacos", "Jakarta, Indonesia")
	# print()
	# findARestaurant("Tapas", "Maputo, Mozambique")
	# print()
	# findARestaurant("Falafel", "Cairo, Egypt")
	# print()
	# findARestaurant("Spaghetti", "New Delhi, India")
	# print()
	# findARestaurant("Cappuccino", "Geneva, Switzerland") 
	# print()
	# findARestaurant("Sushi", "Los Angeles, California")
	# print()
	# findARestaurant("Steak", "La Paz, Bolivia")
	# print()
	# findARestaurant("Gyros", "Sydney Austrailia")