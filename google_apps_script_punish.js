/*
 * Immediate email solution for Punish.
 * Receives jobs from GitHub Actions, writes new jobs to the Google Sheet,
 * and emails Punish immediately when new jobs are added.
 */

const SHEET_ID = "1nridtqY_EkI47W8dcKOBhuMLCazepmH9JNPuDXyuYLA";
const SHEET_NAME = "Sheet1";
const RECIPIENTS = ["punishmidha21@gmail.com"];

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const incomingJobs = data.jobs || [];
    const jobs = incomingJobs.filter(isRealJob);

    if (jobs.length === 0) {
      return jsonResponse({
        status: "success",
        message: "No real jobs to add"
      });
    }

    const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
    const existingLinks = getExistingLinks(sheet);
    const addedJobs = [];

    jobs.forEach(job => {
      const link = String(job["Apply Link"] || "").trim();
      if (!link || existingLinks.has(link)) {
        return;
      }

      sheet.insertRowBefore(2);
      sheet.getRange(2, 1, 1, 6).setValues([[
        job["Company"] || "",
        job["Title"] || "",
        job["Type"] || "",
        job["Stipend/CTC"] || "",
        link,
        job["Last Updated"] || formatTimestamp(new Date())
      ]]);
      sheet.getRange(2, 1, 1, 6).setBackground("#f0f7ff");

      existingLinks.add(link);
      addedJobs.push(job);
    });

    if (addedJobs.length > 0) {
      sendEmailForNewJobs(addedJobs);
    }

    return jsonResponse({
      status: "success",
      message: `Added ${addedJobs.length} new jobs${addedJobs.length > 0 ? " and sent email" : ""}`,
      added: addedJobs.length,
      emailSent: addedJobs.length > 0
    });
  } catch (error) {
    return jsonResponse({
      status: "error",
      message: error.toString()
    });
  }
}

function isRealJob(job) {
  return Boolean(
    job &&
    String(job["Company"] || "").trim() &&
    String(job["Title"] || "").trim() &&
    String(job["Apply Link"] || "").trim()
  );
}

function getExistingLinks(sheet) {
  const existingLinks = new Set();
  const lastRow = sheet.getLastRow();

  if (lastRow <= 1) {
    return existingLinks;
  }

  const links = sheet.getRange(2, 5, lastRow - 1, 1).getValues();
  links.forEach(row => {
    const link = String(row[0] || "").trim();
    if (link) {
      existingLinks.add(link);
    }
  });

  return existingLinks;
}

function sendEmailForNewJobs(jobs) {
  const tableRows = jobs.map(job => `
    <tr>
      <td style="padding: 8px; border: 1px solid #ddd;">${escapeHtml(job["Company"])}</td>
      <td style="padding: 8px; border: 1px solid #ddd;">${escapeHtml(job["Title"])}</td>
      <td style="padding: 8px; border: 1px solid #ddd;">${escapeHtml(job["Type"])}</td>
      <td style="padding: 8px; border: 1px solid #ddd;">${escapeHtml(job["Stipend/CTC"])}</td>
      <td style="padding: 8px; border: 1px solid #ddd;"><a href="${escapeAttribute(job["Apply Link"])}" style="color: #4285f4; text-decoration: none;">Apply Here</a></td>
      <td style="padding: 8px; border: 1px solid #ddd; font-size: 11px; color: #666;">${escapeHtml(job["Last Updated"])}</td>
    </tr>
  `).join("");

  const htmlBody = `
    <div style="font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto;">
      <h2 style="color: #1a73e8;">${jobs.length} new jobs for Punish</h2>
      <p style="color: #5f6368;">Fresh jobs were just added to the tracker.</p>

      <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
        <tr style="background-color: #f8f9fa;">
          <th style="padding: 12px; border: 1px solid #ddd; text-align: left;">Company</th>
          <th style="padding: 12px; border: 1px solid #ddd; text-align: left;">Role</th>
          <th style="padding: 12px; border: 1px solid #ddd; text-align: left;">Type</th>
          <th style="padding: 12px; border: 1px solid #ddd; text-align: left;">CTC/Stipend</th>
          <th style="padding: 12px; border: 1px solid #ddd; text-align: left;">Apply</th>
          <th style="padding: 12px; border: 1px solid #ddd; text-align: left;">Added</th>
        </tr>
        ${tableRows}
      </table>

      <p style="color: #5f6368; font-size: 12px;">
        View all jobs in the <a href="https://docs.google.com/spreadsheets/d/${SHEET_ID}/edit" style="color: #4285f4;">Google Sheet</a>.
      </p>
    </div>
  `;

  MailApp.sendEmail({
    to: RECIPIENTS.join(","),
    subject: `${jobs.length} new AI/ML and SDE jobs for Punish`,
    htmlBody
  });

  Logger.log(`Sent email with ${jobs.length} new jobs to ${RECIPIENTS.join(", ")}`);
}

