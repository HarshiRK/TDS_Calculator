# TDS (Tax Deducted at Source) Compliance Calculator

A professional, high-performance web application designed for Chartered Accountant (CA) firms, Company Secretary (CS) firms, and corporate finance/tax teams to instantly calculate TDS rates, threshold breaches, and track legal citations.

---

## Features

1. **Hot-Swappable Rates Sheet**: Reads directly from `backend/data/tds_rates.xlsx` at runtime on every request. Swapping the file updates all rates and rules immediately.
2. **Compliance Explanations**: Fully detailed legal citations and logic footnotes mapped directly from the Income Tax Act, 1961.
3. **Smart PAN Penalty Resolution**: Automatically applies Section 206AA overrides (higher rate of 20% or 5% under Section 194Q) if the PAN status is toggled off.
4. **Aggregate Payment Adjustments**: Supports multi-threshold evaluation for contractor payments (Section 194C) via a single/aggregate toggle.
5. **Indian Currency Formatting**: Commas are dynamically added using the Indian numbering system format (e.g. `1,50,000` instead of `150,000`) for visual accuracy.
6. **Recent Calculation Glance Drawer**: Automatically logs the last 5 calculations in `localStorage` for rapid double-check workflows.

---

## Excel Rate Sheet Template Structure

The calculator reads `backend/data/tds_rates.xlsx` dynamically. If replacing this file, ensure the following columns are present case-insensitively:

| Column Header | Data Type | Description |
| :--- | :--- | :--- |
| **Row ID** | Text | A unique alphanumeric identifier for each rate row (e.g. `194C-01`). |
| **Section** | Text | The Income Tax Act section code (e.g. `194C`, `194J`). |
| **Nature of Payment** | Text | Nature of transaction (e.g. `Payments to Contractors`). |
| **Payer Category** | Text | Text description specifying who is liable to deduct TDS. |
| **Payee Type** | Text | Broad recipient type (e.g. `Individual/HUF` or `Non-Individual Resident`). |
| **Threshold Amount (Rs)** | Numeric | Monetary threshold limit. No TDS is deducted below this. |
| **Threshold Condition** | Text | Operator to evaluate threshold (`>` or `>=`). |
| **Threshold Sub-condition** | Text | Conditions describing limits (e.g. `Single payment in FY`). |
| **Rate of TDS (%)** | Text/Numeric | Standard TDS percentage. Enter numeric value (e.g. `1`, `10`) or `Avg` for Salary. |
| **Payee Sub-type for Rate** | Text | Detailed payee keyword match (e.g. `Individual / HUF payee` or `Company / Firm`). |
| **Effective From** | Date/Text | Commencement date of this tax rate. |
| **Effective To** | Date/Text | Expiration date of this tax rate. |
| **Notes** | Text | Compliance notes and remarks, displayed in the legal panel. |

---

## How to Run & Host on Streamlit

### 1. Run Locally (Streamlit)
To start the Streamlit application directly:
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```
This launches the full TDS calculator UI on **`http://localhost:8501`**.

---

### 2. Deploy to Streamlit Community Cloud (Free Hosting)
You can host this application online for your team in under 2 minutes:

1. Push this project folder to a GitHub repository.
2. Sign in to **[share.streamlit.io](https://share.streamlit.io)** using your GitHub account.
3. Click **"New app"**.
4. Select your repository, branch (`main`), and set the **Main file path** to:
   ```
   streamlit_app.py
   ```
5. Click **"Deploy!"**. Streamlit Cloud will automatically install `requirements.txt` and launch your live public/private web app with a shareable URL.

---

## Alternative: React + Flask Mode

If you prefer to run the separate React frontend and Flask API:
```bash
# Run both servers concurrently
npm run dev
```
- React UI: `http://localhost:5173`
- Flask API: `http://127.0.0.1:5000`

