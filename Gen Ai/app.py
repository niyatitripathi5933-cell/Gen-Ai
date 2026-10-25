"""
🏗️ Multimodal Construction Intelligence Platform
SkillWallet Capstone Project 1

An intelligent decision-support system analyzing site photos to audit PPE safety
compliance, classify concrete cracks, estimate construction costs and real estate
valuation in INR, and provide weather-aware daily protocols.

Author: SkillWallet AI Engineer
Platform ID: 6ac4c98d1dcde6d7857c1642
"""

import streamlit as st
import json
import time
from PIL import Image

from utils import (
    configure_gemini,
    analyze_image_with_gemini,
    chat_with_gemini,
    PPE_AUDIT_PROMPT,
    CRACK_DIAGNOSIS_PROMPT,
    DEMO_PPE_RESULT,
    DEMO_CRACK_RESULT,
    get_severity_color,
    get_status_color,
    generate_pollinations_url,
)
from calculators import (
    calculate_project_costs,
    get_structure_types,
    get_tier_options,
    format_inr,
    MILESTONES,
)
from weather import get_weather_data, get_all_conditions

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG & CUSTOM CSS
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Construction Intelligence Platform | SkillWallet",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    /* ── Import Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* ── Global ── */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* ── Metric Cards ── */
    .metric-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #252b3b 100%);
        border: 1px solid rgba(255, 107, 53, 0.2);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #FF6B35, #FF8C61, #FF6B35);
    }
    .metric-card:hover {
        border-color: rgba(255, 107, 53, 0.5);
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(255, 107, 53, 0.15);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FF6B35, #FF8C61);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 8px 0;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #8892a4;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }
    .metric-icon {
        font-size: 2rem;
        margin-bottom: 4px;
    }
    
    /* ── Status Pills ── */
    .status-pill {
        display: inline-block;
        padding: 6px 18px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .pill-green { background: rgba(40, 167, 69, 0.15); color: #28a745; border: 1px solid rgba(40, 167, 69, 0.3); }
    .pill-orange { background: rgba(253, 126, 20, 0.15); color: #fd7e14; border: 1px solid rgba(253, 126, 20, 0.3); }
    .pill-red { background: rgba(220, 53, 69, 0.15); color: #dc3545; border: 1px solid rgba(220, 53, 69, 0.3); }
    .pill-critical { background: rgba(255, 0, 64, 0.15); color: #ff0040; border: 1px solid rgba(255, 0, 64, 0.3); }
    
    /* ── Alert Cards ── */
    .alert-card {
        border-radius: 12px;
        padding: 18px 22px;
        margin: 10px 0;
        border-left: 4px solid;
        transition: all 0.2s ease;
    }
    .alert-card:hover {
        transform: translateX(4px);
    }
    .alert-critical {
        background: rgba(255, 0, 64, 0.08);
        border-left-color: #ff0040;
    }
    .alert-high {
        background: rgba(220, 53, 69, 0.08);
        border-left-color: #dc3545;
    }
    .alert-medium {
        background: rgba(253, 126, 20, 0.08);
        border-left-color: #fd7e14;
    }
    .alert-info {
        background: rgba(23, 162, 184, 0.08);
        border-left-color: #17a2b8;
    }
    .alert-title {
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 6px;
    }
    .alert-desc {
        font-size: 0.9rem;
        color: #b0b8c8;
        line-height: 1.5;
    }
    
    /* ── PPE Checklist ── */
    .ppe-item {
        display: flex;
        align-items: center;
        padding: 12px 16px;
        background: rgba(26, 31, 46, 0.6);
        border-radius: 10px;
        margin: 6px 0;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: all 0.2s ease;
    }
    .ppe-item:hover {
        background: rgba(26, 31, 46, 0.9);
        border-color: rgba(255, 107, 53, 0.2);
    }
    
    /* ── Progress Bar ── */
    .progress-container {
        background: rgba(26, 31, 46, 0.8);
        border-radius: 12px;
        padding: 8px;
        margin: 16px 0;
    }
    .progress-bar {
        height: 28px;
        border-radius: 8px;
        background: linear-gradient(90deg, #FF6B35, #FF8C61, #FFB088);
        transition: width 1s ease-in-out;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.85rem;
        color: #0E1117;
    }
    
    /* ── Milestone Timeline ── */
    .milestone {
        padding: 10px 16px;
        border-radius: 8px;
        margin: 4px 0;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .ms-done { background: rgba(40, 167, 69, 0.1); color: #28a745; }
    .ms-active { background: rgba(255, 107, 53, 0.15); color: #FF6B35; border: 1px solid rgba(255, 107, 53, 0.3); font-weight: 600; }
    .ms-pending { background: rgba(108, 117, 125, 0.1); color: #6c757d; }
    
    /* ── Chat ── */
    .chat-user {
        background: linear-gradient(135deg, #FF6B35, #FF8C61);
        color: #0E1117;
        padding: 14px 20px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        font-weight: 500;
        max-width: 85%;
        margin-left: auto;
    }
    .chat-assistant {
        background: rgba(26, 31, 46, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 14px 20px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        max-width: 85%;
        line-height: 1.6;
    }
    
    /* ── Section Headers ── */
    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #FF6B35;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 24px 0 12px;
        padding-bottom: 8px;
        border-bottom: 2px solid rgba(255, 107, 53, 0.2);
    }
    
    /* ── Sidebar Styling ── */
    .sidebar-header {
        text-align: center;
        padding: 16px 0;
    }
    .sidebar-header h1 {
        font-size: 1.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FF6B35, #FFB088);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* ── Hazard Table ── */
    .hazard-row {
        padding: 14px 18px;
        border-radius: 10px;
        margin: 8px 0;
        border: 1px solid rgba(255, 255, 255, 0.05);
        background: rgba(26, 31, 46, 0.5);
    }
    
    /* ── Repair Card ── */
    .repair-card {
        background: rgba(26, 31, 46, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    .repair-card:hover {
        border-color: rgba(255, 107, 53, 0.3);
        transform: translateY(-2px);
    }
    
    /* ── Weather Card ── */
    .weather-header {
        text-align: center;
        padding: 30px;
        border-radius: 16px;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }
    .weather-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
    }
    .weather-icon {
        font-size: 4rem;
        margin-bottom: 8px;
    }
    
    /* ── Animations ── */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animate-in {
        animation: fadeInUp 0.5s ease forwards;
    }
    
    /* ── Score Gauge ── */
    .score-gauge {
        text-align: center;
        padding: 24px;
    }
    .score-number {
        font-size: 4.5rem;
        font-weight: 900;
        line-height: 1;
    }
    .score-label {
        font-size: 1rem;
        color: #8892a4;
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* ── Hide Streamlit Defaults ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# SESSION STATE INITIALIZATION
# ─────────────────────────────────────────────────────────────

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "gemini_model" not in st.session_state:
    st.session_state.gemini_model = None
if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = True


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h1>🏗️ Construction Intelligence</h1>
        <p style="color: #8892a4; font-size: 0.85rem;">SkillWallet Capstone Project 1</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # API Key Input
    st.markdown("##### 🔑 API Configuration")
    api_key = st.text_input(
        "Google Gemini API Key",
        type="password",
        placeholder="Enter your Gemini API key...",
        help="Get your free API key from https://makersuite.google.com/app/apikey"
    )
    
    if api_key:
        try:
            st.session_state.gemini_model = configure_gemini(api_key)
            st.session_state.demo_mode = False
            st.success("✅ API Connected — Live AI Mode")
        except Exception as e:
            st.error(f"❌ Connection failed: {e}")
            st.session_state.demo_mode = True
    else:
        st.session_state.demo_mode = True
        st.info("ℹ️ Running in **Demo Mode** — Enter API key for live AI analysis")
    
    st.markdown("---")
    
    # Architecture Overview
    with st.expander("📐 Architecture Overview", expanded=False):
        st.markdown("""
        **System Architecture:**
        
        ```
        ┌─────────────────────┐
        │   Streamlit UI      │
        │  ┌───────────────┐  │
        │  │  4 Tab Modules │  │
        │  └───────┬───────┘  │
        │          │          │
        │  ┌───────▼───────┐  │
        │  │  AI Engine     │  │
        │  │  (Gemini 1.5)  │  │
        │  └───────┬───────┘  │
        │          │          │
        │  ┌───────▼───────┐  │
        │  │ JSON Contracts │  │
        │  └───────────────┘  │
        └─────────────────────┘
        ```
        
        **Modules:**
        - 🔍 PPE Safety Vision (OSHA + IS 456)
        - 🧱 Crack Diagnostics Engine
        - 💰 Cost & Valuation Calculator
        - 🤖 AI Construction Chatbot
        - 🌦️ Weather Advisory System
        """)
    
    # Platform Info
    with st.expander("ℹ️ Platform Details", expanded=False):
        st.markdown(f"""
        | Property | Value |
        |---|---|
        | Platform ID | `6ac4c98d` |
        | Category | Gen AI / Real Estate |
        | Stack | Python · Streamlit · Gemini |
        | Version | 1.0.0 |
        | Mode | {"🟢 Live AI" if not st.session_state.demo_mode else "🟡 Demo"} |
        """)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 10px 0;">
        <p style="color: #5a6577; font-size: 0.75rem;">
            Built with ❤️ for SkillWallet<br/>
            Multimodal Construction Intelligence Platform<br/>
            © 2024 Capstone Project 1
        </p>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# MAIN CONTENT — TAB NAVIGATION
# ─────────────────────────────────────────────────────────────

st.markdown("""
<div style="text-align: center; padding: 10px 0 20px;">
    <h1 style="font-size: 2.2rem; font-weight: 800; margin: 0;">
        🏗️ Multimodal Construction Intelligence Platform
    </h1>
    <p style="color: #8892a4; font-size: 1rem; margin-top: 6px;">
        AI-Powered Site Safety · Structural Diagnostics · Cost Estimation · Weather Advisory
    </p>
</div>
""", unsafe_allow_html=True)

if st.session_state.demo_mode:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(255, 107, 53, 0.1), rgba(255, 140, 97, 0.05));
                border: 1px solid rgba(255, 107, 53, 0.3); border-radius: 12px; padding: 14px 20px;
                text-align: center; margin-bottom: 20px;">
        <strong style="color: #FF6B35;">🎭 Demonstration Mode Active</strong>
        <span style="color: #b0b8c8;"> — AI analysis uses sample data. Enter your Gemini API key in the sidebar for live results.</span>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "🦺 Site Safety & PPE Audit",
    "🧱 Crack Diagnostics",
    "💰 Planning & Valuation",
    "🤖 Site Assistant & Weather"
])


# ═════════════════════════════════════════════════════════════
# TAB 1: SITE SAFETY & PPE AUDIT
# ═════════════════════════════════════════════════════════════

with tab1:
    st.markdown('<div class="section-header">📋 Construction Site Safety & PPE Compliance Audit</div>', unsafe_allow_html=True)
    st.markdown("Upload a construction site photograph to analyze worker PPE compliance under **OSHA 29 CFR 1926** and **IS 456** standards.")
    
    col_upload, col_info = st.columns([2, 1])
    
    with col_upload:
        uploaded_ppe = st.file_uploader(
            "Upload Site Photo",
            type=["jpg", "jpeg", "png"],
            key="ppe_uploader",
            help="Upload a clear construction site photo (JPG/PNG)"
        )
    
    with col_info:
        st.markdown("""
        **What we analyze:**
        - 🪖 Hard Hats / Helmets
        - 🦺 High-Visibility Vests
        - 👢 Steel-Toe Boots
        - 🪢 Safety Harnesses
        - 🧤 Safety Gloves
        - 🥽 Eye Protection
        """)
    
    if uploaded_ppe:
        image = Image.open(uploaded_ppe)
        
        col_img, col_results = st.columns([1, 2])
        
        with col_img:
            st.image(image, caption="📸 Uploaded Site Photo", use_container_width=True)
        
        with col_results:
            if not st.session_state.demo_mode and st.session_state.gemini_model:
                with st.spinner("🔍 Analyzing PPE compliance with Gemini AI..."):
                    result = analyze_image_with_gemini(
                        st.session_state.gemini_model, image, PPE_AUDIT_PROMPT
                    )
                    if result is None:
                        st.warning("⚠️ AI analysis returned unexpected format. Showing demo data.")
                        result = DEMO_PPE_RESULT
            else:
                result = DEMO_PPE_RESULT
            
            # ── Safety Score Display ──
            score = result.get("safety_score", 0)
            status = result.get("overall_status", "Unknown")
            
            if score >= 80:
                score_color = "#28a745"
                pill_class = "pill-green"
            elif score >= 60:
                score_color = "#fd7e14"
                pill_class = "pill-orange"
            elif score >= 40:
                score_color = "#dc3545"
                pill_class = "pill-red"
            else:
                score_color = "#ff0040"
                pill_class = "pill-critical"
            
            st.markdown(f"""
            <div class="metric-card" style="margin-bottom: 20px;">
                <div class="score-gauge">
                    <div class="score-number" style="color: {score_color};">{score}</div>
                    <div class="score-label">Safety Score</div>
                    <div style="margin-top: 12px;">
                        <span class="{pill_class} status-pill">{status}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # ── PPE Detection Checklist ──
        st.markdown('<div class="section-header">🦺 PPE Detection Checklist</div>', unsafe_allow_html=True)
        
        ppe_cols = st.columns(2)
        for i, item in enumerate(result.get("ppe_detection", [])):
            with ppe_cols[i % 2]:
                detected = item.get("detected", False)
                compliance = item.get("compliance", "Unknown")
                icon = "✅" if detected else "❌"
                comp_color = get_status_color(compliance)
                
                st.markdown(f"""
                <div class="ppe-item">
                    <span style="font-size: 1.3rem; margin-right: 12px;">{icon}</span>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; font-size: 0.95rem;">{item.get("item", "")}</div>
                        <div style="font-size: 0.8rem; color: #8892a4;">{item.get("notes", "")}</div>
                    </div>
                    <span class="status-pill" style="background: {comp_color}22; color: {comp_color}; border: 1px solid {comp_color}44;">
                        {compliance}
                    </span>
                </div>
                """, unsafe_allow_html=True)
        
        # ── Identified Hazards ──
        st.markdown('<div class="section-header">⚠️ Identified Site Hazards</div>', unsafe_allow_html=True)
        
        for hazard in result.get("hazards", []):
            severity = hazard.get("severity", "Medium")
            sev_color = get_severity_color(severity)
            alert_class = f"alert-{severity.lower()}" if severity.lower() in ["critical", "high", "medium"] else "alert-info"
            
            st.markdown(f"""
            <div class="alert-card {alert_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div class="alert-title">{hazard.get("hazard", "")}</div>
                    <span class="status-pill" style="background: {sev_color}22; color: {sev_color}; border: 1px solid {sev_color}44;">
                        {severity}
                    </span>
                </div>
                <div class="alert-desc">📍 <strong>Location:</strong> {hazard.get("location", "")}</div>
                <div class="alert-desc">🔧 <strong>Corrective Action:</strong> {hazard.get("corrective_action", "")}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # ── Recommendations ──
        st.markdown('<div class="section-header">💡 Recommendations</div>', unsafe_allow_html=True)
        for rec in result.get("recommendations", []):
            st.markdown(f"- {rec}")
        
        # ── Download JSON Report ──
        st.markdown('<div class="section-header">📥 Download Report</div>', unsafe_allow_html=True)
        
        report_json = json.dumps(result, indent=2)
        st.download_button(
            label="⬇️ Download Full JSON Report",
            data=report_json,
            file_name="ppe_safety_audit_report.json",
            mime="application/json",
            use_container_width=True,
        )


# ═════════════════════════════════════════════════════════════
# TAB 2: CRACK DIAGNOSTICS & STRUCTURAL INTEGRITY
# ═════════════════════════════════════════════════════════════

with tab2:
    st.markdown('<div class="section-header">🔬 Crack Diagnostics & Structural Integrity Analysis</div>', unsafe_allow_html=True)
    st.markdown("Upload an image of concrete/masonry surface to classify defects, estimate crack width, and receive engineering repair recommendations.")
    
    col_upload2, col_info2 = st.columns([2, 1])
    
    with col_upload2:
        uploaded_crack = st.file_uploader(
            "Upload Surface Photo",
            type=["jpg", "jpeg", "png"],
            key="crack_uploader",
            help="Upload a clear photo of the cracked surface (JPG/PNG)"
        )
    
    with col_info2:
        st.markdown("""
        **Defect Types Detected:**
        - Hairline Cracks
        - Settlement Cracks
        - Structural Shear Cracks
        - Thermal Expansion Cracks
        - Spalling & Delamination
        - Corrosion-Induced Cracks
        """)
    
    if uploaded_crack:
        image_crack = Image.open(uploaded_crack)
        
        col_img2, col_res2 = st.columns([1, 2])
        
        with col_img2:
            st.image(image_crack, caption="📸 Uploaded Surface Photo", use_container_width=True)
        
        with col_res2:
            if not st.session_state.demo_mode and st.session_state.gemini_model:
                with st.spinner("🔬 Analyzing structural defects with Gemini AI..."):
                    crack_result = analyze_image_with_gemini(
                        st.session_state.gemini_model, image_crack, CRACK_DIAGNOSIS_PROMPT
                    )
                    if crack_result is None:
                        st.warning("⚠️ AI analysis returned unexpected format. Showing demo data.")
                        crack_result = DEMO_CRACK_RESULT
            else:
                crack_result = DEMO_CRACK_RESULT
            
            # ── Diagnosis Cards ──
            defect = crack_result.get("defect_type", "Unknown")
            severity = crack_result.get("severity", "Unknown")
            width = crack_result.get("estimated_crack_width_mm", 0)
            risk = crack_result.get("structural_risk", "Unknown")
            
            mc1, mc2, mc3, mc4 = st.columns(4)
            
            with mc1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">🔍</div>
                    <div class="metric-label">Defect Type</div>
                    <div class="metric-value" style="font-size: 1.2rem;">{defect}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with mc2:
                sev_color = get_severity_color(severity)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">⚡</div>
                    <div class="metric-label">Severity</div>
                    <div class="metric-value" style="font-size: 1.3rem; color: {sev_color}; -webkit-text-fill-color: {sev_color};">{severity}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with mc3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">📏</div>
                    <div class="metric-label">Crack Width</div>
                    <div class="metric-value">{width} mm</div>
                </div>
                """, unsafe_allow_html=True)
            
            with mc4:
                risk_color = get_severity_color(risk)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">🏗️</div>
                    <div class="metric-label">Structural Risk</div>
                    <div class="metric-value" style="font-size: 1.3rem; color: {risk_color}; -webkit-text-fill-color: {risk_color};">{risk}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # ── Crack Pattern ──
        st.markdown('<div class="section-header">📐 Crack Pattern Analysis</div>', unsafe_allow_html=True)
        st.info(f"**Pattern:** {crack_result.get('crack_pattern', 'N/A')}")
        
        # ── Root Causes ──
        st.markdown('<div class="section-header">🔎 Root Causes</div>', unsafe_allow_html=True)
        for cause in crack_result.get("root_causes", []):
            st.markdown(f"- {cause}")
        
        # ── Recommended Repairs ──
        st.markdown('<div class="section-header">🔧 Recommended Engineering Repairs</div>', unsafe_allow_html=True)
        
        for repair in crack_result.get("recommended_repairs", []):
            urgency = repair.get("urgency", "Medium")
            urg_color = get_severity_color(urgency) if urgency in ["Immediate", "High"] else get_severity_color("Medium") if urgency == "Medium" else "#6c757d"
            
            st.markdown(f"""
            <div class="repair-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <div style="font-size: 1.1rem; font-weight: 700; color: #FF6B35;">🔧 {repair.get("method", "")}</div>
                    <span class="status-pill" style="background: {urg_color}22; color: {urg_color}; border: 1px solid {urg_color}44;">
                        {urgency}
                    </span>
                </div>
                <div style="color: #b0b8c8; line-height: 1.6; margin-bottom: 8px;">{repair.get("description", "")}</div>
                <div style="color: #FF8C61; font-weight: 600;">💰 Estimated Cost: {repair.get("estimated_cost", "N/A")}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # ── Monitoring Plan ──
        st.markdown('<div class="section-header">📊 Monitoring Plan</div>', unsafe_allow_html=True)
        st.success(crack_result.get("monitoring_plan", "No monitoring plan available."))
        
        # ── Standards ──
        standards = crack_result.get("standards_referenced", [])
        if standards:
            st.markdown(f"**Standards Referenced:** {' · '.join(standards)}")
        
        # ── Download ──
        crack_json = json.dumps(crack_result, indent=2)
        st.download_button(
            label="⬇️ Download Crack Diagnosis Report (JSON)",
            data=crack_json,
            file_name="crack_diagnosis_report.json",
            mime="application/json",
            use_container_width=True,
        )


# ═════════════════════════════════════════════════════════════
# TAB 3: PLANNING & REAL ESTATE VALUATION
# ═════════════════════════════════════════════════════════════

with tab3:
    st.markdown('<div class="section-header">💰 Project Planning & Real Estate Valuation Engine</div>', unsafe_allow_html=True)
    st.markdown("Configure your project parameters to get comprehensive cost estimates, material requirements, and market valuation in INR.")
    
    # ── Input Form ──
    col_input1, col_input2, col_input3, col_input4 = st.columns(4)
    
    with col_input1:
        structure_type = st.selectbox(
            "🏢 Structure Type",
            get_structure_types(),
            help="Select the type of construction project"
        )
    
    with col_input2:
        sqft = st.number_input(
            "📐 Built-up Area (sqft)",
            min_value=100,
            max_value=500000,
            value=2500,
            step=100,
            help="Total built-up area in square feet"
        )
    
    with col_input3:
        tier = st.selectbox(
            "📍 Location Tier",
            get_tier_options(),
            help="Indian city tier classification"
        )
    
    with col_input4:
        completion = st.slider(
            "📊 Completion %",
            min_value=0,
            max_value=100,
            value=45,
            step=5,
            help="Current project completion percentage"
        )
    
    # ── Calculate ──
    costs = calculate_project_costs(structure_type, sqft, tier, completion)
    
    st.markdown("---")
    
    # ── Financial Metrics Cards ──
    st.markdown('<div class="section-header">📊 Financial Overview</div>', unsafe_allow_html=True)
    
    fm1, fm2, fm3, fm4 = st.columns(4)
    
    with fm1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">💰</div>
            <div class="metric-label">Total Project Budget</div>
            <div class="metric-value">{costs['total_budget_formatted']}</div>
            <div style="color: #8892a4; font-size: 0.8rem;">₹{costs['rate_per_sqft']:,}/sqft</div>
        </div>
        """, unsafe_allow_html=True)
    
    with fm2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">📈</div>
            <div class="metric-label">CapEx Incurred</div>
            <div class="metric-value">{costs['capex_incurred_formatted']}</div>
            <div style="color: #8892a4; font-size: 0.8rem;">{completion}% completed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with fm3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">⏳</div>
            <div class="metric-label">CapEx Remaining</div>
            <div class="metric-value">{costs['capex_remaining_formatted']}</div>
            <div style="color: #8892a4; font-size: 0.8rem;">{100 - completion}% to go</div>
        </div>
        """, unsafe_allow_html=True)
    
    with fm4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🏠</div>
            <div class="metric-label">Market Valuation</div>
            <div class="metric-value" style="font-size: 1.6rem;">{costs['market_valuation_formatted']}</div>
            <div style="color: #8892a4; font-size: 0.8rem;">Current estimated value</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ── Material Requirements ──
    st.markdown('<div class="section-header">🧱 Material Requirements</div>', unsafe_allow_html=True)
    
    mat1, mat2, mat3 = st.columns(3)
    
    with mat1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">⚙️</div>
            <div class="metric-label">Steel Required</div>
            <div class="metric-value">{costs['total_steel_mt']:.1f} MT</div>
            <div style="color: #8892a4; font-size: 0.8rem;">({costs['total_steel_kg']:,.0f} kg) · {costs['steel_cost_formatted']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with mat2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🧱</div>
            <div class="metric-label">Cement Required</div>
            <div class="metric-value">{costs['total_cement_bags']:,.0f} bags</div>
            <div style="color: #8892a4; font-size: 0.8rem;">(50 kg bags) · {costs['cement_cost_formatted']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with mat3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🏗️</div>
            <div class="metric-label">Total Material Cost</div>
            <div class="metric-value">{costs['material_cost_formatted']}</div>
            <div style="color: #8892a4; font-size: 0.8rem;">Steel + Cement estimate</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ── Milestone Progress ──
    st.markdown('<div class="section-header">📅 Construction Milestone Tracker</div>', unsafe_allow_html=True)
    
    # Progress Bar
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {max(completion, 3)}%;">
            {completion}% Complete
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Milestone List
    ms_cols = st.columns(2)
    for i, ms in enumerate(MILESTONES):
        with ms_cols[i % 2]:
            if completion >= ms["end"]:
                ms_class = "ms-done"
                status_icon = "✅"
            elif completion >= ms["start"]:
                ms_class = "ms-active"
                status_icon = "🔄"
            else:
                ms_class = "ms-pending"
                status_icon = "⏳"
            
            st.markdown(f"""
            <div class="milestone {ms_class}">
                <span>{ms['icon']}</span>
                <span style="flex: 1;">{ms['name']}</span>
                <span>{status_icon}</span>
                <span style="font-size: 0.75rem; color: #8892a4;">{ms['start']}-{ms['end']}%</span>
            </div>
            """, unsafe_allow_html=True)
    
    # ── 3D Architectural Rendering ──
    st.markdown('<div class="section-header">🎨 Conceptual 3D Architectural Rendering</div>', unsafe_allow_html=True)
    st.markdown("*Powered by Pollinations AI — Generates a conceptual architectural visualization based on your project parameters.*")
    
    if st.button("🖼️ Generate 3D Concept Rendering", use_container_width=True, type="primary"):
        with st.spinner("🎨 Generating architectural visualization via Pollinations AI..."):
            render_url = generate_pollinations_url(structure_type, sqft, tier)
            try:
                import requests
                response = requests.get(render_url, timeout=30)
                if response.status_code == 200:
                    render_image = Image.open(io.BytesIO(response.content))
                    st.image(render_image, caption=f"🏛️ Conceptual Rendering: {structure_type} | {sqft:,} sqft | {tier.split('(')[0].strip()}", use_container_width=True)
                else:
                    st.image(render_url, caption=f"🏛️ Conceptual Rendering: {structure_type}", use_container_width=True)
            except Exception:
                st.image(render_url, caption=f"🏛️ Conceptual Rendering: {structure_type}", use_container_width=True)
    
    import io


# ═════════════════════════════════════════════════════════════
# TAB 4: DAILY SITE ASSISTANT & WEATHER-AWARE ADVISORY
# ═════════════════════════════════════════════════════════════

with tab4:
    st.markdown('<div class="section-header">🌦️ Weather-Aware Site Advisory & Construction Assistant</div>', unsafe_allow_html=True)
    
    # ── Weather Advisory Section ──
    weather_col, chat_col = st.columns([1, 1])
    
    with weather_col:
        st.markdown("##### 🌦️ Weather Condition Selector")
        selected_weather = st.selectbox(
            "Current Weather Condition",
            get_all_conditions(),
            help="Select the current weather condition to see safety protocols"
        )
        
        weather_data = get_weather_data(selected_weather)
        
        # Weather Header Card
        risk_color = weather_data["color"]
        st.markdown(f"""
        <div class="weather-header" style="background: linear-gradient(135deg, {risk_color}15, {risk_color}08); border: 1px solid {risk_color}33;">
            <div class="weather-icon">{weather_data['icon']}</div>
            <div style="font-size: 1.4rem; font-weight: 700;">{selected_weather}</div>
            <div style="margin-top: 8px;">
                <span class="status-pill" style="background: {risk_color}22; color: {risk_color}; border: 1px solid {risk_color}44;">
                    Risk Level: {weather_data['risk_level']}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Safety Alerts
        st.markdown("##### ⚠️ Active Safety Alerts")
        for alert in weather_data["alerts"]:
            priority = alert.get("priority", "INFO")
            alert_class = {
                "CRITICAL": "alert-critical",
                "HIGH": "alert-high",
                "MEDIUM": "alert-medium",
                "INFO": "alert-info",
            }.get(priority, "alert-info")
            
            st.markdown(f"""
            <div class="alert-card {alert_class}">
                <div class="alert-title">{alert.get('icon', '')} {alert.get('title', '')}</div>
                <div class="alert-desc">{alert.get('description', '')}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Protocols Checklist
        st.markdown("##### 📋 Safety Protocols")
        for protocol in weather_data["protocols"]:
            st.checkbox(protocol, key=f"proto_{protocol[:20]}")
    
    with chat_col:
        st.markdown("##### 🤖 Construction Engineering Assistant")
        st.markdown("*Ask questions about construction, structural engineering, safety standards, cost estimation, or any site-related topic.*")
        
        # Chat Container
        chat_container = st.container(height=450)
        
        with chat_container:
            if not st.session_state.chat_history:
                st.markdown("""
                <div class="chat-assistant">
                    👋 <strong>Welcome!</strong> I'm your Construction Engineering Assistant.<br/><br/>
                    I can help with:<br/>
                    • Structural engineering queries (RCC, steel design)<br/>
                    • Indian building codes (IS 456, IS 1893, NBC)<br/>
                    • Cost estimation & quantity surveying<br/>
                    • Safety compliance (OSHA, IS standards)<br/>
                    • Construction best practices<br/><br/>
                    <em>Ask me anything about your construction project!</em>
                </div>
                """, unsafe_allow_html=True)
            else:
                for msg in st.session_state.chat_history:
                    if msg["role"] == "user":
                        st.markdown(f"""
                        <div class="chat-user">{msg['content']}</div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="chat-assistant">{msg['content']}</div>
                        """, unsafe_allow_html=True)
        
        # Chat Input
        user_input = st.chat_input("Ask about construction, safety, costs...", key="chat_input")
        
        if user_input:
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Generate response
            if not st.session_state.demo_mode and st.session_state.gemini_model:
                with st.spinner("🤔 Thinking..."):
                    response = chat_with_gemini(
                        st.session_state.gemini_model,
                        st.session_state.chat_history[:-1],
                        user_input
                    )
            else:
                # Demo response
                demo_responses = {
                    "default": (
                        "Great question! In demo mode, I'm providing a sample response. "
                        "To get AI-powered answers from Google Gemini, please enter your API key in the sidebar.\n\n"
                        "**Here's a general tip:** When working on construction projects in India, "
                        "always ensure compliance with IS 456:2000 for plain and reinforced concrete, "
                        "IS 1893 for seismic design, and follow NBC India 2016 guidelines for overall building standards. "
                        "For cost estimation, consider regional material rate variations across Tier 1, 2, and 3 cities."
                    )
                }
                response = demo_responses["default"]
            
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()
        
        # Clear Chat Button
        if st.session_state.chat_history:
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
