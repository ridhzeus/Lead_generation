import streamlit as st
import pandas as pd
import time
import os
import sys
from datetime import datetime

# Import project modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from scraper import scrape_company_directory
from serper_api import search_multiple_companies
from filters import apply_pre_scraping_filters
from ranker import rank_leads
from data_processor import enhance_company_data
from exporter import export_to_csv

# Page configuration
st.set_page_config(
    page_title="Lead Generation Tool",
    page_icon="📊",
    layout="wide"
)

# App title and description
st.title("📊 B2B Lead Generation Tool")
st.markdown("""
    Generate high-quality B2B leads using web scraping and AI ranking. 
    Choose your industry, set your filters, and get targeted lead lists.
""")

# Sidebar for settings
st.sidebar.title("Settings")

# Choose data source
data_source = st.sidebar.radio(
    "Choose Data Source",
    ["Web Scraping", "Serper API (Google Search)"]
)

# API Key input (if Serper is selected)
api_key = None
if data_source == "Serper API (Google Search)":
    api_key = st.sidebar.text_input("Enter Serper API Key", type="password")
    if not api_key:
        st.sidebar.warning("⚠️ API key is required for Serper API")

# Target industries
st.sidebar.subheader("Target Industries")
default_industries = ["technology", "finance", "healthcare"]
custom_industry = st.sidebar.text_input("Add Custom Industry")

if custom_industry:
    if custom_industry.lower() not in default_industries:
        default_industries.append(custom_industry.lower())

selected_industries = st.sidebar.multiselect(
    "Select Industries",
    options=default_industries,
    default=default_industries[:2]
)

# Lead generation method
st.sidebar.subheader("Lead Generation Method")
use_filters = st.sidebar.checkbox("Apply Pre-Scraping Filters", value=True)
use_ranking = st.sidebar.checkbox("Apply AI-Based Ranking", value=True)

# Filter settings (if enabled)
filter_settings = {}
if use_filters:
    st.sidebar.subheader("Filter Settings")
    min_employees = st.sidebar.number_input("Minimum Employee Count", min_value=0, value=50)
    exclude_keywords = st.sidebar.text_area("Exclude Companies with Keywords (one per line)")
    
    filter_settings = {
        'min_employees': min_employees,
        'industries': selected_industries,
        'exclude_keywords': [kw.strip() for kw in exclude_keywords.split('\n') if kw.strip()]
    }

# Ranking settings (if enabled)
ranking_criteria = {}
if use_ranking:
    st.sidebar.subheader("Ranking Criteria")
    target_industry = st.sidebar.selectbox("Target Industry", options=selected_industries)
    min_emp_ranking = st.sidebar.number_input("Minimum Employees", min_value=0, value=50)
    max_emp_ranking = st.sidebar.number_input("Maximum Employees", min_value=0, value=1000)
    ranking_keywords = st.sidebar.text_area("Prioritize Companies with Keywords (one per line)")
    
    ranking_criteria = {
        'industry': target_industry,
        'min_employees': min_emp_ranking,
        'max_employees': max_emp_ranking,
        'keywords': [kw.strip() for kw in ranking_keywords.split('\n') if kw.strip()]
    }

# Max companies to scrape
max_companies = st.sidebar.slider("Maximum Companies to Process", min_value=10, max_value=500, value=100)

# Main content area with tabs
tab1, tab2, tab3 = st.tabs(["Generate Leads", "Results", "Export"])

