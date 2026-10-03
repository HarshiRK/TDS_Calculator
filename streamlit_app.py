import os
import sys
import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="TDS Compliance Calculator | Income Tax Act, 1961",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Professional Blue & White Custom CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Top Header Bar */
    .top-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
        color: white;
        padding: 1.25rem 1.75rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15);
    }
    .top-header h1 {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
        color: white;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .top-header p {
        font-size: 0.825rem;
        margin: 0.25rem 0 0 0;
        color: #dbeafe;
        font-weight: 400;
    }
    
    /* Card Container */
    .custom-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        margin-bottom: 1.25rem;
    }
    
    /* Section Title */
    .card-title {
        font-size: 0.875rem;
        font-weight: 700;
        color: #1e293b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #f1f5f9;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    /* KPI Metric Cards */
    .metric-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-bottom: 1.25rem;
    }
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.25rem;
        text-align: left;
    }
    .metric-card.highlight {
        background: #eff6ff;
        border-color: #bfdbfe;
    }
    .metric-label {
        font-size: 0.75rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.25rem;
    }
    .metric-value {
        font-size: 1.75rem;
        font-weight: 800;
        color: #1e293b;
        line-height: 1.2;
    }
    .metric-value.blue {
        color: #2563eb;
    }
    
    /* Status Banners */
    .status-banner {
        padding: 0.875rem 1rem;
        border-radius: 8px;
        font-size: 0.8125rem;
        font-weight: 500;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.625rem;
    }
    .status-banner.success {
        background-color: #ecfdf5;
        border: 1px solid #a7f3d0;
        color: #065f46;
    }
    .status-banner.warning {
        background-color: #fffbeb;
        border: 1px solid #fde68a;
        color: #92400e;
    }
    
    /* Explanation Sub-cards */
    .exp-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.875rem;
        margin-top: 0.75rem;
    }
    .exp-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.875rem;
    }
    .exp-title {
        font-size: 0.75rem;
        font-weight: 700;
        color: #475569;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }
    .exp-desc {
        font-size: 0.8125rem;
        color: #334155;
        line-height: 1.45;
        margin: 0;
    }
    
    /* Footer */
    .footer-text {
        text-align: center;
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #e2e8f0;
    }
    
    /* Button primary styling */
    div.stButton > button:first-child {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.2s;
    }
    div.stButton > button:first-child:hover {
        background-color: #1d4ed8;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Built-in Legal Citations & References
# ---------------------------------------------------------
SECTION_REFERENCES = {
    "192": {
        "citation": "Section 192, Income Tax Act, 1961",
        "description": "Tax Deduction on Salary. Payer must deduct tax on estimated annual income using average rates.",
        "rule": "Rule 26 of the Income Tax Rules, 1962."
    },
    "192A": {
        "citation": "Section 192A, Income Tax Act, 1961",
        "description": "Payment of accumulated balance due to an employee from Employees Provident Fund (EPF) scheme.",
        "rule": "Applicable on premature withdrawal exceeding ₹50,000 before 5 years of continuous service."
    },
    "193": {
        "citation": "Section 193, Income Tax Act, 1961",
        "description": "Interest on Securities. Covers interest paid on floating rate savings bonds and debentures.",
        "rule": "Rule 37A of the Income Tax Rules, 1962."
    },
    "194": {
        "citation": "Section 194, Income Tax Act, 1961",
        "description": "Dividends. Paid by a domestic company to a resident shareholder.",
        "rule": "Applicable on dividend distribution or payment, whichever is earlier."
    },
    "194A": {
        "citation": "Section 194A, Income Tax Act, 1961",
        "description": "Interest other than interest on securities (e.g. bank FD interest, interest on loans).",
        "rule": "Includes enhanced limits of ₹50,000 for senior citizens under Section 194A(3)."
    },
    "194B": {
        "citation": "Section 194B, Income Tax Act, 1961",
        "description": "Winnings from lottery, crossword puzzles, card games, or other games of any sort.",
        "rule": "Flat 30% rate under Section 115BB. Non-PAN case has no extra penalty since rate exceeds 20%."
    },
    "194BA": {
        "citation": "Section 194BA, Income Tax Act, 1961",
        "description": "Winnings from online games. Deducted on net winnings.",
        "rule": "Section 194BA inserted by Finance Act, 2023. Flat 30% rate under Section 115BBJ."
    },
    "194BB": {
        "citation": "Section 194BB, Income Tax Act, 1961",
        "description": "Winnings from horse races.",
        "rule": "Flat 30% rate. Applicable at the time of payment."
    },
    "194C": {
        "citation": "Section 194C, Income Tax Act, 1961",
        "description": "Payments to contractors and sub-contractors for carrying out work.",
        "rule": "Rule 30 of the Income Tax Rules. 1% for Individual/HUF payees, 2% for Corporate/Firm/Other payees."
    },
    "194D": {
        "citation": "Section 194D, Income Tax Act, 1961",
        "description": "Insurance commission paid to a resident agent.",
        "rule": "Deduction at the time of credit or payment, whichever is earlier."
    },
    "194DA": {
        "citation": "Section 194DA, Income Tax Act, 1961",
        "description": "Sum paid under a life insurance policy (if not exempt u/s 10(10D)).",
        "rule": "Deducted at 2% (w.e.f. 01-10-2024, previously 5%) on the income component of maturity proceeds."
    },
    "194G": {
        "citation": "Section 194G, Income Tax Act, 1961",
        "description": "Commission, remuneration or prize on the sale of lottery tickets.",
        "rule": "Deducted at 2% (w.e.f. 01-10-2024, previously 5%) on commission exceeding ₹15,000."
    },
    "194H": {
        "citation": "Section 194H, Income Tax Act, 1961",
        "description": "Commission or brokerage paid to resident individuals or firms.",
        "rule": "Deducted at 2% (w.e.f. 01-10-2024, previously 5%) on payments exceeding ₹15,000."
    },
    "194I": {
        "citation": "Section 194-I, Income Tax Act, 1961",
        "description": "Rent. Covers payments for leasing land, buildings, furniture, fittings, machinery, or equipment.",
        "rule": "2% for plant/machinery/equipment; 10% for land/building/furniture/fittings."
    },
    "194IA": {
        "citation": "Section 194-IA, Income Tax Act, 1961",
        "description": "Payment on transfer of certain immovable property (other than agricultural land).",
        "rule": "1% on consideration or stamp duty value, whichever is higher, exceeding ₹50 lakhs."
    },
    "194IB": {
        "citation": "Section 194-IB, Income Tax Act, 1961",
        "description": "Rent paid by certain individuals or HUF not liable to audit under Section 44AB.",
        "rule": "2% (w.e.f. 01-10-2024, previously 5%) on monthly rent exceeding ₹50,000."
    },
    "194J": {
        "citation": "Section 194J, Income Tax Act, 1961",
        "description": "Fees for professional or technical services, royalty, or non-compete fees.",
        "rule": "2% for technical services, cinematographic royalties, or call centers; 10% for professional fees."
    },
    "194K": {
        "citation": "Section 194K, Income Tax Act, 1961",
        "description": "Income in respect of units of a mutual fund (other than capital gains).",
        "rule": "10% rate on income distributions exceeding ₹5,000 in a financial year."
    },
    "194LA": {
        "citation": "Section 194LA, Income Tax Act, 1961",
        "description": "Compensation on compulsory acquisition of certain immovable property.",
        "rule": "10% rate on compensation exceeding ₹2.5 lakhs in a financial year."
    },
    "194M": {
        "citation": "Section 194M, Income Tax Act, 1961",
        "description": "Contractor, commission, or professional fees paid by individuals/HUFs not covered u/s 194C, 194H, or 194J.",
        "rule": "2% (w.e.f. 01-10-2024, previously 5%) on aggregate payments exceeding ₹50 lakhs in a FY."
    },
    "194N": {
        "citation": "Section 194N, Income Tax Act, 1961",
        "description": "Cash withdrawal from banks, co-operative societies, or post offices.",
        "rule": "2% or 5% depending on amount slabs and non-filer status (under Section 194N 2nd proviso)."
    },
    "194P": {
        "citation": "Section 194P, Income Tax Act, 1961",
        "description": "Deduction of tax in case of specified senior citizens (age >= 75 years).",
        "rule": "The bank computes tax liability after giving effect to deductions and rebate u/s 87A."
    },
    "194Q": {
        "citation": "Section 194Q, Income Tax Act, 1961",
        "description": "Deduction of tax on payment for purchase of goods.",
        "rule": "0.1% on value exceeding ₹50 lakhs. Rate is 5% in no-PAN cases (exception to the standard 20% u/s 206AA)."
    },
    "194R": {
        "citation": "Section 194R, Income Tax Act, 1961",
        "description": "Tax on benefit or perquisite arising from business or exercise of a profession.",
        "rule": "10% on benefits exceeding ₹20,000 in a financial year."
    }
}

PENALTY_PAN_REFERENCE = {
    "citation": "Section 206AA, Income Tax Act, 1961",
    "description": "Higher rate of TDS in case of non-furnishing of Permanent Account Number (PAN).",
    "rule": "Tax shall be deducted at 20% (or 5% under Section 194Q), or the statutory rate, whichever is higher."
}

def get_legal_reference(section_code):
    normalized = str(section_code).strip().upper()
    if normalized in ["194-I", "194I"]:
        return SECTION_REFERENCES.get("194I")
    if normalized in ["194-IA", "194IA"]:
        return SECTION_REFERENCES.get("194IA")
    if normalized in ["194-IB", "194IB"]:
        return SECTION_REFERENCES.get("194IB")
    return SECTION_REFERENCES.get(normalized, {
        "citation": f"Section {section_code}, Income Tax Act, 1961",
        "description": "Standard TDS provisions under Chapter XVII-B.",
        "rule": "Applicable statutory rules apply."
    })

# ---------------------------------------------------------
# Built-in Default TDS Rate Dataset (Fail-safe for Cloud)
# ---------------------------------------------------------
BUILTIN_RATES = [
  {"row_id": "192-01", "section": "192", "nature_of_payment": "Salary", "payer_category": "Any employer", "payee_type": "Individual/HUF", "threshold_amount": 0.0, "threshold_condition": "N/A", "threshold_sub_condition": "Basic exemption limit applies", "rate_of_tds": "Avg", "payee_sub_type_rate": "All employees", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "Rate = average income-tax on estimated annual salary. No fixed %."},
  {"row_id": "192A-01", "section": "192A", "nature_of_payment": "Premature EPF withdrawal", "payer_category": "Trustees of EPF Scheme", "payee_type": "Individual/HUF", "threshold_amount": 50000.0, "threshold_condition": ">=", "threshold_sub_condition": "Aggregate payment in FY", "rate_of_tds": "10", "payee_sub_type_rate": "All", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "TDS on taxable withdrawal. No deduction if Form 15G/15H submitted."},
  {"row_id": "193-01", "section": "193", "nature_of_payment": "Interest on Securities", "payer_category": "Any payer", "payee_type": "Any Resident", "threshold_amount": 10000.0, "threshold_condition": ">", "threshold_sub_condition": "Interest on Savings Bonds / Govt securities", "rate_of_tds": "10", "payee_sub_type_rate": "All", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "Savings Bonds & notified Govt securities included."},
  {"row_id": "193-02", "section": "193", "nature_of_payment": "Interest on Securities (Debentures)", "payer_category": "Any payer", "payee_type": "Individual/HUF", "threshold_amount": 5000.0, "threshold_condition": ">", "threshold_sub_condition": "Debentures by listed public company", "rate_of_tds": "10", "payee_sub_type_rate": "Individual/HUF", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "Threshold Rs 5,000 for this specific debenture case only."},
  {"row_id": "193-03", "section": "193", "nature_of_payment": "Interest on Securities (Other cases)", "payer_category": "Any payer", "payee_type": "Any Resident", "threshold_amount": 0.0, "threshold_condition": "N/A", "threshold_sub_condition": "Any other case", "rate_of_tds": "10", "payee_sub_type_rate": "All", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "No monetary threshold in other cases."},
  {"row_id": "194-01", "section": "194", "nature_of_payment": "Dividend (Individual Shareholder)", "payer_category": "Principal Officer of domestic company", "payee_type": "Individual/HUF", "threshold_amount": 5000.0, "threshold_condition": ">", "threshold_sub_condition": "Dividend paid other than cash in FY", "rate_of_tds": "10", "payee_sub_type_rate": "Individual", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "Deduct before making payment or distribution."},
  {"row_id": "194-02", "section": "194", "nature_of_payment": "Dividend (Non-Individual Shareholder)", "payer_category": "Principal Officer of domestic company", "payee_type": "Non-Individual Resident", "threshold_amount": 0.0, "threshold_condition": "N/A", "threshold_sub_condition": "No threshold for non-individual", "rate_of_tds": "10", "payee_sub_type_rate": "Others", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "No threshold in all other cases."},
  {"row_id": "194A-01", "section": "194A", "nature_of_payment": "Interest from Banks / Co-op Banks / Post Office", "payer_category": "Banking company / Co-op bank / Post office", "payee_type": "Any Resident", "threshold_amount": 40000.0, "threshold_condition": ">", "threshold_sub_condition": "Interest by banking co or post office", "rate_of_tds": "10", "payee_sub_type_rate": "General", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "Standard threshold for bank/co-op/post office deposits."},
  {"row_id": "194A-02", "section": "194A", "nature_of_payment": "Interest from Banks (Senior Citizen)", "payer_category": "Banking company / Co-op bank / Post office", "payee_type": "Senior Citizen", "threshold_amount": 50000.0, "threshold_condition": ">", "threshold_sub_condition": "Interest to resident senior citizen", "rate_of_tds": "10", "payee_sub_type_rate": "Senior Citizen", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "Enhanced threshold of Rs 50,000 for senior citizens."},
  {"row_id": "194A-03", "section": "194A", "nature_of_payment": "Interest (Other Payers / NBFCs / Unsecured Loans)", "payer_category": "Any other payer (non-bank)", "payee_type": "Any Resident", "threshold_amount": 5000.0, "threshold_condition": ">", "threshold_sub_condition": "Other interest cases", "rate_of_tds": "10", "payee_sub_type_rate": "All", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "Applies to NBFCs, companies, firms, individuals."},
  {"row_id": "194B-01", "section": "194B", "nature_of_payment": "Winnings from lottery / crossword / card game / betting", "payer_category": "Person responsible for paying", "payee_type": "Any Person", "threshold_amount": 10000.0, "threshold_condition": ">", "threshold_sub_condition": "Amount or aggregate of amounts in FY", "rate_of_tds": "30", "payee_sub_type_rate": "All", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "Flat 30% at time of payment."},
  {"row_id": "194BA-01", "section": "194BA", "nature_of_payment": "Winnings from online games", "payer_category": "Person responsible for paying", "payee_type": "Any Person", "threshold_amount": 0.0, "threshold_condition": "N/A", "threshold_sub_condition": "Net winnings in user account", "rate_of_tds": "30", "payee_sub_type_rate": "All", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "Flat 30% deducted at end of FY or withdrawal."},
  {"row_id": "194BB-01", "section": "194BB", "nature_of_payment": "Winnings from horse race", "payer_category": "Bookmaker or licence holder", "payee_type": "Any Person", "threshold_amount": 10000.0, "threshold_condition": ">", "threshold_sub_condition": "Amount or aggregate in FY", "rate_of_tds": "30", "payee_sub_type_rate": "All", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "At time of payment."},
  {"row_id": "194C-01", "section": "194C", "nature_of_payment": "Payments to Contractors (Individual / HUF)", "payer_category": "All specified payers", "payee_type": "Individual/HUF", "threshold_amount": 30000.0, "threshold_condition": ">", "threshold_sub_condition": "Single payment in FY", "rate_of_tds": "1", "payee_sub_type_rate": "Individual / HUF payee", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "Rate 1% for Individual/HUF contractors."},
  {"row_id": "194C-02", "section": "194C", "nature_of_payment": "Payments to Contractors (Aggregate - Individual/HUF)", "payer_category": "All specified payers", "payee_type": "Individual/HUF", "threshold_amount": 100000.0, "threshold_condition": ">", "threshold_sub_condition": "Aggregate payments to contractor in FY", "rate_of_tds": "1", "payee_sub_type_rate": "Individual / HUF payee", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "Aggregate threshold Rs 1,00,000."},
  {"row_id": "194C-03", "section": "194C", "nature_of_payment": "Payments to Contractors (Company / Firm / Others)", "payer_category": "All specified payers", "payee_type": "Non-Individual Resident", "threshold_amount": 30000.0, "threshold_condition": ">", "threshold_sub_condition": "Single payment in FY", "rate_of_tds": "2", "payee_sub_type_rate": "Company / Firm / Other payee", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "Rate 2% for Corporate / Firm / Other payees."},
  {"row_id": "194C-04", "section": "194C", "nature_of_payment": "Payments to Contractors (Aggregate - Company / Firm)", "payer_category": "All specified payers", "payee_type": "Non-Individual Resident", "threshold_amount": 100000.0, "threshold_condition": ">", "threshold_sub_condition": "Aggregate payments to contractor in FY", "rate_of_tds": "2", "payee_sub_type_rate": "Company / Firm / Other payee", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "Aggregate threshold Rs 1,00,000 for non-individuals."},
  {"row_id": "194D-01", "section": "194D", "nature_of_payment": "Insurance Commission (Non-corporate)", "payer_category": "Insurance entity", "payee_type": "Resident (Non-corporate)", "threshold_amount": 15000.0, "threshold_condition": ">", "threshold_sub_condition": "Amount or aggregate in FY", "rate_of_tds": "5", "payee_sub_type_rate": "Non-corporate Resident", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "5% rate for resident individuals/firms."},
  {"row_id": "194D-02", "section": "194D", "nature_of_payment": "Insurance Commission (Domestic Company)", "payer_category": "Insurance entity", "payee_type": "Company", "threshold_amount": 15000.0, "threshold_condition": ">", "threshold_sub_condition": "Amount or aggregate in FY", "rate_of_tds": "10", "payee_sub_type_rate": "Domestic Company", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "Higher rate 10% for domestic company."},
  {"row_id": "194DA-01", "section": "194DA", "nature_of_payment": "Sum under Life Insurance Policy", "payer_category": "Insurance entity", "payee_type": "Any Resident", "threshold_amount": 100000.0, "threshold_condition": ">=", "threshold_sub_condition": "Amount or aggregate in FY", "rate_of_tds": "2", "payee_sub_type_rate": "All", "effective_from": "1/10/2024", "effective_to": "31-03-2099", "notes": "Rate 2% w.e.f. 01-10-2024 on income component."},
  {"row_id": "194G-01", "section": "194G", "nature_of_payment": "Commission on sale of lottery tickets", "payer_category": "Specified payer", "payee_type": "Any Resident", "threshold_amount": 15000.0, "threshold_condition": ">", "threshold_sub_condition": "Amount or aggregate in FY", "rate_of_tds": "2", "payee_sub_type_rate": "All", "effective_from": "1/10/2024", "effective_to": "31-03-2099", "notes": "Rate 2% w.e.f. 01-10-2024."},
  {"row_id": "194H-01", "section": "194H", "nature_of_payment": "Commission or Brokerage", "payer_category": "Specified business / company / audited person", "payee_type": "Any Resident", "threshold_amount": 15000.0, "threshold_condition": ">", "threshold_sub_condition": "Amount or aggregate in FY", "rate_of_tds": "2", "payee_sub_type_rate": "All", "effective_from": "1/10/2024", "effective_to": "31-03-2099", "notes": "Rate reduced to 2% w.e.f. 01-10-2024 by Finance Act 2024."},
  {"row_id": "194I-01", "section": "194-I", "nature_of_payment": "Rent — Plant, Machinery & Equipment", "payer_category": "Specified business / company / audited person", "payee_type": "Any Resident", "threshold_amount": 240000.0, "threshold_condition": ">", "threshold_sub_condition": "Amount or aggregate in FY", "rate_of_tds": "2", "payee_sub_type_rate": "Plant & Machinery / Equipment", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "Lower rate 2% for P&M and equipment leasing."},
  {"row_id": "194I-02", "section": "194-I", "nature_of_payment": "Rent — Land, Building, Furniture & Fittings", "payer_category": "Specified business / company / audited person", "payee_type": "Any Resident", "threshold_amount": 240000.0, "threshold_condition": ">", "threshold_sub_condition": "Amount or aggregate in FY", "rate_of_tds": "10", "payee_sub_type_rate": "Land / Building / Furniture / Fittings", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "Higher rate 10% for immovable property and fittings."},
  {"row_id": "194IA-01", "section": "194-IA", "nature_of_payment": "Payment on transfer of immovable property", "payer_category": "Transferee / Buyer", "payee_type": "Any Resident", "threshold_amount": 5000000.0, "threshold_condition": ">=", "threshold_sub_condition": "Consideration or stamp value >= 50 Lakhs", "rate_of_tds": "1", "payee_sub_type_rate": "All", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "1% TDS on consideration or stamp duty value."},
  {"row_id": "194IB-01", "section": "194-IB", "nature_of_payment": "Rent by Individual/HUF (not audited u/s 44AB)", "payer_category": "Individual/HUF tenant", "payee_type": "Any Resident", "threshold_amount": 50000.0, "threshold_condition": ">", "threshold_sub_condition": "Per month or part of month", "rate_of_tds": "2", "payee_sub_type_rate": "All", "effective_from": "1/10/2024", "effective_to": "31-03-2099", "notes": "Rate 2% w.e.f. 01-10-2024. Deduct at last month of tenancy."},
  {"row_id": "194J-01", "section": "194J", "nature_of_payment": "Fees for Technical Services / Royalty for Films", "payer_category": "Specified payer", "payee_type": "Any Resident", "threshold_amount": 30000.0, "threshold_condition": ">", "threshold_sub_condition": "Amount or aggregate per category in FY", "rate_of_tds": "2", "payee_sub_type_rate": "Technical services / Cinematographic royalty", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "2% for fees for technical services and royalty for films."},
  {"row_id": "194J-02", "section": "194J", "nature_of_payment": "Fees — Call Centre Operations only", "payer_category": "Specified payer", "payee_type": "Any Resident", "threshold_amount": 30000.0, "threshold_condition": ">", "threshold_sub_condition": "Amount or aggregate in FY", "rate_of_tds": "2", "payee_sub_type_rate": "Call centre payee", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "2% where payee is engaged ONLY in call centre operations."},
  {"row_id": "194J-03", "section": "194J", "nature_of_payment": "Fees for Professional Services / Director Remuneration / Non-compete", "payer_category": "Specified payer", "payee_type": "Any Resident", "threshold_amount": 30000.0, "threshold_condition": ">", "threshold_sub_condition": "Amount or aggregate per category in FY", "rate_of_tds": "10", "payee_sub_type_rate": "Professional fees / Director fees", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "10% for professional fees, other royalties, director fees."},
  {"row_id": "194K-01", "section": "194K", "nature_of_payment": "Income on Mutual Fund units", "payer_category": "Mutual fund entity", "payee_type": "Any Resident", "threshold_amount": 5000.0, "threshold_condition": ">", "threshold_sub_condition": "Amount or aggregate in FY", "rate_of_tds": "10", "payee_sub_type_rate": "All", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "10% at time of credit/payment."},
  {"row_id": "194LA-01", "section": "194LA", "nature_of_payment": "Compensation on compulsory acquisition of immovable property", "payer_category": "Acquiring authority", "payee_type": "Any Resident", "threshold_amount": 250000.0, "threshold_condition": ">", "threshold_sub_condition": "Amount or aggregate in FY", "rate_of_tds": "10", "payee_sub_type_rate": "All", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "10% on compensation exceeding Rs 2.5 Lakhs."},
  {"row_id": "194M-01", "section": "194M", "nature_of_payment": "Contractor / Commission / Professional fees by Individuals/HUFs", "payer_category": "Individual/HUF not covered u/s 194C/H/J", "payee_type": "Any Resident", "threshold_amount": 5000000.0, "threshold_condition": ">", "threshold_sub_condition": "Aggregate in FY exceeds 50 Lakhs", "rate_of_tds": "2", "payee_sub_type_rate": "All", "effective_from": "1/10/2024", "effective_to": "31-03-2099", "notes": "Rate 2% w.e.f. 01-10-2024 on aggregate exceeding Rs 50 Lakhs."},
  {"row_id": "194N-01", "section": "194N", "nature_of_payment": "Cash withdrawals exceeding ₹1 Crore (ROI filed)", "payer_category": "Banking company / Co-op bank / Post office", "payee_type": "Any Resident", "threshold_amount": 10000000.0, "threshold_condition": ">", "threshold_sub_condition": "Cash withdrawn in FY", "rate_of_tds": "2", "payee_sub_type_rate": "ROI filed", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "Standard 2% once aggregate exceeds Rs 1 Crore."},
  {"row_id": "194P-01", "section": "194P", "nature_of_payment": "Pension + bank interest for specified senior citizen (age >= 75)", "payer_category": "Specified bank", "payee_type": "Senior Citizen", "threshold_amount": 0.0, "threshold_condition": "N/A", "threshold_sub_condition": "Basic exemption limit", "rate_of_tds": "Avg", "payee_sub_type_rate": "All", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "Bank computes tax after rebate u/s 87A."},
  {"row_id": "194Q-01", "section": "194Q", "nature_of_payment": "Purchase of goods exceeding ₹50 Lakhs", "payer_category": "Buyer (turnover > Rs 10 Crore)", "payee_type": "Any Resident", "threshold_amount": 5000000.0, "threshold_condition": ">", "threshold_sub_condition": "Value of goods purchased in FY", "rate_of_tds": "0.1", "payee_sub_type_rate": "All", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "0.1% on amount exceeding Rs 50 Lakhs only. 5% penalty rate in no-PAN cases."},
  {"row_id": "194R-01", "section": "194R", "nature_of_payment": "Benefit or perquisite arising from business or profession", "payer_category": "Specified business payer", "payee_type": "Any Resident", "threshold_amount": 20000.0, "threshold_condition": ">", "threshold_sub_condition": "Value of benefit in FY", "rate_of_tds": "10", "payee_sub_type_rate": "All", "effective_from": "1/4/2024", "effective_to": "31-03-2099", "notes": "10% before providing benefit."}
]

def load_rates():
    """
    Attempts to read fresh Excel file if available; otherwise falls back to BUILTIN_RATES.
    """
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "backend", "data", "tds_rates.xlsx"),
        os.path.join(os.path.dirname(__file__), "data", "tds_rates.xlsx"),
        os.path.join(os.path.dirname(__file__), "tds_rates.xlsx"),
        os.path.join(os.path.dirname(__file__), "TDS_Master_Data.xlsx"),
    ]
    for p in possible_paths:
        if os.path.exists(p):
            try:
                df = pd.read_excel(p, engine="openpyxl")
                if not df.empty and "Section" in df.columns:
                    # Clean columns
                    df.columns = [str(c).strip().lower() for c in df.columns]
                    mapping = {
                        "row id": "row_id", "section": "section", "nature of payment": "nature_of_payment",
                        "payer category": "payer_category", "payee type": "payee_type",
                        "threshold amount (rs)": "threshold_amount", "threshold condition": "threshold_condition",
                        "threshold sub-condition": "threshold_sub_condition", "rate of tds (%)": "rate_of_tds",
                        "payee sub-type for rate": "payee_sub_type_rate", "effective from": "effective_from",
                        "effective to": "effective_to", "notes": "notes"
                    }
                    df = df.rename(columns={c: mapping[c] for c in df.columns if c in mapping})
                    if "threshold_amount" in df.columns:
                        df["threshold_amount"] = pd.to_numeric(df["threshold_amount"], errors="coerce").fillna(0.0)
                    return df.to_dict(orient="records")
            except Exception:
                pass
    return BUILTIN_RATES

