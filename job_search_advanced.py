import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import json
import time
import re

class AdvancedJobSearcher:
    def __init__(self):
        self.jobs = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        # Your profile criteria
        self.skills = ['Spring Boot', 'Java', 'Machine Learning', 'Python', 'AWS', 'ReactJS', 'TensorFlow', 'OpenCV']
        self.min_stipend = 35000  # Rs per month
        self.min_ctc = 1200000  # Rs per annum
        self.graduation_year = 2026
        
    def extract_salary(self, salary_text):
        """Extract numeric salary from text"""
        if not salary_text or salary_text == 'Not disclosed':
            return None
            
        # Remove commas and convert to lowercase
        salary_text = salary_text.replace(',', '').lower()
        
        # Extract numbers
        numbers = re.findall(r'\d+\.?\d*', salary_text)
        if not numbers:
            return None
            
        salary = float(numbers[0])
        
        # Convert to annual salary in Rs
        if 'lpa' in salary_text or 'lac' in salary_text or 'lakh' in salary_text:
            salary = salary * 100000
        elif 'k' in salary_text and 'month' in salary_text:
            salary = salary * 1000 * 12
        elif 'month' in salary_text:
            salary = salary * 12
            
        return salary
    
    def matches_criteria(self, job_data):
        """Check if job matches minimum criteria"""
        if 'Salary' in job_data and job_data['Salary'] != 'Not disclosed':
            salary = self.extract_salary(job_data['Salary'])
            if salary:
                # For internships
                if 'intern' in job_data['Title'].lower():
                    if salary < (self.min_stipend * 12):
                        return False
                # For full-time roles
                else:
                    if salary < self.min_ctc:
                        return False
        
        return True
    
    def search_linkedin_api_style(self):
        """More targeted LinkedIn search"""
        search_queries = [
            'AI ML Intern 2026',
            'Machine Learning Intern 2026 graduate',
            'ML Engineer fresher',
            'Data Scientist intern',
            'Deep Learning Intern',
            'Computer Vision Intern',
            'NLP Engineer fresher'
        ]
        
        for query in search_queries:
            try:
                # LinkedIn Jobs API (public listings)
                encoded_query = query.replace(' ', '%20')
                url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={encoded_query}&location=India&f_E=2%2C1&f_TPR=r86400&start=0"
                
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    job_listings = soup.find_all('li')
                    
                    for listing in job_listings[:8]:
                        try:
                            title_elem = listing.find('h3', class_='base-search-card__title')
                            company_elem = listing.find('h4', class_='base-search-card__subtitle')
                            location_elem = listing.find('span', class_='job-search-card__location')
                            link_elem = listing.find('a', class_='base-card__full-link')
                            time_elem = listing.find('time')
                            
                            if title_elem and company_elem and link_elem:
                                job_link = link_elem.get('href', '')
                                
                                job_data = {
                                    'Title': title_elem.text.strip(),
                                    'Company': company_elem.text.strip(),
                                    'Location': location_elem.text.strip() if location_elem else 'India',
                                    'Link': job_link,
                                    'Source': 'LinkedIn',
                                    'Date_Found': datetime.now().strftime('%Y-%m-%d'),
                                    'Posted': time_elem.get('datetime') if time_elem else 'Recently',
                                    'Status': 'New',
                                    'Salary': 'Not disclosed'
                                }
                                
                                self.jobs.append(job_data)
                        except Exception as e:
                            continue
                
                time.sleep(3)  # Rate limiting
                
            except Exception as e:
                print(f"LinkedIn search error for '{query}': {e}")
    
    def search_internshala(self):
        """Search Internshala for high-paying internships"""
        try:
            base_url = "https://internshala.com/internships/machine%20learning,artificial%20intelligence,data%20science-internship/"
            
            response = requests.get(base_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                internships = soup.find_all('div', class_='individual_internship')
                
                for internship in internships[:15]:
                    try:
                        title = internship.find('h3', class_='job-title')
                        company = internship.find('p', class_='company-name')
                        stipend = internship.find('span', class_='stipend')
                        link = internship.find('a', class_='view_detail_button')
                        
                        if title and company:
                            stipend_text = stipend.text.strip() if stipend else 'Not disclosed'
                            
                            job_data = {
                                'Title': title.text.strip(),
                                'Company': company.text.strip(),
                                'Location': 'India',
                                'Link': f"https://internshala.com{link['href']}" if link else '',
                                'Source': 'Internshala',
                                'Date_Found': datetime.now().strftime('%Y-%m-%d'),
                                'Status': 'New',
                                'Salary': stipend_text
                            }
                            
                            # Filter by minimum stipend
                            if self.matches_criteria(job_data):
                                self.jobs.append(job_data)
                                
                    except Exception as e:
                        continue
                        
        except Exception as e:
            print(f"Internshala search error: {e}")
    
    def search_naukri_targeted(self):
        """Enhanced Naukri search with better filtering"""
        search_terms = [
            'machine-learning-engineer-intern',
            'ai-engineer-fresher',
            'data-scientist-intern',
            'ml-engineer-0-1-years',
            'computer-vision-intern',
            'nlp-engineer-fresher'
        ]
        
        for term in search_terms:
            try:
                url = f"https://www.naukri.com/{term}-jobs-in-india"
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    articles = soup.find_all('article', class_='jobTuple')
                    
                    for article in articles[:10]:
                        try:
                            title = article.find('a', class_='title')
                            company = article.find('a', class_='subTitle')
                            salary = article.find('span', class_='salary')
                            experience = article.find('span', class_='expwdth')
                            
                            if title and company:
                                # Filter for freshers/interns
                                exp_text = experience.text.strip() if experience else ''
                                if 'years' in exp_text.lower():
                                    exp_num = re.findall(r'\d+', exp_text)
                                    if exp_num and int(exp_num[0]) > 2:
                                        continue  # Skip if > 2 years required
                                
                                salary_text = salary.text.strip() if salary else 'Not disclosed'
                                
                                job_data = {
                                    'Title': title.text.strip(),
                                    'Company': company.text.strip(),
                                    'Location': 'India',
                                    'Link': f"https://www.naukri.com{title['href']}" if title else '',
                                    'Source': 'Naukri',
                                    'Date_Found': datetime.now().strftime('%Y-%m-%d'),
                                    'Status': 'New',
                                    'Salary': salary_text,
                                    'Experience': exp_text
                                }
                                
                                if self.matches_criteria(job_data):
                                    self.jobs.append(job_data)
                                    
                        except Exception as e:
                            continue
                
                time.sleep(2)
                
            except Exception as e:
                print(f"Naukri search error for '{term}': {e}")
    
    def search_wellfound_startups(self):
        """Search Wellfound for startup opportunities"""
        roles = ['machine-learning-engineer', 'data-scientist', 'ai-engineer']
        
        for role in roles:
            try:
                url = f"https://wellfound.com/role/r/{role}?locations=India&experience=junior"
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    # Wellfound uses React, so we might get limited data
                    # Consider using their API for better results
                    print(f"Wellfound search for {role} - may need API integration")
                    
            except Exception as e:
                print(f"Wellfound search error: {e}")
    
    def search_cutshort(self):
        """Search Cutshort for tech jobs"""
        try:
            url = "https://cutshort.io/jobs/machine-learning-jobs-in-india"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                job_cards = soup.find_all('div', class_='job-card')
                
                for card in job_cards[:10]:
                    try:
                        title = card.find('h2')
                        company = card.find('h3')
                        salary = card.find('span', class_='salary')
                        link = card.find('a')
                        
                        if title and company:
                            job_data = {
                                'Title': title.text.strip(),
                                'Company': company.text.strip(),
                                'Location': 'India',
                                'Link': f"https://cutshort.io{link['href']}" if link else '',
                                'Source': 'Cutshort',
                                'Date_Found': datetime.now().strftime('%Y-%m-%d'),
                                'Status': 'New',
                                'Salary': salary.text.strip() if salary else 'Not disclosed'
                            }
                            
                            if self.matches_criteria(job_data):
                                self.jobs.append(job_data)
                                
                    except Exception as e:
                        continue
                        
        except Exception as e:
            print(f"Cutshort search error: {e}")
    
    def remove_duplicates(self):
        """Remove duplicate job listings"""
        seen = set()
        unique_jobs = []
        
        for job in self.jobs:
            identifier = (job['Title'].lower(), job['Company'].lower())
            if identifier not in seen:
                seen.add(identifier)
                unique_jobs.append(job)
        
        self.jobs = unique_jobs
    
    def update_excel(self, filename='jobs.xlsx'):
        """Update Excel file with new jobs"""
        try:
            # Remove duplicates in current search
            self.remove_duplicates()
            
            # Try to read existing file
            try:
                existing_df = pd.read_excel(filename)
                existing_links = set(existing_df['Link'].values)
            except FileNotFoundError:
                existing_df = pd.DataFrame()
                existing_links = set()
            
            # Filter out jobs that already exist
            new_jobs = [job for job in self.jobs if job['Link'] not in existing_links and job['Link']]
            
            if new_jobs:
                new_df = pd.DataFrame(new_jobs)
                
                # Combine with existing data
                if not existing_df.empty:
                    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
                else:
                    combined_df = new_df
                
                # Sort by date found (newest first)
                combined_df = combined_df.sort_values('Date_Found', ascending=False)
                
                # Save to Excel with formatting
                with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                    combined_df.to_excel(writer, index=False, sheet_name='Jobs')
                    
                    # Get the worksheet
                    worksheet = writer.sheets['Jobs']
                    
                    # Auto-adjust column widths
                    for column in worksheet.columns:
                        max_length = 0
                        column = [cell for cell in column]
                        for cell in column:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except:
                                pass
                        adjusted_width = min(max_length + 2, 50)
                        worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
                
                print(f"✅ Added {len(new_jobs)} new jobs to {filename}")
                print(f"📊 Total jobs in database: {len(combined_df)}")
                return len(new_jobs)
            else:
                print("ℹ️  No new jobs found in this search")
                return 0
                
        except Exception as e:
            print(f"❌ Error updating Excel: {e}")
            return 0

def main():
    print("=" * 60)
    print("🔍 AUTOMATED JOB SEARCH")
    print("=" * 60)
    print(f"⏰ Search time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}")
    print(f"🎯 Target: AI/ML Internships & Fresher Roles")
    print(f"💰 Min Stipend: ₹35,000/month | Min CTC: ₹12 LPA")
    print("=" * 60)
    
    searcher = AdvancedJobSearcher()
    
    # Run all searches
    print("\n🔎 Searching LinkedIn...")
    searcher.search_linkedin_api_style()
    print(f"   Found {len(searcher.jobs)} listings")
    
    print("\n🔎 Searching Naukri...")
    initial_count = len(searcher.jobs)
    searcher.search_naukri_targeted()
    print(f"   Found {len(searcher.jobs) - initial_count} new listings")
    
    print("\n🔎 Searching Internshala...")
    initial_count = len(searcher.jobs)
    searcher.search_internshala()
    print(f"   Found {len(searcher.jobs) - initial_count} new listings")
    
    print("\n🔎 Searching Cutshort...")
    initial_count = len(searcher.jobs)
    searcher.search_cutshort()
    print(f"   Found {len(searcher.jobs) - initial_count} new listings")
    
    print("\n🔎 Searching Wellfound...")
    searcher.search_wellfound_startups()
    
    # Update Excel
    print("\n" + "=" * 60)
    print("💾 Updating Excel file...")
    new_jobs_count = searcher.update_excel()
    
    print("=" * 60)
    print(f"✅ SEARCH COMPLETE!")
    print(f"📈 Total jobs found: {len(searcher.jobs)}")
    print(f"🆕 New jobs added: {new_jobs_count}")
    print("=" * 60)

if __name__ == "__main__":
    main()