# Generate leads tab
with tab1:
    st.header("Generate Leads")
    st.markdown("""
        Click the button below to start generating leads based on your settings.
        Data will be collected from selected sources and processed according to your filters and ranking criteria.
    """)
    
    if st.button("🚀 Generate Leads", use_container_width=True):
        if not selected_industries:
            st.error("⚠️ Please select at least one industry")
        elif data_source == "Serper API (Google Search)" and not api_key:
            st.error("⚠️ Please enter your Serper API key")
        else:
            # Progress indicators
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Initialize result storage
            if 'leads_data' not in st.session_state:
                st.session_state.leads_data = []
                
            # Step 1: Collect data
            status_text.text("🔍 Collecting company data...")
            all_companies = []
            
            if data_source == "Serper API (Google Search)":
                progress_bar.progress(10)
                status_text.text(f"🔍 Searching for companies using Serper API...")
                
                all_companies = search_multiple_companies(
                    selected_industries, 
                    api_key, 
                    max_companies // len(selected_industries)
                )
            else:
                # Web scraping example (would need to be adapted to actual site structure)
                # This is a placeholder that simulates scraping
                for i, industry in enumerate(selected_industries):
                    progress_value = 10 + (i * 20 // len(selected_industries))
                    progress_bar.progress(progress_value)
                    status_text.text(f"🔍 Scraping data for {industry} industry...")
                    time.sleep(1)  # Simulate scraping delay
                    
                    # In real implementation: replace with actual scraping
                    # url = f"https://example-directory.com/companies/{industry}"
                    # industry_companies = scrape_company_directory(url)
                    
                    # Simulated data for demonstration
                    industry_companies = [
                        {
                            'name': f"{industry.capitalize()} Company {j}",
                            'website': f"https://www.{industry}company{j}.com",
                            'industry': industry,
                            'employee_count': f"{(j+1)*50}-{(j+1)*100}",
                            'description': f"A leading {industry} company specializing in innovative solutions."
                        } for j in range(max_companies // len(selected_industries))
                    ]
                    
                    all_companies.extend(industry_companies)
            
            status_text.text(f"✅ Collected {len(all_companies)} companies")
            progress_bar.progress(40)
            
            # Step 2: Apply filters
            if use_filters and filter_settings:
                status_text.text("🔍 Applying filters...")
                all_companies = apply_pre_scraping_filters(all_companies, filter_settings)
                status_text.text(f"✅ {len(all_companies)} companies passed filters")
            
            progress_bar.progress(60)
            
            # Step 3: Enhance data
        
            status_text.text("🔍 Enhancing company data and converting positions to Software Developer...")

            # Use actual data enhancement instead of simulation
            all_companies = enhance_company_data(all_companies)

            progress_bar.progress(80)
            
            # Step 4: Apply ranking
            if use_ranking and ranking_criteria:
                status_text.text("🔍 Ranking companies by relevance...")
                all_companies = rank_leads(all_companies, ranking_criteria)
            
            progress_bar.progress(100)
            status_text.text(f"✅ Successfully generated {len(all_companies)} leads!")
            
            # Store results in session state
            st.session_state.leads_data = all_companies
            
            # Show success message
            st.success(f"Successfully generated {len(all_companies)} leads! Go to the Results tab to view them.")

# Results tab
with tab2:
    if 'leads_data' in st.session_state and st.session_state.leads_data:
        leads = st.session_state.leads_data
        
        # Summary metrics
        st.header("Results Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Leads", len(leads))
        with col2:
            industry_counts = {}
            for lead in leads:
                industry = lead.get('industry', 'unknown')
                industry_counts[industry] = industry_counts.get(industry, 0) + 1
            top_industry = max(industry_counts.items(), key=lambda x: x[1])[0]
            st.metric("Top Industry", top_industry.capitalize())
        with col3:
            if use_ranking:
                avg_score = sum(lead.get('relevance_score', 0) for lead in leads) / len(leads)
                st.metric("Avg. Relevance Score", f"{avg_score:.1f}")
            else:
                st.metric("Industries", len(set(lead.get('industry', '') for lead in leads)))
        
        # Results table
        st.header("Lead Results")
        
        # Prepare DataFrame
        df_leads = pd.DataFrame(leads)
        
        # Handle job titles column (convert dict to string)
        if 'job_titles' in df_leads.columns:
            df_leads['job_titles_str'] = df_leads['job_titles'].apply(
                lambda x: "; ".join([f"{name}: {title}" for name, title in x.items()]) if isinstance(x, dict) else x
            )
            df_leads = df_leads.drop('job_titles', axis=1)
            df_leads = df_leads.rename(columns={'job_titles_str': 'job_titles'})
        
        # Display dataframe
        st.dataframe(df_leads, use_container_width=True)
    else:
        st.info("No leads generated yet. Go to the Generate Leads tab to get started.")

# Export tab
with tab3:
    st.header("Export Results")
    
    if 'leads_data' in st.session_state and st.session_state.leads_data:
        leads = st.session_state.leads_data
        
        st.markdown(f"You have **{len(leads)}** leads ready to export.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Export to CSV")
            export_filename = st.text_input(
                "Filename", 
                value=f"lead_generation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            
            if st.button("Export to CSV", use_container_width=True):
                # Create results directory if needed
                os.makedirs('results', exist_ok=True)
                filepath = os.path.join('results', export_filename)
                
                # Create DataFrame and export
                df_leads = pd.DataFrame(leads)
                
                # Handle job titles column (convert dict to string)
                if 'job_titles' in df_leads.columns:
                    df_leads['job_titles'] = df_leads['job_titles'].apply(
                        lambda x: "; ".join([f"{name}: {title}" for name, title in x.items()]) if isinstance(x, dict) else x
                    )
                
                df_leads.to_csv(filepath, index=False)
                
                # Provide download link
                with open(filepath, 'rb') as f:
                    st.download_button(
                        label="Download CSV File",
                        data=f,
                        file_name=export_filename,
                        mime="text/csv",
                        use_container_width=True
                    )
        
        with col2:
            st.subheader("Export to Google Sheets")
            sheet_name = st.text_input("Sheet Name", value="Lead Generation Results")
            
            st.markdown("""
                > ℹ️ Exporting to Google Sheets requires additional setup:
                > 1. Set up Google OAuth credentials
                > 2. Install `gspread` package
                > 3. Configure authentication in the app
            """)
            
            if st.button("Export to Google Sheets", disabled=True, use_container_width=True):
                st.info("Google Sheets export functionality will be implemented here")
    else:
        st.info("No leads generated yet. Go to the Generate Leads tab to get started.")

# Footer
st.markdown("---")
st.markdown("### How to Use This Tool")
with st.expander("Show Instructions"):
    st.markdown("""
        1. **Select your data source** in the sidebar
        2. **Choose target industries** you want to generate leads for
        3. **Configure filters and ranking** criteria if you want to use them
        4. **Generate leads** by clicking the button in the Generate Leads tab
        5. **View results** in the Results tab
        6. **Export your leads** from the Export tab
        
        For best results:
        - Be specific with your industry selection
        - Use relevant keywords in the ranking criteria
        - Start with a smaller number of companies first to test
    """)