# filepath: d:\completed\shelter.com\crm\utils.py
import pandas as pd
import csv
from django.db import transaction
from .models import Customer, CustomerUpload

def process_customer_upload(upload_id):
    """Process uploaded customer file (CSV/Excel)"""
    try:
        upload = CustomerUpload.objects.get(id=upload_id)
        upload.status = 'processing'
        upload.save()
        
        file_path = upload.file.path
        errors = []
        
        # Read file based on extension
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:  # Excel files
            df = pd.read_excel(file_path)
        
        upload.total_records = len(df)
        upload.save()
        
        processed = 0
        failed = 0
        
        # Process each row
        with transaction.atomic():
            for index, row in df.iterrows():
                try:
                    # Map CSV columns to model fields
                    customer_data = {
                        'first_name': str(row.get('first_name', '')).strip(),
                        'last_name': str(row.get('last_name', '')).strip(),
                        'email': str(row.get('email', '')).strip().lower(),
                        'phone': str(row.get('phone', '')).strip(),
                        'whatsapp': str(row.get('whatsapp', '')).strip(),
                        'address': str(row.get('address', '')).strip(),
                        'city': str(row.get('city', '')).strip(),
                        'status': str(row.get('status', 'lead')).strip().lower(),
                        'priority': str(row.get('priority', 'medium')).strip().lower(),
                        'source': str(row.get('source', 'upload')).strip(),
                        'notes': str(row.get('notes', '')).strip(),
                    }
                    
                    # Validate required fields
                    if not customer_data['first_name'] or not customer_data['email']:
                        errors.append(f"Row {index + 1}: Missing required fields (first_name, email)")
                        failed += 1
                        continue
                    
                    # Check if customer already exists
                    if Customer.objects.filter(email=customer_data['email']).exists():
                        errors.append(f"Row {index + 1}: Customer with email {customer_data['email']} already exists")
                        failed += 1
                        continue
                    
                    # Create customer
                    Customer.objects.create(**customer_data, created_by=upload.uploaded_by)
                    processed += 1
                    
                except Exception as e:
                    errors.append(f"Row {index + 1}: {str(e)}")
                    failed += 1
        
        # Update upload status
        upload.processed_records = processed
        upload.failed_records = failed
        upload.error_log = '\n'.join(errors) if errors else ''
        upload.status = 'completed' if failed == 0 else 'failed'
        upload.save()
        
    except Exception as e:
        upload.status = 'failed'
        upload.error_log = str(e)
        upload.save()
        raise e