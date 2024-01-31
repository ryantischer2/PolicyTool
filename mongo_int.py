from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")  # Update with your MongoDB URI if different
db = client.your_database_name  # Replace with your database name
policies_collection = db.policies  # Replace with your collection name

def save_policy_to_mongodb(policy):
    policies_collection.insert_one(policy)