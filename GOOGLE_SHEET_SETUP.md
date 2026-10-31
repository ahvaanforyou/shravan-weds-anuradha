# 💍 Shravan & Hima Bindu Wedding — Google Sheets Dashboard & RSVP Setup Guide

This guide explains how to set up your Google Sheet with the **Royal Executive Dashboard**, **live Reception totals**, and **Smart In-Place RSVP Row Updates** (just like the Kalyan Wedding setup).

---

### Key Features of this Setup:
1. **Executive Dashboard (Rows 1–3)**:
   - **Total Responses**: `=COUNTA(B8:B)`
   - **Total Guests (Headcount)**: `=SUM(D8:D)`
   - **Attending Reception**: `=SUMIF(E8:E, "Attending", D8:D)` *(Live headcount attending Reception)*
   - **Declined Count**: `=COUNTIF(E8:E, "Declined")` *(Live count of declined parties)*
   - **Attendance Breakdown**: Live summary of parties and guest counts
2. **Dedicated Columns (Rows 7+)**:
   - `Timestamp`
   - `Guest / Family Name`
   - `Phone / WhatsApp Number`
   - `Total Guests`
   - `Attendance Status` *(Attending / Declined with badge styling)*
   - `Events Attending` *(Wedding Reception)*
   - `Warm Wishes / Blessings`
3. **Smart In-Place Row Editing**:
   - When a guest edits their RSVP on the website, it locates their existing row by phone or name and **updates that exact row** instead of creating a duplicate.
   - All live formulas in the dashboard immediately recalculate!
4. **Resilient Offline / Local Fallback**:
   - Responses are immediately saved to browser local storage so even if network lags, the user always sees their confirmed response with celebratory confetti.

---

### Step 1: Open Google Sheets Apps Script
1. Open a new or existing **Google Sheet** (e.g. named `Shravan & Hima Bindu Wedding RSVPs`).
2. Rename the active sheet tab at the bottom to: **`RSVP Responses`**.
3. In the top menu, click **Extensions** > **Apps Script**.
4. Select all existing text in the editor (`Code.gs`) and delete it.

---

### Step 2: Paste the Master Script
1. Open [`google-sheet-script.gs`](./google-sheet-script.gs) in this repository.
2. Copy the entire contents of [`google-sheet-script.gs`](./google-sheet-script.gs) and paste it into the Apps Script editor.
3. Click the 💾 **Save** icon (or press `Ctrl+S`).

---

### Step 3: Run `setupSheet`
1. In the toolbar at the top of Apps Script, find the function dropdown menu (it may say `doPost`).
2. Click the dropdown and select **`setupSheet`**.
3. Click **▶ Run**.
4. *(If prompted, click "Review permissions", select your Google account, click "Advanced" > "Go to Untitled project (unsafe)", and click "Allow")*.
5. Switch back to your Google Sheet:
   - You will see the **Royal Navy & Gold Executive Dashboard** at the top with:
     - Master Title Banner in Royal Navy Blue & Gold
     - Live metric cards showing **Total Responses**, **Total Guests**, **Attending Reception**, and **Declined**
     - Table headers in Row 7 in Royal Navy
     - Sample test row at Row 8 with badge styling
     - Top 7 rows frozen so the dashboard stays visible as you scroll!

---

### Step 4: Deploy as Webhook
1. In Apps Script, click the blue **Deploy** button (top right) and choose **New deployment** (or **Manage deployments** > edit).
2. Click **Select type** (gear icon) > **Web app**.
3. Fill in the fields:
   - **Description**: `Shravan & Hima Bindu RSVP Webhook`
   - **Execute as**: `Me (your email)`
   - **Who has access**: `Anyone` *(⚠️ CRITICAL: DO NOT select "Only myself", otherwise the website cannot send RSVPs!)*
4. Click **Deploy**.
5. Copy the **Web App URL** (starts with `https://script.google.com/macros/s/.../exec`).

---

### Step 5: Connect Webhook URL in `script.js`
Your Google Sheets Webhook URL is now connected in `script.js`:
```js
const GOOGLE_SHEET_WEBHOOK_URL = 'https://script.google.com/macros/s/AKfycbz0sEemDhwFNvyDz_cajxdWdbQPt5w_3GSe48h1FPoqlCG2Aa8OP8JbiZyReO_w3G1m4Q/exec';
```
All RSVP submissions from the website are now recorded and updated directly in your Google Sheet!
