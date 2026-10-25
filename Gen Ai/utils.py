"""
Utility Functions & AI Prompt Engineering Module
Handles Gemini API integration, prompt templates, and demo data fallbacks.
"""

import json
import io
import base64
from PIL import Image

# ─────────────────────────────────────────────────────────────
# DEMO / FALLBACK DATA (used when no API key is provided)
# ─────────────────────────────────────────────────────────────

DEMO_PPE_RESULT = {
    "safety_score": 72,
    "overall_status": "Needs Improvement",
    "ppe_detection": [
        {"item": "Hard Hat / Helmet", "detected": True, "compliance": "Compliant", "notes": "Visible on 3 of 4 workers"},
        {"item": "High-Visibility Vest", "detected": True, "compliance": "Partial", "notes": "Only 2 workers wearing reflective vests"},
        {"item": "Steel-Toe Boots", "detected": False, "compliance": "Non-Compliant", "notes": "Cannot confirm safety footwear on any worker"},
        {"item": "Safety Harness", "detected": False, "compliance": "Non-Compliant", "notes": "Workers at height without fall protection"},
        {"item": "Safety Gloves", "detected": True, "compliance": "Compliant", "notes": "Gloves visible on workers handling materials"},
        {"item": "Eye Protection", "detected": False, "compliance": "Non-Compliant", "notes": "No safety goggles observed during cutting operations"}
    ],
    "hazards": [
        {
            "hazard": "Fall Risk - Unguarded Edge",
            "severity": "Critical",
            "location": "Upper floor slab edge",
            "corrective_action": "Install temporary guardrails or safety nets immediately. All workers at height must use double-lanyard fall arrest systems."
        },
        {
            "hazard": "Electrical Exposure",
            "severity": "High",
            "location": "Near temporary power distribution board",
            "corrective_action": "Install GFCI protection on all temporary circuits. Ensure all cables are properly insulated and routed away from water sources."
        },
        {
            "hazard": "Material Storage Hazard",
            "severity": "Medium",
            "location": "Ground floor staging area",
            "corrective_action": "Reorganize material stacking to maintain proper clearance. Secure top-heavy stacks with bracing."
        },
        {
            "hazard": "Dust Exposure",
            "severity": "Low",
            "location": "Concrete cutting area",
            "corrective_action": "Provide N95 respirators to workers in dusty areas. Use water suppression during cutting operations."
        }
    ],
    "recommendations": [
        "Conduct immediate safety stand-down for PPE compliance training",
        "Install permanent guardrails on all open edges above 6 feet",
        "Implement daily PPE inspection checklist",
        "Assign a dedicated safety marshal for each work zone"
    ],
    "standards_referenced": ["OSHA 29 CFR 1926", "IS 456:2000", "NBC India 2016"]
}

DEMO_CRACK_RESULT = {
    "defect_type": "Settlement Crack",
    "severity": "Moderate",
    "estimated_crack_width_mm": 1.8,
    "crack_pattern": "Diagonal stepping pattern following mortar joints",
    "structural_risk": "Medium",
    "root_causes": [
        "Differential settlement of foundation due to uneven soil bearing capacity",
        "Inadequate foundation depth for soil conditions",
        "Possible water table fluctuation causing soil volume changes",
        "Absence of proper plinth beam to distribute loads"
    ],
    "recommended_repairs": [
        {
            "method": "Epoxy Injection",
            "description": "Inject structural epoxy resin into crack to restore tensile strength. Use low-viscosity epoxy (500-1500 cps) for cracks under 2mm.",
            "estimated_cost": "₹150-300 per running foot",
            "urgency": "High"
        },
        {
            "method": "Structural Re-grouting",
            "description": "Pressure grout the foundation zone with cement-bentonite slurry to improve soil bearing capacity and arrest further settlement.",
            "estimated_cost": "₹500-1200 per sqft of treated area",
            "urgency": "High"
        },
        {
            "method": "Carbon Fiber Reinforcement",
            "description": "Apply CFRP strips across crack path to provide additional tensile reinforcement and prevent crack propagation.",
            "estimated_cost": "₹800-1500 per running foot",
            "urgency": "Medium"
        },
        {
            "method": "Underpinning",
            "description": "If settlement continues, underpin the foundation with micro-piles or mass concrete to reach stable bearing stratum.",
            "estimated_cost": "₹2000-5000 per sqft",
            "urgency": "Monitor"
        }
    ],
    "monitoring_plan": "Install crack width gauges at 3 points along the crack. Record measurements weekly for 3 months. If crack width increases by more than 0.3mm, escalate to structural underpinning.",
    "standards_referenced": ["IS 456:2000", "IS 13920", "ACI 224R-01"]
}


