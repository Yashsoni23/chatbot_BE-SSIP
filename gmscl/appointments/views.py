from django.http import JsonResponse
from pymongo import MongoClient

connection_string = "mongodb+srv://yashsoni48678:yashsoni48678@cluster0.9ugqo1y.mongodb.net/gmscl"
client = MongoClient(connection_string)
