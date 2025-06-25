import streamlit as st
import pandas as pd

# Factor weights
factors = {
    "Durability": 19.13,
    "Cost Effectiveness": 19.29,
    "Buildability": 17.79,
    "Embodied Carbon": 15.71,
    "Availability": 14.41,
    "Aesthetics": 13.66
}

# Predefined criteria and 5-point qualitative scales
criteria = {
    "Durability": {
        "Weather resistance": ["Poor", "Fair", "Good", "Very Good", "Excellent"],
        "UV resistance": ["Poor", "Fair", "Good", "Very Good", "Excellent"],
        "Service life": ["20 years", "30 years", "50 years", "100 years", "Over 100 years"],
        "Maintenance frequency": ["Every 10 yrs", "Every 20 yrs", "Every 30 yrs", "Every 50 yrs", "Over 50 yrs"]
    },
    "Cost Effectiveness": {
        "Maintenance cost": ["Very High", "High", "Moderate", "Low", "Very Low"],
        "Upfront material cost": ["Very High", "High", "Moderate", "Low", "Very Low"],
        "Financial incentives": ["None", "Low", "Moderate", "High", "Very High"]
    },
    "Buildability": {
        "Ease of handling": ["Very Difficult", "Difficult", "Moderate", "Easy", "Very Easy"],
        "Specialist equipment required": ["Extensive", "High", "Moderate", "Low", "None"],
        "Expertise availability": ["Rare", "Limited", "Some", "Common", "Very Common"],
        "Compatibility with materials": ["1", "2", "3", "4", "5"]  # Number of compatible materials
    },
    "Embodied Carbon": {
        "Production (cradle to gate)": ["Very High", "High", "Moderate", "Low", "Very Low"],
        "End-of-life: Recycle": ["Never", "Rarely", "Sometimes", "Often", "Always"],
        "End-of-life: Reuse": ["Never", "Rarely", "Sometimes", "Often", "Always"],
        "End-of-life: Recovery": ["Never", "Rarely", "Sometimes", "Often", "Always"]
    }
}

# Optional: material selection
materials = ["Wood", "Hemp", "Rammed Earth", "Straw Bale"]
selected_material = st.selectbox("Select Material", materials)

# Score tracker
total_score = 0
score_table = []

# User input section
for factor, weight in factors.items():
    if factor in criteria:
        st.subheader(factor)
        for item, options in criteria[factor].items():
            choice = st.selectbox(f"{item}", options, key=f"{factor}_{item}")
            score = options.index(choice) + 1  # Convert to 1–5 scale
            score_table.append({
                "Factor": factor,
                "Item": item,
                "Option": choice,
                "Score": score,
                "Weight": weight
            })

# Create DataFrame and compute weighted total
df = pd.DataFrame(score_table)
df["Weighted Contribution"] = df["Score"] * df["Weight"] / 5
total_score = df["Weighted Contribution"].sum()

# Display results
st.markdown(f"### Final Weighted Score for {selected_material}: **{total_score:.2f}**")
if st.checkbox("Show Detailed Table"):
    st.dataframe(df)
