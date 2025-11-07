"""
Hypothesis 3: Healthcare Access and Diabetes - COMPLETE
Module for creating ALL interactive visualizations related to healthcare access and diabetes risk.
Includes: Coverage indicators, income trends, access barriers, and individual conditions.
Note: BMI categories and condition counts have been moved to hypothesis_h5.py as they are pre-existing conditions.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Color Constants
PRIMARY = "#931A23"        # Your brand
SECONDARY = "#E8C6AE"      # Accent
GRID = "rgba(0, 0, 0, 0.08)"
CHART_COLORS = ['#D24C49', '#A64A47', '#931A23']


def create_healthcare_coverage_chart(df, income_level='$25k-$35k'):
    """
    Create subplots showing healthcare coverage indicators for a specific income level.
    Displays side-by-side comparison of healthcare coverage and cost barriers.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The diabetes dataset
    income_level : str
        One of: '< $10k', '$10k-$15k', '$15k-$20k', '$20k-$25k', 
                '$25k-$35k', '$35k-$50k', '$50k-$75k', '> $75k'
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Side-by-side bar chart
    """
    df = df.copy()
    df.columns = df.columns.str.lower()
    
    # Map income to labels
    income_mapping = {
        1: '< $10k',
        2: '$10k-$15k',
        3: '$15k-$20k',
        4: '$20k-$25k',
        5: '$25k-$35k',
        6: '$35k-$50k',
        7: '$50k-$75k',
        8: '> $75k'
    }
    
    df['income_label'] = df['income'].map(income_mapping)
    
    # Filter data for this income level
    income_data = df[df['income_label'] == income_level]
    
    # Healthcare Coverage
    coverage_df = income_data.groupby('anyhealthcare', observed=True)['diabetes_binary'].mean() * 100
    coverage_no = coverage_df.get(0, np.nan)
    coverage_yes = coverage_df.get(1, np.nan)
    
    # Cost Barriers
    cost_df = income_data.groupby('nodocbccost', observed=True)['diabetes_binary'].mean() * 100
    cost_no = cost_df.get(0, np.nan)
    cost_yes = cost_df.get(1, np.nan)
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Any Healthcare Coverage', 'Cost Barrier to Doctor in Past 12 Months'),
        horizontal_spacing=0.15
    )
    
    # Add trace for Healthcare Coverage
    fig.add_trace(go.Bar(
        x=['No', 'Yes'],
        y=[coverage_no, coverage_yes],
        marker=dict(color=["#E8C6AE", "#931A23"]),
        text=[f"{coverage_no:.1f}%" if not np.isnan(coverage_no) else "", 
              f"{coverage_yes:.1f}%" if not np.isnan(coverage_yes) else ""],
        textposition='outside',
        showlegend=False,
        hovertemplate='Response: %{x}<br>Diabetes Rate: %{y:.1f}%<extra></extra>',
    ), row=1, col=1)
    
    # Add trace for Cost Barriers
    fig.add_trace(go.Bar(
        x=['No', 'Yes'],
        y=[cost_no, cost_yes],
        marker=dict(color=["#E8C6AE", "#931A23"]),
        text=[f"{cost_no:.1f}%" if not np.isnan(cost_no) else "", 
              f"{cost_yes:.1f}%" if not np.isnan(cost_yes) else ""],
        textposition='outside',
        showlegend=False,
        hovertemplate='Response: %{x}<br>Diabetes Rate: %{y:.1f}%<extra></extra>',
    ), row=1, col=2)
    
    fig.update_xaxes(title_text="Response", row=1, col=1)
    fig.update_xaxes(title_text="Response", row=1, col=2)
    fig.update_yaxes(title_text="Diabetes Rate (%)", row=1, col=1, range=[0, 100])
    fig.update_yaxes(title_text="Diabetes Rate (%)", row=1, col=2, range=[0, 100])
    
    fig.update_layout(
        title_text=f"Diabetes Rate by Healthcare Access Barriers - {income_level} Income",
        height=500,
        barmode='group',
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='x unified',
        showlegend=False,
    )
    
    return fig


def create_income_trends_dual_chart(df):
    """
    Create side-by-side line charts showing:
    1. Diabetes rate by income level
    2. Percentage lacking healthcare coverage by income level
    """
    df = df.copy()
    df.columns = df.columns.str.lower()
    
    # Diabetes rate by income
    income_data = df.groupby('income')['diabetes_binary'].mean() * 100
    income_counts = df.groupby('income').size()
    
    income_df = pd.DataFrame({
        'Income Group': income_data.index.map({
            1: '< $10k', 2: '$10k-$15k', 3: '$15k-$20k', 4: '$20k-$25k',
            5: '$25k-$35k', 6: '$35k-$50k', 7: '$50k-$75k', 8: '> $75k'
        }),
        'Diabetes Rate (%)': income_data.values,
        'Count': income_counts.values
    })
    
    # No healthcare coverage by income
    no_coverage = df[df['anyhealthcare'] == 0]
    coverage_income_data = (
        no_coverage.groupby('income').size() / 
        df.groupby('income').size() * 100
    )
    total_counts = df.groupby('income').size()
    no_coverage_counts = no_coverage.groupby('income').size()
    
    coverage_df = pd.DataFrame({
        'Income Group': coverage_income_data.index.map({
            1: '< $10k', 2: '$10k-$15k', 3: '$15k-$20k', 4: '$20k-$25k',
            5: '$25k-$35k', 6: '$35k-$50k', 7: '$50k-$75k', 8: '> $75k'
        }),
        'No Coverage (%)': coverage_income_data.values,
        'Total Count': total_counts.values,
        'No Coverage Count': no_coverage_counts.values
    })
    
    # Create subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Diabetes Rate by Income', 'Lack of Healthcare Coverage by Income'),
        horizontal_spacing=0.12
    )
    
    # Left plot: Diabetes rate
    fig.add_trace(go.Scatter(
        x=income_df['Income Group'],
        y=income_df['Diabetes Rate (%)'],
        mode='lines+markers',
        name='Diabetes Rate',
        line=dict(color='#931A23', width=3),
        marker=dict(size=8, color='white', line=dict(color='#931A23', width=2)),
        text=[f"{val:.1f}%" for val in income_df['Diabetes Rate (%)']],
        textposition='top center',
        customdata=income_df[['Count']],
        hovertemplate='Income: %{x}<br>Diabetes Rate: %{y:.1f}%<br>Count: %{customdata[0]:,}<extra></extra>',
    ), row=1, col=1)
    
    # Right plot: No coverage
    fig.add_trace(go.Scatter(
        x=coverage_df['Income Group'],
        y=coverage_df['No Coverage (%)'],
        mode='lines+markers',
        name='No Coverage Rate',
        line=dict(color='#E8C6AE', width=3),
        marker=dict(size=8, color='white', line=dict(color='#E8C6AE', width=2)),
        text=[f"{val:.1f}%" for val in coverage_df['No Coverage (%)']],
        textposition='top center',
        customdata=np.column_stack((
            coverage_df['No Coverage (%)'].values,
            coverage_df['No Coverage Count'].values,
            coverage_df['Total Count'].values
        )),
        hovertemplate='Income: %{x}<br>No Coverage: %{y:.1f}%<br>Uninsured: %{customdata[1]:,}<br>Total: %{customdata[2]:,}<extra></extra>',
        showlegend=False
    ), row=1, col=2)
    
    fig.update_xaxes(title_text="Income Group", row=1, col=1)
    fig.update_xaxes(title_text="Income Group", row=1, col=2)
    fig.update_yaxes(title_text="Diabetes Rate (%)", row=1, col=1, range=[0, 100])
    fig.update_yaxes(title_text="No Coverage (%)", row=1, col=2, range=[0, 100])
    
    fig.update_layout(
        title_text="Income Level: Relationship with Diabetes and Healthcare Coverage",
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='x unified',
    )
    
    return fig


def create_income_trends_dual_chart(df):
    """
    Create side-by-side line charts showing:
    1. Diabetes rate by income level
    2. Percentage lacking healthcare coverage by income level
    """
    df = df.copy()
    df.columns = df.columns.str.lower()
    
    # Diabetes rate by income
    income_data = df.groupby('income')['diabetes_binary'].mean() * 100
    income_counts = df.groupby('income').size()
    
    income_df = pd.DataFrame({
        'Income Group': income_data.index.map({
            1: '< $10k', 2: '$10k-$15k', 3: '$15k-$20k', 4: '$20k-$25k',
            5: '$25k-$35k', 6: '$35k-$50k', 7: '$50k-$75k', 8: '> $75k'
        }),
        'Diabetes Rate (%)': income_data.values,
        'Count': income_counts.values
    })
    
    # No healthcare coverage by income
    no_coverage = df[df['anyhealthcare'] == 0]
    coverage_income_data = (
        no_coverage.groupby('income').size() / 
        df.groupby('income').size() * 100
    )
    total_counts = df.groupby('income').size()
    no_coverage_counts = no_coverage.groupby('income').size()
    
    coverage_df = pd.DataFrame({
        'Income Group': coverage_income_data.index.map({
            1: '< $10k', 2: '$10k-$15k', 3: '$15k-$20k', 4: '$20k-$25k',
            5: '$25k-$35k', 6: '$35k-$50k', 7: '$50k-$75k', 8: '> $75k'
        }),
        'No Coverage (%)': coverage_income_data.values,
        'Total Count': total_counts.values,
        'No Coverage Count': no_coverage_counts.values
    })
    
    # Create subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Diabetes Rate by Income', 'Lack of Healthcare Coverage by Income'),
        horizontal_spacing=0.12
    )
    
    # Left plot: Diabetes rate
    fig.add_trace(go.Scatter(
        x=income_df['Income Group'],
        y=income_df['Diabetes Rate (%)'],
        mode='lines+markers',
        name='Diabetes Rate',
        line=dict(color='#931A23', width=3),
        marker=dict(size=8, color='white', line=dict(color='#931A23', width=2)),
        text=[f"{val:.1f}%" for val in income_df['Diabetes Rate (%)']],
        textposition='top center',
        customdata=income_df[['Count']],
        hovertemplate='Income: %{x}<br>Diabetes Rate: %{y:.1f}%<br>Count: %{customdata[0]:,}<extra></extra>',
    ), row=1, col=1)
    
    # Right plot: No coverage
    fig.add_trace(go.Scatter(
        x=coverage_df['Income Group'],
        y=coverage_df['No Coverage (%)'],
        mode='lines+markers',
        name='No Coverage Rate',
        line=dict(color='#E8C6AE', width=3),
        marker=dict(size=8, color='white', line=dict(color='#E8C6AE', width=2)),
        text=[f"{val:.1f}%" for val in coverage_df['No Coverage (%)']],
        textposition='top center',
        customdata=np.column_stack((
            coverage_df['No Coverage (%)'].values,
            coverage_df['No Coverage Count'].values,
            coverage_df['Total Count'].values
        )),
        hovertemplate='Income: %{x}<br>No Coverage: %{y:.1f}%<br>Uninsured: %{customdata[1]:,}<br>Total: %{customdata[2]:,}<extra></extra>',
        showlegend=False
    ), row=1, col=2)
    
    fig.update_xaxes(title_text="Income Group", row=1, col=1)
    fig.update_xaxes(title_text="Income Group", row=1, col=2)
    fig.update_yaxes(title_text="Diabetes Rate (%)", row=1, col=1, range=[0, 100])
    fig.update_yaxes(title_text="No Coverage (%)", row=1, col=2, range=[0, 100])
    
    fig.update_layout(
        title_text="Income Level: Relationship with Diabetes and Healthcare Coverage",
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='x unified',
    )
    
    return fig


def create_access_barriers_chart(df):
    """Create bar chart showing cumulative effect of access barriers."""
    df = df.copy()
    df.columns = df.columns.str.lower()
    
    # Create barriers variable (0, 1, or 2)
    df['barriers_count'] = 0
    df.loc[df['nodocbccost'] == 1, 'barriers_count'] += 1
    df.loc[df['anyhealthcare'] == 0, 'barriers_count'] += 1
    
    barriers_data = df.groupby('barriers_count')['diabetes_binary'].mean() * 100
    barriers_counts = df.groupby('barriers_count').size()
    
    barrier_labels = {
        0: 'No Barriers',
        1: '1 Barrier',
        2: '2 Barriers'
    }
    
    barriers_df = pd.DataFrame({
        'Barriers': [barrier_labels[i] for i in barriers_data.index],
        'Diabetes Rate (%)': barriers_data.values,
        'Count': barriers_counts.values
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=barriers_df['Barriers'],
        y=barriers_df['Diabetes Rate (%)'],
        marker=dict(color=CHART_COLORS),
        text=[f"{val:.1f}%" for val in barriers_df['Diabetes Rate (%)']],
        textposition='outside',
        customdata=barriers_df[['Count']],
        hovertemplate='%{x}<br>Diabetes Rate: %{y:.1f}%<br>Count: %{customdata[0]:,}<extra></extra>',
    ))
    
    fig.update_layout(
        title="Cumulative Effect of Healthcare Access Barriers",
        xaxis_title="Number of Access Barriers",
        yaxis_title="Diabetes Rate (%)",
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white',
    )
    
    fig.update_yaxes(range=[0, 100])
    
    return fig