function sendJobUpdates() {
  const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
  const data = sheet.getDataRange().getValues().slice(1);
  const newJobs = data.filter(row => {
    const lastUpdated = parseFormattedTimestamp(row[5]);
    if (!lastUpdated) {
      return false;
    }

    const diffHours = (Date.now() - lastUpdated.getTime()) / (1000 * 60 * 60);
    return diffHours <= 6;
  }).slice(0, 20);

  if (newJobs.length === 0) {
    Logger.log("No new jobs found. Skipping summary email.");
    return;
  }

  const jobs = newJobs.map(row => ({
    "Company": row[0],
    "Title": row[1],
    "Type": row[2],
    "Stipend/CTC": row[3],
    "Apply Link": row[4],
    "Last Updated": row[5]
  }));

  sendEmailForNewJobs(jobs);
}

function setupEmailTrigger() {
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => {
    if (trigger.getHandlerFunction() === "sendJobUpdates") {
      ScriptApp.deleteTrigger(trigger);
    }
  });

  ScriptApp.newTrigger("sendJobUpdates")
    .timeBased()
    .everyHours(6)
    .create();

  Logger.log("Set up trigger for 6-hour summary emails");
}

function testWebApp() {
  const testData = {
    jobs: [{
      "Company": "Test Company",
      "Title": "Test ML Intern",
      "Type": "Internship",
      "Stipend/CTC": "Rs 40000/month",
      "Apply Link": "https://example.com/test-job-" + Date.now(),
      "Last Updated": formatTimestamp(new Date())
    }]
  };

  const result = doPost({
    postData: {
      contents: JSON.stringify(testData)
    }
  });

  Logger.log(result.getContent());
}

function formatTimestamp(date) {
  const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const day = date.getDate().toString().padStart(2, "0");
  const month = months[date.getMonth()];
  const year = date.getFullYear();
  let hours = date.getHours();
  const minutes = date.getMinutes().toString().padStart(2, "0");
  const ampm = hours >= 12 ? "PM" : "AM";

  hours = hours % 12;
  hours = hours || 12;

  return `${day} ${month}, ${year} ${hours}:${minutes} ${ampm}`;
}

function parseFormattedTimestamp(timestampStr) {
  try {
    if (timestampStr instanceof Date) {
      return timestampStr;
    }

    const months = {
      Jan: 0,
      Feb: 1,
      Mar: 2,
      Apr: 3,
      May: 4,
      Jun: 5,
      Jul: 6,
      Aug: 7,
      Sep: 8,
      Oct: 9,
      Nov: 10,
      Dec: 11
    };

    const parts = String(timestampStr || "").split(" ");
    if (parts.length < 5) {
      return null;
    }

    const day = parseInt(parts[0], 10);
    const month = months[parts[1].replace(",", "")];
    const year = parseInt(parts[2], 10);
    const timeParts = parts[3].split(":");
    let hours = parseInt(timeParts[0], 10);
    const minutes = parseInt(timeParts[1], 10);
    const ampm = parts[4];

    if (ampm === "PM" && hours !== 12) {
      hours += 12;
    }
    if (ampm === "AM" && hours === 12) {
      hours = 0;
    }

    return new Date(year, month, day, hours, minutes);
  } catch (error) {
    const fallback = new Date(timestampStr);
    return Number.isNaN(fallback.getTime()) ? null : fallback;
  }
}

function jsonResponse(payload) {
  return ContentService
    .createTextOutput(JSON.stringify(payload))
    .setMimeType(ContentService.MimeType.JSON);
}

function escapeHtml(value) {
  return String(value || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function escapeAttribute(value) {
  return escapeHtml(value).replace(/`/g, "&#96;");
}