# ─────────────────────────────────────────────────────────────
# GEMINI AI PROMPT TEMPLATES
# ─────────────────────────────────────────────────────────────

PPE_AUDIT_PROMPT = """You are an expert construction safety auditor certified in OSHA 29 CFR 1926 and IS 456:2000 standards.

Analyze this construction site photograph and provide a comprehensive PPE (Personal Protective Equipment) safety compliance audit.

Respond ONLY with valid JSON (no markdown, no code fences) in this exact structure:
{
    "safety_score": <integer 0-100>,
    "overall_status": "<Compliant|Needs Improvement|Non-Compliant|Critical Violation>",
    "ppe_detection": [
        {
            "item": "<PPE item name>",
            "detected": <true|false>,
            "compliance": "<Compliant|Partial|Non-Compliant>",
            "notes": "<specific observation>"
        }
    ],
    "hazards": [
        {
            "hazard": "<hazard description>",
            "severity": "<Low|Medium|High|Critical>",
            "location": "<where in the image>",
            "corrective_action": "<detailed remedy>"
        }
    ],
    "recommendations": ["<actionable recommendation>"],
    "standards_referenced": ["<standard codes>"]
}

PPE items to check: Hard Hat/Helmet, High-Visibility Vest, Steel-Toe Boots, Safety Harness, Safety Gloves, Eye Protection, Respiratory Protection.
Be thorough, specific, and reference actual observations from the image."""

CRACK_DIAGNOSIS_PROMPT = """You are an expert structural engineer specializing in concrete pathology and building diagnostics, certified in IS 456:2000 and ACI 318.

Analyze this image of a concrete/masonry surface and provide a comprehensive crack diagnosis.

Respond ONLY with valid JSON (no markdown, no code fences) in this exact structure:
{
    "defect_type": "<Hairline|Settlement|Structural Shear|Thermal Expansion|Spalling|Corrosion-Induced|Shrinkage|Flexural>",
    "severity": "<Minor|Moderate|Severe|Critical>",
    "estimated_crack_width_mm": <float>,
    "crack_pattern": "<description of crack pattern and orientation>",
    "structural_risk": "<Low|Medium|High|Critical>",
    "root_causes": ["<cause 1>", "<cause 2>"],
    "recommended_repairs": [
        {
            "method": "<repair technique>",
            "description": "<detailed procedure>",
            "estimated_cost": "<cost range in INR>",
            "urgency": "<Immediate|High|Medium|Monitor>"
        }
    ],
    "monitoring_plan": "<monitoring instructions>",
    "standards_referenced": ["<applicable standards>"]
}

Classify the defect type accurately. Estimate crack width based on visual proportions. Provide practical, cost-effective repair methods prioritized by urgency."""

CHATBOT_SYSTEM_PROMPT = """You are an expert Construction Engineering Assistant with deep knowledge in:
- Structural engineering (RCC, steel, pre-stressed concrete)
- Construction project management (CPM, PERT, Lean Construction)
- Indian building codes (IS 456, IS 1893, NBC India)
- OSHA safety standards and IS safety codes
- Cost estimation and quantity surveying for Indian markets
- Building materials science and testing
- Geotechnical engineering and foundation design
- MEP (Mechanical, Electrical, Plumbing) systems
- Green building and sustainability (IGBC, GRIHA ratings)
- Real estate valuation in the Indian market

Provide detailed, practical, and accurate answers. Reference specific IS codes, OSHA standards, or industry best practices where applicable. Use Indian units (INR, sqft, kg) when discussing costs and quantities. Be conversational yet professional."""


