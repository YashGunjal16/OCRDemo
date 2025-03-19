"""Configuration settings for the document processing system."""

# MongoDB connection settings
MONGODB_URI = "mongodb+srv://Yash:Yash%40123@cluster0.cllxj.mongodb.net/"
MONGODB_DB_NAME = "document_db"

# from urllib.parse import quote_plus

# USERNAME = "Yash"  # Replace with your actual username
# PASSWORD = "Yash@123"  # Replace with your actual password

# ENCODED_USERNAME = quote_plus(USERNAME)
# ENCODED_PASSWORD = quote_plus(PASSWORD)

# MONGODB_URI = f"mongodb+srv://{ENCODED_USERNAME}:{ENCODED_PASSWORD}@cluster0.cllxj.mongodb.net/document_db"

print("MongoDB URI:", MONGODB_URI)  # Check if encoding is applied correctly


# OCR settings
TESSERACT_PATH = None  # Set to None to use default path, or specify custom path
OCR_LANGUAGE = "eng"  # Default language for OCR

# Processing settings
MAX_WORKERS = 4  # Number of parallel workers for batch processing
OUTPUT_DIR = "results"  # Default directory for output files

# Plugin settings
PLUGINS_DIR = "plugins"  # Directory for custom plugins