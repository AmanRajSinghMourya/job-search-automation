# Quick Start

1. Paste `google_apps_script_punish.js` into the Google Sheet's Apps Script project.
2. Deploy it as a Web App.
3. Add the deployed URL to GitHub as the repository secret `WEB_APP_URL`.
4. Open the GitHub Actions tab.
5. Run `Job Search for Punish` manually once to test.

The repo is Punish-only. The workflow runs `job_search_for_punish.py`, searches Data Analyst / BI roles, and the Apps Script emails only `punishmidha21@gmail.com`.