# ---------------------------------------------------------
# Calculation Engine
# ---------------------------------------------------------
def calculate_tds_direct(data, rates_list):
    section = data["section"]
    deductee_type = data["deducteeType"]
    amount = float(data["amount"])
    has_pan = data.get("hasPAN", True)
    row_id = data.get("rowId")
    is_aggregate = data.get("isAggregate", False)

    # 1. Filter rows by section
    section_rows = [r for r in rates_list if str(r.get("section", "")).strip().upper() == str(section).strip().upper()]
    if not section_rows:
        section_rows = rates_list[:1]

    base_row = None
    if row_id:
        for r in section_rows:
            if str(r.get("row_id", "")).strip().upper() == str(row_id).strip().upper():
                base_row = r
                break
    if not base_row:
        base_row = section_rows[0]

    # 2. Select sub-row based on payee type
    is_ind_huf = deductee_type in ["Individual", "HUF"]
    same_payment_rows = section_rows

    if str(section) == "194C":
        target_sub = "Aggregate" if is_aggregate else "Single"
        matched_agg = [r for r in section_rows if target_sub.lower() in str(r.get("threshold_sub_condition", "")).lower()]
        if matched_agg:
            same_payment_rows = matched_agg

    matched_row = None
    for r in same_payment_rows:
        payee_sub = str(r.get("payee_sub_type_rate", "")).lower()
        payee_type_str = str(r.get("payee_type", "")).lower()
        if is_ind_huf:
            if "individual" in payee_sub or "huf" in payee_sub or "individual" in payee_type_str or payee_sub in ["all", "general"]:
                matched_row = r
                break
        else:
            if "company" in payee_sub or "firm" in payee_sub or "other" in payee_sub or "non-individual" in payee_type_str or payee_sub == "all":
                matched_row = r

    if not matched_row:
        matched_row = base_row

    rate_str = str(matched_row.get("rate_of_tds", "0")).strip().lower()
    is_salary_or_avg = (rate_str == "avg")
    standard_rate = 0.0
    if not is_salary_or_avg:
        try:
            standard_rate = float(rate_str)
        except ValueError:
            standard_rate = 0.0

    threshold = float(matched_row.get("threshold_amount", 0.0))
    nature_of_payment = matched_row.get("nature_of_payment", "")
    row_id_applied = matched_row.get("row_id", "")
    notes = matched_row.get("notes", "")

    condition = str(matched_row.get("threshold_condition", ">")).strip()
    if condition == ">=":
        is_breached = (amount >= threshold)
    elif condition == "N/A" or threshold == 0:
        is_breached = True
    else:
        is_breached = (amount > threshold)

    is_194q = (str(section).strip().upper() == "194Q")
    applicable_rate = standard_rate
    pan_note = "Valid PAN provided. Standard statutory rate applied."
    rate_reason = ""
    is_warning = False
    warning_message = ""

    if not has_pan:
        is_warning = True
        if is_194q:
            applicable_rate = 5.0
            pan_note = "No PAN provided. Penalty rate of 5% applied under Section 206AA (specific exception for Section 194Q)."
        elif is_salary_or_avg:
            applicable_rate = 20.0
            pan_note = "No PAN provided. Higher penalty rate of 20% applied under Section 206AA."
        else:
            applicable_rate = max(20.0, standard_rate)
            pan_note = f"No PAN provided. Higher penalty rate of {applicable_rate}% applied under Section 206AA."

    tds_amount = 0.0
    threshold_note = ""

    if not is_breached:
        tds_amount = 0.0
        threshold_note = f"Below compliance threshold of ₹{threshold:,.2f}. No TDS is deductible."
        rate_reason = "No TDS deducted as gross transaction amount is within the threshold limit."
        is_warning = True
        warning_message = f"Transaction amount ₹{amount:,.2f} is below the statutory TDS threshold of ₹{threshold:,.2f}."
    else:
        threshold_note = f"Threshold of ₹{threshold:,.2f} is breached. TDS is applicable."
        if is_salary_or_avg and has_pan:
            tds_amount = 0.0
            rate_reason = "TDS on Salary (Section 192) / Pension (Section 194P) is computed on average tax slab rates."
            threshold_note = "Basic exemption limit applies based on the taxpayer's chosen tax regime."
        else:
            if is_194q:
                excess_amount = max(0.0, amount - 5000000.0)
                tds_amount = (excess_amount * applicable_rate) / 100.0
                rate_reason = f"Deducted at {applicable_rate}% on the amount exceeding ₹50,00,000 (₹{excess_amount:,.2f})."
            else:
                tds_amount = (amount * applicable_rate) / 100.0
                rate_reason = f"Deducted at {applicable_rate}% on the gross amount of ₹{amount:,.2f}."

    tds_amount = round(tds_amount, 2)
    net_payable = round(amount - tds_amount, 2)

    legal_ref = get_legal_reference(section)
    legal_basis = f"{legal_ref['citation']} — {legal_ref['description']}"
    if not has_pan:
        legal_basis += f" Read with {PENALTY_PAN_REFERENCE['citation']} (No-PAN higher rate)."
    if notes:
        legal_basis += f" Rate footnote: {notes}"

    return {
        "grossAmount": amount,
        "applicableRate": 0.0 if is_salary_or_avg and has_pan else applicable_rate,
        "thresholdLimit": threshold,
        "tdsAmount": tds_amount,
        "netPayable": net_payable,
        "section": str(section),
        "natureOfPayment": nature_of_payment,
        "rowIdApplied": row_id_applied,
        "explanation": {
            "rateReason": rate_reason,
            "legalBasis": legal_basis,
            "thresholdNote": threshold_note,
            "panNote": pan_note
        },
        "isWarning": is_warning,
        "warningMessage": warning_message
    }

