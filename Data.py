from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import sys, json


class Data:
	def __init__(self):
		engine = create_engine('sqlite:///restaurants.db')
		Base.metadata.bind = engine
		DBSession = sessionmaker(bind=engine)
		self.session = DBSession()
		app = Flask(__name__)

	def get_restaurant(self, id):
		query = f'SELECT * FROM restaurant WHERE id={int(id)}'
		result = self.session.execute(query)
		# result = self.run_query(query)
		try:
			return json.dumps([dict(x) for x in result])
		except:
			return 'Restaurant Id not found'

	def get_all_restaurants(self):
		query = 'SELECT * FROM restaurant'
		result = self.session.execute(query)
		# result = self.run_query(query)
		return json.dumps([dict(x) for x in result])
		return str(result)

	def update_data(self, id, restaurant_name=None, restaurant_address=None, imageURL=None):
		query = f'UPDATE restaurant '
		if not restaurant_name and not restaurant_address and not imageURL:
			return 
		else:
			query += 'SET ' 
			if restaurant_name != None:
				query += f'restaurant_name="{restaurant_name}", '
			if restaurant_address != None:
				query += f'restaurant_address="{restaurant_address}", '
			if imageURL != None:
				query += f'imageURL="{imageURL}", '
		query = query[:-2] + f' WHERE id={int(id)}'
		self.run_query(query)
		return 

	def delete_data(self, id):
		query = f'DELETE FROM restaurant WHERE id={int(id)}'
		try:
			self.run_query(query)
			return True
		except:
			return False

	def run_query(self, query):
		print(query)
		try:
			result = self.session.execute(query)
			result = result.fetchall()
		except:
			result = None
		finally:
			self.session.commit()
			return result
