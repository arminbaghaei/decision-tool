import plotly.graph_objects as go

# Radar chart of final factor scores (normalized to 0–100 for clarity)
if st.checkbox("Show Radar Chart of Factor Scores"):
    radar_scores = []
    factor_labels = []
    
    for factor in factors:
        # Get average score per factor (1–7)
        scores = [entry["Score"] for entry in score_table if entry["Factor"] == factor]
        avg_score = sum(scores) / len(scores)
        normalized = avg_score * 100 / 7  # scale to 0–100 for radar clarity
        radar_scores.append(normalized)
        factor_labels.append(factor)

    radar_scores.append(radar_scores[0])  # to close the loop in radar
    factor_labels.append(factor_labels[0])

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
