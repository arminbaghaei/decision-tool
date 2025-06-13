import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Factors and their weights
factors = {
    "Durability": 19.13,
    "Cost Effectiveness": 19.29,
    "Buildability": 17.79,
    "Embodied Carbon": 15.71,
    "Availability": 14.41,
    "Aesthetics": 13.66
}

# SWOT parameters per factor
swot_criteria = {
    "Durability": [
        "UV/moisture resistance",
        "Service life",
        "Maintenance frequency",
        "Resilience under weather"
    ],
    "Cost Effectiveness": [
        "Maintenance savings",
        "Upfront cost",
        "Financial incentives",
        "Price volatility"
    ],
    "Buildability": [
        "Ease of handling",
        "Tools required",
        "Training available",
        "Retrofit compatibility"
    ],
    "Embodied Carbon": [
        "Low impact manufacturing",
        "Supply chain emissions",
        "Carbon certification",
        "Greenwashing risk"
    ],
    "Availability": [
        "Local supply chains",
        "Transport costs",
        "Production scalability",
        "Material scarcity"
    ],
    "Aesthetics": [
        "Visual appeal",
        "Finish options",
        "Design adaptability",
        "Style bias"
    ]
}

# List of materials
materials = ["Wood", "Hemp", "Rammed Earth", "Straw Bale"]

# App title
st.title("Zero-Carbon Material Selection Tool (SWOT-Based)")

# Material selector
selected_material = st.selectbox("Select Material:", materials)

# Score tracking
total_score = 0
score_table = []

# Input loop: scores per SWOT item under each factor
for factor, weight in factors.items():
    st.subheader(factor)
    factor_score = 0
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**SWOT Parameters**")
    with col2:
        st.markdown("**Score (1–7)**")
    
    for criterion in swot_criteria[factor]:
        score = st.slider(f"{criterion}", 1, 7, 1, key=f"{selected_material}_{factor}_{criterion}")
        factor_score += score
        score_table.append({
            "Factor": factor,
            "SWOT Item": criterion,
            "Score": score,
            "Weight": weight
        })
    
    # Calculate weighted contribution per factor
    average_factor_score = factor_score / len(swot_criteria[factor])
    weighted_factor_score = average_factor_score * weight / 7
    total_score += weighted_factor_score

# Show total score
st.markdown(f"## Final Weighted Score for {selected_material}: {total_score:.2f}")

# Optional: Display score table
if st.checkbox("Show Detailed SWOT Score Table"):
    df = pd.DataFrame(score_table)
    df["Weighted Contribution"] = df["Score"] * df["Weight"] / 7
    st.dataframe(df)

# Optional: Radar Chart
if score_table and st.checkbox("Show Radar Chart of Factor Scores"):
    radar_scores = []
    factor_labels = []

    for factor in factors:
        scores = [entry["Score"] for entry in score_table if entry["Factor"] == factor]
        avg_score = sum(scores) / len(scores)
        normalized = avg_score * 100 / 7  # scale to 0–100
        radar_scores.append(normalized)
        factor_labels.append(factor)

    radar_scores.append(radar_scores[0])     # loop closure
    factor_labels.append(factor_labels[0])   # loop closure

    fig = go.Figure(data=go.Scatterpolar(
        r=radar_scores,
        theta=factor_labels,
        fill='toself',
        name=selected_material
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title=f"Performance Radar Chart for {selected_material}"
    )
    st.plotly_chart(fig)
