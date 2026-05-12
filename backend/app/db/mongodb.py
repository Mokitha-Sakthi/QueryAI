import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from dotenv import load_dotenv

load_dotenv()

def get_mongodb_connection():
    try:
        uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        return client
    except ServerSelectionTimeoutError:
        print("MongoDB: Server selection timed out. Is MongoDB running?")
        return None
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def get_mongodb_schema():
    client = get_mongodb_connection()
    if not client:
        return {"_error": "Could not connect to MongoDB. Check MONGODB_URI in .env file."}

    try:
        db_name = os.getenv("MONGODB_DATABASE", "test")
        db = client[db_name]
        collections = db.list_collection_names()

        schema = {}
        for coll_name in collections:
            sample_doc = db[coll_name].find_one()
            if sample_doc:
                fields = [
                    {"field": key, "type": type(value).__name__}
                    for key, value in sample_doc.items()
                ]
                schema[coll_name] = fields
            else:
                schema[coll_name] = []

        return schema
    except Exception as e:
        print(f"Error fetching MongoDB schema: {e}")
        return {"_error": str(e)}
    finally:
        if client:
            client.close()
