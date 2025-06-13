
import streamlit as st
import pandas as pd

# Define the factors and their weights
factors = {
    "Durability": 19.13,
    "Cost Effectiveness": 19.29,
    "Buildability": 17.79,
    "Embodied Carbon": 15.71,
    "Availability": 14.41,
    "Aesthetics": 13.66
}

# Define the materials and placeholder SWOT scores for each factor (user will input these)
materials = ["Wood", "Hemp", "Rammed Earth", "Straw Bale"]

st.title("Zero-Carbon Building Material Decision Tool")
st.markdown("### Evaluate materials based on six weighted factors.")

selected_material = st.selectbox("Choose a material to evaluate:", materials)

scores = {}
st.markdown("#### Enter scores (1 to 5) for each factor:")

for factor in factors:
    scores[factor] = st.slider(factor, 1, 5, 3)

# Calculate final weighted score
weighted_score = sum(scores[factor] * weight for factor, weight in factors.items()) / 100

st.markdown(f"### Final Weighted Score for {selected_material}: {weighted_score:.2f}")

# Optionally display a table of scores
if st.checkbox("Show Score Breakdown"):
    score_df = pd.DataFrame({
        "Factor": list(factors.keys()),
        "Weight": list(factors.values()),
        "User Score": [scores[f] for f in factors],
        "Weighted Score": [scores[f] * factors[f] / 100 for f in factors]
    })
    st.dataframe(score_df)
