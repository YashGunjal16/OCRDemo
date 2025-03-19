from flask import Flask, request, render_template, jsonify
import os
import uuid
from document_processor import DocumentProcessor
from config import MONGODB_URI, OUTPUT_DIR
from bson.objectid import ObjectId

app = Flask(__name__)

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Initialize document processor
processor = DocumentProcessor(MONGODB_URI)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Generate unique filename
    filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    file_path = os.path.join(OUTPUT_DIR, filename)
    file.save(file_path)
    
    # Process document
    try:
        result = processor.process_document(file_path)
        return jsonify({
            "status": "success",
            "original_filename": file.filename,
            "processed_filename": filename,
            "result": result
        })
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route('/documents', methods=['GET'])
def get_documents():
    if not processor.db:
        return jsonify({"error": "Database not connected"}), 500
    
    try:
        collection = processor.db["documents"]  # Ensure collection name is correct
        documents = list(collection.find({}, {"content": 0}).sort("processed_date", -1).limit(100))
        
        for doc in documents:
            doc["_id"] = str(doc["_id"])
        
        return jsonify(documents)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/documents/<document_id>', methods=['GET'])
def get_document(document_id):
    if not processor.db:
        return jsonify({"error": "Database not connected"}), 500
    
    try:
        collection = processor.db["documents"]
        document = collection.find_one({"_id": ObjectId(document_id)})
        
        if not document:
            return jsonify({"error": "Document not found"}), 404
        
        document["_id"] = str(document["_id"])
        return jsonify(document)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)