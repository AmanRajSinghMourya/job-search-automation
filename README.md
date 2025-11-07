# Automated Job Search System

This GitHub Actions workflow automatically searches for AI/ML internships and jobs every 6 hours and updates an Excel file.

## Features
- **Automated searches** every 6 hours (00:00, 06:00, 12:00, 18:00 UTC)
- Searches multiple platforms: LinkedIn, Naukri, Instahire, Wellfound
- Filters for:
  - AI/ML internships and fresher roles
  - Minimum stipend: ₹35,000+/month
  - Minimum CTC: ₹12 LPA+
  - 2026 graduates
- Removes duplicates automatically
- Updates Excel file with new jobs only

## Setup Instructions

### 1. Create a New GitHub Repository
1. Go to GitHub and create a new repository (e.g., `job-search-automation`)
2. Make it **private** to protect your job search data

### 2. Upload Files to Repository
Upload these files to your repository:
- `.github/workflows/job-search.yml` (the workflow file)
- `job_search.py` (the Python script)
- `jobs.xlsx` (create an empty Excel file with these columns: Title, Company, Location, Link, Source, Date_Found, Status, Salary)

### 3. Create Empty Excel File
Create a file named `jobs.xlsx` with these column headers:
- Title
- Company
- Location
- Link
- Source
- Date_Found
- Status
- Salary

### 4. Enable GitHub Actions
1. Go to your repository Settings
2. Click on "Actions" → "General"
3. Under "Workflow permissions", select "Read and write permissions"
4. Click "Save"

### 5. Connect Your Email Automation
Since you already have the Excel → Email part set up:
1. Make sure your email automation can access the `jobs.xlsx` file from this GitHub repo
2. You can either:
   - Clone the repo locally and point your automation to it
   - Use GitHub API to download the file periodically
   - Set up a webhook to trigger when the file changes

### 6. Manual Trigger (Optional)
You can manually trigger the workflow:
1. Go to "Actions" tab in your repository
2. Click on "Daily Job Search"
3. Click "Run workflow"

## How It Works

1. **GitHub Actions runs the workflow** every 6 hours
2. **Python script searches** multiple job portals
3. **Filters results** based on your criteria
4. **Updates Excel file** with only new jobs (removes duplicates)
5. **Commits changes** back to the repository
6. **Your email automation** picks up the updated Excel file and sends you the links

## Customization

### Change Search Frequency
Edit `.github/workflows/job-search.yml`:
```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
  # - cron: '0 0 * * *'   # Daily at midnight
  # - cron: '0 0,12 * * *' # Twice daily
```

### Adjust Search Keywords
Edit `job_search.py` and modify the keywords arrays:
```python
keywords = ['AI ML intern', 'Machine Learning intern', 'AI Engineer fresher']
```

### Add More Job Portals
You can add more search functions to `job_search.py` for other job boards.

## Important Notes

1. **Rate Limiting**: The script includes delays between requests to avoid being blocked
2. **Web Scraping**: Some sites may change their HTML structure - you might need to update the script
3. **API Access**: Consider using official APIs (LinkedIn, Naukri) for more reliable results
4. **GitHub Actions Limits**: Free tier has 2000 minutes/month (this uses ~5 mins/day)

## Troubleshooting

If jobs aren't being found:
1. Check the "Actions" tab for error messages
2. Test the script locally: `python job_search.py`
3. Some job sites may block automated requests - consider rotating user agents
4. LinkedIn might require authentication - consider using their API with a developer account

## Privacy & Security

- Keep your repository **private** to protect your job search
- Don't commit sensitive information (API keys, passwords)
- Use GitHub Secrets for any API keys needed

## Next Steps

Once this is running:
1. Monitor for a few days to see the quality of results
2. Adjust search keywords as needed
3. Add more job portals if required
4. Consider adding filters for specific companies or locations

---

**Need help?** Check the GitHub Actions logs for detailed error messages.
