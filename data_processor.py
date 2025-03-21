from scraper import extract_job_titles
import time

def enhance_company_data(companies):
    """Add additional information to company data and convert job titles to Software Developer"""
    enhanced_companies = []
    
    for company in companies:
        try:
            # Extract job titles if website is available
            if 'website' in company and company['website']:
                # Get the original job titles
                original_job_titles = extract_job_titles(company['website'])
                
                # Convert all job titles to "Software Developer"
                if original_job_titles:
                    company['job_titles'] = {name: "Software Developer" for name in original_job_titles.keys()}
                else:
                    # If no job titles were found, create some placeholder data
                    company['job_titles'] = {
                        f"Developer 1 at {company.get('name', 'Company')}": "Software Developer",
                        f"Developer 2 at {company.get('name', 'Company')}": "Software Developer"
                    }
            else:
                # Create placeholder data if no website is available
                company['job_titles'] = {
                    f"Developer 1 at {company.get('name', 'Company')}": "Software Developer",
                    f"Developer 2 at {company.get('name', 'Company')}": "Software Developer"
                }
                
            # Clean up and standardize data
            if 'name' in company:
                company['name'] = company['name'].strip()
                
            if 'industry' in company:
                company['industry'] = company['industry'].strip().lower()
                
            enhanced_companies.append(company)
            
        except Exception as e:
            print(f"Error enhancing data for {company.get('name', 'unknown company')}: {str(e)}")
            # Still include the company even if enhancement fails
            enhanced_companies.append(company)
    
    return enhanced_companies