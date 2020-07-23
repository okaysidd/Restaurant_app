from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import sys


engine = create_engine('sqlite:///restaurants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


class InsertData:
	
	def insert_data(self, restaurant_name, restaurant_address, imageURL):
		new_id = self.get_next_id()

		query = f'INSERT INTO restaurant (restaurant_name, restaurant_address, restaurant_image, id) VALUES ("{restaurant_name}", "{restaurant_address}", "{imageURL}", "{new_id}")'

		session.execute(query)
		session.commit()
		session.close()

	
	def get_next_id(self):

		query = 'SELECT * FROM restaurant'

		result = session.execute(query).fetchall()
		if len(result) == 0:
			new_id = 1

		else:
			ids = [int(x[0]) for x in result]
			new_id = max(ids) + 1

		return new_id

if __name__ == '__main__':
	restaurant_name = sys.argv[1]
	restaurant_address = sys.argv[2]
	imageURL = sys.argv[3]

	obj = InsertData()
	obj.insert_data(restaurant_name, restaurant_address, imageURL)
