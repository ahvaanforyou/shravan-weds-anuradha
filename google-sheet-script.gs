/**
 * =======================================================================
 * 💍 SHRAVAN & HIMA BINDU WEDDING — GOOGLE SHEETS RSVP WEBHOOK & DASHBOARD
 * =======================================================================
 * 
 * FEATURES:
 * 1. EXECUTIVE DASHBOARD WITH LIVE METRICS & FORMULAS (Rows 1-3):
 *    - Total Responses: COUNTA(B8:B)
 *    - Total Headcount / Guests: SUM(D8:D)
 *    - Total Attending Reception Headcount: SUMIF(E8:E, "Attending", D8:D)
 *    - Declined Count: COUNTIF(E8:E, "Declined")
 *    - Live Attendance Summary Breakdown
 * 
 * 2. STRUCTURED GUEST DATA COLUMNS (Rows 7+):
 *    - Col A: Timestamp
 *    - Col B: Guest / Family Name
 *    - Col C: Phone / WhatsApp Number
 *    - Col D: Total Guests
 *    - Col E: Attendance Status (Attending / Declined with badge styling)
 *    - Col F: Events Attending (Wedding Reception)
 *    - Col G: Warm Wishes / Blessings
 * 
 * 3. SMART IN-PLACE ROW EDITING:
 *    - When a guest edits their response on the website, it locates their existing row
 *      by phone number or name and updates that EXACT row in-place!
 *    - Prevents duplicates and keeps dashboard formulas 100% accurate.
 * 
 * =======================================================================
 * HOW TO SET UP (Takes ~1 minute):
 * 1. Create a new Google Sheet (or open an existing one).
 *    Rename the sheet tab to: "RSVP Responses"
 * 2. In Google Sheets top menu, click Extensions > Apps Script.
 * 3. Delete any default code in Code.gs, and PASTE THIS ENTIRE SCRIPT.
 * 4. Press Ctrl + S to save.
 * 5. In the toolbar at the top, select the function "setupSheet" from the dropdown.
 * 6. Click "Run" (▶).
 *    - If Google asks for permissions: Click "Review permissions" -> Select your account ->
 *      Click "Advanced" -> Click "Go to Untitled project (unsafe)" -> Click "Allow".
 *    - You will see the Royal Navy & Gold Executive Dashboard appear in your sheet!
 * 7. Click the blue "Deploy" button (top right) > "New deployment".
 *    - Click gear icon (Select type) > Choose "Web app".
 *    - Description: "Shravan & Hima Bindu RSVP Webhook"
 *    - Execute as: "Me (your email)"
 *    - Who has access: "Anyone" (CRITICAL: Do NOT choose "Only myself")
 *    - Click "Deploy".
 * 8. Copy the Web App URL (ends in /exec).
 * 9. Paste this URL into `GOOGLE_SHEET_WEBHOOK_URL` in `script.js`!
 * =======================================================================
 */

var SHEET_NAME = "RSVP Responses";

var HEADERS = [
  "Timestamp",
  "Guest / Family Name",
  "Phone / WhatsApp Number",
  "Total Guests",
  "Attendance Status",
  "Events Attending",
  "Warm Wishes / Blessings"
];

/**
 * Normalizes phone numbers to digits only for accurate matching
 */
function cleanPhone(p) {
  if (!p) return "";
  return String(p).replace(/\D/g, "");
}

/**
 * Normalizes text for clean comparison
 */
function cleanText(t) {
  if (!t) return "";
  return String(t).trim().toLowerCase();
}

/**
 * Searches the sheet to find an existing row for this guest.
 * Returns the 1-based row number (e.g. 8, 9...) if found, or -1 if new.
 */
