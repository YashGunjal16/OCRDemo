import pymongo
from pymongo import MongoClient

from urllib.parse import quote_plus

username = "Yash"
password = "Yash@123"  # Example password with special character (@)

encoded_password = quote_plus(password)
connection_string = f"mongodb+srv://{username}:{encoded_password}@cluster0.cllxj.mongodb.net/"

def test_database_insertion():
    try:
        client = MongoClient(connection_string)
        db = client.document_db
        collection = db.documents  # Access the "documents" collection

        # Insert a test document
        test_doc = {"file_name": "test_file.pdf", "status": "success"}
        insert_result = collection.insert_one(test_doc)

        print(f"Inserted document ID: {insert_result.inserted_id}")

        # Fetch all documents and print
        print("\nFetching all documents in 'documents' collection:")
        for doc in collection.find():
            print(doc)

    except Exception as e:
        print(f"Error inserting data: {e}")

if __name__ == "__main__":
    test_database_insertion()
