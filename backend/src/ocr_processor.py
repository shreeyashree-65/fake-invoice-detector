import pytesseract
import cv2
import numpy as np
from PIL import Image
import re
from typing import Dict, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InvoiceOCRProcessor:
    def __init__(self):
        """Initialize OCR processor with default settings"""
        # Configure pytesseract if needed (path to tesseract executable)
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Preprocess the image for better OCR results
        
        Args:
            image_path: Path to the invoice image
            
        Returns:
            Preprocessed image as numpy array
        """
        try:
            # Read the image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not read image from {image_path}")
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply noise reduction
            denoised = cv2.fastNlMeansDenoising(gray)
            
            # Apply adaptive thresholding
            thresh = cv2.adaptiveThreshold(
                denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
            
            # Apply morphological operations to clean up
            kernel = np.ones((1, 1), np.uint8)
            cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            return cleaned
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            raise
    
    def extract_text_from_image(self, image_path: str) -> str:
        """
        Extract text from invoice image using OCR
        
        Args:
            image_path: Path to the invoice image
            
        Returns:
            Extracted text as string
        """
        try:
            # Preprocess the image
            processed_image = self.preprocess_image(image_path)
            
            # Configure OCR settings
            custom_config = r'--oem 3 --psm 6'
            
            # Extract text
            text = pytesseract.image_to_string(processed_image, config=custom_config)
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error extracting text from image: {str(e)}")
            raise
    
    def parse_invoice_data(self, text: str) -> Dict[str, str]:
        """
        Parse extracted text to identify invoice fields
        
        Args:
            text: Raw OCR text from invoice
            
        Returns:
            Dictionary with parsed invoice data
        """
        invoice_data = {
            'invoice_id': '',
            'vendor_name': '',
            'amount': '',
            'tax_amount': '',
            'tax_rate': '',
            'description': '',
            'date': ''
        }
        
        try:
            # Split text into lines
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            # Extract invoice ID
            invoice_id_pattern = r'(?:invoice|inv|bill)[\s#]*:?\s*([A-Z0-9\-]+)'
            for line in lines:
                match = re.search(invoice_id_pattern, line, re.IGNORECASE)
                if match:
                    invoice_data['invoice_id'] = match.group(1)
                    break
            
            # Extract vendor name (usually in first few lines)
            vendor_patterns = [
                r'(?:from|to|vendor|company)[\s:]*([A-Za-z\s&.,]+)',
                r'^([A-Za-z\s&.,]+)(?:Inc|Corp|Ltd|LLC|Company)',
            ]
            
            for line in lines[:5]:  # Check first 5 lines
                for pattern in vendor_patterns:
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        invoice_data['vendor_name'] = match.group(1).strip()
                        break
                if invoice_data['vendor_name']:
                    break
            
            # Extract amounts
            amount_patterns = [
                r'(?:total|amount|subtotal)[\s:]*\$?([0-9,]+\.?[0-9]*)',
                r'(?:total|amount|subtotal)[\s:]*([0-9,]+\.?[0-9]*)',
                r'\$([0-9,]+\.?[0-9]*)',
            ]
            
            amounts = []
            for line in lines:
                for pattern in amount_patterns:
                    matches = re.findall(pattern, line, re.IGNORECASE)
                    for match in matches:
                        # Clean and validate amount
                        clean_amount = match.replace(',', '')
                        try:
                            float(clean_amount)
                            amounts.append(clean_amount)
                        except ValueError:
                            continue
            
            # Assign amounts (largest is usually total)
            if amounts:
                amounts_float = [float(amt) for amt in amounts]
                amounts_float.sort(reverse=True)
                
                if len(amounts_float) >= 1:
                    invoice_data['amount'] = str(amounts_float[0])
                if len(amounts_float) >= 2:
                    invoice_data['tax_amount'] = str(amounts_float[0] - amounts_float[1])
            
            # Extract tax rate
            tax_rate_pattern = r'(?:tax|vat)[\s:]*([0-9]+\.?[0-9]*)\s*%'
            for line in lines:
                match = re.search(tax_rate_pattern, line, re.IGNORECASE)
                if match:
                    invoice_data['tax_rate'] = str(float(match.group(1)) / 100)
                    break
            
            # Extract date
            date_patterns = [
                r'(?:date|issued)[\s:]*([0-9]{1,2}[\/\-][0-9]{1,2}[\/\-][0-9]{2,4})',
                r'([0-9]{1,2}[\/\-][0-9]{1,2}[\/\-][0-9]{2,4})',
                r'([0-9]{4}[\/\-][0-9]{1,2}[\/\-][0-9]{1,2})',
            ]
            
            for line in lines:
                for pattern in date_patterns:
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        invoice_data['date'] = match.group(1)
                        break
                if invoice_data['date']:
                    break
            
            # Extract description (look for common service descriptions)
            description_keywords = [
                'service', 'product', 'consulting', 'software', 'license',
                'support', 'maintenance', 'hardware', 'equipment'
            ]
            
            description_lines = []
            for line in lines:
                for keyword in description_keywords:
                    if keyword.lower() in line.lower():
                        description_lines.append(line)
                        break
            
            if description_lines:
                invoice_data['description'] = ' '.join(description_lines[:2])  # First 2 relevant lines
            
            return invoice_data
            
        except Exception as e:
            logger.error(f"Error parsing invoice data: {str(e)}")
            return invoice_data
    
    def process_invoice_image(self, image_path: str) -> Dict[str, str]:
        """
        Complete pipeline to process invoice image
        
        Args:
            image_path: Path to the invoice image
            
        Returns:
            Dictionary with extracted invoice data
        """
        try:
            # Extract text from image
            text = self.extract_text_from_image(image_path)
            logger.info(f"Extracted text: {text[:200]}...")  # Log first 200 chars
            
            # Parse invoice data from text
            invoice_data = self.parse_invoice_data(text)
            
            # Fill in defaults for missing fields
            if not invoice_data['invoice_id']:
                invoice_data['invoice_id'] = 'OCR-EXTRACTED'
            if not invoice_data['vendor_name']:
                invoice_data['vendor_name'] = 'Unknown Vendor'
            if not invoice_data['amount']:
                invoice_data['amount'] = '0.00'
            if not invoice_data['tax_amount']:
                invoice_data['tax_amount'] = '0.00'
            if not invoice_data['tax_rate']:
                invoice_data['tax_rate'] = '0.18'
            if not invoice_data['description']:
                invoice_data['description'] = 'OCR extracted invoice'
            if not invoice_data['date']:
                from datetime import datetime
                invoice_data['date'] = datetime.now().strftime('%Y-%m-%d')
            
            return invoice_data
            
        except Exception as e:
            logger.error(f"Error processing invoice image: {str(e)}")
            raise

# Usage example
if __name__ == "__main__":
    processor = InvoiceOCRProcessor()
    
    # Test with a sample image (you would need to provide an actual image path)
    # result = processor.process_invoice_image("sample_invoice.jpg")
    # print(result)
    
    print("OCR Processor initialized successfully!")
    print("To test, provide an invoice image path to process_invoice_image() method")
