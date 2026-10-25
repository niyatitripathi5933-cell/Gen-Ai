"""
Construction Cost & Real Estate Valuation Calculator Module
Provides estimation for Indian construction projects with tier-based pricing.
"""

# Base rates in INR per sqft (2024 estimates)
CONSTRUCTION_RATES = {
    "Residential - Standard": {"tier1": 2200, "tier2": 1600, "tier3": 1200},
    "Residential - Premium": {"tier1": 3500, "tier2": 2800, "tier3": 2000},
    "Residential - Luxury": {"tier1": 5500, "tier2": 4200, "tier3": 3200},
    "Commercial - Office": {"tier1": 3800, "tier2": 2800, "tier3": 2200},
    "Commercial - Retail": {"tier1": 4200, "tier2": 3200, "tier3": 2500},
    "Industrial - Warehouse": {"tier1": 1800, "tier2": 1400, "tier3": 1000},
    "Industrial - Factory": {"tier1": 2500, "tier2": 2000, "tier3": 1500},
    "Institutional - School/Hospital": {"tier1": 3200, "tier2": 2500, "tier3": 1800},
}

# Market valuation multipliers
VALUATION_MULTIPLIERS = {
    "tier1": 2.8,  # Tier 1 cities (Mumbai, Delhi, Bangalore)
    "tier2": 2.2,  # Tier 2 cities (Pune, Jaipur, Lucknow)
    "tier3": 1.7,  # Tier 3 cities (Indore, Coimbatore, Vizag)
}

# Material requirements per sqft
MATERIAL_RATES = {
    "steel_kg_per_sqft": {
        "Residential - Standard": 4.5,
        "Residential - Premium": 5.5,
        "Residential - Luxury": 6.5,
        "Commercial - Office": 6.0,
        "Commercial - Retail": 5.5,
        "Industrial - Warehouse": 7.0,
        "Industrial - Factory": 8.0,
        "Institutional - School/Hospital": 5.5,
    },
    "cement_bags_per_sqft": {
        "Residential - Standard": 0.4,
        "Residential - Premium": 0.45,
        "Residential - Luxury": 0.5,
        "Commercial - Office": 0.5,
        "Commercial - Retail": 0.48,
        "Industrial - Warehouse": 0.35,
        "Industrial - Factory": 0.45,
        "Institutional - School/Hospital": 0.45,
    }
}

# Material unit costs (INR)
STEEL_RATE_PER_KG = 75  # INR
CEMENT_RATE_PER_BAG = 380  # INR (50 kg bag)

# Milestone definitions
MILESTONES = [
    {"name": "Foundation & Excavation", "start": 0, "end": 15, "icon": "🏗️"},
    {"name": "Structural Framework (RCC)", "start": 15, "end": 35, "icon": "🏛️"},
    {"name": "Brickwork & Masonry", "start": 35, "end": 50, "icon": "🧱"},
    {"name": "MEP (Plumbing, Electrical)", "start": 50, "end": 65, "icon": "⚡"},
    {"name": "Plastering & Waterproofing", "start": 65, "end": 75, "icon": "🎨"},
    {"name": "Flooring & Tiling", "start": 75, "end": 85, "icon": "🪨"},
    {"name": "Painting & Finishing", "start": 85, "end": 95, "icon": "🖌️"},
    {"name": "Handover & Punch List", "start": 95, "end": 100, "icon": "🔑"},
]


def format_inr(amount: float) -> str:
    """Format amount in Indian numbering system (Lakhs/Crores)."""
    if amount >= 1_00_00_000:
        return f"₹{amount / 1_00_00_000:.2f} Cr"
    elif amount >= 1_00_000:
        return f"₹{amount / 1_00_000:.2f} L"
    else:
        return f"₹{amount:,.0f}"


def get_tier_key(tier: str) -> str:
    """Convert tier display name to key."""
    mapping = {
        "Tier 1 (Metro: Mumbai, Delhi, Bangalore)": "tier1",
        "Tier 2 (City: Pune, Jaipur, Lucknow)": "tier2",
        "Tier 3 (Town: Indore, Coimbatore, Vizag)": "tier3",
    }
    return mapping.get(tier, "tier2")


def calculate_project_costs(structure_type: str, sqft: float, tier: str, completion_pct: float) -> dict:
    """
    Calculate comprehensive project costs and valuations.
    
    Returns dict with all financial and material metrics.
    """
    tier_key = get_tier_key(tier)
    
    # Base construction cost
    rate_per_sqft = CONSTRUCTION_RATES.get(structure_type, {}).get(tier_key, 2000)
    total_budget = rate_per_sqft * sqft
    
    # Capital expenditure based on completion
    capex_incurred = total_budget * (completion_pct / 100)
    capex_remaining = total_budget - capex_incurred
    
    # Market valuation
    multiplier = VALUATION_MULTIPLIERS.get(tier_key, 2.0)
    market_valuation = total_budget * multiplier * (completion_pct / 100) * 0.85  # 85% of theoretical for realistic estimate
    # Minimum valuation = land + construction done
    market_valuation = max(market_valuation, capex_incurred * 1.1)
    
    # Material calculations
    steel_per_sqft = MATERIAL_RATES["steel_kg_per_sqft"].get(structure_type, 5.0)
    cement_per_sqft = MATERIAL_RATES["cement_bags_per_sqft"].get(structure_type, 0.4)
    
    total_steel_kg = steel_per_sqft * sqft
    total_cement_bags = cement_per_sqft * sqft
    
    steel_cost = total_steel_kg * STEEL_RATE_PER_KG
    cement_cost = total_cement_bags * CEMENT_RATE_PER_BAG
    
    # Milestone tracking
    current_milestone = None
    completed_milestones = []
    upcoming_milestones = []
    
    for ms in MILESTONES:
        if completion_pct >= ms["end"]:
            completed_milestones.append(ms)
        elif completion_pct >= ms["start"]:
            current_milestone = ms
        else:
            upcoming_milestones.append(ms)
    
    return {
        "rate_per_sqft": rate_per_sqft,
        "total_budget": total_budget,
        "total_budget_formatted": format_inr(total_budget),
        "capex_incurred": capex_incurred,
        "capex_incurred_formatted": format_inr(capex_incurred),
        "capex_remaining": capex_remaining,
        "capex_remaining_formatted": format_inr(capex_remaining),
        "market_valuation": market_valuation,
        "market_valuation_formatted": format_inr(market_valuation),
        "total_steel_kg": total_steel_kg,
        "total_steel_mt": total_steel_kg / 1000,
        "steel_cost": steel_cost,
        "steel_cost_formatted": format_inr(steel_cost),
        "total_cement_bags": total_cement_bags,
        "cement_cost": cement_cost,
        "cement_cost_formatted": format_inr(cement_cost),
        "material_cost_total": steel_cost + cement_cost,
        "material_cost_formatted": format_inr(steel_cost + cement_cost),
        "current_milestone": current_milestone,
        "completed_milestones": completed_milestones,
        "upcoming_milestones": upcoming_milestones,
        "completion_pct": completion_pct,
        "sqft": sqft,
        "structure_type": structure_type,
        "tier": tier,
    }


def get_structure_types() -> list:
    """Return all available structure types."""
    return list(CONSTRUCTION_RATES.keys())


def get_tier_options() -> list:
    """Return all available city tier options."""
    return [
        "Tier 1 (Metro: Mumbai, Delhi, Bangalore)",
        "Tier 2 (City: Pune, Jaipur, Lucknow)",
        "Tier 3 (Town: Indore, Coimbatore, Vizag)",
    ]
