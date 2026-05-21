import pymongo

def get_schema(uri, db_name):
    client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
    db = client[db_name] if db_name and db_name != 'default' else client.get_database()
    
    schema = []
    for coll_name in db.list_collection_names():
        sample = db[coll_name].find_one()
        fields = []
        if sample:
            for k, v in sample.items():
                fields.append({"column_name": k, "data_type": type(v).__name__})
        schema.append({
            "table_name": coll_name,
            "columns": fields
        })
    return schema
