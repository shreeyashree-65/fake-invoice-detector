import pandas as pd
import numpy as np
from textblob import TextBlob
from datetime import datetime
import re
from difflib import SequenceMatcher

class InvoiceFeatureExtractor:
    def __init__(self):
        # Known legitimate vendor names for similarity matching
        self.legitimate_vendors = [
            "Microsoft Corporation", "Apple Inc", "Google LLC", "Amazon Web Services",
            "IBM Corporation", "Oracle Corporation", "Salesforce Inc", "Adobe Systems",
            "Intel Corporation", "Cisco Systems", "Dell Technologies", "HP Inc"
        ]
        
        # Common legitimate invoice description patterns
        self.legitimate_descriptions = [
            "software licensing", "cloud services", "consulting services", 
            "hardware procurement", "maintenance support", "technical support"
        ]
    
    def extract_features(self, invoice_data):
        """
        Extract comprehensive features from invoice data
        
        Args:
            invoice_data: DataFrame or dict containing invoice information
            
        Returns:
            DataFrame with extracted features
        """
        if isinstance(invoice_data, dict):
            invoice_data = pd.DataFrame([invoice_data])
        
        features = pd.DataFrame()
        
        # Text-based features
        features['vendor_name_similarity'] = invoice_data['vendor_name'].apply(
            self._calculate_vendor_similarity
        )
        features['description_legitimacy'] = invoice_data['description'].apply(
            self._analyze_description_legitimacy
        )
        features['description_sentiment'] = invoice_data['description'].apply(
            self._calculate_sentiment
        )
        features['description_length'] = invoice_data['description'].apply(len)
        features['description_word_count'] = invoice_data['description'].apply(
            lambda x: len(x.split())
        )
        
        # Numerical features
        features['amount_roundness'] = invoice_data['amount'].apply(
            self._calculate_amount_roundness
        )
        features['tax_accuracy'] = self._calculate_tax_accuracy(
            invoice_data['amount'], invoice_data['tax_amount'], invoice_data['tax_rate']
        )
        features['amount_log'] = np.log1p(invoice_data['amount'])
        features['tax_rate_deviation'] = abs(invoice_data['tax_rate'] - 0.18)  # Standard rate
        
        # Invoice ID patterns
        features['invoice_id_pattern'] = invoice_data['invoice_id'].apply(
            self._analyze_invoice_id_pattern
        )
        features['invoice_id_length'] = invoice_data['invoice_id'].apply(len)
        
        # Date-based features
        features['date_recency'] = invoice_data['date'].apply(
            self._calculate_date_recency
        )
        features['is_weekend'] = invoice_data['date'].apply(
            self._is_weekend
        )
        
        # Combined features
        features['amount_to_tax_ratio'] = invoice_data['amount'] / (invoice_data['tax_amount'] + 1e-6)
        features['total_amount'] = invoice_data['amount'] + invoice_data['tax_amount']
        
        return features
    
    def _calculate_vendor_similarity(self, vendor_name):
        """Calculate similarity to known legitimate vendors"""
        max_similarity = 0
        for legit_vendor in self.legitimate_vendors:
            similarity = SequenceMatcher(None, vendor_name.lower(), legit_vendor.lower()).ratio()
            max_similarity = max(max_similarity, similarity)
        return max_similarity
    
    def _analyze_description_legitimacy(self, description):
        """Analyze if description contains legitimate business terms"""
        description_lower = description.lower()
        legitimacy_score = 0
        
        # Check for legitimate business terms
        for term in self.legitimate_descriptions:
            if term in description_lower:
                legitimacy_score += 1
        
        # Check for vague terms (negative indicators)
        vague_terms = ["miscellaneous", "various", "general", "emergency", "urgent"]
        for term in vague_terms:
            if term in description_lower:
                legitimacy_score -= 1
        
        return max(0, legitimacy_score)  # Ensure non-negative
    
    def _calculate_sentiment(self, description):
        """Calculate sentiment polarity of description"""
        try:
            blob = TextBlob(description)
            return blob.sentiment.polarity
        except:
            return 0
    
    def _calculate_amount_roundness(self, amount):
        """Calculate how 'round' an amount is (fake invoices often use round numbers)"""
        # Check if amount is a round number
        if amount % 1000 == 0:
            return 1.0  # Very round
        elif amount % 100 == 0:
            return 0.7  # Somewhat round
        elif amount % 10 == 0:
            return 0.3  # Slightly round
        else:
            return 0.0  # Not round
    
    def _calculate_tax_accuracy(self, amounts, tax_amounts, tax_rates):
        """Calculate how accurate the tax calculation is"""
        expected_tax = amounts * tax_rates
        tax_error = abs(tax_amounts - expected_tax) / (expected_tax + 1e-6)
        return 1 / (1 + tax_error)  # Higher score for accurate calculations
    
    def _analyze_invoice_id_pattern(self, invoice_id):
        """Analyze invoice ID pattern legitimacy"""
        # Legitimate patterns: INV-1234, 2024-001, etc.
        # Illegitimate: random strings, too short/long
        
        if re.match(r'^INV-\d{4}$', invoice_id):
            return 1.0  # Standard format
        elif re.match(r'^\d{4}-\d{3}$', invoice_id):
            return 0.8  # Year-number format
        elif re.match(r'^[A-Z]{2,3}-\d{4,6}$', invoice_id):
            return 0.6  # Company prefix format
        elif len(invoice_id) < 5 or len(invoice_id) > 15:
            return 0.2  # Too short or too long
        else:
            return 0.4  # Other patterns
    
    def _calculate_date_recency(self, date):
        """Calculate how recent the invoice date is"""
        if isinstance(date, str):
            date = pd.to_datetime(date)
        
        days_old = (datetime.now() - date).days
        
        if days_old < 30:
            return 1.0  # Very recent
        elif days_old < 90:
            return 0.8  # Recent
        elif days_old < 365:
            return 0.6  # Moderate
        else:
            return 0.2  # Old
    
    def _is_weekend(self, date):
        """Check if invoice date is on weekend (suspicious for business invoices)"""
        if isinstance(date, str):
            date = pd.to_datetime(date)
        
        return 1 if date.weekday() >= 5 else 0
    
    def get_feature_names(self):
        """Return list of all feature names"""
        return [
            'vendor_name_similarity', 'description_legitimacy', 'description_sentiment',
            'description_length', 'description_word_count', 'amount_roundness',
            'tax_accuracy', 'amount_log', 'tax_rate_deviation', 'invoice_id_pattern',
            'invoice_id_length', 'date_recency', 'is_weekend', 'amount_to_tax_ratio',
            'total_amount'
        ]

# Usage example
if __name__ == "__main__":
    # Test with sample data
    sample_data = {
        'vendor_name': ['Microsoft Corp', 'Microsft Corp'],
        'description': ['Software licensing services', 'Miscellaneous expenses'],
        'amount': [1000.0, 5000.0],
        'tax_amount': [180.0, 900.0],
        'tax_rate': [0.18, 0.18],
        'invoice_id': ['INV-1234', 'XYZABC123'],
        'date': ['2024-01-15', '2024-01-20']
    }
    
    df = pd.DataFrame(sample_data)
    extractor = InvoiceFeatureExtractor()
    features = extractor.extract_features(df)
    
    print("Extracted Features:")
    print(features)
    print("\nFeature Names:")
    print(extractor.get_feature_names())
