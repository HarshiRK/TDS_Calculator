import os
import sys
import pandas as pd
import streamlit as st

# Add current directory to path so backend imports work seamlessly
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.calculator import calculate_tds, validate_inputs
from backend.excel_reader import read_rates, EXCEL_PATH

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
# Data Loading
# ---------------------------------------------------------
try:
    rates = read_rates()
except Exception as e:
    st.error(f"⚠️ Error loading TDS rates sheet: {str(e)}")
    st.stop()

# Build section options list
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
# Sidebar: Guide, Template & Rate Sheet Info
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 📘 Help & Reference")
    
    with st.expander("ℹ️ How to Use This Tool", expanded=False):
        st.markdown(
            """
            1. **Select Section**: Pick the applicable section code (e.g. `194C` for Contractors, `194J` for Technical/Professional).
            2. **Payer & Payee**: Choose Deductor (who pays) and Deductee (who receives). Deductee type determines the applicable rate.
            3. **Gross Amount**: Input the invoice / payment amount before tax.
            4. **PAN Status**: Toggle 'No PAN' to verify Section 206AA penalty rate (20% or 5% for Sec 194Q).
            5. **Review Citation**: Read the legal basis and rate justification for audit documentation.
            """
        )

    st.markdown("---")
    st.markdown("### 📊 Rate Sheet Status")
    st.success(f"Loaded **{len(rates)}** rate rules from Excel database.")
    
    # Download Active Rate Sheet
    if os.path.exists(EXCEL_PATH):
        with open(EXCEL_PATH, "rb") as f:
            st.download_button(
                label="📥 Download Active Rate Sheet (.xlsx)",
                data=f,
                file_name="tds_rates.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            
    st.markdown("---")
    st.markdown(
        """
        <div style='font-size: 0.75rem; color: #64748b;'>
        <strong>Professional Note:</strong><br>
        Rates are sourced from the Income Tax Act, 1961 as amended by Finance Act, 2024.<br>
        Always cross-verify special exemptions (Form 15G/15H, lower deduction certificates u/s 197) prior to challan generation.
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
    # Prepare payload
    calc_payload = {
        "rowId": selected_sec_obj["id"],
        "section": current_section_code,
        "deductorType": deductor_val,
        "deducteeType": deductee_val,
        "amount": amount_val,
        "hasPAN": st.session_state.has_pan,
        "isAggregate": is_agg_val
    }

    # Execute calculation
    try:
        results = calculate_tds(calc_payload)
        
        # Save to history
        hist_entry = {
            "section": results["section"],
            "nature": results["natureOfPayment"],
            "amount": results["grossAmount"],
            "tds": results["tdsAmount"],
            "rate": results["applicableRate"],
            "hasPAN": st.session_state.has_pan
        }
        # Avoid duplicate top entry
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
