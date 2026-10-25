"""
Weather-Aware Safety Protocols Module
Provides dynamic safety alerts and protocols based on weather conditions.
"""

WEATHER_PROTOCOLS = {
    "Normal": {
        "icon": "☀️",
        "risk_level": "Low",
        "color": "#28a745",
        "alerts": [
            {
                "title": "Standard Operations",
                "description": "All construction activities may proceed under normal safety protocols.",
                "icon": "✅",
                "priority": "INFO"
            },
            {
                "title": "Routine PPE Compliance",
                "description": "Ensure all workers maintain standard PPE: hard hats, safety vests, steel-toe boots.",
                "icon": "🦺",
                "priority": "INFO"
            },
            {
                "title": "Hydration Reminder",
                "description": "Maintain regular water breaks every 60 minutes for all site personnel.",
                "icon": "💧",
                "priority": "INFO"
            }
        ],
        "protocols": [
            "Follow standard OSHA safety checklist",
            "Conduct morning toolbox talk",
            "Inspect scaffolding and fall protection systems",
            "Verify crane load charts are current",
            "Ensure first-aid stations are stocked"
        ]
    },
    "High Wind": {
        "icon": "🌬️",
        "risk_level": "High",
        "color": "#dc3545",
        "alerts": [
            {
                "title": "⚠️ CRANE OPERATIONS SUSPENDED",
                "description": "All crane and lifting operations MUST be suspended when wind speeds exceed 20 mph (32 km/h). Secure all suspended loads immediately.",
                "icon": "🏗️",
                "priority": "CRITICAL"
            },
            {
                "title": "Scaffolding Safety Alert",
                "description": "Inspect all scaffolding connections. Workers above 6 feet must use double lanyards. Secure loose materials and tarps.",
                "icon": "🔧",
                "priority": "HIGH"
            },
            {
                "title": "Material Securing Protocol",
                "description": "All loose materials, formwork panels, and sheet metal must be secured or stored. Flying debris is the #1 wind-related hazard.",
                "icon": "📦",
                "priority": "HIGH"
            },
            {
                "title": "Evacuation Readiness",
                "description": "Brief all workers on evacuation routes. If gusts exceed 40 mph, initiate site evacuation protocol.",
                "icon": "🚨",
                "priority": "CRITICAL"
            }
        ],
        "protocols": [
            "Suspend all crane and hoisting operations above 20 mph winds",
            "Secure all loose materials, debris, and formwork",
            "Reinforce scaffolding tie-backs and bracing",
            "Workers at height must use double fall protection",
            "Monitor wind speed with on-site anemometer every 15 minutes",
            "Prepare evacuation if gusts exceed 40 mph",
            "Postpone concrete pouring if wind causes rapid moisture loss"
        ]
    },
    "Heavy Rain": {
        "icon": "🌧️",
        "risk_level": "High",
        "color": "#fd7e14",
        "alerts": [
            {
                "title": "⚠️ ELECTRICAL HAZARD MITIGATION",
                "description": "Disconnect all temporary electrical connections. Use GFCI-protected circuits only. No welding operations permitted in wet conditions.",
                "icon": "⚡",
                "priority": "CRITICAL"
            },
            {
                "title": "Concrete Curing Protocol",
                "description": "Cover all freshly poured concrete with waterproof curing blankets. Delay new pours until 24 hours after rain stops. Water-cement ratio compromised by rain.",
                "icon": "🧱",
                "priority": "HIGH"
            },
            {
                "title": "Slip & Fall Prevention",
                "description": "Deploy anti-slip mats on walkways. Reduce speed limits for site vehicles to 5 mph. Extra caution on ramps and slopes.",
                "icon": "⚠️",
                "priority": "HIGH"
            },
            {
                "title": "Excavation Flooding Risk",
                "description": "Monitor all open excavations for water accumulation. Activate dewatering pumps. Do NOT allow workers in flooded trenches.",
                "icon": "🕳️",
                "priority": "CRITICAL"
            }
        ],
        "protocols": [
            "Disconnect temporary electrical connections immediately",
            "Use only GFCI-protected circuits in wet areas",
            "Cover fresh concrete with curing blankets",
            "Postpone new concrete pours for 24 hours post-rain",
            "Deploy anti-slip mats on all walkways and ramps",
            "Activate dewatering pumps in excavations",
            "Prohibit welding and cutting operations in wet conditions",
            "Reduce site vehicle speed to 5 mph",
            "Monitor soil stability around foundations"
        ]
    },
    "Extreme Heat": {
        "icon": "🔥",
        "risk_level": "Medium-High",
        "color": "#e83e8c",
        "alerts": [
            {
                "title": "⚠️ HEAT STRESS PREVENTION",
                "description": "Mandatory water breaks every 20 minutes. Rotate workers in shaded areas. Watch for heat exhaustion symptoms: dizziness, nausea, excessive sweating.",
                "icon": "🌡️",
                "priority": "CRITICAL"
            },
            {
                "title": "Modified Work Schedule",
                "description": "Shift heavy labor to early morning (6-10 AM) and late afternoon (4-6 PM). Reduce midday work intensity by 50%.",
                "icon": "🕐",
                "priority": "HIGH"
            },
            {
                "title": "Concrete Curing Adjustments",
                "description": "Increase curing water application frequency. Use retarder admixtures to prevent flash setting. Monitor concrete temperature — max 90°F (32°C).",
                "icon": "🧱",
                "priority": "HIGH"
            },
            {
                "title": "Equipment Cooling",
                "description": "Allow machinery cool-down periods every 2 hours. Check hydraulic fluid temperatures. Inspect tire pressures (heat expansion risk).",
                "icon": "🔧",
                "priority": "MEDIUM"
            }
        ],
        "protocols": [
            "Mandatory hydration breaks every 20 minutes",
            "Provide shaded rest areas with cooling stations",
            "Shift heavy labor to cooler hours (6-10 AM, 4-6 PM)",
            "Train supervisors on heat stroke recognition",
            "Keep first-aid kits stocked with ice packs and electrolytes",
            "Use retarder admixtures in concrete mixes",
            "Increase curing water application by 50%",
            "Monitor equipment operating temperatures",
            "Provide UV-protective gear and sunscreen"
        ]
    }
}


def get_weather_data(condition: str) -> dict:
    """Return the weather protocol data for a given condition."""
    return WEATHER_PROTOCOLS.get(condition, WEATHER_PROTOCOLS["Normal"])


def get_all_conditions() -> list:
    """Return all available weather conditions."""
    return list(WEATHER_PROTOCOLS.keys())
