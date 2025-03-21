# exporter.py

import pandas as pd
import os
import datetime

def export_to_csv(companies, filename=None):
    """Export companies data to CSV file"""
    if not filename:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"lead_generation_results_{timestamp}.csv"
    
    # Flatten job titles for CSV
    flattened_companies = []
    for company in companies:
        company_copy = company.copy()
        
        # Convert dict of job titles to string
        if 'job_titles' in company_copy and isinstance(company_copy['job_titles'], dict):
            job_titles_str = "; ".join([f"{name}: {title}" for name, title in company_copy['job_titles'].items()])
            company_copy['job_titles'] = job_titles_str
            
        flattened_companies.append(company_copy)
    
    df = pd.DataFrame(flattened_companies)
    
    # Create directory if it doesn't exist
    os.makedirs('results', exist_ok=True)
    filepath = os.path.join('results', filename)
    
    df.to_csv(filepath, index=False)
    print(f"Results exported to {filepath}")
    return filepath

def export_to_google_sheets(companies, sheet_name=None):
    """Export companies data to Google Sheets"""
    # This would require Google Sheets API setup
    # For now, just note that this would be implemented here
    print("Google Sheets export would be implemented here")
    print("This requires setting up OAuth2 credentials for Google Sheets API")
    return None