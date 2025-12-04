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
        self.min_stipend = 20000  # Rs per month
        self.min_ctc = 500000  # Rs per annum

        # Google Sheet configuration
        self.SHEET_ID = '1nridtqY_EkI47W8dcKOBhuMLCazepmH9JNPuDXyuYLA'

        # Web App URL (you'll set this in GitHub Secrets)
        self.WEB_APP_URL = os.environ.get('WEB_APP_URL', '')

        # Company career pages from placement tracker (BTech 2026)
        self.company_career_pages = {
            # Top Tech Companies
            'Google': 'https://careers.google.com/jobs/results/?location=India',
            'Microsoft': 'https://careers.microsoft.com/professionals/us/en/search-results?keywords=India',
            'Amazon': 'https://www.amazon.jobs/en/search?base_query=&loc_query=India&country=IND',
            'Apple': 'https://www.apple.com/careers/in/',
            'Adobe': 'https://www.adobe.com/careers.html',
            'Flipkart': 'https://www.flipkartcareers.com/',
            'Meesho': 'https://www.meesho.io/jobs',
            'Zomato': 'https://www.zomato.com/careers',
            'PhonePe': 'https://www.phonepe.com/careers/job-openings/',
            'Intuit': 'https://www.intuit.com/in/careers/',

            # Finance & Banking
            'Goldman Sachs': 'https://www.goldmansachs.com/careers/apply',
            'JP Morgan': 'https://careers.jpmorgan.com/in/en/home',
            'Morgan Stanley': 'https://www.morganstanley.com/careers/career-opportunities-search',
            'American Express': 'https://jobs.americanexpress.com/india/jobs',
            'Visa': 'https://corporate.visa.com/en/jobs/',
            'PayPal': 'https://www.paypal.com/in/webapps/mpp/jobs/locations',
            'Wells Fargo': 'https://www.wellsfargojobs.com/en/jobs/',
            'Citi': 'https://jobs.citi.com/search-jobs/India',
            'Bank of New York Mellon': 'https://bfryrsc.wd1.myworkdayjobs.com/BK',
            'BlackRock': 'https://careers.blackrock.com/location/india-jobs/45831/1269750/2',
            'UBS': 'https://www.ubs.com/global/en/careers.html',
            'IDFC': 'https://www.idfcfirstbank.com/careers',
            'DBS': 'https://www.dbs.com/careers/',
            'BNP Paribas': 'https://careers.bnpparibas.com/index.html',
            'MUFG': 'https://careers.mufgamericas.com/',
            'HSBC': 'https://www.hsbc.com/careers',

            # Tech & Software
            'Cisco': 'https://jobs.cisco.com/jobs/SearchJobs/India',
            'Oracle': 'https://careers.oracle.com/en/sites/jobsearch/jobs?location=India&locationId=300000000106947&locationLevel=country&mode=location',
            'Dell': 'https://jobs.dell.com/en/india-jobs',
            'HP': 'https://jobs.hp.com/',
            'HPE': 'https://careers.hpe.com/jobs',
            'IBM': 'https://www.ibm.com/careers/search?field_keyword_08[0]=India',
            'Infosys': 'https://www.infosys.com/careers/apply.html',
            'Accenture': 'https://www.accenture.com/in-en/careers/jobsearch',
            'Deloitte': 'https://jobsindia.deloitte.com/viewalljobs/',
            'Cognizant': 'https://careers.cognizant.com/global-en/',
            'TCS': 'https://www.tcs.com/careers',
            'Wipro': 'https://careers.wipro.com/',
            'LTIMindtree': 'https://www.ltimindtree.com/careers/',
            'Tech Mahindra': 'https://careers.techmahindra.com/',
            'HCL': 'https://www.hcltech.com/careers',
            'Marvell': 'https://marvell.wd1.myworkdayjobs.com/MarvellCareers',
            'Nutanix': 'https://careers.nutanix.com/en/jobs/',
            'Commvault': 'https://careers.commvault.com/',
            'Couchbase': 'https://www.couchbase.com/careers/',
            'Workday': 'https://www.workday.com/en-us/company/careers/open-positions.html',
            'OKTA': 'https://www.okta.com/company/careers/job-listing/',
            'Juniper Networks': 'https://jobs.juniper.net/',
            'Samsung': 'https://www.samsung.com/in/about-us/careers/',
            'AMD': 'https://careers.amd.com/',
            'Qualcomm': 'https://www.qualcomm.com/company/careers',

            # Consulting & Professional Services
            'EY': 'https://careers.ey.com/ey/search',
            'KPMG': 'https://kpmg.com/in/en/home/careers.html',
            'PwC': 'https://www.pwc.in/careers.html',
            'Bain': 'https://www.bain.com/careers/',
            'BCG': 'https://careers.bcg.com/',
            'McKinsey': 'https://www.mckinsey.com/careers',
            'ZS Associates': 'https://www.zs.com/careers',
            'Fractal Analytics': 'https://fractal.ai/careers/',
            'Tredence': 'https://www.tredence.com/careers',

            # E-commerce & Retail
            'Walmart': 'https://tech.walmart.com/content/walmart-global-tech/en_us/careers.html',
            'Airtel': 'https://www.airtel.in/careers/',
            'Unilever': 'https://careers.unilever.com/',
            'PepsiCo': 'https://www.pepsicojobs.com/main/',

            # Healthcare & Pharma
            'Optum': 'https://careers.unitedhealthgroup.com/',
            'Labcorp': 'https://careers.labcorp.com/',
            'Thermofisher': 'https://jobs.thermofisher.com/',

            # Fintech & Payments
            'Razorpay': 'https://razorpay.com/jobs/',
            'CRED': 'https://careers.cred.club/',
            'Groww': 'https://groww.in/careers',
            'Zerodha': 'https://zerodha.com/careers/',

            # Manufacturing & Engineering
            'Honeywell': 'https://careers.honeywell.com/',
            'GE': 'https://jobs.gecareers.com/',
            'Siemens': 'https://jobs.siemens.com/careers',
            'Bosch': 'https://www.bosch.in/careers/',
            'Caterpillar': 'https://careers.caterpillar.com/',
            'Baker Hughes': 'https://careers.bakerhughes.com/',
            'Schlumberger': 'https://careers.slb.com/',
            'Shell': 'https://www.shell.com/careers.html',
            'Rolls Royce': 'https://careers.rolls-royce.com/',
            'BMW': 'https://www.bmwgroup.jobs/',
            'Volvo': 'https://www.volvogroup.com/en/careers.html',
            'Toshiba': 'https://www.toshiba.co.jp/worldwide/recruit/',
            'Schneider': 'https://www.se.com/ww/en/about-us/careers/',
            'Ericsson': 'https://www.ericsson.com/en/careers',
            'Garmin': 'https://careers.garmin.com/',
            'Visteon': 'https://www.visteon.com/careers/',
            'Aptiv': 'https://www.aptiv.com/en/careers',

            # Insurance & Financial Services
            'CHUBB': 'https://careers.chubb.com/',
            'Swiss Re': 'https://careers.swissre.com/',
            'Guardian': 'https://www.guardianlife.com/careers',
            'Fidelity': 'https://jobs.fidelity.com/',
            'Bajaj Finserv': 'https://www.bajajfinserv.in/careers',

            # Other Notable Companies
            'Thoughtworks': 'https://www.thoughtworks.com/careers',
            'Atlassian': 'https://www.atlassian.com/company/careers',
            'Salesforce': 'https://www.salesforce.com/company/careers/',
            'ServiceNow': 'https://www.servicenow.com/careers.html',
            'Splunk': 'https://www.splunk.com/en_us/careers.html',
            'VMware': 'https://careers.vmware.com/',
            'NetApp': 'https://www.netapp.com/company/careers/',
            'Broadcom': 'https://www.broadcom.com/company/careers',
            'NatWest': 'https://jobs.natwestgroup.com/',
            'SOCIETE GENERALE': 'https://careers.societegenerale.com/',
            'Commonwealth Bank': 'https://www.commbank.com.au/about-us/careers.html',
            'London Stock Exchange': 'https://www.lseg.com/en/careers',
            'Nielsen': 'https://careers.nielsen.com/',
            'Sabre': 'https://www.sabre.com/careers/',
            'Pegasystems': 'https://www.pega.com/about/careers',
            'Epsilon': 'https://www.epsilon.com/us/about-us/careers',
            'ION': 'https://iongroup.com/careers/',
            'Bottomline': 'https://www.bottomline.com/us/about/careers',
            'RingCentral': 'https://www.ringcentral.com/whyringcentral/company/careers.html',
            'Zenoti': 'https://www.zenoti.com/careers',
            'Tekion': 'https://tekion.com/careers',
            'Kinaxis': 'https://www.kinaxis.com/en/careers',
            'PTC': 'https://www.ptc.com/en/about/careers',
            'QSC': 'https://www.qsc.com/about-qsc/careers/',
            'Sapiens': 'https://sapiens.com/careers/',
            'Ramco Systems': 'https://www.ramco.com/careers/',
            'ITC Infotech': 'https://www.itcinfotech.com/careers/',
            'Incedo': 'https://www.incedoinc.com/careers/',
            'Prodapt': 'https://www.prodapt.com/careers/',
            'EMIDS': 'https://www.emids.com/careers/',
            'Verizon': 'https://www.verizon.com/about/careers',
            'Fastenal': 'https://careers.fastenal.com/',
            'Zynga': 'https://www.zynga.com/careers/',

            # Additional Companies from Placement Tracker
            'ADP': 'https://jobs.adp.com/en/locations/apac/india/',
            'ASM Technology': 'https://www.asm.com/careers',
            'Accordion': 'https://www.accordionpartners.com/careers/',
            'AVEVA': 'https://www.aveva.com/en/about/careers/',
            'Blend': 'https://blend.com/company/careers/',
            'Broadridge': 'https://broadridge.wd5.myworkdayjobs.com/Careers',
            'Futures First': 'https://www.futuresfirst.com/careers/',
            'GE Vernova': 'https://jobs.gecareers.com/',
            'Greenway Healthcare': 'https://www.greenwayhealth.com/about/careers',
            'Human Resocia': 'https://corporate.resocia.jp/en/recruit/',
            'KLA': 'https://www.kla.com/careers/locations/india',
            'Leadsquared': 'https://www.leadsquared.com/careers/',
            'MIQ Digital': 'https://www.wearemiq.com/careers/',
            'Movate': 'https://www.movate.com/careers/',
            'Niyo Solutions': 'https://www.goniyo.com/careers',
            'Poshmark': 'https://poshmark.com/careers',
            'Presidio': 'https://www.presidio.com/careers/',
            'Quantiphi': 'https://quantiphi.com/careers/',
            'Rystad Energy': 'https://www.rystadenergy.com/about/careers/',
            'SAP Labs': 'https://jobs.sap.com/go/SAP-Jobs-in-India/851201/',
            'Saviynt': 'https://saviynt.com/careers',
            'Shipsy': 'https://shipsy.io/careers/',
            'SolarWinds': 'https://jobs.solarwinds.com/',
            'Seven Eleven': 'https://careers.7-eleven.com/',
            'TechMojo': 'https://www.techmojo.com/careers/',
            'TresVista': 'https://www.tresvista.com/careers/',
            'Western Digital': 'https://www.westerndigital.com/en-in/careers',
            'Watchguard': 'https://www.watchguard.com/wgrd-about/careers',
            'Zluri': 'https://www.zluri.com/careers',
            'XFLOW Payments': 'https://www.xflowpay.com/careers',
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
        """More targeted LinkedIn search"""
        search_queries = [
            "Software Developer Intern 2026",
            "SDE Intern 2026",
            "Python Developer Intern",
            "Java Developer Intern",
            "Full Stack Developer Intern",
            "Web Developer Intern",
            "Software Engineer Intern",
            "Backend Developer Intern",
            "Frontend Developer Intern"
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
            base_url = "https://internshala.com/internships/web%20development,software%20development,python-internship/"
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
            'software-developer-intern',
            'python-developer-fresher',
            'java-developer-intern',
            'web-developer-intern',
            'software-engineer-intern-2026'
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
        """Search company career pages from placement tracker companies"""
        # Priority companies to search (high CTC companies from placement tracker)
        priority_companies = [
            # 40+ LPA companies
            'Google', 'Microsoft', 'Amazon', 'Adobe', 'Apple', 'Meesho', 'Zomato',
            # 30+ LPA companies
            'Goldman Sachs', 'Flipkart', 'PayPal', 'PhonePe', 'Commvault', 'Couchbase',
            'Visa', 'Zynga', 'XFLOW Payments',
            # 20+ LPA companies
            'JP Morgan', 'Morgan Stanley', 'Cisco', 'Bank of New York Mellon', 'Wells Fargo',
            'Walmart', 'OKTA', 'Marvell', 'Samsung', 'KLA', 'Workday', 'Human Resocia',
            'BlackRock', 'MUFG', 'Western Digital', 'Tekion', 'Saviynt', 'Blend',
            # 15+ LPA companies
            'American Express', 'Intuit', 'Oracle', 'Dell', 'Nutanix', 'Optum',
            'Bain', 'IDFC', 'ION', 'Juniper Networks', 'Fastenal', 'GE Vernova',
            'Futures First', 'Niyo Solutions', 'Nielsen', 'Caterpillar', 'Sabre',
            'Airtel', 'Pegasystems', 'Swiss Re', 'ZS Associates', 'Bottomline',
            # Other notable companies
            'Honeywell', 'Accenture', 'Deloitte', 'EY', 'KPMG', 'PwC',
            'Infosys', 'DBS', 'CHUBB', 'Fidelity', 'UBS', 'Epsilon', 'Broadridge'
        ]

        search_keywords = [
            'intern', 'fresher', 'graduate', 'entry level', 'associate',
            'software engineer', 'developer', 'sde', '2025', '2026'
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

                    # Check if page has relevant job listings
                    has_relevant_jobs = any(keyword in page_text for keyword in search_keywords)

                    if has_relevant_jobs:
                        # Try to extract job listings from common patterns
                        # Look for job cards/listings
                        job_elements = soup.find_all(['div', 'li', 'article'], class_=lambda x: x and any(
                            term in str(x).lower() for term in ['job', 'position', 'opening', 'career', 'listing', 'card']
                        ))

                        for elem in job_elements[:10]:
                            try:
                                # Try to extract title
                                title_elem = elem.find(['h2', 'h3', 'h4', 'a', 'span'], class_=lambda x: x and any(
                                    term in str(x).lower() for term in ['title', 'name', 'position', 'role', 'job-title']
                                ))

                                if title_elem:
                                    title_text = title_elem.get_text().strip()

                                    # Check if it's a relevant role (intern/fresher/entry-level)
                                    title_lower = title_text.lower()
                                    is_relevant = any(kw in title_lower for kw in ['intern', 'fresher', 'graduate', 'entry', 'associate', 'junior', 'trainee'])

                                    if is_relevant and len(title_text) > 5 and len(title_text) < 150:
                                        # Try to get job link
                                        link_elem = elem.find('a', href=True)
                                        job_link = ''
                                        if link_elem:
                                            href = link_elem.get('href', '')
                                            if href.startswith('http'):
                                                job_link = href
                                            elif href.startswith('/'):
                                                # Extract base URL
                                                from urllib.parse import urlparse
                                                parsed = urlparse(career_url)
                                                job_link = f"{parsed.scheme}://{parsed.netloc}{href}"
                                            else:
                                                job_link = career_url

                                        job_type = 'Internship' if 'intern' in title_lower else 'Full-time'

                                        job_data = {
                                            'Company': company,
                                            'Title': title_text,
                                            'Type': job_type,
                                            'Salary': 'Not disclosed',
                                            'Link': job_link if job_link else career_url,
                                            'Source': 'Company Career Page'
                                        }

                                        # Avoid duplicates within this search
                                        is_duplicate = any(
                                            j['Title'].lower() == title_text.lower() and j['Company'].lower() == company.lower()
                                            for j in self.jobs
                                        )

                                        if not is_duplicate:
                                            self.jobs.append(job_data)
                                            jobs_found += 1

                            except Exception as e:
                                continue

                time.sleep(2)  # Rate limiting

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
            print("⚠️  WEB_APP_URL not set. Jobs will be saved to JSON only.")
            return False

        try:
            # Add separator rows before new jobs for visual clarity
            jobs_to_send = []

            if add_separator and formatted_jobs:
                now = datetime.now()
                separator_time = now.strftime('%d %b, %Y %I:%M %p').replace(' 0', ' ')

                # Add empty row for spacing
                jobs_to_send.append({
                    'Company': '',
                    'Title': '',
                    'Type': '',
                    'Stipend/CTC': '',
                    'Apply Link': '',
                    'Last Updated': ''
                })

                # Add separator row with timestamp
                jobs_to_send.append({
                    'Company': f'━━━━ NEW JOBS ADDED ON {separator_time} ━━━━',
                    'Title': '',
                    'Type': '',
                    'Stipend/CTC': '',
                    'Apply Link': '',
                    'Last Updated': separator_time
                })

                # Add another empty row for spacing
                jobs_to_send.append({
                    'Company': '',
                    'Title': '',
                    'Type': '',
                    'Stipend/CTC': '',
                    'Apply Link': '',
                    'Last Updated': ''
                })

            # Add the actual jobs
            jobs_to_send.extend(formatted_jobs)

            response = requests.post(
                self.WEB_APP_URL,
                json={'jobs': jobs_to_send},
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
            existing_links, existing_jobs = self.get_existing_jobs_from_sheet()

            # Filter out jobs that already exist (by link OR by title+company)
            new_jobs = []
            for job in self.jobs:
                if not job['Link']:
                    continue

                # Check if job exists by link
                if job['Link'] in existing_links:
                    continue

                # Check if job exists by title + company
                job_identifier = (job['Title'].lower(), job['Company'].lower())
                if job_identifier in existing_jobs:
                    continue

                new_jobs.append(job)

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
    print("🔍 AUTOMATED JOB SEARCH FOR PUNISH")
    print("=" * 70)
    print(f"⏰ Search time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}")
    print(f"🎯 Target: Software Development Internships/Jobs for 2026 Batch")
    print(f"💰 Min Stipend: ₹20,000/month | Min CTC: ₹5 LPA")
    print(f"📧 Recipient: Punish")
    print(f"🏢 Sources: LinkedIn, Naukri, Internshala + Company Career Pages")
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

    print("\n🔎 Searching Company Career Pages (Placement Tracker Companies)...")
    initial_count = len(searcher.jobs)
    career_jobs = searcher.search_company_career_pages()
    print(f"   Found {len(searcher.jobs) - initial_count} new listings from company career pages")

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
