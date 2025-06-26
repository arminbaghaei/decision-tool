import streamlit as st
import pandas as pd

# -------------------------------------------
# 🔹 Introduction Section
# -------------------------------------------
st.title("🏗️ Zero-Carbon Material Evaluation Tool")

st.markdown("""
In the pursuit of low-emission, sustainable buildings, selecting the most appropriate construction materials is a complex yet critical task. This decision-making tool assists users—such as architects, engineers, researchers, and policymakers—in evaluating and comparing zero-carbon building materials based on a comprehensive set of performance factors.

The tool applies a multi-criteria decision-making (MCDM) framework that incorporates six weighted categories: **Durability**, **Cost Effectiveness**, **Buildability**, **Embodied Carbon**, **Availability**, and **Aesthetics**. Each category contains detailed, context-specific evaluation items drawn from literature and industry standards, including lifecycle carbon impact, local supply chain considerations, and qualitative usability features.

Users select a material and assign scores based on predefined descriptors, ranging from quantitative metrics (e.g., embodied carbon in kg CO₂-eq/m², cost per square meter) to qualitative indicators (e.g., weather resistance, ease of handling). Final scores are automatically weighted and aggregated to support transparent and evidence-based decision-making.

This tool is designed with New Zealand's construction context in mind but can be adapted for broader international use.
""")

# -------------------------------------------
# 🔹 Factor Weights
# -------------------------------------------
factors = {
    "Durability": 19.13,
    "Cost Effectiveness": 19.29,
    "Buildability": 17.79,
    "Embodied Carbon": 15.71,
    "Availability": 14.41,
    "Aesthetics": 13.66
}

# -------------------------------------------
# 🔹 Evaluation Criteria per Factor
# -------------------------------------------
criteria = {
    "Durability": {
        "Weather resistance": ["10%", "20%", "30%", "40%", "50%"],
        "UV resistance": ["10%", "20%", "30%", "40%", "50%"],
        "Service life": ["20 years", "30 years", "50 years", "100 years", "Over 100 years"],
        "Maintenance frequency": ["Every 10 yrs", "Every 20 yrs", "Every 30 yrs", "Every 50 yrs", "Over 50 yrs"]
    },
    "Cost Effectiveness": {
        "Maintenance cost (NZD/sqm)": ["$60+", "$40-$60", "$30-$40", "$20-$30", "Less than $20"],
        "Upfront material cost (NZD/sqm)": ["$150+", "$100-$150", "$70-$100", "$40-$70", "Less than $40"],
        "Financial incentives": ["None", "Low", "Moderate", "High", "Very High"]
    },
    "Buildability": {
        "Ease of handling": ["Very Difficult", "Difficult", "Moderate", "Easy", "Very Easy"],
        "Specialist equipment required": ["Extensive", "High", "Moderate", "Low", "None"],
        "Expertise availability": ["Rare", "Limited", "Some", "Common", "Very Common"],
        "Compatibility with materials": ["1 material", "2 materials", "3 materials", "4 materials", "5+ materials"]
    },
    "Embodied Carbon": {
        "Production (cradle to gate) [kg CO₂-eq/m²]": [
            "Very High (>100)", 
            "High (75–100)", 
            "Moderate (50–75)", 
            "Low (25–50)", 
            "Very Low (<25)"
        ],
        "End-of-life: Recycle": ["Never", "Rarely", "Sometimes", "Often", "Always"],
        "End-of-life: Reuse": ["Never", "Rarely", "Sometimes", "Often", "Always"],
        "End-of-life: Recovery": ["Never", "Rarely", "Sometimes", "Often", "Always"]
    },
    "Availability": {
        "Local supply chains": ["None", "Limited", "Moderate", "Strong", "Very Strong"],
        "Transport costs": ["Very High", "High", "Moderate", "Low", "Very Low"],
        "Production scalability": ["None", "Low", "Moderate", "High", "Very High"],
        "Material scarcity": ["Very Rare", "Rare", "Moderate", "Common", "Very Common"]
    },
    "Aesthetics": {
        "Visual appeal": ["Very Poor", "Poor", "Moderate", "Attractive", "Excellent"],
        "Finish options": ["Very Limited", "Limited", "Moderate", "Varied", "Extensive"],
        "Design adaptability": ["Very Rigid", "Rigid", "Moderate", "Flexible", "Very Flexible"],
        "Style bias": ["Highly Biased", "Biased", "Neutral", "Adaptive", "Universal"]
    }
}

# -------------------------------------------
# 🔹 Material Defaults for Cost
# -------------------------------------------
nz_prices = {
    "Wood": {
        "Maintenance cost (NZD/sqm)": "$60+",
        "Upfront material cost (NZD/sqm)": "$100-$150"
    },
    "Hemp": {
        "Maintenance cost (NZD/sqm)": "$40-$60",
        "Upfront material cost (NZD/sqm)": "$70-$100"
    },
    "Rammed Earth": {
        "Maintenance cost (NZD/sqm)": "$30-$40",
        "Upfront material cost (NZD/sqm)": "$40-$70"
    },
    "Straw Bale": {
        "Maintenance cost (NZD/sqm)": "$20-$30",
        "Upfront material cost (NZD/sqm)": "Less than $40"
    }
}

# -------------------------------------------
# 🔹 Material Selection & Scoring
# -------------------------------------------
materials = list(nz_prices.keys())
selected_material = st.selectbox("Select Material", materials)

score_table = []
total_score = 0

for factor, weight in factors.items():
    if factor in criteria:
        st.subheader(factor)
        for item, options in criteria[factor].items():
            if item in nz_prices[selected_material]:
                default_value = nz_prices[selected_material][item]
                default_index = options.index(default_value)
                selected_option = st.selectbox(f"{item}", options, index=default_index, key=f"{factor}_{item}")
            else:
                selected_option = st.selectbox(f"{item}", options, key=f"{factor}_{item}")
            score = options.index(selected_option) + 1
            weighted = score * weight / 5
            score_table.append({
                "Factor": factor,
                "Item": item,
                "Selected Option": selected_option,
                "Score (1-5)": score,
                "Weight": weight,
                "Weighted Contribution": weighted
            })
            total_score += weighted

# -------------------------------------------
# 🔹 Final Result Display
# -------------------------------------------
st.markdown(f"### ✅ Final Weighted Score for **{selected_material}**: **{total_score:.2f}**")

if st.checkbox("Show Detailed Score Table"):
    df = pd.DataFrame(score_table)
    st.dataframe(df)
