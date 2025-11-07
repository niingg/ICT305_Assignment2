"""
Hypothesis 5: Pre-existing Health Conditions and Diabetes
Module for creating interactive visualizations related to pre-existing cardiometabolic conditions and diabetes risk.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Color Constants
PRIMARY = "#931A23"        # Your brand
SECONDARY = "#E8C6AE"      # Accent
GRID = "rgba(0, 0, 0, 0.08)"

def create_preexisting_conditions_chart(df, sort_by="Prevalence"):
    """
    Create an interactive chart showing diabetes rates and relative risk for individual pre-existing conditions.
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
    
    for condition_name, condition_col in conditions.items():
        no_rate = df[df[condition_col] == 0]['diabetes_binary'].mean() * 100
        yes_rate = df[df[condition_col] == 1]['diabetes_binary'].mean() * 100
        relative_risk = yes_rate / no_rate if no_rate > 0 else 1.0
        
        prevalence_data.append({
            'Condition': condition_name,
            'No Rate': no_rate,
            'Yes Rate': yes_rate,
            'Relative Risk': relative_risk
        })
    
    if sort_by == "Relative Risk":
        sorted_data = sorted(prevalence_data, key=lambda x: x['Relative Risk'], reverse=True)
    else:  # Prevalence
        sorted_data = sorted(prevalence_data, key=lambda x: x['Yes Rate'], reverse=True)
    
    sorted_df = pd.DataFrame(sorted_data)
    
    # Create figure with 2 traces total
    fig = go.Figure()
    
    # Add "No" trace (all conditions)
    fig.add_trace(go.Bar(
        x=sorted_df['Condition'],
        y=sorted_df['No Rate'],
        name='No',
        marker=dict(color='#E8C6AE'),
        text=[f"{val:.1f}%" for val in sorted_df['No Rate']],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>No Condition: %{y:.1f}%<extra></extra>',
    ))
    
    # Add "Yes" trace (all conditions)
    fig.add_trace(go.Bar(
        x=sorted_df['Condition'],
        y=sorted_df['Yes Rate'],
        name='Yes',
        marker=dict(color='#931A23'),
        text=[f"{val:.1f}%" for val in sorted_df['Yes Rate']],
        textposition='outside',
        customdata=sorted_df['Relative Risk'],
        hovertemplate='<b>%{x}</b><br>Has Condition: %{y:.1f}%<br>Relative Risk: %{customdata:.2f}x<extra></extra>',
    ))
    
    fig.update_layout(
        title_text=f"Effect of Pre-Existing Factors on Diabetes Rates (Sorted by {sort_by})",
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

def create_preexisting_conditions_demographics_chart(df):
    """
    Create an interactive chart showing diabetes rates by pre-existing conditions across demographics.
    Shows relationship between diabetes rates, number of pre-existing conditions, and age/sex.
    
    Conditions counted: stroke, heartdiseaseorattack, highbp, highchol, obesity (bmi >= 30)
    
    Dropdown allows switching between:
    - Age Group (5 age bands)
    - Sex (Female/Male)
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The diabetes dataset
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Interactive figure with dropdown to switch between Age and Sex groupings
    """
    df = df.copy()
    df.columns = df.columns.str.lower()
    
    # Create conditions count (0-5)
    df['conditions_count'] = 0
    df.loc[df['stroke'] == 1, 'conditions_count'] += 1
    df.loc[df['heartdiseaseorattack'] == 1, 'conditions_count'] += 1
    df.loc[df['highbp'] == 1, 'conditions_count'] += 1
    df.loc[df['highchol'] == 1, 'conditions_count'] += 1
    df.loc[df['bmi'] >= 30, 'conditions_count'] += 1
    
    # Create binary conditions variable (0 = no conditions, 1 = any conditions)
    df['conditions_binary'] = 0
    df.loc[df['conditions_count'] > 0, 'conditions_binary'] = 1
    
    # Create age groups
    df['age_group'] = pd.cut(
        df['age'],
        bins=[0, 2, 5, 8, 11, 13],
        labels=['18-29', '30-44', '45-59', '60-74', '75+'],
        include_lowest=True
    )
    
    # Create sex mapping
    sex_mapping = {0: 'Female', 1: 'Male'}
    df['sex_label'] = df['sex'].map(sex_mapping)
    
    # ========== AGE GROUPS ==========
    age_conditions_grouped = df.groupby(['age_group', 'conditions_binary'], observed=True)['diabetes_binary'].mean().reset_index()
    age_conditions_grouped['diabetes_rate_pct'] = age_conditions_grouped['diabetes_binary'] * 100
    age_conditions_grouped['Response'] = age_conditions_grouped['conditions_binary'].map({0: 'No', 1: 'Yes'})
    age_conditions_counts = df.groupby(['age_group', 'conditions_binary'], observed=True).size().reset_index(name='Count')
    age_conditions_grouped = age_conditions_grouped.merge(age_conditions_counts, on=['age_group', 'conditions_binary'])
    
    df_age_no = age_conditions_grouped[age_conditions_grouped['Response'] == 'No']
    df_age_yes = age_conditions_grouped[age_conditions_grouped['Response'] == 'Yes']
    
    # ========== SEX GROUPS ==========
    sex_conditions_grouped = df.groupby(['sex_label', 'conditions_binary'], observed=True)['diabetes_binary'].mean().reset_index()
    sex_conditions_grouped['diabetes_rate_pct'] = sex_conditions_grouped['diabetes_binary'] * 100
    sex_conditions_grouped['Response'] = sex_conditions_grouped['conditions_binary'].map({0: 'No', 1: 'Yes'})
    sex_conditions_counts = df.groupby(['sex_label', 'conditions_binary'], observed=True).size().reset_index(name='Count')
    sex_conditions_grouped = sex_conditions_grouped.merge(sex_conditions_counts, on=['sex_label', 'conditions_binary'])
    
    df_sex_no = sex_conditions_grouped[sex_conditions_grouped['Response'] == 'No']
    df_sex_yes = sex_conditions_grouped[sex_conditions_grouped['Response'] == 'Yes']
    
    fig = go.Figure()
    
    # ========== AGE TRACES ==========
    fig.add_trace(go.Bar(
        x=df_age_no['age_group'].astype(str),
        y=df_age_no['diabetes_rate_pct'],
        name='No Pre-Existing Conditions',
        marker=dict(color='#EEC8A3'),
        text=[f"{val:.1f}" for val in df_age_no['diabetes_rate_pct']],
        textposition='outside',
        textfont=dict(size=11),
        customdata=df_age_no[['Count']],
        hovertemplate='<b>%{x}</b><br>Has Pre-Existing Conditions: No<br>Diabetes Rate (%): %{y:.1f}<br>Count: %{customdata[0]:,}<extra></extra>',
        legendgroup='No',
        showlegend=True,
        visible=True
    ))
    
    fig.add_trace(go.Bar(
        x=df_age_yes['age_group'].astype(str),
        y=df_age_yes['diabetes_rate_pct'],
        name='Has Pre-Existing Conditions',
        marker=dict(color='#931A23'),
        text=[f"{val:.1f}" for val in df_age_yes['diabetes_rate_pct']],
        textposition='outside',
        textfont=dict(size=11),
        customdata=df_age_yes[['Count']],
        hovertemplate='<b>%{x}</b><br>Has Pre-Existing Conditions: Yes<br>Diabetes Rate (%): %{y:.1f}<br>Count: %{customdata[0]:,}<extra></extra>',
        legendgroup='Yes',
        showlegend=True,
        visible=True
    ))
    
    # ========== SEX TRACES ==========
    fig.add_trace(go.Bar(
        x=df_sex_no['sex_label'],
        y=df_sex_no['diabetes_rate_pct'],
        name='No Pre-Existing Conditions',
        marker=dict(color='#EEC8A3'),
        text=[f"{val:.1f}" for val in df_sex_no['diabetes_rate_pct']],
        textposition='outside',
        textfont=dict(size=11),
        customdata=df_sex_no[['Count']],
        hovertemplate='<b>%{x}</b><br>Has Pre-Existing Conditions: No<br>Diabetes Rate (%): %{y:.1f}<br>Count: %{customdata[0]:,}<extra></extra>',
        legendgroup='No',
        showlegend=False,
        visible=False
    ))
    
    fig.add_trace(go.Bar(
        x=df_sex_yes['sex_label'],
        y=df_sex_yes['diabetes_rate_pct'],
        name='Has Pre-Existing Conditions',
        marker=dict(color='#931A23'),
        text=[f"{val:.1f}" for val in df_sex_yes['diabetes_rate_pct']],
        textposition='outside',
        textfont=dict(size=11),
        customdata=df_sex_yes[['Count']],
        hovertemplate='<b>%{x}</b><br>Has Pre-Existing Conditions: Yes<br>Diabetes Rate (%): %{y:.1f}<br>Count: %{customdata[0]:,}<extra></extra>',
        legendgroup='Yes',
        showlegend=False,
        visible=False
    ))
    
    # Create dropdown buttons
    buttons = [
        dict(
            label='Age Group',
            method='update',
            args=[
                {'visible': [True, True, False, False]},
                {'xaxis': {'title': 'Age Group (Years)'}}
            ]
        ),
        dict(
            label='Sex',
            method='update',
            args=[
                {'visible': [False, False, True, True]},
                {'xaxis': {'title': 'Sex'}}
            ]
        )
    ]
    
    # Update layout
    fig.update_layout(
        updatemenus=[dict(
            active=0,
            buttons=buttons,
            direction='down',
            pad={'r': 10, 't': 10},
            showactive=True,
            x=0.01,
            xanchor='left',
            y=1.15,
            yanchor='top'
        )],
        title=dict(
            text='Diabetes Rate by Demographics and Pre-Existing Conditions',
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title='Age Group (Years)',
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='black',
            ticks='outside',
            ticklen=5,
            tickwidth=1,
            tickcolor='black'
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
        barmode='group',
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            title='Pre-Existing Conditions',
            orientation='v',
            yanchor='top',
            y=1,
            xanchor='right',
            x=1.2
        ),
        height=600,
        hovermode='closest',
    )
    
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=False)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=False, range=[0, 100])
    
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
        'Conditions': [condition_labels.get(i, f'{i} Conditions') for i in range(6)],
        'Diabetes Rate (%)': [cond_data.get(i, 0) for i in range(6)],
        'Count': [cond_counts.get(i, 0) for i in range(6)]
    })
    
    fig = go.Figure()
    
    # Color gradient from yellow to dark red
    colors = ["#FFF1A4", '#EEC8A3', '#DD9C7C', '#D24C49', '#A64A47', '#931A23']
    
    for i, (idx, row) in enumerate(cond_df.iterrows()):
        fig.add_trace(go.Bar(
            x=[row['Conditions']],
            y=[row['Diabetes Rate (%)']],
            name=row['Conditions'],
            marker=dict(color=colors[i]),
            text=[f"{row['Diabetes Rate (%)']:.1f}%"],
            textposition='outside',
            customdata=[[row['Count']]],
            hovertemplate='<b>%{x}</b><br>Diabetes Rate: %{y:.1f}%<br>Count: %{customdata[0][0]:,}<extra></extra>',
            showlegend=False,
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