function findExistingRowIndex(sheet, data, startRow) {
  var lastRow = sheet.getLastRow();
  if (lastRow < startRow) return -1;

  var numRows = lastRow - startRow + 1;
  // Read Col B (Name) & Col C (Phone) from startRow to lastRow
  var values = sheet.getRange(startRow, 2, numRows, 2).getValues();

  var targetPhone = cleanPhone(data.phone || data.contact || data.tel);
  var targetOrigPhone = cleanPhone(data.originalPhone || data.original_phone);
  var targetName = cleanText(data.name || data.fullName);
  var targetOrigName = cleanText(data.originalName || data.original_name);

  // 1. Primary check: Phone match (search newest rows first)
  if (targetPhone || targetOrigPhone) {
    for (var i = values.length - 1; i >= 0; i--) {
      var rowPhone = cleanPhone(values[i][1]); // Col C
      if (rowPhone && rowPhone.length >= 7) {
        if (targetPhone && (rowPhone === targetPhone || rowPhone.slice(-10) === targetPhone.slice(-10))) {
          return startRow + i;
        }
        if (targetOrigPhone && (rowPhone === targetOrigPhone || rowPhone.slice(-10) === targetOrigPhone.slice(-10))) {
          return startRow + i;
        }
      }
    }
  }

  // 2. Secondary check: Name match
  if (targetName || targetOrigName) {
    for (var j = values.length - 1; j >= 0; j--) {
      var rowName = cleanText(values[j][0]); // Col B
      if (rowName && rowName.length > 2) {
        if (targetName && rowName === targetName) {
          return startRow + j;
        }
        if (targetOrigName && rowName === targetOrigName) {
          return startRow + j;
        }
      }
    }
  }

  return -1; // New guest RSVP
}

/**
 * INITIALIZES THE ROYAL NAVY & GOLD DASHBOARD & STYLED DATA TABLE
 * Run this from Apps Script editor!
 */
function setupSheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.getActiveSheet();
    sheet.setName(SHEET_NAME);
  }
  sheet.clear();

  // Set column widths for optimal readability
  sheet.setColumnWidth(1, 160); // Timestamp
  sheet.setColumnWidth(2, 220); // Guest Name
  sheet.setColumnWidth(3, 190); // Phone / WhatsApp
  sheet.setColumnWidth(4, 110); // Total Guests
  sheet.setColumnWidth(5, 140); // Attendance Status
  sheet.setColumnWidth(6, 170); // Events Attending
  sheet.setColumnWidth(7, 360); // Warm Wishes / Blessings

  // =========================================================================
  // ROW 1: MASTER TITLE BANNER (Royal Navy #133979 & Warm Gold #D4AF37)
  // =========================================================================
  sheet.getRange("A1:G1").merge()
    .setValue("✨ SHRAVAN & HIMA BINDU — WEDDING RECEPTION RSVP DASHBOARD ✨")
    .setBackground("#133979") // Royal Navy Blue
    .setFontColor("#FFE58F")  // Bright Gold
    .setFontFamily("Georgia")
    .setFontSize(13)
    .setFontWeight("bold")
    .setHorizontalAlignment("center")
    .setVerticalAlignment("middle");
  sheet.setRowHeight(1, 40);

  // =========================================================================
  // ROW 2: DASHBOARD METRIC LABELS
  // =========================================================================
  sheet.getRange("A2:C2").merge().setValue("📊 TOTAL RESPONSES").setHorizontalAlignment("center");
  sheet.getRange("D2").setValue("👥 TOTAL GUESTS").setHorizontalAlignment("center");
  sheet.getRange("E2").setValue("🌸 ATTENDING RECEPTION").setHorizontalAlignment("center");
  sheet.getRange("F2").setValue("🕊️ DECLINED").setHorizontalAlignment("center");
  sheet.getRange("G2").setValue("🎉 ATTENDANCE SUMMARY").setHorizontalAlignment("center");

  // Style Metric Headers
  sheet.getRange("A2:C2").setBackground("#0D234C").setFontColor("#FFE58F").setFontSize(9).setFontWeight("bold").setVerticalAlignment("middle");
  sheet.getRange("D2").setBackground("#133979").setFontColor("#FFFFFF").setFontSize(9).setFontWeight("bold").setVerticalAlignment("middle");
  sheet.getRange("E2").setBackground("#1A4B9C").setFontColor("#FFFFFF").setFontSize(9).setFontWeight("bold").setVerticalAlignment("middle");
  sheet.getRange("F2").setBackground("#4A5568").setFontColor("#FFFFFF").setFontSize(9).setFontWeight("bold").setVerticalAlignment("middle");
  sheet.getRange("G2").setBackground("#0D234C").setFontColor("#FFE58F").setFontSize(9).setFontWeight("bold").setVerticalAlignment("middle");
  sheet.setRowHeight(2, 24);

  // =========================================================================
  // ROW 3: LIVE METRIC FORMULAS (Recalculate automatically with every RSVP)
  // =========================================================================
  sheet.getRange("A3:C3").merge().setFormula('=COUNTA(B8:B)');
  sheet.getRange("D3").setFormula('=SUM(D8:D)');
  sheet.getRange("E3").setFormula('=SUMIF(E8:E, "Attending", D8:D)'); // Headcount attending reception
  sheet.getRange("F3").setFormula('=COUNTIF(E8:E, "Declined")');        // Parties declined
  sheet.getRange("G3").setFormula('="Attending: " & COUNTIF(E8:E, "Attending") & " parties (" & SUMIF(E8:E, "Attending", D8:D) & " guests) | Declined: " & COUNTIF(E8:E, "Declined")');

  // Format Metric Values
  var valRange = sheet.getRange("A3:G3");
  valRange.setFontFamily("Georgia")
    .setFontSize(15)
    .setFontWeight("bold")
    .setHorizontalAlignment("center")
    .setVerticalAlignment("middle")
    .setBorder(true, true, true, true, true, true, "#D4AF37", SpreadsheetApp.BorderStyle.SOLID);
  sheet.setRowHeight(3, 34);

  // Custom Card Backgrounds
  sheet.getRange("A3:C3").setBackground("#F4F7FC").setFontColor("#0D234C");
  sheet.getRange("D3").setBackground("#FFFBEA").setFontColor("#133979").setFontSize(17); // Big Headcount
  sheet.getRange("E3").setBackground("#EBF3FE").setFontColor("#1A4B9C").setFontSize(16); // Attending Headcount
  sheet.getRange("F3").setBackground("#F7FAFC").setFontColor("#4A5568").setFontSize(16); // Declined Count
  sheet.getRange("G3").setBackground("#F4F7FC").setFontColor("#0D234C").setFontSize(10);

  // Empty separator rows
  sheet.setRowHeight(4, 8);
  sheet.setRowHeight(5, 8);

  // =========================================================================
  // ROW 6: TABLE SECTION BANNER
  // =========================================================================
  sheet.getRange("A6:G6").merge()
    .setValue("  📋 DETAILED GUEST RESPONSES (SMART IN-PLACE UPDATING)")
    .setBackground("#E8EEF8")
    .setFontColor("#133979")
    .setFontFamily("Georgia")
    .setFontSize(10)
    .setFontWeight("bold")
    .setVerticalAlignment("middle");
  sheet.setRowHeight(6, 24);

  // =========================================================================
  // ROW 7: COLUMN HEADERS
  // =========================================================================
  sheet.getRange(7, 1, 1, HEADERS.length).setValues([HEADERS]);
  var headerRange = sheet.getRange("A7:G7");
  headerRange.setBackground("#133979") // Royal Navy Blue
    .setFontColor("#FFFFFF")
    .setFontFamily("Georgia")
    .setFontSize(10)
    .setFontWeight("bold")
    .setHorizontalAlignment("center")
    .setVerticalAlignment("middle")
    .setBorder(true, true, true, true, true, true, "#D4AF37", SpreadsheetApp.BorderStyle.SOLID);
  sheet.setRowHeight(7, 30);

  // Freeze top 7 rows so dashboard & headers stay locked when scrolling
  sheet.setFrozenRows(7);

  // =========================================================================
  // ROW 8: SAMPLE TEST ROW
  // =========================================================================
  var testRow = [
    new Date().toLocaleString("en-US", { timeZone: "Asia/Kolkata" }),
    "Sample Guest (Example)",
    "+91 98765 43210",
    2,
    "Attending",
    "Wedding Reception",
    "Heartiest congratulations to Shravan & Hima Bindu! Wishing you both a lifetime of bliss."
  ];

  sheet.appendRow(testRow);
  formatDataRow(sheet, 8, "Attending");

  Logger.log("🎉 SUCCESS! Dashboard initialized with live Reception metrics!");
  return "SUCCESS: Dashboard initialized with live Reception metrics!";
}

/**
 * Styles a guest row with clean fonts and badge styling
 */
