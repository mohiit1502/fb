from pymongo import MongoClient
import json
import re
from bson import ObjectId

class Product:
    def __init__(self, id, name, description, price):
        self.id = id
        self.name = name
        self.description = description
        self.price = price


class MongoProductDao:
    def __init__(self):
        config = json.load(open('./config.json', 'r'))
        client = MongoClient(config['mongo_host'], config['mongo_port'])
        self.db = client[config['db_name']]

    def save(self, product):
        self.db.products.insert_one(product)

    def search_by_name(self, name):
        result_cursor = self.db.products.find({'name': re.compile(name, re.IGNORECASE)})
        matches = []
        for prod in result_cursor:
            matches.append(prod)
        return matches

    def delete_by_id(self, _id):
        self.db.products.delete_one({'_id': ObjectId(_id)})

    def update_by_id(self, _id, prod):
        self.db.products.update_one({'_id': ObjectId(_id)}, {'$set': prod})

    def list_all_products(self):
        return self.db.products.find()

    def add_stuff(self):
        for i in range(10):
            product = dict()
            product['name'] = "name" + str(i)
            product['description'] = "description" + str(i)
            product['price'] = "price" + str(i)
            self.db.products.insert_one(product)
