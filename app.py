import plotly.graph_objects as go

# Display radar chart if requested
if st.checkbox("Show Radar Chart of Factor Scores"):
    if score_table:
        radar_scores = []
        factor_labels = []

        for factor in factors:
            scores = [entry["Score"] for entry in score_table if entry["Factor"] == factor]
            avg_score = sum(scores) / len(scores)
            normalized = avg_score * 100 / 7  # normalize to 0–100
            radar_scores.append(normalized)
            factor_labels.append(factor)

        # Close the radar chart loop
        radar_scores.append(radar_scores[0])
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
    else:
        st.warning("Please evaluate at least one material first.")
