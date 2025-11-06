"""
Hypothesis 5: Pre-existing Health Conditions and Diabetes
Module for creating interactive visualizations related to pre-existing cardiometabolic conditions and diabetes risk.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go


def create_preexisting_conditions_chart(df):
    """
    Create an interactive chart showing diabetes rates and relative risk for individual pre-existing conditions.
    Dropdown allows switching between:
    - Prevalence: Diabetes rate for each condition (Yes vs No)
    - Relative Risk: Ratio of diabetes rate (Yes/No) for each condition
    
    Conditions analyzed: Stroke, Heart Disease, High Blood Pressure, High Cholesterol
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The diabetes dataset
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Interactive figure with dropdown to switch between sorting methods
    """
    df = df.copy()
    df.columns = df.columns.str.lower()
    
    conditions = {
        'High Blood Pressure': 'highbp',
        'High Cholesterol': 'highchol',
        'Heart Disease': 'heartdiseaseorattack',
        'Stroke': 'stroke'
    }
    
    # Calculate prevalence and relative risk for each condition
    prevalence_data = []
    relative_risk_data = []
    
    for condition_name, condition_col in conditions.items():
        # Calculate diabetes rate for Yes and No
        no_rate = df[df[condition_col] == 0]['diabetes_binary'].mean() * 100
        yes_rate = df[df[condition_col] == 1]['diabetes_binary'].mean() * 100
        
        # Calculate relative risk (ratio of yes rate to no rate)
        relative_risk = yes_rate / no_rate if no_rate > 0 else 1.0
        
        prevalence_data.append({
            'Condition': condition_name,
            'No Rate': no_rate,
            'Yes Rate': yes_rate,
            'Relative Risk': relative_risk
        })
        
        relative_risk_data.append({
            'Condition': condition_name,
            'No Rate': no_rate,
            'Yes Rate': yes_rate,
            'Relative Risk': relative_risk
        })
    
    prev_df = pd.DataFrame(prevalence_data).sort_values('Yes Rate', ascending=False)
    risk_df = pd.DataFrame(relative_risk_data).sort_values('Relative Risk', ascending=False)
    
    # Create figure
    fig = go.Figure()
    
    # Trace 1: Prevalence sorted (default - visible)
    for i, row in prev_df.iterrows():
        # No group (light tan)
        fig.add_trace(go.Bar(
            x=[row['Condition']],
            y=[row['No Rate']],
            name='No',
            marker=dict(color='#E8C6AE'),
            text=[f"{row['No Rate']:.1f}"],
            textposition='outside',
            legendgroup='Prevalence_No',
            showlegend=(row['Condition'] == prev_df.iloc[0]['Condition']),
            visible=True,
            hovertemplate='<b>%{x}</b><br>No Condition: %{y:.1f}%<extra></extra>',
        ))
        
        # Yes group (dark red)
        fig.add_trace(go.Bar(
            x=[row['Condition']],
            y=[row['Yes Rate']],
            name='Yes',
            marker=dict(color='#931A23'),
            text=[f"{row['Yes Rate']:.1f}"],
            textposition='outside',
            legendgroup='Prevalence_Yes',
            showlegend=(row['Condition'] == prev_df.iloc[0]['Condition']),
            visible=True,
            hovertemplate='<b>%{x}</b><br>Has Condition: %{y:.1f}%<extra></extra>',
        ))
    
    # Trace 2: Relative Risk sorted (hidden - will show with dropdown)
    for i, row in risk_df.iterrows():
        # No group (light tan)
        fig.add_trace(go.Bar(
            x=[row['Condition']],
            y=[row['No Rate']],
            name='No',
            marker=dict(color='#E8C6AE'),
            text=[f"{row['No Rate']:.1f}"],
            textposition='outside',
            legendgroup='Risk_No',
            showlegend=False,
            visible=False,
            hovertemplate='<b>%{x}</b><br>No Condition: %{y:.1f}%<br>Relative Risk: %{customdata[0]:.2f}x<extra></extra>',
            customdata=[[row['Relative Risk']]],
        ))
        
        # Yes group (dark red)
        fig.add_trace(go.Bar(
            x=[row['Condition']],
            y=[row['Yes Rate']],
            name='Yes',
            marker=dict(color='#931A23'),
            text=[f"{row['Yes Rate']:.1f}"],
            textposition='outside',
            legendgroup='Risk_Yes',
            showlegend=False,
            visible=False,
            hovertemplate='<b>%{x}</b><br>Has Condition: %{y:.1f}%<br>Relative Risk: %{customdata[0]:.2f}x<extra></extra>',
            customdata=[[row['Relative Risk']]],
        ))
    
    # Create dropdown menu
    fig.update_layout(
        updatemenus=[dict(
            active=0,
            buttons=[
                dict(
                    label='Sort by Prevalence',
                    method='update',
                    args=[
                        {'visible': [True] * 8 + [False] * 8},
                        {'title': 'Effect of Pre-Existing Factors on Diabetes Rates',
                         'xaxis.title': 'Pre-Existing Factors'}
                    ]
                ),
                dict(
                    label='Sort by Relative Risk',
                    method='update',
                    args=[
                        {'visible': [False] * 8 + [True] * 8},
                        {'title': 'Effect of Pre-Existing Factors on Diabetes Rates (Sorted by Relative Risk)',
                         'xaxis.title': 'Pre-Existing Factors'}
                    ]
                )
            ],
            direction='down',
            pad={'r': 10, 't': 10},
            showactive=True,
            x=0.12,
            xanchor='left',
            y=1.15,
            yanchor='top'
        )],
        title_text="Effect of Pre-Existing Factors on Diabetes Rates",
        height=500,
        barmode='group',
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='x unified',
        legend=dict(
            orientation='v',
            yanchor='top',
            y=1,
            xanchor='right',
            x=1.02
        )
    )
    
    fig.update_xaxes(title_text="Pre-Existing Factors")
    fig.update_yaxes(title_text="Diabetes Rate (%)", range=[0, 100])
    
    return fig


def create_bmi_categories_chart(df):
    """
    Create a bar chart showing diabetes rates by BMI category.
    
    BMI Categories:
    - Underweight: < 18.5
    - Healthy: 18.5 - 25
    - Overweight: 25 - 30
    - Class 1 Obesity: 30 - 35
    - Class 2 Obesity: 35 - 40
    - Class 3 Obesity: > 40
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The diabetes dataset with bmi column
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Bar chart of diabetes rates by BMI category
    """
    df = df.copy()
    df.columns = df.columns.str.lower()
    
    # Create BMI categories
    df['bmi_class'] = 0
    df.loc[df['bmi'] < 18.5, 'bmi_class'] = 0
    df.loc[(df['bmi'] >= 18.5) & (df['bmi'] < 25), 'bmi_class'] = 1
    df.loc[(df['bmi'] >= 25) & (df['bmi'] < 30), 'bmi_class'] = 2
    df.loc[(df['bmi'] >= 30) & (df['bmi'] < 35), 'bmi_class'] = 3
    df.loc[(df['bmi'] >= 35) & (df['bmi'] < 40), 'bmi_class'] = 4
    df.loc[(df['bmi'] >= 40), 'bmi_class'] = 5
    
    # Calculate data
    bmi_data = df.groupby('bmi_class')['diabetes_binary'].mean() * 100
    bmi_counts = df.groupby('bmi_class').size()
    
    bmi_df = pd.DataFrame({
        'Category': bmi_data.index.map({
            0: 'Underweight (<18.5)',
            1: 'Healthy (18.5-25)',
            2: 'Overweight (25-30)',
            3: 'Class 1 Obesity (30-35)',
            4: 'Class 2 Obesity (35-40)',
            5: 'Class 3 Obesity (>40)'
        }),
        'Diabetes Rate (%)': bmi_data.values,
        'Count': bmi_counts.values
    })
    
    category_order = [
        'Underweight (<18.5)',
        'Healthy (18.5-25)',
        'Overweight (25-30)',
        'Class 1 Obesity (30-35)',
        'Class 2 Obesity (35-40)',
        'Class 3 Obesity (>40)'
    ]
    
    bmi_df['Category'] = pd.Categorical(bmi_df['Category'], categories=category_order, ordered=True)
    bmi_df = bmi_df.sort_values('Category')
    
    fig = go.Figure()
    
    # Color gradient: yellow to dark red
    colors = ["#FFF1A4", '#EEC8A3', '#DD9C7C', '#D24C49', '#A64A47', '#931A23']
    
    for i, (idx, row) in enumerate(bmi_df.iterrows()):
        fig.add_trace(go.Bar(
            x=[row['Category']],
            y=[row['Diabetes Rate (%)']],
            name=row['Category'],
            marker=dict(color=colors[i]),
            text=[f"{row['Diabetes Rate (%)']:.1f}"],
            textposition='outside',
            textfont=dict(size=11),
            customdata=[[row['Category'], row['Diabetes Rate (%)'], row['Count']]],
            hovertemplate='<b>%{customdata[0]}</b><br>Diabetes Rate (%): %{customdata[1]:.1f}<br>Count: %{customdata[2]:,}<extra></extra>',
            showlegend=True,
        ))
    
    fig.update_layout(
        title=dict(
            text='Diabetes Rate by BMI Category',
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title='Adult BMI Categories (USA)',
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='black',
            ticks='outside',
            ticklen=5,
            tickwidth=1,
            tickcolor='black',
            tickangle=0,
            categoryorder='array',
            categoryarray=category_order
        ),
        yaxis=dict(
            title='Diabetes Rate (%)',
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='black',
            ticks='outside',
            ticklen=5,
            tickwidth=1,
            tickcolor='black'
        ),
        height=700,
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='closest',
        legend=dict(
            title='BMI Category',
            orientation='v',
            yanchor='top',
            y=1,
            xanchor='left',
            x=1.02
        )
    )
    
    fig.update_yaxes(range=[0, 100])
    
    return fig


def create_condition_count_chart(df):
    """
    Create a bar chart showing diabetes rates by number of pre-existing conditions.
    
    Pre-existing conditions include: stroke, heart disease/attack, high BP, high cholesterol, elevated BMI (≥30)
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The diabetes dataset
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Bar chart of diabetes rates by condition count
    """
    df = df.copy()
    df.columns = df.columns.str.lower()
    
    # Count number of pre-existing conditions
    # Conditions: stroke, heartdiseaseorattack, highbp, highchol, bmi >= 30
    df['condition_count'] = (
        df['stroke'].astype(int) + 
        df['heartdiseaseorattack'].astype(int) + 
        df['highbp'].astype(int) + 
        df['highchol'].astype(int) +
        (df['bmi'] >= 30).astype(int)
    )
    
    cond_data = df.groupby('condition_count')['diabetes_binary'].mean() * 100
    cond_counts = df.groupby('condition_count').size()
    
    condition_labels = {
        0: 'No Conditions',
        1: '1 Condition',
        2: '2 Conditions',
        3: '3 Conditions',
        4: '4 Conditions',
        5: '5 Conditions'
    }
    
    cond_df = pd.DataFrame({
        'Conditions': [condition_labels.get(i, f'{i} Conditions') for i in cond_data.index],
        'Diabetes Rate (%)': cond_data.values,
        'Count': cond_counts.values
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=cond_df['Conditions'],
        y=cond_df['Diabetes Rate (%)'],
        marker=dict(color='#931A23'),
        text=[f"{val:.1f}%" for val in cond_df['Diabetes Rate (%)']],
        textposition='outside',
        customdata=cond_df[['Count']],
        hovertemplate='%{x}<br>Diabetes Rate: %{y:.1f}%<br>Count: %{customdata[0]:,}<extra></extra>',
    ))
    
    fig.update_layout(
        title="Diabetes Rate by Number of Pre-Existing Conditions",
        xaxis_title="Number of Pre-Existing Conditions (Stroke, Heart Disease, High BP, High Cholesterol, Elevated BMI)",
        yaxis_title="Diabetes Rate (%)",
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white',
    )
    
    fig.update_yaxes(range=[0, 100])
    
    return fig