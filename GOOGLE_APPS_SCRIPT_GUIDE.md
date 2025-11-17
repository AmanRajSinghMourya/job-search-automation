# Google Apps Script Integration Guide

## Overview
This guide explains how to update your Google Apps Script Web App to work with the enhanced job search automation that includes spacing and better organization of new vs old jobs.

## Updated Payload Format

The Python scripts now send a more structured payload:

```json
{
  "jobs": [
    {
      "Company": "Example Corp",
      "Title": "Software Engineer Intern",
      "Type": "Internship",
      "Stipend/CTC": "₹30,000/month",
      "Apply Link": "https://...",
      "Last Updated": "17 Nov 2025, 5:30 PM"
    }
  ],
  "metadata": {
    "batch_date": "17 Nov 2025, 5:30 PM",
    "job_count": 5,
    "add_separator": true
  }
}
```

## Google Apps Script Code

Update your Google Apps Script Web App (`doPost` function) to handle the new format:

```javascript
function doPost(e) {
  try {
    // Parse incoming data
    var data = JSON.parse(e.postData.contents);
    var jobs = data.jobs || [];
    var metadata = data.metadata || {};

    // Open the spreadsheet
    var sheet = SpreadsheetApp.openById('YOUR_SHEET_ID').getActiveSheet();

    // If no jobs, return early
    if (jobs.length === 0) {
      return ContentService.createTextOutput(JSON.stringify({
        'message': 'No jobs to add',
        'status': 'success'
      })).setMimeType(ContentService.MimeType.JSON);
    }

    // Add separator if requested (for visual organization)
    if (metadata.add_separator === true) {
      var lastRow = sheet.getLastRow();

      // Only add separator if there's existing data
      if (lastRow > 1) {
        // Add 2 empty rows for spacing
        sheet.insertRowAfter(lastRow);
        sheet.insertRowAfter(lastRow + 1);

        // Add a header row for the new batch
        var headerRow = lastRow + 3;
        sheet.insertRowAfter(lastRow + 2);

        var batchHeader = [
          '━━━ NEW JOBS ADDED ━━━',
          metadata.batch_date || 'Unknown Date',
          metadata.job_count + ' new jobs',
          '',
          '',
          ''
        ];

        sheet.getRange(headerRow, 1, 1, 6).setValues([batchHeader]);
        sheet.getRange(headerRow, 1, 1, 6).setFontWeight('bold');
        sheet.getRange(headerRow, 1, 1, 6).setBackground('#E8F0FE');
      }
    }

    // Prepare rows for new jobs
    var rows = [];
    for (var i = 0; i < jobs.length; i++) {
      var job = jobs[i];
      rows.push([
        job['Company'] || '',
        job['Title'] || '',
        job['Type'] || '',
        job['Stipend/CTC'] || '',
        job['Apply Link'] || '',
        job['Last Updated'] || ''
      ]);
    }

    // Append new jobs to the sheet
    if (rows.length > 0) {
      var lastRow = sheet.getLastRow();
      sheet.getRange(lastRow + 1, 1, rows.length, 6).setValues(rows);
    }

    // Return success response
    return ContentService.createTextOutput(JSON.stringify({
      'message': jobs.length + ' jobs added successfully',
      'status': 'success',
      'jobs_added': jobs.length
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    // Return error response
    return ContentService.createTextOutput(JSON.stringify({
      'message': 'Error: ' + error.toString(),
      'status': 'error'
    })).setMimeType(ContentService.MimeType.JSON);
  }
}
```

## Alternative: Simpler Version (No Separator)

If you prefer a simpler version without the batch headers:

```javascript
function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var jobs = data.jobs || [];

    var sheet = SpreadsheetApp.openById('YOUR_SHEET_ID').getActiveSheet();

    if (jobs.length === 0) {
      return ContentService.createTextOutput(JSON.stringify({
        'message': 'No jobs to add',
        'status': 'success'
      })).setMimeType(ContentService.MimeType.JSON);
    }

    // Add 1 empty row for spacing before new jobs
    var lastRow = sheet.getLastRow();
    if (lastRow > 1 && data.metadata && data.metadata.add_separator) {
      sheet.insertRowAfter(lastRow);
      lastRow = lastRow + 1;
    }

    // Prepare and append rows
    var rows = [];
    for (var i = 0; i < jobs.length; i++) {
      var job = jobs[i];
      rows.push([
        job['Company'] || '',
        job['Title'] || '',
        job['Type'] || '',
        job['Stipend/CTC'] || '',
        job['Apply Link'] || '',
        job['Last Updated'] || ''
      ]);
    }

    if (rows.length > 0) {
      sheet.getRange(lastRow + 1, 1, rows.length, 6).setValues(rows);
    }

    return ContentService.createTextOutput(JSON.stringify({
      'message': jobs.length + ' jobs added successfully',
      'status': 'success'
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      'message': 'Error: ' + error.toString(),
      'status': 'error'
    })).setMimeType(ContentService.MimeType.JSON);
  }
}
```

## Setup Instructions

1. Open your Google Sheet
2. Go to **Extensions > Apps Script**
3. Replace the existing `doPost` function with one of the versions above
4. Update `YOUR_SHEET_ID` with your actual Google Sheet ID
5. Save the script
6. Deploy as Web App:
   - Click **Deploy > New deployment**
   - Select type: **Web app**
   - Execute as: **Me**
   - Who has access: **Anyone**
   - Click **Deploy**
7. Copy the Web App URL and add it to your GitHub Secrets as:
   - `WEB_APP_URL` (for Sakshi)
   - `WEB_APP_URL_AMAN` (for Aman)
   - `WEB_APP_URL_PUNISH` (for Punish)

## Key Features

### Duplicate Prevention
- The Python scripts check existing job links before sending
- Only new jobs (not in the sheet) are sent to the Web App
- No manual duplicate removal needed

### Visual Organization
- New job batches are separated from old jobs
- Optional batch headers show when jobs were added
- Empty rows provide clear visual spacing
- Each job includes a timestamp

### Metadata Tracking
- `batch_date`: When the jobs were found
- `job_count`: Number of new jobs in this batch
- `add_separator`: Whether to add visual spacing

## Testing

Test your Web App with:
```bash
curl -X POST YOUR_WEB_APP_URL \
  -H "Content-Type: application/json" \
  -d '{
    "jobs": [{
      "Company": "Test Corp",
      "Title": "Test Position",
      "Type": "Internship",
      "Stipend/CTC": "₹25,000/month",
      "Apply Link": "https://example.com",
      "Last Updated": "17 Nov 2025, 5:30 PM"
    }],
    "metadata": {
      "batch_date": "17 Nov 2025, 5:30 PM",
      "job_count": 1,
      "add_separator": true
    }
  }'
```

## Troubleshooting

If jobs aren't being added:
1. Check that the Web App URL is correct in GitHub Secrets
2. Verify the Apps Script has permission to edit the sheet
3. Check the Apps Script execution logs (View > Logs)
4. Ensure the sheet ID is correct in the Apps Script code

## Sheet Headers

Make sure your Google Sheet has these column headers in row 1:
1. Company
2. Title
3. Type
4. Stipend/CTC
5. Apply Link
6. Last Updated
