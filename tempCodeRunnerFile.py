# scraper.py

import requests
from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config import REQUEST_DELAY_MIN_SEC, REQUEST_DELAY_MAX_SEC, MAX_PAGES_PER_SEARCH

def setup_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def scrape_company_directory(url, max_pages=MAX_PAGES_PER_SEARCH):
    driver = setup_selenium()
    companies = []
    
    for page in range(1, max_pages + 1):
        try:
            page_url = f"{url}?page={page}"
            driver.get(page_url)
            time.sleep(random.uniform(REQUEST_DELAY_MIN_SEC, REQUEST_DELAY_MAX_SEC))
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            company_cards = soup.find_all('div', class_='company-card')  # Adjust based on actual HTML structure
            
            if not company_cards:
                print(f"No more company cards found on page {page}")
                break
            
            for card in company_cards:
                try:
                    company = {
                        'name': card.find('h3', class_='company-name').text.strip(),
                        'website': card.find('a', class_='company-website')['href'],
                        'industry': card.find('span', class_='industry').text.strip(),
                        'employee_count': card.find('span', class_='employee-count').text.strip(),
                        'description': card.find('p', class_='description').text.strip()
                    }
                    companies.append(company)
                except Exception as e:
                    print(f"Error parsing company card: {str(e)}")
        except Exception as e:
            print(f"Error scraping page {page}: {str(e)}")
    
    driver.quit()
    return companies

def extract_job_titles(company_url):
    driver = setup_selenium()
    job_titles = {}
    
    try:
        # Try different pages where leadership might be listed
        possible_paths = ["/about", "/team", "/leadership", "/company", ""]
        
        for path in possible_paths:
            full_url = company_url + path if company_url[-1] != "/" else company_url + path
            driver.get(full_url)
            time.sleep(random.uniform(REQUEST_DELAY_MIN_SEC, REQUEST_DELAY_MAX_SEC))
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Look for common leadership patterns
            leadership_sections = [
                soup.find('section', class_=lambda x: x and 'leadership' in x.lower()),
                soup.find('div', class_=lambda x: x and 'team' in x.lower()),
                soup.find('div', class_=lambda x: x and 'leadership' in x.lower()),
                soup.find('section', class_=lambda x: x and 'team' in x.lower())
            ]
            
            for section in leadership_sections:
                if section:
                    leader_elements = section.find_all(['div', 'article'], class_=lambda x: x and any(term in x.lower() for term in ['leader', 'member', 'profile', 'person', 'team-member']))
                    
                    if leader_elements:
                        for leader in leader_elements:
                            name_elem = leader.find(['h3', 'h4', 'h5', 'strong', 'b'])
                            title_elem = leader.find(['p', 'span'], class_=lambda x: x and any(term in x.lower() for term in ['title', 'position', 'role']))
                            
                            if name_elem and title_elem:
                                name = name_elem.text.strip()
                                title = title_elem.text.strip()
                                job_titles[name] = title
                        
                        if job_titles:
                            break
            
            if job_titles:
                break
    except Exception as e:
        print(f"Error extracting job titles: {str(e)}")
    finally:
        driver.quit()
        
    return job_titles