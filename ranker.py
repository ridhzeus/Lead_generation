# ranker.py

from filters import parse_employee_count

def rank_leads(companies, target_criteria):
    if not target_criteria:
        return companies
        
    for company in companies:
        score = 0
        
        # Industry match (highest weight)
        if target_criteria.get('industry') and company.get('industry'):
            if company.get('industry').lower() == target_criteria.get('industry').lower():
                score += 30
        
        # Employee count range
        if company.get('employee_count'):
            try:
                emp_count = parse_employee_count(company.get('employee_count', '0'))
                min_emp = target_criteria.get('min_employees', 0)
                max_emp = target_criteria.get('max_employees', float('inf'))
                
                if min_emp <= emp_count <= max_emp:
                    score += 20
            except:
                pass
        
        # Keyword matching in description (medium weight)
        if target_criteria.get('keywords') and company.get('description'):
            description = company.get('description', '').lower()
            for keyword in target_criteria.get('keywords', []):
                if keyword.lower() in description:
                    score += 5
        
        # Executive presence (low weight)
        if company.get('job_titles') and len(company.get('job_titles', {})) > 0:
            score += min(10, len(company.get('job_titles', {})) * 2)
        
        company['relevance_score'] = score
    
    # Sort by relevance score
    ranked_companies = sorted(companies, key=lambda x: x.get('relevance_score', 0), reverse=True)
    return ranked_companies