function formatDataRow(sheet, rowNum, status) {
  var rowRange = sheet.getRange(rowNum, 1, 1, 7);
  rowRange.setFontFamily("Arial")
    .setFontSize(10)
    .setVerticalAlignment("middle")
    .setBorder(true, true, true, true, true, true, "#E2E8F0", SpreadsheetApp.BorderStyle.SOLID);

  sheet.setRowHeight(rowNum, 28);

  // Center Total Guests, Attendance Status, and Events
  sheet.getRange(rowNum, 4, 1, 3).setHorizontalAlignment("center");
  sheet.getRange(rowNum, 4).setFontWeight("bold"); // Bold total guests

  // Badge colors for Attendance Status (Col E)
  var cellStatus = sheet.getRange(rowNum, 5);
  if (status === "Attending") {
    cellStatus.setBackground("#EBF3FE").setFontColor("#133979").setFontWeight("bold"); // Royal Blue Badge
  } else {
    cellStatus.setBackground("#F1F5F9").setFontColor("#64748B").setFontWeight("normal"); // Slate Gray Badge
  }
}

/**
 * Ensures table structure exists before receiving webhooks
 */
function ensureInitialized(sheet) {
  if (sheet.getLastRow() < 7 || sheet.getRange(7, 1).getValue() !== "Timestamp") {
    setupSheet();
  }
}

/**
 * Handles RSVP submissions and edits from the website
 */
function doPost(e) {
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(10000);

    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName(SHEET_NAME);
    if (!sheet) {
      sheet = ss.getActiveSheet();
      sheet.setName(SHEET_NAME);
    }
    ensureInitialized(sheet);

    var data = {};
    if (e && e.postData && e.postData.contents) {
      try {
        data = JSON.parse(e.postData.contents);
      } catch (parseErr) {
        data = e.parameter || {};
      }
    } else if (e && e.parameter) {
      data = e.parameter;
    }

    var startRow = 8;
    if (sheet.getRange(1, 1).getValue() === "Timestamp") {
      startRow = 2;
    } else if (sheet.getRange(7, 1).getValue() === "Timestamp") {
      startRow = 8;
    }

    var baseTimestamp = data.timestamp 
      ? new Date(data.timestamp).toLocaleString("en-US", { timeZone: "Asia/Kolkata" }) 
      : new Date().toLocaleString("en-US", { timeZone: "Asia/Kolkata" });

    var name = (data.name || data.fullName || "-").toString().trim();
    var phone = (data.phone || data.contact || "-").toString().trim();
    var attending = (data.attending === "yes" || data.attending === "Attending" || data.attending === true) ? "Attending" : "Declined";
    
    var guestCount = 0;
    if (attending === "Attending") {
      guestCount = Number(data.guests !== undefined ? data.guests : (data.guestCount || data.guest_count || 1));
      if (isNaN(guestCount) || guestCount <= 0) {
        guestCount = 1;
      }
    }

    var events = (attending === "Attending") ? (data.events || "Wedding Reception") : "None";
    var message = (data.message || data.note || data.warm_wishes || "-").toString().trim();

    // Check for existing RSVP (Smart In-Place Row Edit)
    var existingRow = findExistingRowIndex(sheet, data, startRow);
    var isUpdate = (existingRow > 0);
    var targetRow = isUpdate ? existingRow : Math.max(startRow, sheet.getLastRow() + 1);
    var displayTimestamp = isUpdate ? (baseTimestamp + " (Edited)") : baseTimestamp;

    var rowValues = [
      displayTimestamp,
      name,
      phone,
      guestCount,
      attending,
      events,
      message
    ];

    sheet.getRange(targetRow, 1, 1, rowValues.length).setValues([rowValues]);
    formatDataRow(sheet, targetRow, attending);

    SpreadsheetApp.flush();

    var actionTaken = isUpdate ? "updated" : "created";
    Logger.log("RSVP " + actionTaken + " successfully at row " + targetRow + " for " + name);

    return ContentService.createTextOutput(JSON.stringify({
      status: "success",
      action: actionTaken,
      message: isUpdate ? "RSVP updated in same row in Google Sheets" : "RSVP recorded in Google Sheets",
      name: name,
      rowNumber: targetRow
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    Logger.log("Error in doPost: " + error.toString());
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      message: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);

  } finally {
    lock.releaseLock();
  }
}

/**
 * Health check endpoint for testing in browser
 */
function doGet(e) {
  return ContentService.createTextOutput("💍 Shravan & Hima Bindu Wedding RSVP Webhook is ACTIVE and connected! Ready to receive RSVPs.")
    .setMimeType(ContentService.MimeType.TEXT);
}
