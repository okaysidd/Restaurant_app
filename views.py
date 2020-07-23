from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import sys
import codecs
from Data import Data
# sys.stdout = codecs.getwriter('utf8')(sys.stdout)
# sys.stderr = codecs.getwriter('utf8')(sys.stderr)


foursquare_client_id = ''
foursquare_client_secret = ''
google_api_key = ''

engine = create_engine('sqlite:///restaurants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
	data = Data()
	if request.method == "POST":
		location = request.args.get('location')
		mealType = request.args.get('mealType')
		print(f'location = {location}, meal = {mealType}')
		if location == None or mealType == None:
			return 'Incorrect arguments'
		else:
			return findARestaurant(str(mealType).lower(), str(location).lower())
	elif request.method == "GET":
			restaurants = data.get_all_restaurants()
			return restaurants
	else:
		return 'Incorrect method used'
	
@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
	data = Data()
	if request.method == "GET":
		restaurant = data.get_restaurant(id)
		if len(restaurant) == 0 or restaurant == '[]':
			return 'Restaurant Id not found'
		else:
			return restaurant

	elif request.method == "PUT":
		restaurant_name = request.args.get('name')
		restaurant_address = request.args.get('address')
		imageURL = request.args.get('image')
		# sending update request
		# TODO: check if the id exists
		data.update_data(id, restaurant_name=restaurant_name, restaurant_address=restaurant_address, imageURL=imageURL)
		# returning updated record
		return data.get_restaurant(id)

	elif request.method == "DELETE":
		if data.delete_data(id):
			return 'Deleted'
		else:
			return 'Some error occured, could not delete.'

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)


# query = 'SELECT * FROM restaurant'
# query = 'INSERT INTO restaurant (restaurant_name, restaurant_address, restaurant_image, id) VALUES ("Some restaurant", "Some address", "Image", "1")'
# print(query)
# result = session.execute(query)
# session.commit()
# print(result.fetchall())
