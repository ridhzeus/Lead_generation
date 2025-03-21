# serper_api.py

import requests
import json
import time
from config import REQUEST_DELAY_MIN_SEC

def serper_api_search(query, api_key, num_results=10):
    url = "https://serpapi.com/search"
    
    params = {
        "q": query,
        "api_key": api_key,
        "num": num_results
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {str(e)}")
        return {"error": str(e)}

def extract_company_info(results):
    companies = []
    
    for result in results.get('organic_results', []):
        try:
            company = {
                'name': result.get('title', '').split('|')[0].strip(),
                'website': result.get('link', ''),
                'description': result.get('snippet', '')
            }
            companies.append(company)
        except Exception as e:
            print(f"Error extracting company info: {str(e)}")
    
    return companies

def search_multiple_companies(industry_list, api_key, results_per_query=10):
    all_companies = []
    
    for industry in industry_list:
        query = f"top companies in {industry} industry"
        print(f"Searching for: {query}")
        
        results = serper_api_search(query, api_key, results_per_query)
        
        if 'error' in results:
            print(f"Error in API response for {industry}: {results['error']}")
            continue
            
        companies = extract_company_info(results)
        
        # Add industry info
        for company in companies:
            company['industry'] = industry
        
        all_companies.extend(companies)
        time.sleep(REQUEST_DELAY_MIN_SEC)  # Be nice to the API
    
    return all_companies
