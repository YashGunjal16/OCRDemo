# **OCRDemo**

## **Overview**

OCRDemo is a simple Optical Character Recognition (OCR) system that extracts text from images and documents. This project allows users to upload images or document files and process them to extract readable text, storing the extracted data in a database.

## **Features**

- Upload and process images/documents for text extraction
- Supports multiple file formats (`.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`, `.pdf`)
- Extracted text is stored in a database
- Simple and user-friendly interface
- Built with Python, Flask, and Tesseract OCR

## **Installation & Setup**

### **Prerequisites**

Ensure you have the following installed on your system:

- Python (≥3.8)
- Flask
- Tesseract-OCR
- Required Python dependencies

### **1. Clone the Repository**

```sh
git clone https://github.com/YashGunjal16/OCRDemo.git
cd OCRDemo
```

### **2. Install Dependencies**

```sh
pip install -r requirements.txt
```

### **3. Install Tesseract-OCR**

- **Windows**: Download and install Tesseract-OCR from [here](https://github.com/UB-Mannheim/tesseract/wiki)
- **Linux (Ubuntu/Debian)**:
  ```sh
  sudo apt install tesseract-ocr
  ```
- **MacOS**:
  ```sh
  brew install tesseract
  ```

### **4. Run the Application**

```sh
python app.py
```

The app will start running on `http://127.0.0.1:5000/`.

---

## **Usage**

1. Open the web application in your browser.
2. Upload an image or document.
3. Click the **Process** button to extract text.
4. Extracted text will be stored in the database.

---

## **Project Structure**

```
OCRDemo/
│── doc/                    # Documentation files
│   │── AUTHORS             # Contributor details
│   │── LICENSE             # License file
│   │── README.md           # Project documentation
│── plugins/                # Additional processing plugins
│   │── excel_plugin.py     # Excel processing plugin
│── results/                # Stores extracted text results
│── templates/              # HTML templates
│   │── index.html          # Main web interface
│── config.py               # Configuration settings
│── document_processor.py   # Main document processing logic
│── mongodb_helper.py       # MongoDB interaction module
│── output.json             # Sample output storage
│── plugin_framework.py     # Framework for additional plugins
│── setup_database.py       # Database setup script
│── web_interface.py        # Web interface logic
```

---

## **Technologies Used**

- **Backend**: Python, Flask
- **OCR Engine**: Tesseract-OCR
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite/MongoDB (based on configuration)

---

## **Future Enhancements**

- Support for handwriting recognition
- Improved UI/UX
- Cloud integration for scalable storage
- Multi-language OCR support

---

## **Contributing**

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch (`feature-new`)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## **License**

This project is open-source and available under the **MIT License**.

