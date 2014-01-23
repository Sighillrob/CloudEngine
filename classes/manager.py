import pymongo
from bson.objectid import ObjectId
from django.conf import settings
from classes.utils import validate_db_name


class ClassesManager(object):
    client = pymongo.MongoClient(settings.MONGO_HOST)
    
    def get_classes(self, db, app):
        db = validate_db_name(db)
        db = self.client[db]
        collections = db.collection_names(include_system_collections=False)
        app_classes = []
        for coll in collections:
            doc = db[coll].find_one({'app_id' : app.key})
            if doc: app_classes.append(coll)
        return app_classes
    
    
    def get_class(self, db, app, klass, query, sort_key=None, direction = None):
        db = validate_db_name(db)
        
        try:
            assert(direction == pymongo.ASCENDING or direction == pymongo.DESCENDING)
        except AssertionError:
            raise Exception("valid values for order are 1 & -1")
        
        db = self.client[db]
        collection = db[klass]
        query['app_id'] = app.key
        cursor = collection.find(query, {"app_id": False})      # app_id is used only by server
        if sort_key:
            cursor = cursor.sort(sort_key, direction)
            
        res = [doc for doc in cursor]

        for doc in res:
            objid = doc["_id"]
            doc["_id"] = str(objid)
        
        return res
    
    
    def delete_class(self, db, app, klass):
        db = validate_db_name(db)
        db = self.client[db]
        if klass in db.collection_names():
            collection = db[klass]
            collection.remove({'app_id': app.key})


    def add_object(self, db, app, klass, obj):
        db = validate_db_name(db)
        db = self.client[db]
        collection = db[klass]
        keys = obj.keys()
        if ("_id" in keys) or ("app_id" in keys):
            raise Exception("Invalid object. _id/app_id is a reserved field")
        
        obj['app_id'] = app.key
        objid = collection.insert(obj)
        return objid
    
    
    def add_multiple_objects(self, db, app, klass, objects):
        db = validate_db_name(db)
        db = self.client[db]
        collection = db[klass]
        for obj in objects:
            keys = obj.keys()
            if ("_id" in keys) or ("app_id" in keys):
                raise Exception("Invalid object. _id/app_id is a reserved field")
            obj['app_id'] = app.key
        ids = collection.insert(objects)
        return ids
        
        
    def get_object(self, db, klass, id):
        db = validate_db_name(db)
        db = self.client[db]
        collection = db[klass]
        query = {"_id": ObjectId(id)}
        obj = collection.find_one( query,
                                  {"app_id": False})
        if obj:
            objid = obj["_id"]
            obj["_id"] = str(objid)
        return obj
        
        
    def update_object(self, db, klass, id, obj):
        db = validate_db_name(db)
        db = self.client[db]
        collection = db[klass]
        updates = obj.keys()
        if ("_id" in updates) or ("app_id" in updates):
            raise Exception("Invalid object. _id/app_id is a reserved field")
        collection.update({"_id": ObjectId(id)},
                          {"$set": obj})               # todo: set multi = true??
        
        
    def delete_object(self, db, klass, id):
        db = validate_db_name(db)
        db = self.client[db]
        collection = db[klass]
        collection.remove(ObjectId(id))
        
        
    def delete_app_data(self, db, app):
        db = validate_db_name(db)
        db = self.client[db]
        collections = db.collection_names(include_system_collections=False)
        for collection in collections:
            col = db[collection]
            col.remove({'app_id': app.key})
            
        
        
        
        
        
        
        
        
        
        
        
        