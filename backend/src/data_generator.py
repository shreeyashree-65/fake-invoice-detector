import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string

class InvoiceDataGenerator:
    def __init__(self, num_samples=1000):
        self.num_samples = num_samples
        self.genuine_vendors = [
            "Microsoft Corp", "Apple Inc", "Google LLC", "Amazon Web Services",
            "IBM Corporation", "Oracle Corporation", "Salesforce Inc"
        ]
        self.fake_vendors = [
            "Microsft Corp", "Aple Inc", "Gogle LLC", "Amazon Web Servces",
            "IBM Corporaton", "Oracl Corporation", "Salesforec Inc"
        ]
    
    def generate_invoice_data(self):
        """Generate both genuine and fake invoice data"""
        genuine_data = self._generate_genuine_invoices()
        fake_data = self._generate_fake_invoices()
        
        # Combine and shuffle
        all_data = pd.concat([genuine_data, fake_data], ignore_index=True)
        all_data = all_data.sample(frac=1).reset_index(drop=True)
        
        return all_data
    
    def _generate_genuine_invoices(self):
        """Generate genuine invoice data with realistic patterns"""
        data = []
        
        for i in range(self.num_samples // 2):
            # Genuine invoices have consistent patterns
            vendor = random.choice(self.genuine_vendors)
            amount = round(random.uniform(100, 10000), 2)
            tax_rate = 0.18  # Standard tax rate
            tax_amount = round(amount * tax_rate, 2)
            
            # Generate realistic invoice number
            invoice_num = f"INV-{random.randint(1000, 9999)}"
            
            # Generate description
            descriptions = [
                "Software licensing and support services",
                "Cloud computing services for Q1 2024",
                "Professional consulting services",
                "Hardware procurement and installation"
            ]
            
            data.append({
                'invoice_id': invoice_num,
                'vendor_name': vendor,
                'amount': amount,
                'tax_amount': tax_amount,
                'tax_rate': tax_rate,
                'description': random.choice(descriptions),
                'date': self._generate_date(),
                'is_fake': 0  # 0 = genuine
            })
        
        return pd.DataFrame(data)
    
    def _generate_fake_invoices(self):
        """Generate fake invoice data with suspicious patterns"""
        data = []
        
        for i in range(self.num_samples // 2):
            # Fake invoices have suspicious patterns
            vendor = random.choice(self.fake_vendors)  # Misspelled names
            
            # Unusual amounts (round numbers, very high/low)
            if random.random() < 0.3:
                amount = random.choice([1000, 5000, 10000, 25000])  # Suspiciously round
            else:
                amount = round(random.uniform(50, 50000), 2)
            
            # Incorrect tax calculations
            if random.random() < 0.4:
                tax_rate = random.uniform(0.05, 0.30)  # Unusual tax rate
                tax_amount = round(amount * tax_rate + random.uniform(-50, 50), 2)  # Wrong calculation
            else:
                tax_rate = 0.18
                tax_amount = round(amount * tax_rate, 2)
            
            # Suspicious invoice numbers
            if random.random() < 0.3:
                invoice_num = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            else:
                invoice_num = f"INV-{random.randint(1000, 9999)}"
            
            # Suspicious descriptions
            fake_descriptions = [
                "Miscellaneous services and products",
                "General business expenses",
                "Various professional services",
                "Emergency maintenance work"
            ]
            
            data.append({
                'invoice_id': invoice_num,
                'vendor_name': vendor,
                'amount': amount,
                'tax_amount': tax_amount,
                'tax_rate': tax_rate,
                'description': random.choice(fake_descriptions),
                'date': self._generate_date(),
                'is_fake': 1  # 1 = fake
            })
        
        return pd.DataFrame(data)
    
    def _generate_date(self):
        """Generate a random date within the last year"""
        start_date = datetime.now() - timedelta(days=365)
        end_date = datetime.now()
        
        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randrange(days_between)
        
        return start_date + timedelta(days=random_days)
    
    def save_data(self, filename='invoice_data.csv'):
        """Generate and save the invoice data"""
        data = self.generate_invoice_data()
        import os
        # Get the current directory path and navigate to data folder
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(os.path.dirname(current_dir), 'data')
        file_path = os.path.join(data_dir, filename)
        data.to_csv(file_path, index=False)
        print(f"Generated {len(data)} invoices and saved to {file_path}")
        return data

# Usage example
if __name__ == "__main__":
    generator = InvoiceDataGenerator(num_samples=1000)
    data = generator.save_data()
    print(data.head())