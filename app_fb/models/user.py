from pymongo import MongoClient
import re
from bson import ObjectId
import json


class User:
    def __init__(self, username, password, posts, notifications, first_name, last_name, email, gender, locale, phone, address, friends, status, messages, image_url):
        self.username = username
        self.password = password
        self.posts = posts
        self.notifications = notifications
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.locale = locale
        self.phone = phone
        self.address = address
        self.friends = friends
        self.status = status
        self.messages = messages
        self.image_url = image_url


class MongoUserDao:
    def __init__(self):
        config = json.load(open('./config.json', 'r'))
        client = MongoClient(config['mongo_host'], config['mongo_port'])
        self.db = client[config['db_name']]

    def save(self, user):
        self.db.users.insert_one(user)

    def search_by_name(self, name):
        result_cursor = self.db.users.find({'first_name': name})
        matches = []
        for user in result_cursor:
            matches.append(user)
        return matches

    def delete_by_id(self, _id):
        self.db.users.delete_one({'_id': ObjectId(_id)})

    def update_by_id(self, _id, user):
        self.db.users.update_one({'_id': ObjectId(_id)}, {'$set': user})

    def authenticate(self, user):
        if user.username is None or user.password is None:
            return False
        result_cursor = self.db.users.find({'username': user.username, 'password':user.password})
        if result_cursor.count() == 0:
            return False
        else:
            return True

    def list_all_users(self):
        return self.db.users.find()

    def add_stuff(self):
        for i in range(10):
            user = dict()

            user['first_name'] = "first_name" + str(i)
            user['last_name'] = "last_name" + str(i)
            user['email'] = "email" + str(i)
            if i % 2 == 0:
                user['gender'] = 'Male'
                user['locale'] = 'en-IN'
            else:
                user['gender'] = 'Female'
                user['locale'] = 'en-US'
            user['username'] = "username" + str(i)
            user['password'] = "password" + str(i)
            user['image_url'] = '/app/images/image' + str(i) + '.png'
            self.db.users.insert_one(user)

    def find_user_name_by_credentials(self, user):
        a = 3 if True else 1
        result_cursor = self.db.users.find({'username': user.username})
        matches = []
        for user in result_cursor:
            matches.append(user)
        return matches[0]['first_name'] + " " + matches[0]['last_name'] if len(matches) > 0 else None

    def check_if_user_exists(self, username):
        result_cursor = self.db.users.find({'username': username})
        matches = []
        for user in result_cursor:
            matches.append(user)
        if len(matches) > 0:
            return True
        else:
            return False

    def add_to_cart(self, user_id, product_id):
        condition = {'_id': ObjectId(user_id)}
        cursor = self.db.users.find(condition)
        user_data = cursor[0] if cursor.count() > 0 else None
        if user_data is None:
            return False

        if 'cart' not in user_data:
            user_data['cart'] = []

        if ObjectId(product_id) not in user_data['cart']:
            user_data['cart'].append(ObjectId(product_id))
            self.db.users.update_one(filter=condition, update={'$set':user_data})
            return True

    def get_by_id(self, _id):
        query = {
            '_id': ObjectId(_id)
        }
        cursor = self.db.users.find(query)
        user = cursor[0] if cursor.count() > 0 else None
        return user

    def get_id_by_username(self, username):
        cursor = self.db.users.find({'username': username})
        user_data = cursor[0] if cursor.count() > 0 else None
        if user_data is None:
            return "Anonymous"
        else:
            matches = []
            for user in cursor:
                matches.append(user)
            return matches[0]['_id']

    def get_usercart_by_userid(self, user_id):
        user = self.get_by_id(user_id)
        return user['cart']

    def add_user_post(self, post, _id):
        user = self.get_by_id(_id)
        if user is not None:
            if 'posts' in user:
                user['posts'].append(post)
            else:
                posts = []
                posts.append(post)
                user['posts'] = posts
            self.db.users.update_one({'_id': ObjectId(_id)}, {'$set': user})

    def get_user_posts(self, _id):
        user = self.get_by_id(_id)
        if 'posts' in user:
            return user['posts']
        else:
            return None

