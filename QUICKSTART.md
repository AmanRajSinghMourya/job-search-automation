# 🚀 QUICK START GUIDE

## What You Have

Your automated job search system that:
- ✅ Searches 5+ job portals (LinkedIn, Naukri, Internshala, Cutshort, Wellfound)
- ✅ Runs automatically every 6 hours
- ✅ Filters for AI/ML roles with ₹35k+ stipend / ₹12 LPA+ salary
- ✅ Updates Excel file with only NEW jobs (no duplicates)
- ✅ Works with your existing email automation

## 📁 Files Included

```
job-automation/
├── .github/workflows/job-search.yml  # GitHub Actions workflow
├── job_search.py                     # Basic job searcher
├── job_search_advanced.py            # Advanced searcher (RECOMMENDED)
├── jobs.xlsx                         # Excel template
├── requirements.txt                  # Python dependencies
├── setup.sh                          # Setup script
└── README.md                         # Full documentation
```

## ⚡ 5-Minute Setup

### Option 1: Use Advanced Searcher (RECOMMENDED)

1. **Download all files** to your computer

2. **Open terminal** in the downloaded folder

3. **Run setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

4. **Create GitHub repository:**
   - Go to https://github.com/new
   - Name: `job-search-automation`
   - Set to **PRIVATE** ✓
   - Click "Create repository"

5. **Connect and push:**
   ```bash
   git remote add origin https://github.com/YOUR-USERNAME/job-search-automation.git
   git branch -M main
   git push -u origin main
   ```

6. **Enable GitHub Actions:**
   - Go to your repo → Settings → Actions → General
   - Select "Read and write permissions"
   - Save

7. **Update workflow to use advanced searcher:**
   - Edit `.github/workflows/job-search.yml`
   - Change line 25 from:
     ```yaml
     run: python job_search.py
     ```
     to:
     ```yaml
     run: python job_search_advanced.py
     ```
   - Commit and push:
     ```bash
     git add .github/workflows/job-search.yml
     git commit -m "Use advanced job searcher"
     git push
     ```

8. **Test it manually:**
   - Go to Actions tab
   - Click "Daily Job Search"
   - Click "Run workflow"
   - Wait 2-3 minutes
   - Check if `jobs.xlsx` was updated

9. **Connect your email automation** to read `jobs.xlsx`

### Option 2: Manual Testing First

Before setting up automation, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the script
python job_search_advanced.py

# Check jobs.xlsx for results
```

## 🎯 What the Advanced Searcher Does

The `job_search_advanced.py` file:
- ✅ Searches multiple platforms simultaneously
- ✅ **Filters by salary** (removes jobs below your minimum)
- ✅ **Removes duplicates** automatically
- ✅ **Better search queries** tailored to your profile
- ✅ **Formats Excel nicely** with auto-adjusted columns
- ✅ **Checks for freshers/interns only**
- ✅ Includes more job portals

## 📊 Excel File Structure

Your `jobs.xlsx` will have these columns:
- **Title**: Job title
- **Company**: Company name
- **Location**: Job location
- **Link**: Direct application link
- **Source**: Which job portal
- **Date_Found**: When job was found
- **Status**: New/Applied/Rejected
- **Salary**: Disclosed salary/stipend
- **Experience**: Required experience
- **Posted**: When job was posted

## 🔧 Customization

### Change Search Frequency

Edit `.github/workflows/job-search.yml`:

```yaml
schedule:
  - cron: '0 */6 * * *'   # Every 6 hours (CURRENT)
  # - cron: '0 */4 * * *'   # Every 4 hours
  # - cron: '0 0 * * *'     # Once daily at midnight
  # - cron: '0 9,18 * * *'  # Twice daily (9 AM & 6 PM)
```

### Adjust Salary Filters

Edit `job_search_advanced.py` (lines 13-16):

```python
self.min_stipend = 35000   # Change minimum stipend
self.min_ctc = 1200000     # Change minimum CTC (in Rs)
self.graduation_year = 2026 # Your graduation year
```

### Add More Keywords

Edit `job_search_advanced.py` and add to search queries:

```python
search_queries = [
    'AI ML Intern 2026',
    'Machine Learning Intern 2026 graduate',
    'YOUR NEW KEYWORD HERE',
    # Add more...
]
```

## 🔍 Monitoring

### Check if it's working:

1. **GitHub Actions tab** - See all runs and their status
2. **jobs.xlsx** - Should update every 6 hours with new jobs
3. **Your email** - Should receive updates from your automation

### If no jobs are found:

- Check GitHub Actions logs for errors
- Some sites may be blocking requests - this is normal
- Try running manually: `python job_search_advanced.py`
- Check if the websites changed their structure

## 🛡️ Privacy & Security

- Keep repository **PRIVATE** ✓
- Never commit API keys or passwords
- Your job search data stays private
- GitHub Actions runs in a secure container

## 💡 Pro Tips

1. **Run manually first** to see what jobs it finds
2. **Adjust search keywords** based on results quality
3. **Mark jobs as "Applied"** in Excel to track progress
4. **Add notes column** in Excel for your thoughts
5. **Back up Excel file** periodically

## 🆘 Troubleshooting

### No new jobs appearing?
- LinkedIn might need authentication (use their API)
- Some sites block automated requests
- Try different search keywords

### GitHub Actions failing?
- Check the Actions tab for error logs
- Ensure permissions are set correctly
- Try manually: `python job_search_advanced.py`

### Excel not updating?
- Check file permissions
- Ensure openpyxl is installed
- Look for error messages in Actions logs

## 📧 Connecting Your Email Automation

Since you have the email part sorted:

1. **Option A**: Email automation reads `jobs.xlsx` from GitHub
   - Use GitHub API to download file
   - Check file's last modified time
   - Email only if file changed

2. **Option B**: Clone repo locally, email reads from there
   - `git clone https://github.com/YOUR-USERNAME/job-search-automation.git`
   - `git pull` periodically to get updates
   - Email automation reads local `jobs.xlsx`

3. **Option C**: Use GitHub webhook
   - Set up webhook to trigger when `jobs.xlsx` changes
   - Webhook triggers your email automation

## 📞 Need Help?

1. Check full `README.md` for detailed docs
2. Review GitHub Actions logs for errors
3. Test script locally: `python job_search_advanced.py`
4. Check if websites are accessible

## ✅ Success Checklist

- [ ] Downloaded all files
- [ ] Created private GitHub repository
- [ ] Pushed code to GitHub
- [ ] Enabled GitHub Actions with write permissions
- [ ] Changed workflow to use `job_search_advanced.py`
- [ ] Tested manually (ran workflow once)
- [ ] Verified `jobs.xlsx` was created/updated
- [ ] Connected email automation
- [ ] Received first email with jobs

---

## 🎉 That's It!

Your automated job search is now running! It will search every 6 hours and update your Excel file. Your email automation will then send you the new listings.

**Good luck with your job search! 🚀**