# ---------------------------------------------------------
# State Initialization
# ---------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "selected_section_idx" not in st.session_state:
    st.session_state.selected_section_idx = 0

if "gross_amount" not in st.session_state:
    st.session_state.gross_amount = 150000.0

if "deductor_type" not in st.session_state:
    st.session_state.deductor_type = "Private Limited Company"

if "deductee_type" not in st.session_state:
    st.session_state.deductee_type = "Individual"

if "has_pan" not in st.session_state:
    st.session_state.has_pan = True

if "is_aggregate" not in st.session_state:
    st.session_state.is_aggregate = False

# ---------------------------------------------------------
# Header Bar
# ---------------------------------------------------------
st.markdown(
    """
    <div class="top-header">
        <h1>⚖️ TDS Compliance Calculator</h1>
        <p>Income Tax Act, 1961 Compliance & Filing Verification Desk — Professional CA/CS Edition</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Load Rates
# ---------------------------------------------------------
rates = load_rates()

section_options = []
seen = set()
for r in rates:
    row_id = r.get("row_id")
    section = r.get("section")
    nature = r.get("nature_of_payment")
    key = (section, nature)
    if key not in seen:
        seen.add(key)
        section_options.append({
            "id": row_id,
            "section_code": str(section),
            "nature_of_payment": str(nature),
            "label": f"{section} — {nature}"
        })

section_options = sorted(section_options, key=lambda x: str(x["section_code"]))
section_labels = [opt["label"] for opt in section_options]

# ---------------------------------------------------------
# Sidebar: Guide & Info
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 📘 Help & Reference")
    
    with st.expander("ℹ️ How to Use This Tool", expanded=False):
        st.markdown(
            """
            1. **Select Section**: Pick the applicable section code (e.g. `194C` for Contractors, `194J` for Technical/Professional).
            2. **Payer & Payee**: Choose Deductor (who pays) and Deductee (who receives).
            3. **Gross Amount**: Input the invoice / payment amount before tax.
            4. **PAN Status**: Toggle 'No PAN' to verify Section 206AA penalty rate (20% or 5% for Sec 194Q).
            5. **Review Citation**: Read the legal basis and rate justification for audit documentation.
            """
        )

    st.markdown("---")
    st.markdown("### 📊 Rate Database Status")
    st.success(f"Active rate rules loaded: **{len(rates)}** rules.")

    st.markdown("---")
    st.markdown(
        """
        <div style='font-size: 0.75rem; color: #64748b;'>
        <strong>Compliance Note:</strong><br>
        Rates are updated as per the Income Tax Act, 1961 (amended by Finance Act, 2024).<br>
        Verify specific certificates (Form 15G/15H, lower deduction certificate u/s 197) prior to challan payment.
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------------------------------
# Main Two-Column Layout
# ---------------------------------------------------------
col_form, col_result = st.columns([1.1, 1.3], gap="large")

# ---------------------------------------------------------
# Column 1: Transaction Details Input Form
# ---------------------------------------------------------
with col_form:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    
    header_col1, header_col2 = st.columns([2, 1])
    with header_col1:
        st.markdown('<div class="card-title">1. Transaction Details</div>', unsafe_allow_html=True)
    with header_col2:
        if st.button("🔄 Reset Form", use_container_width=True):
            st.session_state.selected_section_idx = 0
            st.session_state.gross_amount = 150000.0
            st.session_state.deductor_type = "Private Limited Company"
            st.session_state.deductee_type = "Individual"
            st.session_state.has_pan = True
            st.session_state.is_aggregate = False
            st.rerun()

    # Section No Selectbox
    selected_idx = st.selectbox(
        "TDS Section No. *",
        options=range(len(section_labels)),
        format_func=lambda i: section_labels[i],
        index=st.session_state.selected_section_idx,
        help="Select the applicable section code under Chapter XVII-B of the Income Tax Act, 1961."
    )
    st.session_state.selected_section_idx = selected_idx
    selected_sec_obj = section_options[selected_idx]
    current_section_code = selected_sec_obj["section_code"]

    # Nature of Payment (Auto-filled / locked display)
    st.text_input(
        "Nature of Payment (Auto-filled)",
        value=selected_sec_obj["nature_of_payment"],
        disabled=True,
        help="Specific transaction category corresponding to the selected Section."
    )

    # Deductor & Deductee Selectors
    c_ded1, c_ded2 = st.columns(2)
    deductor_opts = [
        "Individual", "HUF", "Partnership Firm", "Private Limited Company",
        "Public Limited Company", "LLP", "Government", "Others"
    ]
    deductee_opts = [
        "Individual", "HUF", "Partnership Firm", "Domestic Company",
        "Foreign Company", "Others"
    ]

    with c_ded1:
        deductor_val = st.selectbox(
            "Deductor Type (Payer) *",
            options=deductor_opts,
            index=deductor_opts.index(st.session_state.deductor_type) if st.session_state.deductor_type in deductor_opts else 3,
            help="Legal constitution of the entity making the taxable payment."
        )
        st.session_state.deductor_type = deductor_val

    with c_ded2:
        deductee_val = st.selectbox(
            "Deductee Type (Payee) *",
            options=deductee_opts,
            index=deductee_opts.index(st.session_state.deductee_type) if st.session_state.deductee_type in deductee_opts else 0,
            help="Legal status of the recipient. Determines whether Individual/HUF or Corporate rates apply."
        )
        st.session_state.deductee_type = deductee_val

    # Gross Amount Input
    amount_val = st.number_input(
        "Gross Payment Amount (₹) *",
        min_value=1.0,
        max_value=1000000000.0,
        value=float(st.session_state.gross_amount),
        step=5000.0,
        format="%.2f",
        help="Total taxable payment before deduction of TDS. Format: e.g. ₹1,50,000"
    )
    st.session_state.gross_amount = amount_val

    # PAN Status Selection
    st.markdown("<label style='font-size: 0.875rem; font-weight: 600; color: #334155; margin-bottom: 4px; display: block;'>PAN Status</label>", unsafe_allow_html=True)
    pan_status_label = st.radio(
        "PAN Status",
        options=["Valid PAN Provided", "No PAN (Higher Rate u/s 206AA)"],
        index=0 if st.session_state.has_pan else 1,
        horizontal=True,
        label_visibility="collapsed",
        help="Under Section 206AA, non-furnishing of PAN attracts a higher rate of 20% (or 5% under Section 194Q)."
    )
    st.session_state.has_pan = (pan_status_label == "Valid PAN Provided")

    # Section 194C Special Checkbox
    is_agg_val = False
    if current_section_code == "194C":
        is_agg_val = st.checkbox(
            "Is this part of aggregate annual payments to this contractor?",
            value=st.session_state.is_aggregate,
            help="Applies the aggregate threshold of ₹1,00,000 in place of the single-transaction threshold of ₹30,000."
        )
        st.session_state.is_aggregate = is_agg_val

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Column 2: Calculation Results & Explanation Panel
# ---------------------------------------------------------
with col_result:
    calc_payload = {
        "rowId": selected_sec_obj["id"],
        "section": current_section_code,
        "deductorType": deductor_val,
        "deducteeType": deductee_val,
        "amount": amount_val,
        "hasPAN": st.session_state.has_pan,
        "isAggregate": is_agg_val
    }

    try:
        results = calculate_tds_direct(calc_payload, rates)
        
        # Save to history
        hist_entry = {
            "section": results["section"],
            "nature": results["natureOfPayment"],
            "amount": results["grossAmount"],
            "tds": results["tdsAmount"],
            "rate": results["applicableRate"],
            "hasPAN": st.session_state.has_pan
        }
        if not st.session_state.history or st.session_state.history[0] != hist_entry:
            st.session_state.history.insert(0, hist_entry)
            st.session_state.history = st.session_state.history[:5]

    except Exception as err:
        st.error(f"Calculation Error: {str(err)}")
        results = None

    if results:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">2. Calculation Results</div>', unsafe_allow_html=True)

        # Status Banner
        if results["isWarning"]:
            st.markdown(
                f"""
                <div class="status-banner warning">
                    <span>⚠️</span>
                    <span><strong>Advisory Note:</strong> {results['warningMessage'] or 'Non-standard compliance rule applied.'}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="status-banner success">
                    <span>✅</span>
                    <span><strong>Standard Compliance Verified:</strong> Transaction qualifies for standard statutory deduction parameters.</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Prominent KPI Metrics
        tds_formatted = f"₹ {results['tdsAmount']:,.2f}"
        net_formatted = f"₹ {results['netPayable']:,.2f}"
        
        st.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-card highlight">
                    <div class="metric-label">TDS Amount Deductible</div>
                    <div class="metric-value blue">{tds_formatted}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Net Amount Payable</div>
                    <div class="metric-value">{net_formatted}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Breakdown Table
        df_breakdown = pd.DataFrame([
            {"Component": "Gross Transaction Amount", "Value": f"₹ {results['grossAmount']:,.2f}"},
            {"Component": "Statutory Rate Applied", "Value": f"{results['applicableRate']}%"},
            {"Component": "Statutory Threshold Limit", "Value": f"₹ {results['thresholdLimit']:,.2f}"},
            {"Component": "TDS Deducted", "Value": f"- ₹ {results['tdsAmount']:,.2f}"},
            {"Component": "Net Balance Payable", "Value": f"₹ {results['netPayable']:,.2f}"},
        ])
        
        st.markdown("**Detailed Breakdown Table:**")
        st.dataframe(
            df_breakdown,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Component": st.column_config.TextColumn("Statutory Component", width="medium"),
                "Value": st.column_config.TextColumn("Computed Figure / Rate", width="medium"),
            }
        )

        # Legal Explanation & Citations Panel
        exp = results["explanation"]
        st.markdown('<div class="card-title" style="margin-top: 1.25rem;">3. Compliance Explanation & Legal Citation</div>', unsafe_allow_html=True)
        
        st.markdown(
            f"""
            <div class="exp-grid">
                <div class="exp-box">
                    <div class="exp-title">Why this rate?</div>
                    <p class="exp-desc">{exp.get('rateReason', 'Standard rate applied.')}</p>
                </div>
                <div class="exp-box">
                    <div class="exp-title">PAN Compliance</div>
                    <p class="exp-desc">{exp.get('panNote', 'Valid PAN provided.')}</p>
                </div>
                <div class="exp-box">
                    <div class="exp-title">Threshold Verification</div>
                    <p class="exp-desc">{exp.get('thresholdNote', 'Threshold limit checked.')}</p>
                </div>
                <div class="exp-box">
                    <div class="exp-title">Legal Basis (Act Citation)</div>
                    <p class="exp-desc">{exp.get('legalBasis', 'Income Tax Act, 1961.')}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Recent Checks Glance Section
# ---------------------------------------------------------
if st.session_state.history:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    c_hist_title, c_hist_btn = st.columns([4, 1])
    with c_hist_title:
        st.markdown('<div class="card-title" style="margin-bottom: 0.5rem;">🕒 Recent Checks (Last 5 Calculations)</div>', unsafe_allow_html=True)
    with c_hist_btn:
        if st.button("🗑️ Clear History", key="clear_hist", use_container_width=True):
            st.session_state.history = []
            st.rerun()

    cols = st.columns(len(st.session_state.history))
    for idx, item in enumerate(st.session_state.history):
        with cols[idx]:
            pan_badge = "✅ PAN" if item["hasPAN"] else "⚠️ No-PAN"
            st.markdown(
                f"""
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.75rem; font-size: 0.75rem;">
                    <div style="font-weight: 700; color: #1e3a8a; font-family: monospace;">Sec {item['section']}</div>
                    <div style="color: #64748b; font-size: 0.7rem; margin: 0.2rem 0;">Amt: <strong>₹{item['amount']:,.0f}</strong></div>
                    <div style="color: #2563eb; font-weight: 700;">TDS: ₹{item['tds']:,.0f} ({item['rate']}%)</div>
                    <div style="color: #94a3b8; font-size: 0.65rem; margin-top: 0.25rem;">{pan_badge}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown(
    """
    <div class="footer-text">
        TDS Calculator Professional • Income Tax Act, 1961 • Sourced dynamically from rate sheet database.<br>
        For professional verification only. Verify compliance parameters with a qualified tax auditor before filing returns.
    </div>
    """,
    unsafe_allow_html=True
)
