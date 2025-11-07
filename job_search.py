import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json
import time
import os

class JobSearcher:
    def __init__(self):
        self.jobs = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    def search_linkedin_jobs(self):
        """Search LinkedIn for AI/ML internships and jobs"""
        keywords = ['AI ML intern', 'Machine Learning intern', 'AI Engineer fresher']
        
        for keyword in keywords:
            try:
                url = f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '%20')}&location=India&f_E=2&f_TPR=r86400"
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    job_cards = soup.find_all('div', class_='base-card')
                    
                    for card in job_cards[:10]:  # Limit to top 10 per keyword
                        try:
                            title = card.find('h3', class_='base-search-card__title')
                            company = card.find('h4', class_='base-search-card__subtitle')
                            location = card.find('span', class_='job-search-card__location')
                            link = card.find('a', class_='base-card__full-link')
                            
                            if title and company and link:
                                self.jobs.append({
                                    'Title': title.text.strip(),
                                    'Company': company.text.strip(),
                                    'Location': location.text.strip() if location else 'Not specified',
                                    'Link': link['href'],
                                    'Source': 'LinkedIn',
                                    'Date_Found': datetime.now().strftime('%Y-%m-%d'),
                                    'Status': 'New'
                                })
                        except Exception as e:
                            continue
                            
                time.sleep(2)  # Rate limiting
            except Exception as e:
                print(f"Error searching LinkedIn for {keyword}: {e}")
                
    def search_naukri_jobs(self):
        """Search Naukri.com for AI/ML jobs"""
        keywords = ['AI-ML-intern', 'Machine-Learning-fresher', 'Deep-Learning-intern']
        
        for keyword in keywords:
            try:
                url = f"https://www.naukri.com/{keyword}-jobs"
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    job_tuples = soup.find_all('article', class_='jobTuple')
                    
                    for job in job_tuples[:10]:
                        try:
                            title_elem = job.find('a', class_='title')
                            company_elem = job.find('a', class_='subTitle')
                            salary_elem = job.find('span', class_='salary')
                            link_elem = job.find('a', class_='title')
                            
                            if title_elem and company_elem:
                                salary_text = salary_elem.text.strip() if salary_elem else 'Not disclosed'
                                
                                # Filter by minimum salary if disclosed
                                if salary_elem and ('lakh' in salary_text.lower() or 'lac' in salary_text.lower()):
                                    # Extract salary number
                                    salary_parts = salary_text.split('-')
                                    if len(salary_parts) > 0:
                                        first_num = ''.join(filter(str.isdigit, salary_parts[0]))
                                        if first_num and int(first_num) < 12:
                                            continue  # Skip if less than 12 LPA
                                
                                self.jobs.append({
                                    'Title': title_elem.text.strip(),
                                    'Company': company_elem.text.strip(),
                                    'Location': 'India',
                                    'Link': f"https://www.naukri.com{link_elem['href']}" if link_elem else '',
                                    'Source': 'Naukri',
                                    'Date_Found': datetime.now().strftime('%Y-%m-%d'),
                                    'Status': 'New',
                                    'Salary': salary_text
                                })
                        except Exception as e:
                            continue
                            
                time.sleep(2)
            except Exception as e:
                print(f"Error searching Naukri for {keyword}: {e}")
    
    def search_instahire(self):
        """Search Instahire for internships"""
        try:
            url = "https://www.instahyre.com/search-jobs/?category=machine-learning-data-science"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                job_cards = soup.find_all('div', class_='job-card')
                
                for card in job_cards[:15]:
                    try:
                        title = card.find('h3')
                        company = card.find('p', class_='company-name')
                        salary = card.find('span', class_='salary')
                        link = card.find('a')
                        
                        if title and company:
                            self.jobs.append({
                                'Title': title.text.strip(),
                                'Company': company.text.strip(),
                                'Location': 'India',
                                'Link': f"https://www.instahyre.com{link['href']}" if link else '',
                                'Source': 'Instahyre',
                                'Date_Found': datetime.now().strftime('%Y-%m-%d'),
                                'Status': 'New',
                                'Salary': salary.text.strip() if salary else 'Not disclosed'
                            })
                    except Exception as e:
                        continue
        except Exception as e:
            print(f"Error searching Instahyre: {e}")
    
    def search_wellfound(self):
        """Search Wellfound (AngelList) for startup jobs"""
        try:
            url = "https://wellfound.com/role/l/machine-learning-engineer/india"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Wellfound uses React, so scraping might be limited
                # This is a placeholder - you might need to use their API
                print("Wellfound search attempted - may need API access")
        except Exception as e:
            print(f"Error searching Wellfound: {e}")
    
    def update_excel(self, filename='jobs.xlsx'):
        """Update Excel file with new jobs"""
        try:
            # Try to read existing file
            try:
                existing_df = pd.read_excel(filename)
                existing_links = set(existing_df['Link'].values)
            except FileNotFoundError:
                existing_df = pd.DataFrame()
                existing_links = set()
            
            # Filter out duplicate jobs
            new_jobs = [job for job in self.jobs if job['Link'] not in existing_links]
            
            if new_jobs:
                new_df = pd.DataFrame(new_jobs)
                
                # Combine with existing data
                if not existing_df.empty:
                    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
                else:
                    combined_df = new_df
                
                # Sort by date
                combined_df = combined_df.sort_values('Date_Found', ascending=False)
                
                # Save to Excel
                combined_df.to_excel(filename, index=False)
                print(f"Added {len(new_jobs)} new jobs to {filename}")
                return len(new_jobs)
            else:
                print("No new jobs found")
                return 0
                
        except Exception as e:
            print(f"Error updating Excel: {e}")
            return 0

def main():
    print("Starting job search...")
    print(f"Search time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    searcher = JobSearcher()
    
    # Run all searches
    print("Searching LinkedIn...")
    searcher.search_linkedin_jobs()
    
    print("Searching Naukri...")
    searcher.search_naukri_jobs()
    
    print("Searching Instahire...")
    searcher.search_instahire()
    
    print("Searching Wellfound...")
    searcher.search_wellfound()
    
    # Update Excel
    new_jobs_count = searcher.update_excel()
    
    print(f"Search complete! Found {len(searcher.jobs)} total jobs, {new_jobs_count} new jobs added.")

if __name__ == "__main__":
    main()