def configure_gemini(api_key: str):
    """Configure and return the Gemini model."""
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model


def analyze_image_with_gemini(model, image: Image.Image, prompt: str) -> dict:
    """
    Send an image + prompt to Gemini and parse the JSON response.
    """
    try:
        response = model.generate_content([prompt, image])
        text = response.text.strip()
        
        # Clean potential markdown code fences
        if text.startswith("```"):
            text = text.split("\n", 1)[1]  # Remove first line
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
        
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to extract JSON from response
        try:
            start = text.index("{")
            end = text.rindex("}") + 1
            return json.loads(text[start:end])
        except (ValueError, json.JSONDecodeError):
            return None
    except Exception as e:
        return None


def chat_with_gemini(model, messages: list, user_message: str) -> str:
    """
    Multi-turn chat with Gemini.
    """
    try:
        chat = model.start_chat(history=[])
        
        # Send system prompt first
        chat.send_message(CHATBOT_SYSTEM_PROMPT)
        
        # Replay conversation history
        for msg in messages:
            if msg["role"] == "user":
                chat.send_message(msg["content"])
            # Assistant messages are already in history
        
        # Send current message
        if messages and messages[-1]["role"] == "user" and messages[-1]["content"] == user_message:
            # Already sent as part of history replay
            response = chat.history[-1]
            return response.parts[0].text
        
        response = chat.send_message(user_message)
        return response.text
    except Exception as e:
        return f"I apologize, but I encountered an error: {str(e)}. Please check your API key and try again."


def image_to_base64(image: Image.Image) -> str:
    """Convert PIL Image to base64 string."""
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()


def get_severity_color(severity: str) -> str:
    """Return color hex for severity level."""
    colors = {
        "Low": "#28a745",
        "Minor": "#28a745",
        "Medium": "#fd7e14",
        "Moderate": "#fd7e14",
        "High": "#dc3545",
        "Severe": "#dc3545",
        "Critical": "#ff0040",
        "INFO": "#17a2b8",
        "MEDIUM": "#fd7e14",
        "CRITICAL": "#ff0040",
    }
    return colors.get(severity, "#6c757d")


def get_status_color(status: str) -> str:
    """Return color hex for compliance status."""
    colors = {
        "Compliant": "#28a745",
        "Partial": "#fd7e14",
        "Non-Compliant": "#dc3545",
        "Needs Improvement": "#fd7e14",
        "Critical Violation": "#ff0040",
    }
    return colors.get(status, "#6c757d")


def generate_pollinations_url(structure_type: str, sqft: float, tier: str) -> str:
    """Generate a Pollinations AI image URL for architectural concept rendering."""
    # Build descriptive prompt for the architectural rendering
    tier_desc = {
        "Tier 1 (Metro: Mumbai, Delhi, Bangalore)": "modern metropolitan Indian city skyline",
        "Tier 2 (City: Pune, Jaipur, Lucknow)": "growing Indian city landscape",
        "Tier 3 (Town: Indore, Coimbatore, Vizag)": "emerging Indian town setting",
    }
    
    location = tier_desc.get(tier, "Indian urban setting")
    
    prompt = (
        f"Professional 3D architectural rendering of a {structure_type.lower()} building, "
        f"{sqft:.0f} sqft, in a {location}. "
        f"Photorealistic, golden hour lighting, landscaped surroundings, "
        f"modern Indian architecture style, high detail, 8K quality"
    )
    
    # URL-encode the prompt
    import urllib.parse
    encoded = urllib.parse.quote(prompt)
    
    return f"https://image.pollinations.ai/prompt/{encoded}?width=800&height=500&nologo=true"
