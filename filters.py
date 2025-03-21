# filters.py

def apply_pre_scraping_filters(companies, filters):
    if not filters:
        return companies
        
    filtered_companies = []
    
    for company in companies:
        # Skip if doesn't meet employee count requirement
        if filters.get('min_employees') and company.get('employee_count'):
            try:
                emp_count = parse_employee_count(company.get('employee_count', '0'))
                if emp_count < filters.get('min_employees'):
                    continue
            except:
                pass
            
        # Skip if industry doesn't match
        if filters.get('industries') and company.get('industry'):
            if company.get('industry').lower() not in [ind.lower() for ind in filters.get('industries')]:
                continue
            
        # Skip if contains excluded keywords
        if filters.get('exclude_keywords'):
            should_exclude = False
            description = company.get('description', '').lower()
            for keyword in filters.get('exclude_keywords'):
                if keyword.lower() in description:
                    should_exclude = True
                    break
            if should_exclude:
                continue
        
        filtered_companies.append(company)
    
    return filtered_companies

def parse_employee_count(emp_count_str):
    # Handle various formats like "100-500", "1,000+", etc.
    try:
        emp_count_str = emp_count_str.lower().replace('employees', '').strip()
        if '-' in emp_count_str:
            return int(emp_count_str.split('-')[0].replace(',', '').strip())
        elif '+' in emp_count_str:
            return int(emp_count_str.replace('+', '').replace(',', '').strip())
        else:
            return int(emp_count_str.replace(',', '').strip())
    except Exception as e:
        print(f"Error parsing employee count '{emp_count_str}': {str(e)}")
        return 0
