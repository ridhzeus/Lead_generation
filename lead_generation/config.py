# config.py

# API keys and configuration
SERPER_API_KEY = "68edae654a881c2bdc42845207e8cdae5458be2d52aaa6b483c52b7b274ae08a"  # Replace with your actual API key

# Scraping settings
REQUEST_DELAY_MIN_SEC = 2
REQUEST_DELAY_MAX_SEC = 5
MAX_PAGES_PER_SEARCH = 5
MAX_COMPANIES = 100

# Default filters
DEFAULT_FILTERS = {
    'min_employees': 50,
    'industries': ['technology', 'finance', 'healthcare'],
    'exclude_keywords': ['bankrupt', 'closed', 'shutdown']
}

# Default ranking criteria
DEFAULT_RANKING_CRITERIA = {
    'industry': 'technology',
    'min_employees': 100,
    'max_employees': 1000,
    'keywords': ['innovation', 'startup', 'AI', 'machine learning']
}
print("Config file is running correctly!")