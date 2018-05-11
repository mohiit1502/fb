from pymongo import MongoClient
import re
from bson import ObjectId
import json
from app_fb.models.user import MongoUserDao

mongo_user_dao = MongoUserDao()

class Post:
    def __init__(self, user, post_type, post_content, updated_time, post_size, likes, comments):
        self.user = user
        self.post_type = post_type
        self.post_content = post_content
        self.updated_time = updated_time
        self.post_size = post_size
        self.likes = likes
        self.comments = comments


class MongoPostDao:
    def __init__(self):
        config = json.load(open('./config.json', 'r'))
        client = MongoClient(config['mongo_host'], config['mongo_port'])
        self.db = client[config['db_name']]

    def save(self, post):
        self.db.posts.insert_one(post)

    def search_by_content(self, post_content):
        result_cursor = self.db.posts.find({'post_content': re.compile(post_content, re.IGNORECASE)})
        matches = []
        for post in result_cursor:
            matches.append(post)
        return matches

    def delete_by_id(self, _id):
        self.db.posts.delete_one({'_id': ObjectId(_id)})

    def update_by_id(self, _id, post):
        self.db.posts.update_one({'_id': ObjectId(_id)}, {'$set': post})

    def list_all_posts_for_user(self, user_id):
        user = mongo_user_dao.get_by_id(user_id)
        if 'posts' in user:
            return user['posts']
        else:
            return []

    def find_posts_by_type(self, post_type):
        a = 3 if True else 1
        result_cursor = self.db.posts.find({'post_type': post_type})
        matches = []
        for post in result_cursor:
            matches.append(post)
        return matches[0]['first_name'] + " " + matches[0]['last_name'] if len(matches) > 0 else None

    def get_by_id(self, _id):
        query = {
            '_id': ObjectId(_id)
        }
        cursor = self.db.posts.find(query)
        post = cursor[0] if cursor.count() > 0 else None
        return post

    def get_id_by_post_content(self, post_content):
        cursor = self.db.posts.find({'post_content': post_content})
        post_data = cursor[0] if cursor.count() > 0 else None
        if post_data is None:
            return "No posts found"
        else:
            matches = []
            for post in cursor:
                matches.append(post)
            return matches[0]['_id']

    def get_comments_by_postid(self, post_id):
        post = self.get_by_id(post_id)
        return post['comments']

