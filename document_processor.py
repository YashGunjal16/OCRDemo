import os
import json
from typing import Dict, List, Any
import pytesseract
from PIL import Image
import cv2
import numpy as np
import PyPDF2
import docx
import pymongo
from datetime import datetime
from bson.objectid import ObjectId

class DocumentProcessor:
    """Main class for processing documents and extracting text."""
    
    def __init__(self, mongodb_uri: str = None):
        """Initialize the document processor with MongoDB connection."""
        self.mongodb_uri = mongodb_uri
        self.mongo_client = None
        self.db = None
        
        if mongodb_uri:
            self.connect_to_mongodb()
    
    def connect_to_mongodb(self):
        """Connect to MongoDB using the provided URI."""
        try:
            self.mongo_client = pymongo.MongoClient(self.mongodb_uri)
            self.db = self.mongo_client.get_database("document_db")  # Explicitly get the database
            
            print("✅ Connected to MongoDB successfully!")
            print(f"📂 Using Database: {self.db.name}")
            print(f"🔍 Available Databases: {self.mongo_client.list_database_names()}")
            
        except Exception as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            self.db = None
    
    def process_document(self, file_path: str) -> Dict[str, Any]:
            """Process a document and extract text based on file type."""
            file_extension = os.path.splitext(file_path)[1].lower()

            # Get file metadata
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)

            result = {
            "file_name": file_name,
            "file_size": file_size,
            "file_type": file_extension,
            "processed_date": datetime.now().isoformat(),
            "content": [],
            "status": "success"
            }

            try:
                if file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
                    result["content"] = self.process_image(file_path)
                elif file_extension == '.pdf':
                    result["content"] = self.process_pdf(file_path)
                elif file_extension in ['.docx', '.doc']:
                    result["content"] = self.process_word(file_path)
                else:
                    result["status"] = "error"
                    result["error"] = f"Unsupported file type: {file_extension}"
            except Exception as e:
                result["status"] = "error"
                result["error"] = str(e)

        # ✅ FIXED: Properly check if MongoDB connection exists
            if self.db is not None and result["status"] == "success":
                self.store_in_mongodb(result)

            return result

    
    def process_image(self, image_path: str) -> List[Dict[str, Any]]:
        """Process an image file using OCR."""
        img = cv2.imread(image_path)
        
        # Preprocess the image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        
        # Perform OCR
        text = pytesseract.image_to_string(binary)
        
        # Get bounding boxes for text regions to maintain sequence
        boxes = pytesseract.image_to_data(binary, output_type=pytesseract.Output.DICT)
        
        content = []
        for i in range(len(boxes['text'])):
            if boxes['text'][i].strip():
                content.append({
                    "text": boxes['text'][i],
                    "page": 1,
                    "block_num": boxes['block_num'][i],
                    "line_num": boxes['line_num'][i],
                    "word_num": boxes['word_num'][i],
                    "confidence": boxes['conf'][i],
                    "position": {
                        "x": boxes['left'][i],
                        "y": boxes['top'][i],
                        "width": boxes['width'][i],
                        "height": boxes['height'][i]
                    }
                })
        
        # Sort by position to maintain sequence (top to bottom, left to right)
        content.sort(key=lambda x: (x['line_num'], x['word_num']))
        
        return content
    
    def process_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Process a PDF file and extract text with sequence information."""
        content = []
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                
                lines = page_text.split('\n') if page_text else []
                
                for line_num, line in enumerate(lines):
                    if line.strip():
                        content.append({
                            "text": line,
                            "page": page_num + 1,
                            "line_num": line_num,
                            "type": "text"
                        })
        
        return content
    
    def process_word(self, docx_path: str) -> List[Dict[str, Any]]:
        """Process a Word document and extract text with sequence information."""
        content = []
        
        doc = docx.Document(docx_path)
        
        for para_num, paragraph in enumerate(doc.paragraphs):
            if paragraph.text.strip():
                content.append({
                    "text": paragraph.text,
                    "paragraph": para_num,
                    "type": "paragraph"
                })
        
        return content
    
    def connect_to_mongodb(self):
        """Connect to MongoDB using the provided URI."""
        try:
            self.mongo_client = pymongo.MongoClient(self.mongodb_uri)
            self.db = self.mongo_client["document_db"]  # Ensure DB name is correct
        
            print("✅ Connected to MongoDB successfully!")
            print(f"📂 Using Database: {self.db.name}")
            print("🔍 Available Collections:", self.db.list_collection_names())
        
        except Exception as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
    
    def store_in_mongodb(self, document_data: Dict[str, Any]) -> str:
        """Store the processed document data in MongoDB."""
        try:
            if self.db is None:
                print("❌ MongoDB connection is not initialized.")
                return None

            collection = self.db["documents"]

            # Debugging: Print what is being inserted
            print(f"📂 Inserting into Collection: {collection.name}")
            print("📝 Data to be inserted:", json.dumps(document_data, indent=4))

            result = collection.insert_one(document_data)
            print(f"✅ Document stored in MongoDB with ID: {result.inserted_id}")
            document_id = str(result.inserted_id)  # Convert ObjectId to string
            print(f"✅ Document stored in MongoDB with ID: {document_id}")

            return document_id

        except Exception as e:
            print(f"❌ Error storing document in MongoDB: {e}")
            return None



# Example usage
if __name__ == "__main__":
    # Replace with your MongoDB connection string
    from urllib.parse import quote_plus

    import urllib.parse

    password = "Yash@123"  # Replace with your actual password
    encoded_password = urllib.parse.quote_plus(password)

    mongodb_uri = f"mongodb+srv://Yash:{encoded_password}@cluster0.cllxj.mongodb.net/?retryWrites=true&w=majority"

    
    processor = DocumentProcessor(mongodb_uri)
    

    def convert_objectid(obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    

    # Example: Process a sample image
    sample_image = "wptest.jpg"
    if os.path.exists(sample_image):
        result = processor.process_document(sample_image)
        print(json.dumps(result, indent=2, default=convert_objectid))
    else:
        print(f"⚠️ Sample file {sample_image} not found. Please provide a valid file path.")
