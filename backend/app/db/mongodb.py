import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_mongodb_connection():
    try:
        uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        client = MongoClient(uri)
        # Verify connection
        client.admin.command('ping')
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def get_mongodb_schema():
    client = get_mongodb_connection()
    if not client:
        return {"error": "Could not connect to MongoDB database."}
    
    try:
        db_name = os.getenv("MONGODB_DATABASE", "test")
        db = client[db_name]
        collections = db.list_collection_names()
        
        schema = {}
        for coll_name in collections:
            # Sample document to infer schema (basic approach)
            sample_doc = db[coll_name].find_one()
            if sample_doc:
                # Exclude _id or keep it, infer keys and basic types
                fields = []
                for key, value in sample_doc.items():
                    fields.append({
                        "field": key,
                        "type": type(value).__name__
                    })
                schema[coll_name] = fields
            else:
                schema[coll_name] = []
        
        return schema
    except Exception as e:
        print(f"Error fetching MongoDB schema: {e}")
        return {"error": str(e)}
    finally:
        if client:
            client.close()
