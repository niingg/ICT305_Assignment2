"""
Hypothesis 4: Self-Rated Health and Diabetes - COMPLETE
Module for creating ALL interactive visualizations related to self-rated health and diabetes risk.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Color Constants
PRIMARY = "#931A23"        # Your brand
SECONDARY = "#E8C6AE"      # Accent
GRID = "rgba(0, 0, 0, 0.08)"

def create_health_trends_chart(df):
    """
    Create a dual-axis chart showing diabetes rates vs unhealthy days trends.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The diabetes dataset
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Dual-axis line chart
    """
    df = df.copy()
    df.columns = df.columns.str.lower()
    
    grouped_df = df.groupby('genhlth').agg({
        'diabetes_binary': 'mean',
        'menthlth': 'mean',
        'physhlth': 'mean'
    }) * 100
    grouped_df.index.name = 'General Health'
    
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Diabetes rate (primary y-axis)
    fig.add_trace(go.Scatter(
        x=grouped_df.index,
        y=grouped_df['diabetes_binary'],
        name='Diabetes Rate (%)',
        line=dict(color="#FBE35A", width=4),
        fill='tozeroy',
        fillcolor='rgba(251,227,90, 0.4)',
        mode='lines+markers',
        marker=dict(size=8),
    ), secondary_y=False)
    
    # Mental unhealthy days (secondary y-axis)
    fig.add_trace(go.Scatter(
        x=grouped_df.index,
        y=grouped_df['menthlth'],
        name='Mental Unhealthy Days',
        line=dict(color="#931A23", width=4),
        fill='tozeroy',
        fillcolor='rgba(147,26,35, 0.4)',
        mode='lines+markers',
        marker=dict(size=8),
    ), secondary_y=True)
    
    # Physical unhealthy days (secondary y-axis)
    fig.add_trace(go.Scatter(
        x=grouped_df.index,
        y=grouped_df['physhlth'],
        name='Physical Unhealthy Days',
        line=dict(color="#E8C6AE", width=4),
        fill='tozeroy',
        fillcolor='rgba(232,198,174, 0.4)',
        mode='lines+markers',
        marker=dict(size=8),
    ), secondary_y=True)
    
    # Update layout
    fig.update_layout(
        title="Health Metrics Trends by General Health Rating",
        xaxis=dict(title="General Health Rating (1=Excellent, 5=Poor)"),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=500,
        hovermode='x unified',
    )
    
    # Set y-axes titles
    fig.update_yaxes(
        title_text="Diabetes Rate (%)",
        titlefont=dict(color="#FBE35A"),
        tickfont=dict(color="#FBE35A"),
        showgrid=False,
        secondary_y=False
    )
    
    fig.update_yaxes(
        title_text="Average Days (per month)",
        titlefont=dict(color="#931A23"),
        tickfont=dict(color="#931A23"),
        showgrid=False,
        secondary_y=True
    )
    
    return fig


def create_functional_limitations_comparison_chart(df):
    """
    Create subplots comparing difficulty walking and physical activity.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The diabetes dataset
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Subplots with difficulty walking and physical activity
    """
    df = df.copy()
    df.columns = df.columns.str.lower()
    
    # Difficulty walking
    diffwalk_data = df.groupby('diffwalk')['diabetes_binary'].mean() * 100
    diffwalk_counts = df.groupby('diffwalk').size()
    diffwalk_df = pd.DataFrame({
        'Response': ['No Difficulty', 'Difficulty'],
        'Diabetes Rate (%)': diffwalk_data.values,
        'Count': diffwalk_counts.values
    })
    diffwalk_no = diffwalk_df[diffwalk_df['Response'] == 'No Difficulty']
    diffwalk_yes = diffwalk_df[diffwalk_df['Response'] == 'Difficulty']
    
    # Physical activity
    physactivity_data = df.groupby('physactivity')['diabetes_binary'].mean() * 100
    physactivity_counts = df.groupby('physactivity').size()
    physactivity_df = pd.DataFrame({
        'Response': ['No Activity', 'Has Activity'],
        'Diabetes Rate (%)': physactivity_data.values,
        'Count': physactivity_counts.values
    })
    physactivity_no = physactivity_df[physactivity_df['Response'] == 'No Activity']
    physactivity_yes = physactivity_df[physactivity_df['Response'] == 'Has Activity']
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Difficulty Walking', 'Physical Activity in the Past Month'),
        horizontal_spacing=0.15
    )
    
    # Difficulty walking - No
    fig.add_trace(go.Bar(
        x=diffwalk_no['Response'],
        y=diffwalk_no['Diabetes Rate (%)'],
        name='No Difficulty',
        marker=dict(color="#E8C6AE", line=dict(color='white', width=2)),
        text=[f"{val:.1f}%" for val in diffwalk_no['Diabetes Rate (%)']],
        textposition='outside',
        customdata=diffwalk_no[['Count']],
        hovertemplate='%{x}<br>Diabetes Rate: %{y:.1f}%<br>Count: %{customdata[0]:,}<extra></extra>',
        legendgroup='diffwalk',
        showlegend=True,
    ), row=1, col=1)
    
    # Difficulty walking - Yes
    fig.add_trace(go.Bar(
        x=diffwalk_yes['Response'],
        y=diffwalk_yes['Diabetes Rate (%)'],
        name='Has Difficulty',
        marker=dict(color="#931A23", line=dict(color='white', width=2)),
        text=[f"{val:.1f}%" for val in diffwalk_yes['Diabetes Rate (%)']],
        textposition='outside',
        customdata=diffwalk_yes[['Count']],
        hovertemplate='%{x}<br>Diabetes Rate: %{y:.1f}%<br>Count: %{customdata[0]:,}<extra></extra>',
        legendgroup='diffwalk',
        showlegend=False,
    ), row=1, col=1)
    
    # Physical activity - No
    fig.add_trace(go.Bar(
        x=physactivity_no['Response'],
        y=physactivity_no['Diabetes Rate (%)'],
        name='No',
        marker=dict(color="#E8C6AE", line=dict(color='white', width=2)),
        text=[f"{val:.1f}%" for val in physactivity_no['Diabetes Rate (%)']],
        textposition='outside',
        customdata=physactivity_no[['Count']],
        hovertemplate='%{x}<br>Diabetes Rate: %{y:.1f}%<br>Count: %{customdata[0]:,}<extra></extra>',
        legendgroup='physactivity',
        showlegend=False,
    ), row=1, col=2)
    
    # Physical activity - Yes
    fig.add_trace(go.Bar(
        x=physactivity_yes['Response'],
        y=physactivity_yes['Diabetes Rate (%)'],
        name='Yes',
        marker=dict(color="#931A23", line=dict(color='white', width=2)),
        text=[f"{val:.1f}%" for val in physactivity_yes['Diabetes Rate (%)']],
        textposition='outside',
        customdata=physactivity_yes[['Count']],
        hovertemplate='%{x}<br>Diabetes Rate: %{y:.1f}%<br>Count: %{customdata[0]:,}<extra></extra>',
        legendgroup='physactivity',
        showlegend=False,
    ), row=1, col=2)
    
    fig.update_yaxes(title_text="Diabetes Rate (%)", row=1, col=1)
    fig.update_yaxes(title_text="Diabetes Rate (%)", row=1, col=2)
    fig.update_yaxes(range=[0, 100], row=1, col=1)
    fig.update_yaxes(range=[0, 100], row=1, col=2)
    
    fig.update_layout(
        title_text="Functional Limitations and Diabetes Rate",
        height=500,
        barmode='group',
        plot_bgcolor='white',
        paper_bgcolor='white',
    )
    
    return fig


def create_functional_limitations_chart(df):
    """
    Create a bar chart showing diabetes rates by number of functional limitations.
    Counts: Physical Activity, General Health, Mental Health, Physical Health, Difficulty Walking
    Creates a composite score from 0-5 limitations.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The diabetes dataset
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Bar chart of diabetes rates by limitation count (0-5)
    """
    df = df.copy()
    df.columns = df.columns.str.lower()
    
    # Create composite limitation score (0-5)
    # Count limitations based on:
    # 1. No physical activity (physactivity == 0)
    # 2. Poor general health (genhlth >= 4, where 5 is worst)
    # 3. Mental health days (menthlth > 0)
    # 4. Physical health days (physhlth > 0)
    # 5. Difficulty walking (diffwalk == 1)
    
    df['limitation_count'] = 0
    
    # Physical activity limitation
    if 'physactivity' in df.columns:
        df.loc[df['physactivity'] == 0, 'limitation_count'] += 1
    
    # General health limitation
    if 'genhlth' in df.columns:
        df.loc[df['genhlth'] >= 4, 'limitation_count'] += 1
    
    # Mental health limitation
    if 'menthlth' in df.columns:
        df.loc[df['menthlth'] > 0, 'limitation_count'] += 1
    
    # Physical health limitation
    if 'physhlth' in df.columns:
        df.loc[df['physhlth'] > 0, 'limitation_count'] += 1
    
    # Difficulty walking limitation
    if 'diffwalk' in df.columns:
        df.loc[df['diffwalk'] == 1, 'limitation_count'] += 1
    
    limit_data = df.groupby('limitation_count')['diabetes_binary'].mean() * 100
    limit_counts = df.groupby('limitation_count').size()
    
    limit_labels = {
        0: 'No Other Limitations',
        1: '1 Limitations',
        2: '2 Limitations',
        3: '3 Limitations',
        4: '4 Limitations',
        5: '5 Limitations'
    }
    
    limit_df = pd.DataFrame({
        'Limitations': [limit_labels.get(i, f'{i} Limitations') for i in range(6)],
        'Diabetes Rate (%)': [limit_data.get(i, 0) for i in range(6)],
        'Count': [limit_counts.get(i, 0) for i in range(6)]
    })
    
    fig = go.Figure()
    
    # Color gradient from yellow to dark red
    colors = ["#FFF1A4", '#EEC8A3', '#DD9C7C', '#D24C49', '#A64A47', '#931A23']
    
    for i, (idx, row) in enumerate(limit_df.iterrows()):
        fig.add_trace(go.Bar(
            x=[row['Limitations']],
            y=[row['Diabetes Rate (%)']],
            name=row['Limitations'],
            marker=dict(color=colors[i]),
            text=[f"{row['Diabetes Rate (%)']:.1f}%"],
            textposition='outside',
            customdata=[[row['Count']]],
            hovertemplate='<b>%{x}</b><br>Diabetes Rate: %{y:.1f}%<br>Count: %{customdata[0][0]:,}<extra></extra>',
            showlegend=False,
        ))
    
    fig.update_layout(
        title="Diabetes Rate by No. of Pre-Existing Limitations",
        xaxis_title="No. of Pre-Existing Conditions<br>(Physical Activity, General Health, Mental Health, Physical Health, Difficulty Walking)",
        yaxis_title="Diabetes Rate (%)",
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='x unified',
        legend=dict(
            title='Number of Conditions',
            orientation='v',
            yanchor='top',
            y=1,
            xanchor='left',
            x=1.02
        )
    )
    
    fig.update_yaxes(range=[0, 100])
    
    return fig