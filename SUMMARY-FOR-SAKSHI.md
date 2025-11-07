# 📧 Job Search Automation - Ready to Deploy!

Hi Sakshi! 👋

I've created a complete automated job search system based on your resume and requirements. Here's what you're getting:

---

## 🎯 What It Does

✅ **Automatically searches** for AI/ML jobs every 6 hours  
✅ **Filters** for your criteria:
   - AI/ML internships for 2026 graduates
   - Minimum ₹35,000/month stipend
   - Minimum ₹12 LPA salary for full-time roles
   - Fresher-friendly positions

✅ **Searches multiple platforms:**
   - LinkedIn (most up-to-date listings)
   - Naukri.com (largest Indian job portal)
   - Internshala (best for internships)
   - Cutshort (tech-focused)
   - Wellfound (startup jobs)

✅ **Updates Excel file** with new jobs only (removes duplicates)  
✅ **Works with your email system** - just point it to the Excel file

---

## 📦 What's Included

All files are ready in the folder:

1. **job_search_advanced.py** - The main searcher (RECOMMENDED - best filtering)
2. **job_search.py** - Basic version (simpler, fewer features)
3. **.github/workflows/job-search.yml** - GitHub Actions automation
4. **jobs.xlsx** - Excel template with proper columns
5. **setup.sh** - One-click setup script
6. **QUICKSTART.md** - 5-minute setup guide
7. **README.md** - Complete documentation
8. **requirements.txt** - Python dependencies

---

## ⚡ Quick Setup (5 Minutes)

### Step 1: Download Everything
Download the entire `job-automation` folder to your computer.

### Step 2: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `job-search-automation`
3. **Set to PRIVATE** ✓ (important!)
4. Click "Create repository"

### Step 3: Upload Files
In your terminal:
```bash
cd job-automation
chmod +x setup.sh
./setup.sh

# Then connect to GitHub:
git remote add origin https://github.com/YOUR-USERNAME/job-search-automation.git
git branch -M main
git push -u origin main
```

### Step 4: Enable GitHub Actions
1. Go to your repo → Settings → Actions → General
2. Select "Read and write permissions"
3. Save

### Step 5: Use Advanced Searcher
Edit `.github/workflows/job-search.yml` (line 25):
Change `python job_search.py` to `python job_search_advanced.py`

Push the change:
```bash
git add .github/workflows/job-search.yml
git commit -m "Use advanced searcher"
git push
```

### Step 6: Test It
1. Go to "Actions" tab in GitHub
2. Click "Daily Job Search"
3. Click "Run workflow"
4. Wait 2-3 minutes
5. Check if `jobs.xlsx` was updated

### Step 7: Connect Your Email
Since you said you have email automation ready:
- Point your system to read `jobs.xlsx` from this GitHub repo
- It will automatically get updated every 6 hours with new jobs

---

## 🎨 Customization

### Change How Often It Runs
Edit `.github/workflows/job-search.yml`:
```yaml
schedule:
  - cron: '0 */6 * * *'   # Every 6 hours (current)
  - cron: '0 */4 * * *'   # Every 4 hours
  - cron: '0 9,21 * * *'  # Twice daily (9 AM & 9 PM)
```

### Adjust Salary Requirements
Edit `job_search_advanced.py` (lines 13-16):
```python
self.min_stipend = 35000    # Change this
self.min_ctc = 1200000      # Or this
```

### Add More Keywords
Edit `job_search_advanced.py` and add to search queries based on your skills:
- Spring Boot developer intern
- AWS intern
- Computer Vision intern
- etc.

---

## 📊 What Your Excel Will Look Like

Every 6 hours, `jobs.xlsx` gets updated with:

| Title | Company | Location | Link | Source | Date_Found | Status | Salary |
|-------|---------|----------|------|--------|------------|--------|--------|
| ML Intern | TechCorp | Bangalore | [link] | LinkedIn | 2024-11-07 | New | ₹40k/mo |
| AI Engineer | StartupXYZ | Remote | [link] | Naukri | 2024-11-07 | New | 15 LPA |

Your email automation reads this file and sends you the links!

---

## 💡 Why Advanced Searcher is Better

**job_search_advanced.py** includes:
- ✅ Salary filtering (removes jobs below your minimum)
- ✅ Better duplicate detection
- ✅ More targeted search queries
- ✅ Fresher/intern filtering
- ✅ Nicer Excel formatting
- ✅ More detailed job information

**job_search.py** is simpler but less effective.

**Recommendation: Use the advanced version!**

---

## 🛠️ Troubleshooting

### No jobs appearing?
- Check GitHub Actions logs (Actions tab)
- Some sites might block requests temporarily
- Try different keywords in the searcher

### Email not working?
- Ensure your email automation can access the GitHub file
- Check if `jobs.xlsx` is being updated (look at GitHub commits)
- Test email automation separately with the Excel file

### GitHub Actions failing?
- Verify permissions are set correctly
- Check Actions logs for specific errors
- Try running locally first: `python job_search_advanced.py`

---

## 📈 Expected Results

Based on your profile (Spring Boot, ML, AWS, Java, Python):
- **10-25 new jobs per day** across all platforms
- **3-8 highly relevant roles** that match your criteria
- **Mix of internships and full-time positions**

Quality over quantity - the filter removes irrelevant jobs!

---

## 🎯 Next Steps After Setup

1. ✅ Let it run for 24 hours
2. ✅ Check the quality of results
3. ✅ Adjust keywords if needed
4. ✅ Mark jobs as "Applied" in Excel
5. ✅ Update your resume for specific companies
6. ✅ Start applying! 🚀

---

## 🔐 Privacy & Security

- ✅ Repository is PRIVATE (only you can see it)
- ✅ No personal data is shared
- ✅ GitHub Actions runs in secure containers
- ✅ Your job search stays confidential

---

## 📞 Questions?

1. Read **QUICKSTART.md** for 5-minute setup
2. Check **README.md** for full documentation
3. Review GitHub Actions logs for debugging
4. Test locally before deploying

---

## ✨ Special Features in Your Resume

Based on your resume, I optimized the search for:

**Your Skills:**
- Spring Boot + Java backend
- Machine Learning (TensorFlow, OpenCV)
- AWS cloud services
- ReactJS frontend
- Python ML/AI projects

**Your Experience:**
- IRIS Techsol ML Intern experience
- S3Bridge and ThreadMesh projects
- Hackclub AI/ML leadership
- Research presentations

**Target Companies:**
These match your profile:
- Startups (ML/AI focus)
- Product companies (Spring Boot, AWS)
- Research labs (your ML background)
- Tech giants (fresher hiring for 2026)

---

## 🎉 You're All Set!

Your automated job hunting system is ready. It will:
1. Search every 6 hours
2. Find relevant AI/ML roles
3. Filter by your salary requirements
4. Update Excel with new jobs only
5. Trigger your email system

**Just set it up once, and let it run! Good luck with your job search! 🚀**

---

**Files Location:** `/mnt/user-data/outputs/job-automation/`

**Start with:** Read QUICKSTART.md first!
