import plotly.express as px
import plotly.graph_objects as go

# Function to plot feature values distribution
def plot_feature_importance(input_values, feature_names):
    fig = px.bar(
        x=feature_names,
        y=input_values,
        labels={'x': 'Telemetry Metrics', 'y': 'Assigned Value'},
        template="plotly_dark"
    )
    fig.update_traces(
        marker_color='#00b4d8',
        marker_line_color='#64ffda',
        marker_line_width=1.5,
        opacity=0.85
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#8892b0",
        margin=dict(l=10, r=10, t=10, b=10),
        height=300,
        xaxis_tickangle=-40,
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)')
    )
    return fig

# Function to generate high-tech radar signature chart
def plot_radar_chart(input_values, feature_names, ranges):
    # Normalize input values to 0-100 based on standard ranges
    normalized_values = []
    for val, name in zip(input_values, feature_names):
        r_min, r_max = ranges[name]["range"]
        if r_max == r_min:
            norm = 50.0
        else:
            norm = ((val - r_min) / (r_max - r_min)) * 100
        normalized_values.append(norm)
    
    # Close the polygon loop for radar plots
    categories = feature_names + [feature_names[0]]
    values = normalized_values + [normalized_values[0]]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(100, 255, 218, 0.15)',
        line=dict(color='#64ffda', width=2),
        name='Planetary Metrics Signature'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                color="#8892b0",
                gridcolor="rgba(255, 255, 255, 0.05)",
                linecolor="rgba(255, 255, 255, 0.05)",
                tickfont=dict(size=8)
            ),
            angularaxis=dict(
                color="#8892b0",
                gridcolor="rgba(255, 255, 255, 0.05)",
                tickfont=dict(size=9)
            ),
            bgcolor="rgba(0,0,0,0)"
        ),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=55, r=55, t=20, b=20),
        height=300
    )
    return fig
