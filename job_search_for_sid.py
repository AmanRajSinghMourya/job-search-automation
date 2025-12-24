import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time
import re
import os

class AIMLJobSearcher:
    def __init__(self):
        self.jobs = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        # Sid's profile criteria for AI/ML roles
        self.min_stipend = 25000  # Rs per month
        self.min_ctc = 600000  # Rs per annum (6 LPA)

        # Google Sheet configuration (same as Punish)
        self.SHEET_ID = '1nridtqY_EkI47W8dcKOBhuMLCazepmH9JNPuDXyuYLA'

        # Web App URL (same as Punish)
        self.WEB_APP_URL = os.environ.get('WEB_APP_URL', '')

        # AI/ML focused company career pages
        self.company_career_pages = {
            # Top AI/ML Companies
            'Google AI': 'https://careers.google.com/jobs/results/?q=machine%20learning&location=India',
            'Microsoft AI': 'https://careers.microsoft.com/professionals/us/en/search-results?keywords=machine%20learning%20India',
            'Meta AI': 'https://www.metacareers.com/jobs?q=machine%20learning&location=India',
            'Amazon AWS AI': 'https://www.amazon.jobs/en/search?base_query=machine+learning&loc_query=India',
            'Apple ML': 'https://www.apple.com/careers/in/',
            'DeepMind': 'https://deepmind.google/careers/',
            'OpenAI': 'https://openai.com/careers/',
            'NVIDIA': 'https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite',
            'Intel AI': 'https://jobs.intel.com/en/search-jobs/India',

            # AI Research Labs & Startups
            'IBM Research': 'https://research.ibm.com/careers',
            'Adobe Research': 'https://research.adobe.com/careers/',
            'Qualcomm AI': 'https://www.qualcomm.com/company/careers',
            'Samsung AI': 'https://research.samsung.com/careers',
            'Uber AI': 'https://www.uber.com/us/en/careers/',

            # Indian AI Startups
            'Flipkart': 'https://www.flipkartcareers.com/',
            'Ola': 'https://www.olacabs.com/careers',
            'Swiggy': 'https://careers.swiggy.com/',
            'Zomato': 'https://www.zomato.com/careers',
            'Meesho': 'https://www.meesho.io/jobs',
            'PhonePe': 'https://www.phonepe.com/careers/job-openings/',
            'CRED': 'https://careers.cred.club/',
            'Razorpay': 'https://razorpay.com/jobs/',
            'Groww': 'https://groww.in/careers',

            # Data Science & Analytics
            'Fractal Analytics': 'https://fractal.ai/careers/',
            'Mu Sigma': 'https://www.mu-sigma.com/careers',
            'Tiger Analytics': 'https://www.tigeranalytics.com/careers/',
            'Tredence': 'https://www.tredence.com/careers',
            'Latent View': 'https://www.latentview.com/careers/',
            'AbsolutData': 'https://www.absolutdata.com/careers/',

            # Finance & Quant
            'Goldman Sachs': 'https://www.goldmansachs.com/careers/apply',
            'JP Morgan': 'https://careers.jpmorgan.com/in/en/home',
            'Morgan Stanley': 'https://www.morganstanley.com/careers/career-opportunities-search',
            'Two Sigma': 'https://www.twosigma.com/careers/',
            'Citadel': 'https://www.citadel.com/careers/',
            'DE Shaw': 'https://www.deshawindia.com/careers',
            'Tower Research': 'https://www.tower-research.com/careers',
            'WorldQuant': 'https://www.worldquant.com/careers/',

            # Healthcare AI
            'Optum': 'https://careers.unitedhealthgroup.com/',
            'Philips': 'https://www.careers.philips.com/',
            'GE Healthcare': 'https://jobs.gecareers.com/',
            'Siemens Healthineers': 'https://jobs.siemens.com/careers',

            # Cloud & MLOps
            'Databricks': 'https://www.databricks.com/company/careers',
            'Snowflake': 'https://careers.snowflake.com/',
            'Confluent': 'https://www.confluent.io/careers/',
            'MongoDB': 'https://www.mongodb.com/careers',
            'Elastic': 'https://www.elastic.co/careers/',

            # Consulting with AI Practice
            'McKinsey QuantumBlack': 'https://www.mckinsey.com/careers',
            'BCG Gamma': 'https://careers.bcg.com/',
            'Bain': 'https://www.bain.com/careers/',
            'Accenture AI': 'https://www.accenture.com/in-en/careers/jobsearch',
            'Deloitte AI': 'https://jobsindia.deloitte.com/viewalljobs/',

            # Semiconductor & Hardware AI
            'AMD': 'https://careers.amd.com/',
            'Marvell': 'https://marvell.wd1.myworkdayjobs.com/MarvellCareers',
            'Xilinx': 'https://careers.amd.com/',
            'Cadence': 'https://www.cadence.com/en_US/home/company/careers.html',
            'Synopsys': 'https://www.synopsys.com/careers.html',

            # Autonomous Vehicles & Robotics
            'Waymo': 'https://waymo.com/careers/',
            'Cruise': 'https://www.getcruise.com/careers',
            'Argo AI': 'https://www.argo.ai/join-us/',
            'Aurora': 'https://aurora.tech/careers',
            'Nuro': 'https://www.nuro.ai/careerslist',

            # Other AI-focused
            'Salesforce Einstein': 'https://www.salesforce.com/company/careers/',
            'ServiceNow': 'https://www.servicenow.com/careers.html',
            'Splunk': 'https://www.splunk.com/en_us/careers.html',
            'Palantir': 'https://www.palantir.com/careers/',
            'C3.ai': 'https://c3.ai/careers/',
            'DataRobot': 'https://www.datarobot.com/careers/',
            'H2O.ai': 'https://h2o.ai/company/careers/',
            'Scale AI': 'https://scale.com/careers',
            'Weights & Biases': 'https://wandb.ai/site/careers',
            'Hugging Face': 'https://huggingface.co/jobs',
            'Cohere': 'https://cohere.com/careers',
            'Anthropic': 'https://www.anthropic.com/careers',
            'Stability AI': 'https://stability.ai/careers',
        }

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
        """AI/ML focused LinkedIn search"""
        search_queries = [
            "Machine Learning Engineer Intern 2026",
            "AI Engineer Intern 2026",
            "Deep Learning Intern",
            "Data Scientist Intern 2026",
            "ML Research Intern",
            "Computer Vision Intern",
            "NLP Engineer Intern",
            "MLOps Intern",
            "AI Research Intern",
            "Data Science Intern",
            "Machine Learning Fresher",
            "AI Developer Intern",
            "Deep Learning Engineer",
            "LLM Engineer Intern",
            "GenAI Engineer Intern"
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
        """Search Internshala for AI/ML internships"""
        ai_ml_categories = [
            "machine%20learning",
            "artificial%20intelligence",
            "data%20science",
            "deep%20learning",
            "computer%20vision",
            "natural%20language%20processing",
            "python%20django%20machine%20learning"
        ]

        for category in ai_ml_categories:
            try:
                base_url = f"https://internshala.com/internships/{category}-internship/"
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

                time.sleep(2)

            except Exception as e:
                print(f"Internshala search error for '{category}': {e}")

    def search_naukri_targeted(self):
        """AI/ML focused Naukri search"""
        search_terms = [
            'machine-learning-engineer-intern',
            'ai-engineer-fresher',
            'data-scientist-intern',
            'deep-learning-intern',
            'nlp-engineer-intern',
            'computer-vision-intern',
            'ml-engineer-fresher',
            'data-science-intern-2026',
            'ai-ml-intern',
            'research-scientist-intern',
            'mlops-engineer-intern',
            'llm-engineer',
            'generative-ai-engineer'
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

    def search_company_career_pages(self):
        """Search AI/ML focused company career pages"""
        # Priority AI/ML companies to search
        priority_companies = [
            'Google AI', 'Microsoft AI', 'NVIDIA', 'Amazon AWS AI', 'Meta AI',
            'IBM Research', 'Adobe Research', 'Samsung AI', 'Intel AI',
            'Flipkart', 'Swiggy', 'Zomato', 'Meesho', 'PhonePe', 'CRED',
            'Fractal Analytics', 'Tiger Analytics', 'Tredence', 'Latent View',
            'Goldman Sachs', 'JP Morgan', 'Morgan Stanley', 'DE Shaw',
            'Databricks', 'Snowflake', 'MongoDB',
            'Palantir', 'Scale AI', 'DataRobot', 'H2O.ai'
        ]

        search_keywords = [
            'machine learning', 'ml', 'ai', 'artificial intelligence',
            'deep learning', 'data science', 'data scientist',
            'nlp', 'computer vision', 'intern', 'fresher', 'graduate',
            'research', 'llm', 'generative ai', '2025', '2026'
        ]

        jobs_found = 0

        for company in priority_companies:
            if company not in self.company_career_pages:
                continue

            career_url = self.company_career_pages[company]

            try:
                response = requests.get(career_url, headers=self.headers, timeout=15)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    page_text = soup.get_text().lower()

                    # Check if page has relevant AI/ML job listings
                    has_relevant_jobs = any(keyword in page_text for keyword in search_keywords)

                    if has_relevant_jobs:
                        job_elements = soup.find_all(['div', 'li', 'article'], class_=lambda x: x and any(
                            term in str(x).lower() for term in ['job', 'position', 'opening', 'career', 'listing', 'card']
                        ))

                        for elem in job_elements[:10]:
                            try:
                                title_elem = elem.find(['h2', 'h3', 'h4', 'a', 'span'], class_=lambda x: x and any(
                                    term in str(x).lower() for term in ['title', 'name', 'position', 'role', 'job-title']
                                ))

                                if title_elem:
                                    title_text = title_elem.get_text().strip()
                                    title_lower = title_text.lower()

                                    # Check if it's an AI/ML relevant role
                                    is_ai_ml = any(kw in title_lower for kw in [
                                        'machine learning', 'ml', 'ai', 'artificial intelligence',
                                        'deep learning', 'data scien', 'nlp', 'natural language',
                                        'computer vision', 'research', 'llm', 'generative'
                                    ])

                                    is_entry_level = any(kw in title_lower for kw in [
                                        'intern', 'fresher', 'graduate', 'entry', 'associate', 'junior', 'trainee'
                                    ])

                                    if (is_ai_ml or is_entry_level) and len(title_text) > 5 and len(title_text) < 150:
                                        link_elem = elem.find('a', href=True)
                                        job_link = ''
                                        if link_elem:
                                            href = link_elem.get('href', '')
                                            if href.startswith('http'):
                                                job_link = href
                                            elif href.startswith('/'):
                                                from urllib.parse import urlparse
                                                parsed = urlparse(career_url)
                                                job_link = f"{parsed.scheme}://{parsed.netloc}{href}"
                                            else:
                                                job_link = career_url

                                        job_type = 'Internship' if 'intern' in title_lower else 'Full-time'

                                        job_data = {
                                            'Company': company.replace(' AI', '').replace(' ML', ''),
                                            'Title': title_text,
                                            'Type': job_type,
                                            'Salary': 'Not disclosed',
                                            'Link': job_link if job_link else career_url,
                                            'Source': 'Company Career Page'
                                        }

                                        is_duplicate = any(
                                            j['Title'].lower() == title_text.lower() and j['Company'].lower() == job_data['Company'].lower()
                                            for j in self.jobs
                                        )

                                        if not is_duplicate:
                                            self.jobs.append(job_data)
                                            jobs_found += 1

                            except Exception as e:
                                continue

                time.sleep(2)

            except Exception as e:
                print(f"Career page search error for '{company}': {e}")
                continue

        return jobs_found

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
        if not self.SHEET_ID:
            return set(), set()

        try:
            csv_url = f"https://docs.google.com/spreadsheets/d/{self.SHEET_ID}/export?format=csv&gid=0"
            response = requests.get(csv_url, timeout=10)

            if response.status_code == 200:
                existing_links = set()
                existing_jobs = set()
                lines = response.text.strip().split('\n')

                for line in lines[1:]:
                    parts = line.split(',')
                    if len(parts) >= 5:
                        company = parts[0].strip('"').lower()
                        title = parts[1].strip('"').lower()
                        link = parts[4].strip('"')

                        if link and link != 'Apply Link':
                            existing_links.add(link)

                        if company and title and company != 'company' and title != 'title':
                            existing_jobs.add((title, company))

                return existing_links, existing_jobs
        except Exception as e:
            print(f"Could not fetch existing jobs: {e}")

        return set(), set()

    def send_to_webapp(self, formatted_jobs, add_separator=True):
        """Send jobs to Google Apps Script Web App with optional separator"""
        if not self.WEB_APP_URL:
            print("  WEB_APP_URL not set. Jobs will be saved to JSON only.")
            return False

        try:
            jobs_to_send = []

            if add_separator and formatted_jobs:
                now = datetime.now()
                separator_time = now.strftime('%d %b, %Y %I:%M %p').replace(' 0', ' ')

                jobs_to_send.append({
                    'Company': '',
                    'Title': '',
                    'Type': '',
                    'Stipend/CTC': '',
                    'Apply Link': '',
                    'Last Updated': ''
                })

                jobs_to_send.append({
                    'Company': f'---- NEW AI/ML JOBS ADDED ON {separator_time} ----',
                    'Title': '',
                    'Type': '',
                    'Stipend/CTC': '',
                    'Apply Link': '',
                    'Last Updated': separator_time
                })

                jobs_to_send.append({
                    'Company': '',
                    'Title': '',
                    'Type': '',
                    'Stipend/CTC': '',
                    'Apply Link': '',
                    'Last Updated': ''
                })

            jobs_to_send.extend(formatted_jobs)

            response = requests.post(
                self.WEB_APP_URL,
                json={'jobs': jobs_to_send},
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                print(f"Web App Response: {result.get('message', 'Success')}")
                return True
            else:
                print(f"Web App returned status: {response.status_code}")
                return False

        except Exception as e:
            print(f"Error sending to Web App: {e}")
            return False

    def process_and_save_jobs(self):
        """Process jobs and send to Google Sheet"""
        try:
            self.remove_duplicates()
            existing_links, existing_jobs = self.get_existing_jobs_from_sheet()

            new_jobs = []
            for job in self.jobs:
                if not job['Link']:
                    continue

                if job['Link'] in existing_links:
                    continue

                job_identifier = (job['Title'].lower(), job['Company'].lower())
                if job_identifier in existing_jobs:
                    continue

                new_jobs.append(job)

            if new_jobs:
                formatted_jobs = []
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

                success = self.send_to_webapp(formatted_jobs)

                if success:
                    print(f"\nSuccessfully sent {len(new_jobs)} AI/ML jobs to Google Sheet!")
                else:
                    print(f"\nCould not send to Google Sheet. Check WEB_APP_URL_SID.")

                print("\nSample of new AI/ML jobs:")
                for i, job in enumerate(formatted_jobs[:5], 1):
                    print(f"\n{i}. {job['Company']} - {job['Title']}")
                    print(f"   Type: {job['Type']} | Salary: {job['Stipend/CTC']}")
                    print(f"   Link: {job['Apply Link'][:70]}...")

                return len(new_jobs), formatted_jobs
            else:
                print("No new AI/ML jobs found in this search")
                return 0, []

        except Exception as e:
            print(f"Error processing jobs: {e}")
            return 0, []

def main():
    print("=" * 70)
    print("AUTOMATED AI/ML JOB SEARCH FOR SID")
    print("=" * 70)
    print(f"Search time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}")
    print(f"Target: AI/ML/Deep Learning Internships & Jobs for 2026 Batch")
    print(f"Min Stipend: Rs.25,000/month | Min CTC: Rs.6 LPA")
    print(f"Recipient: Sid")
    print(f"Focus Areas: Machine Learning, Deep Learning, Data Science, NLP, CV")
    print(f"Sources: LinkedIn, Naukri, Internshala + AI/ML Company Career Pages")
    print("=" * 70)

    searcher = AIMLJobSearcher()

    # Run all searches
    print("\nSearching LinkedIn for AI/ML roles...")
    searcher.search_linkedin_api_style()
    print(f"   Found {len(searcher.jobs)} listings")

    print("\nSearching Naukri for AI/ML roles...")
    initial_count = len(searcher.jobs)
    searcher.search_naukri_targeted()
    print(f"   Found {len(searcher.jobs) - initial_count} new listings")

    print("\nSearching Internshala for AI/ML internships...")
    initial_count = len(searcher.jobs)
    searcher.search_internshala()
    print(f"   Found {len(searcher.jobs) - initial_count} new listings")

    print("\nSearching AI/ML Company Career Pages...")
    initial_count = len(searcher.jobs)
    career_jobs = searcher.search_company_career_pages()
    print(f"   Found {len(searcher.jobs) - initial_count} new listings from company career pages")

    # Process and send jobs
    print("\n" + "=" * 70)
    print("Processing AI/ML jobs and sending to Google Sheet...")
    new_jobs_count, formatted_jobs = searcher.process_and_save_jobs()

    print("=" * 70)
    print(f"SEARCH COMPLETE!")
    print(f"Total AI/ML jobs searched: {len(searcher.jobs)}")
    print(f"New jobs found: {new_jobs_count}")
    print(f"Jobs sent to Google Sheet")
    print("=" * 70)

if __name__ == "__main__":
    main()
