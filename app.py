import streamlit as st
import pandas as pd

# Weights for each factor
factors = {
    "Durability": 19.13,
    "Cost Effectiveness": 19.29,
    "Buildability": 17.79,
    "Embodied Carbon": 15.71,
    "Availability": 14.41,
    "Aesthetics": 13.66
}

# Updated evaluation criteria and standard options
criteria = {
    "Durability": {
        "Weather resistance": ["Poor", "Fair", "Good", "Very Good", "Excellent"],
        "UV resistance": ["Poor", "Fair", "Good", "Very Good", "Excellent"],
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
        "Production (cradle to gate)": ["Very High", "High", "Moderate", "Low", "Very Low"],
        "End-of-life: Recycle": ["Never", "Rarely", "Sometimes", "Often", "Always"],
        "End-of-life: Reuse": ["Never", "Rarely", "Sometimes", "Often", "Always"],
        "End-of-life: Recovery": ["Never", "Rarely", "Sometimes", "Often", "Always"]
    }
}

# Material options
materials = ["Wood", "Hemp", "Rammed Earth", "Straw Bale"]
selected_material = st.selectbox("Select Material", materials)

# Track score and details
score_table = []
total_score = 0

# Collect user input and calculate weighted score
for factor, weight in factors.items():
    if factor in criteria:
        st.subheader(factor)
        for item, options in criteria[factor].items():
            selected_option = st.selectbox(f"{item}", options, key=f"{factor}_{item}")
            score = options.index(selected_option) + 1  # 1 to 5
            weighted = score * weight / 5  # normalize to 5-point scale
            score_table.append({
                "Factor": factor,
                "Item": item,
                "Selected Option": selected_option,
                "Score (1-5)": score,
                "Weight": weight,
                "Weighted Contribution": weighted
            })
            total_score += weighted

# Display final result
st.markdown(f"### ✅ Final Weighted Score for **{selected_material}**: **{total_score:.2f}**")

# Optional detailed table
if st.checkbox("Show Detailed Score Table"):
    df = pd.DataFrame(score_table)
    st.dataframe(df)
