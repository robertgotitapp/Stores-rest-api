from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price',
			type=float,
			required=True,
			help="This field cannot left blank!"
		)
	parser.add_argument('store_id',
		type=int,
		required=True,
		help="Every store needs a store id!"
	)

	@jwt_required()
	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		return {'message': 'Item not found'}, 404

	def post(self, name):
		if ItemModel.find_by_name(name):
			return {'message': "An item with name '{}' is already existed.".format(name)}, 400

		data = Item.parser.parse_args()	
		item = ItemModel( name, **data)
		# try:
		item.save_to_db()
		# except: 
		# 	return {'message': 'An error occurred when inserting item {}.'.format(item.json())}, 500

		return item.json(), 201

	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()

		return {'message': 'Item deleted'}

	def put(self, name):
		data = Item.parser.parse_args()

		item = ItemModel.find_by_name(name)
		
		if item is None:
			item = ItemModel(name, **data)
		else:
			item.price = data['price']
		try:
			item.save_to_db()
		except:
			return {'message': 'An error occurred when inserting item.'}, 500
		return item.json()


class ItemList(Resource):
	def get(self):
		return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}  
		#[item.json() for item in ItemModel.query.all()]
