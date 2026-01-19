#  Fake Invoice Detector

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![React](https://img.shields.io/badge/React-18.2.0-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

AI-powered fake invoice detection system using machine learning to identify fraudulent invoices through text and numerical pattern analysis.

##  Features

- **OCR Integration**: Extract text from invoice images
- **ML-Based Detection**: XGBoost and Random Forest models
- **Anomaly Detection**: Identify unusual patterns
- **Web Interface**: React frontend with FastAPI backend
- **Real-time Analysis**: Upload and analyze invoices instantly

##  Tech Stack

### Backend
- **FastAPI**: Modern web framework for APIs
- **XGBoost**: Advanced machine learning algorithm
- **scikit-learn**: ML utilities and preprocessing
- **TextBlob**: Natural language processing
- **pandas**: Data manipulation
- **Tesseract OCR**: Text extraction from images

### Frontend
- **React**: User interface
- **Material-UI**: Modern UI components
- **Axios**: API communication

##  Installation & Setup

### Quick Setup
```bash
#Clone the repository
git clone https://github.com/shreeyashree-65/fake-invoice-detector.git
cd fake-invoice-detector

#Run automatic setup
python setup.py setup

#Start development servers
python setup.py dev
```

### Manual Setup

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python src/data_generator.py  # Generate training data
python src/model_trainer.py   # Train ML models
python app.py                 # Start FastAPI server
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Docker Setup
```bash
#Build and run with Docker
docker-compose up --build

#Or use the setup script
python setup.py docker-build
python setup.py docker-start
```

### OCR Setup 
For image processing capabilities:

1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install and add to PATH
3. Update `pytesseract.pytesseract.tesseract_cmd` in `ocr_processor.py`


##  Machine Learning Approach

### Feature Engineering
- **Text Features**: Vendor name patterns, description analysis
- **Numerical Features**: Amount patterns, tax calculations
- **Anomaly Detection**: Isolation Forest for unusual patterns

### Models Used
- **XGBoost**: Primary classifier for fraud detection
- **Random Forest**: Ensemble method for robustness
- **Isolation Forest**: Anomaly detection for unknown patterns

### Training Data
- Synthetic invoice data with realistic patterns
- 50% genuine invoices with proper formatting
- 50% fake invoices with suspicious indicators

##  Usage

1. **Upload Invoice**: Drag and drop invoice image
2. **OCR Processing**: Text extraction from image
3. **Feature Extraction**: Analyze text and numerical patterns
4. **ML Prediction**: Classify as genuine or fake
5. **Results**: View prediction with confidence score
   

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Author

**SHREEYA P S** - [shreeyashree-65](https://github.com/shreeyashree-65)

