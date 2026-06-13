# Job Search Automation for Punish

This repository runs a scheduled GitHub Actions job search for Punish and sends new jobs to a Google Apps Script Web App. The Web App writes jobs into the Google Sheet and emails Punish immediately when new jobs are added.

## Current Files

- `.github/workflows/job-search.yml` - daily GitHub Actions workflow
- `job_search_for_punish.py` - Punish-only job search script
- `google_apps_script_punish.js` - Apps Script code to paste into Google Apps Script
- `requirements.txt` - Python dependency list

## GitHub Secret

The workflow expects one repository secret:

```text
WEB_APP_URL
```

Set it to the deployed Google Apps Script Web App URL.

## Schedule

The workflow runs daily at `10:00 UTC` and can also be run manually from the GitHub Actions tab.

## Apps Script Setup

1. Open the target Google Sheet.
2. Go to `Extensions > Apps Script`.
3. Replace the script code with `google_apps_script_punish.js`.
4. Save the project.
5. Deploy as a Web App:
   - Execute as: `Me`
   - Who has access: `Anyone`
6. Copy the Web App URL into the GitHub repository secret `WEB_APP_URL`.

## Punish Configuration

The current Sheet ID is:

```text
1nridtqY_EkI47W8dcKOBhuMLCazepmH9JNPuDXyuYLA
```

The current email recipient is configured in `google_apps_script_punish.js`:

```javascript
const RECIPIENTS = ["punishmidha21@gmail.com"];
```

## Local Test

```bash
python3 -m pip install -r requirements.txt
WEB_APP_URL="YOUR_WEB_APP_URL" python3 job_search_for_punish.py
```
