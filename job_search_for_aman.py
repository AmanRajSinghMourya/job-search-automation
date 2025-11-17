import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time
import re
import os

class SimpleJobSearcher:
    def __init__(self):
        self.jobs = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        # Your profile criteria
        self.min_stipend = 25000  # Rs per month
        self.min_ctc = 600000  # Rs per annum

        # Google Sheet configuration
        self.SHEET_ID = '1bDP0P9WGmPCi54pYOxiUu34ewuIHDW-12b7dsFRnre8'

        # Web App URL (you'll set this in GitHub Secrets)
        self.WEB_APP_URL = os.environ.get('WEB_APP_URL_AMAN', '')

    def extract_salary(self, salary_text):
        """Extract numeric salary from text"""
        if not salary_text or salary_text == 'Not disclosed':
            return None

        salary_text = salary_text.replace(',', '').lower()
        numbers = re.findall(r'\d+\.?\d*', salary_text)
        if not numbers:
            return None

        salary = float(numbers[0])

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
                if 'intern' in job_data['Title'].lower():
                    if salary < (self.min_stipend * 12):
                        return False
                else:
                    if salary < self.min_ctc:
                        return False
        return True

    def format_salary_for_sheet(self, salary_text, job_type):
        """Format salary for Google Sheets display"""
        if not salary_text or salary_text == 'Not disclosed':
            return 'Not disclosed'

        salary = self.extract_salary(salary_text)
        if not salary:
            return salary_text

        if 'intern' in job_type.lower():
            monthly = salary / 12
            return f'₹{int(monthly):,}/month'
        else:
            lpa = salary / 100000
            return f'₹{lpa:.1f} LPA'

    def search_linkedin_api_style(self):
        """More targeted LinkedIn search"""
        search_queries = [
            "Software Engineer Intern 2026",
            "SDE Intern 2026",
            "Frontend Developer Intern",
            "Backend Developer Intern",
            "Full Stack Developer Intern",
            "React Developer Intern",
            "C++ Developer Intern",
            "Cyber Security Intern"
        ]

        for query in search_queries:
            try:
                encoded_query = query.replace(' ', '%20')
                url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={encoded_query}&location=India&f_E=2%2C1&f_TPR=r86400&start=0"

                response = requests.get(url, headers=self.headers, timeout=10)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    job_listings = soup.find_all('li')

                    for listing in job_listings[:5]:
                        try:
                            title_elem = listing.find('h3', class_='base-search-card__title')
                            company_elem = listing.find('h4', class_='base-search-card__subtitle')
                            link_elem = listing.find('a', class_='base-card__full-link')

                            if title_elem and company_elem and link_elem:
                                job_type = 'Internship' if 'intern' in title_elem.text.lower() else 'Full-time'

                                job_data = {
                                    'Company': company_elem.text.strip(),
                                    'Title': title_elem.text.strip(),
                                    'Type': job_type,
                                    'Salary': 'Not disclosed',
                                    'Link': link_elem.get('href', ''),
                                    'Source': 'LinkedIn'
                                }

                                self.jobs.append(job_data)
                        except Exception as e:
                            continue

                time.sleep(3)

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

                for internship in internships[:10]:
                    try:
                        title = internship.find('h3', class_='job-title')
                        company = internship.find('p', class_='company-name')
                        stipend = internship.find('span', class_='stipend')
                        link = internship.find('a', class_='view_detail_button')

                        if title and company:
                            stipend_text = stipend.text.strip() if stipend else 'Not disclosed'

                            job_data = {
                                'Company': company.text.strip(),
                                'Title': title.text.strip(),
                                'Type': 'Internship',
                                'Salary': stipend_text,
                                'Link': f"https://internshala.com{link['href']}" if link else '',
                                'Source': 'Internshala'
                            }

                            if self.matches_criteria(job_data):
                                self.jobs.append(job_data)

                    except Exception as e:
                        continue

        except Exception as e:
            print(f"Internshala search error: {e}")

    def search_naukri_targeted(self):
        """Enhanced Naukri search"""
        search_terms = [
            'machine-learning-engineer-intern',
            'ai-engineer-fresher',
            'data-scientist-intern',
            'spring-boot-developer-intern',
            'java-developer-intern-2026'
        ]

        for term in search_terms:
            try:
                url = f"https://www.naukri.com/{term}-jobs-in-india"
                response = requests.get(url, headers=self.headers, timeout=10)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    articles = soup.find_all('article', class_='jobTuple')

                    for article in articles[:5]:
                        try:
                            title = article.find('a', class_='title')
                            company = article.find('a', class_='subTitle')
                            salary = article.find('span', class_='salary')
                            experience = article.find('span', class_='expwdth')

                            if title and company:
                                exp_text = experience.text.strip() if experience else ''
                                if 'years' in exp_text.lower():
                                    exp_num = re.findall(r'\d+', exp_text)
                                    if exp_num and int(exp_num[0]) > 2:
                                        continue

                                salary_text = salary.text.strip() if salary else 'Not disclosed'
                                job_type = 'Internship' if 'intern' in title.text.lower() else 'Full-time'

                                job_data = {
                                    'Company': company.text.strip(),
                                    'Title': title.text.strip(),
                                    'Type': job_type,
                                    'Salary': salary_text,
                                    'Link': f"https://www.naukri.com{title['href']}" if title else '',
                                    'Source': 'Naukri'
                                }

                                if self.matches_criteria(job_data):
                                    self.jobs.append(job_data)

                        except Exception as e:
                            continue

                time.sleep(2)

            except Exception as e:
                print(f"Naukri search error for '{term}': {e}")

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

    def get_existing_jobs_from_sheet(self):
        """Fetch existing jobs from Google Sheet to avoid duplicates"""
        try:
            csv_url = f"https://docs.google.com/spreadsheets/d/{self.SHEET_ID}/export?format=csv&gid=0"
            response = requests.get(csv_url, timeout=10)

            if response.status_code == 200:
                existing_links = set()
                lines = response.text.strip().split('\n')

                for line in lines[1:]:
                    parts = line.split(',')
                    if len(parts) >= 5:
                        link = parts[4].strip('"')
                        if link and link != 'Apply Link':
                            existing_links.add(link)

                return existing_links
        except Exception as e:
            print(f"Could not fetch existing jobs: {e}")

        return set()

    def send_to_webapp(self, formatted_jobs):
        """Send jobs to Google Apps Script Web App"""
        if not self.WEB_APP_URL:
            print("⚠️  WEB_APP_URL not set. Jobs will be saved to JSON only.")
            return False

        try:
            response = requests.post(
                self.WEB_APP_URL,
                json={'jobs': formatted_jobs},
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                print(f"✅ Web App Response: {result.get('message', 'Success')}")
                return True
            else:
                print(f"❌ Web App returned status: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Error sending to Web App: {e}")
            return False

    def process_and_save_jobs(self):
        """Process jobs and send to Google Sheet"""
        try:
            self.remove_duplicates()
            existing_links = self.get_existing_jobs_from_sheet()

            new_jobs = [job for job in self.jobs if job['Link'] not in existing_links and job['Link']]

            if new_jobs:
                formatted_jobs = []
                # Format: "07 Nov, 2025 5:30 PM"
                now = datetime.now()
                current_time = now.strftime('%d %b, %Y %I:%M %p').replace(' 0', ' ')

                for job in new_jobs:
                    formatted_salary = self.format_salary_for_sheet(job['Salary'], job['Type'])

                    formatted_jobs.append({
                        'Company': job['Company'],
                        'Title': job['Title'],
                        'Type': job['Type'],
                        'Stipend/CTC': formatted_salary,
                        'Apply Link': job['Link'],
                        'Last Updated': current_time
                    })

                # Send to Web App
                success = self.send_to_webapp(formatted_jobs)

                if success:
                    print(f"\n✅ Successfully sent {len(new_jobs)} jobs to Google Sheet!")
                else:
                    print(f"\n⚠️  Could not send to Google Sheet. Check WEB_APP_URL.")

                print("\n📋 Sample of new jobs:")
                for i, job in enumerate(formatted_jobs[:3], 1):
                    print(f"\n{i}. {job['Company']} - {job['Title']}")
                    print(f"   Type: {job['Type']} | Salary: {job['Stipend/CTC']}")
                    print(f"   Link: {job['Apply Link'][:70]}...")

                return len(new_jobs), formatted_jobs
            else:
                print("ℹ️  No new jobs found in this search")
                return 0, []

        except Exception as e:
            print(f"❌ Error processing jobs: {e}")
            return 0, []

def main():
    print("=" * 70)
    print("🔍 AUTOMATED JOB SEARCH FOR AMAN")
    print("=" * 70)
    print(f"⏰ Search time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}")
    print(f"🎯 Target: SDE & Development Internships/Jobs for 2026 Batch")
    print(f"💰 Min Stipend: ₹25,000/month | Min CTC: ₹6 LPA")
    print(f"📧 Recipient: Aman")
    print("=" * 70)

    searcher = SimpleJobSearcher()

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

    # Process and send jobs
    print("\n" + "=" * 70)
    print("💾 Processing jobs and sending to Google Sheet...")
    new_jobs_count, formatted_jobs = searcher.process_and_save_jobs()

    print("=" * 70)
    print(f"✅ SEARCH COMPLETE!")
    print(f"📈 Total jobs searched: {len(searcher.jobs)}")
    print(f"🆕 New jobs found: {new_jobs_count}")
    print(f"📊 Jobs sent to Google Sheet")
    print(f"📧 Your email automation will send notifications")
    print("=" * 70)

if __name__ == "__main__":
    main()
