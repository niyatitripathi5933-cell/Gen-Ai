# 🏗️ Multimodal Construction Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Google_Gemini-1.5_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

> **SkillWallet Capstone Project 1** · Platform ID: `6ac4c98d1dcde6d7857c1642`

An intelligent decision-support system that analyzes construction site photos to audit PPE safety compliance, classify concrete cracks with severity scores, estimate construction costs and real estate valuation in INR, and provide weather-aware daily protocols — all powered by Google Gemini's multimodal AI.

---

## ✨ Features

### 🦺 Tab 1 — Site Safety & PPE Audit (Epic 2)
- Upload construction site photos (JPG/PNG)
- Multimodal AI analysis of worker PPE compliance
- **PPE Checklist:** Helmets, high-vis vests, steel-toe boots, safety harnesses, gloves, eye protection
- **Standards:** OSHA 29 CFR 1926 & IS 456:2000
- Safety score (0–100) with color-coded status pills
- Identified hazards with severity levels (Low → Critical) and corrective remedies
- Downloadable JSON audit report

### 🧱 Tab 2 — Crack Diagnostics & Structural Integrity (Epic 2)
- Upload concrete/masonry surface photos
- AI-powered defect classification:
  - Hairline · Settlement · Structural Shear · Thermal Expansion · Spalling · Corrosion-Induced
- Estimated crack width in mm
- Root cause analysis with engineering repair recommendations
- Repair methods: Epoxy injection, structural re-grouting, CFRP reinforcement, underpinning
- Cost estimates in INR and urgency ratings

### 💰 Tab 3 — Planning & Real Estate Valuation (Epic 3)
- Interactive inputs: structure type, built-up sqft, city tier (Tier 1/2/3), completion %
- **Financial Metrics:** Total budget, CapEx incurred/remaining, market valuation (₹ Lakhs/Crores)
- **Material Requirements:** Steel (MT), cement (bags), with cost breakdowns
- Construction milestone progress tracker with 8 phases
- 3D architectural concept rendering via **Pollinations AI**

### 🤖 Tab 4 — Site Assistant & Weather Advisory (Epic 5)
- **Weather Selector:** Normal, High Wind, Heavy Rain, Extreme Heat
- Dynamic safety alerts per weather condition (crane suspension, electrical hazard mitigation, concrete curing protocols)
- Interactive safety protocol checklists
- **Multi-turn AI Chatbot** for construction engineering Q&A
  - Structural engineering, Indian building codes (IS 456, IS 1893, NBC)
  - Cost estimation, geotechnical engineering, MEP systems
  - Green building (IGBC, GRIHA ratings)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Streamlit Frontend                  │
│  ┌───────────┬───────────┬───────────┬───────────┐  │
│  │ PPE Audit │   Crack   │ Planning  │   Site    │  │
│  │  Tab 1    │  Diag.    │ & Value   │ Assistant │  │
│  │           │  Tab 2    │  Tab 3    │  Tab 4    │  │
│  └─────┬─────┴─────┬─────┴─────┬─────┴─────┬─────┘  │
│        │           │           │           │         │
│  ┌─────▼───────────▼───────────▼───────────▼─────┐  │
│  │            Google Gemini 1.5 Flash            │  │
│  │          (Multimodal Vision + Chat)            │  │
│  └───────────────────┬───────────────────────────┘  │
│                      │                               │
│  ┌───────────────────▼───────────────────────────┐  │
│  │     JSON Data Contracts · Cost Calculators     │  │
│  │    Weather Protocols · Pollinations AI API     │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
Gen Ai/
├── .streamlit/
│   └── config.toml          # Streamlit dark theme & server config
├── app.py                    # Main application (UI, tabs, routing)
├── utils.py                  # Gemini AI integration, prompts, demo data
├── calculators.py            # Cost estimation & valuation engine (INR)
├── weather.py                # Weather-aware safety protocols
├── requirements.txt          # Python dependencies
├── project.txt               # Original project requirements
└── README.md                 # This file
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+** installed ([download](https://python.org/downloads))
- **Google Gemini API Key** (free) — [Get yours here](https://makersuite.google.com/app/apikey)

### Installation

1. **Clone or download** the project:
   ```bash
   git clone <repository-url>
   cd "Gen Ai"
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser:** Navigate to `http://localhost:8501`

5. **Enter your API key** in the sidebar (optional — app works in Demo Mode without it)

---

## 🎭 Demo Mode vs Live AI Mode

| Feature | 🟡 Demo Mode | 🟢 Live AI Mode |
|---|---|---|
| API Key Required | No | Yes (Gemini) |
| PPE Audit | Sample analysis data | Real AI image analysis |
| Crack Diagnostics | Sample diagnosis data | Real AI defect classification |
| Cost Calculator | ✅ Fully functional | ✅ Fully functional |
| Weather Advisory | ✅ Fully functional | ✅ Fully functional |
| Chatbot | Static responses | Multi-turn AI conversations |
| 3D Rendering | ✅ Pollinations AI | ✅ Pollinations AI |

> **Tip:** The app gracefully falls back to Demo Mode if no API key is supplied or if the key is invalid.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.9+** | Core language |
| **Streamlit** | Web framework & UI |
| **Google Gemini 1.5 Flash** | Multimodal AI (vision + text) |
| **Pillow (PIL)** | Image processing |
| **Pollinations AI** | 3D architectural rendering |
| **Custom CSS** | Premium dark UI with animations |

---

## 📊 Kanban Epics Coverage

| Epic | Status | Description |
|---|---|---|
| **Pre-requisites** | ✅ Complete | Python 3.9+, Streamlit, Gemini SDK |
| **Epic 1** | ✅ Complete | Requirements & Environment Setup |
| **Epic 2** | ✅ Complete | PPE Safety Vision & Crack Diagnostics |
| **Epic 3** | ✅ Complete | Project Planning & Real Estate Valuation |
| **Epic 4** | ✅ Complete | Multimodal AI & JSON Contracts |
| **Epic 5** | ✅ Complete | Site Chatbot & Weather Advisory |
| **Epic 6** | ✅ Complete | Interface, Testing, Cloud Deployment |

---

## ☁️ Deploy to Streamlit Community Cloud

This app is designed for **1-click deployment** with zero external database dependencies.

1. Push your code to a **GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set `app.py` as the main file
5. Add your Gemini API key as a **secret** in Streamlit Cloud:
   ```toml
   # .streamlit/secrets.toml
   GEMINI_API_KEY = "your-api-key-here"
   ```
6. Click **Deploy** 🚀

---

## 📐 Standards & Compliance

This platform references the following construction safety and engineering standards:

- **OSHA 29 CFR 1926** — Safety and Health Regulations for Construction
- **IS 456:2000** — Plain and Reinforced Concrete Code of Practice
- **IS 1893** — Criteria for Earthquake Resistant Design
- **IS 13920** — Ductile Detailing of Reinforced Concrete Structures
- **NBC India 2016** — National Building Code
- **ACI 224R-01** — Control of Cracking in Concrete Structures
- **ACI 318** — Building Code Requirements for Structural Concrete

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## 📄 License

This project is part of the **SkillWallet Capstone Program** — Generative AI & Real Estate Decision Support.

---

<div align="center">

**Built with ❤️ for SkillWallet**

*Multimodal Construction Intelligence Platform · Capstone Project 1*

</div>
