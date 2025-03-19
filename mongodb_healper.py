import pymongo
from typing import Dict, Any, List, Optional
import json

class MongoDBHelper:
    """Helper class for MongoDB operations."""
    
    def __init__(self, connection_string: str, db_name: str = "document_db"):
        """Initialize the MongoDB helper."""
        self.connection_string = connection_string
        self.db_name = db_name
        self.client = None
        self.db = None
        self.connect()
    
    def connect(self):
        """Connect to MongoDB."""
        try:
            self.client = pymongo.MongoClient(self.connection_string)
            self.db = self.client[self.db_name]
            print(f"Connected to MongoDB database: {self.db_name}")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
    
    def insert_document(self, collection_name: str, document: Dict[str, Any]) -> Optional[str]:
        """Insert a document into a collection."""
        if not self.db:
            print("Not connected to MongoDB")
            return None
        
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(document)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error inserting document: {e}")
            return None
    
    def find_documents(self, collection_name: str, query: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Find documents in a collection."""
        if not self.db:
            print("Not connected to MongoDB")
            return []
        
        try:
            collection = self.db[collection_name]
            cursor = collection.find(query or {})
            return list(cursor)
        except Exception as e:
            print(f"Error finding documents: {e}")
            return []
    
    def find_document_by_id(self, collection_name: str, document_id: str) -> Optional[Dict[str, Any]]:
        """Find a document by its ID."""
        if not self.db:
            print("Not connected to MongoDB")
            return None
        
        try:
            from bson.objectid import ObjectId
            collection = self.db[collection_name]
            return collection.find_one({"_id": ObjectId(document_id)})
        except Exception as e:
            print(f"Error finding document by ID: {e}")
            return None
    
    def update_document(self, collection_name: str, document_id: str, update_data: Dict[str, Any]) -> bool:
        """Update a document by its ID."""
        if not self.db:
            print("Not connected to MongoDB")
            return False
        
        try:
            from bson.objectid import ObjectId
            collection = self.db[collection_name]
            result = collection.update_one(
                {"_id": ObjectId(document_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating document: {e}")
            return False
    
    def delete_document(self, collection_name: str, document_id: str) -> bool:
        """Delete a document by its ID."""
        if not self.db:
            print("Not connected to MongoDB")
            return False
        
        try:
            from bson.objectid import ObjectId
            collection = self.db[collection_name]
            result = collection.delete_one({"_id": ObjectId(document_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False
    
    def close(self):
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()
            print("MongoDB connection closed")

# Example usage
if __name__ == "__main__":
    # Replace with your MongoDB connection string
    connection_string = "mongodb+srv://Yash:Yash@123@cluster.mongodb.net/document_db"
    
    # Create a MongoDB helper
    mongo_helper = MongoDBHelper(connection_string)
    
    # Example document
    example_doc = {
        "title": "Example Document",
        "content": [
            {"text": "This is an example", "line_num": 0},
            {"text": "Of a document stored in MongoDB", "line_num": 1}
        ],
        "metadata": {
            "source": "Example",
            "date": "2023-01-01"
        }
    }
    
    # Insert the document
    doc_id = mongo_helper.insert_document("documents", example_doc)
    
    if doc_id:
        print(f"Document inserted with ID: {doc_id}")
        
        # Find the document
        doc = mongo_helper.find_document_by_id("documents", doc_id)
        if doc:
            print("Found document:")
            print(json.dumps(doc, default=str, indent=2))
        
        # Update the document
        update_result = mongo_helper.update_document(
            "documents", 
            doc_id, 
            {"metadata.updated": "2023-01-02"}
        )
        print(f"Document updated: {update_result}")
        
        # Delete the document
        delete_result = mongo_helper.delete_document("documents", doc_id)
        print(f"Document deleted: {delete_result}")
    
    # Close the connection
    mongo_helper.close()