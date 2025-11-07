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
    
    fig = go.Figure()
    
    # Diabetes rate
    fig.add_trace(go.Scatter(
        x=grouped_df.index,
        y=grouped_df['diabetes_binary'],
        name='Diabetes Rate (%)',
        line=dict(color="#FBE35A", width=4),
        fill='tozeroy',
        fillcolor='rgba(251,227,90, 0.4)',
        yaxis='y',
        mode='lines+markers',
        marker=dict(size=8),
    ))
    
    # Mental unhealthy days
    fig.add_trace(go.Scatter(
        x=grouped_df.index,
        y=grouped_df['menthlth'],
        name='Mental Unhealthy Days',
        line=dict(color="#931A23", width=4),
        fill='tozeroy',
        fillcolor='rgba(147,26,35, 0.4)',
        yaxis='y2',
        mode='lines+markers',
        marker=dict(size=8),
    ))
    
    # Physical unhealthy days
    fig.add_trace(go.Scatter(
        x=grouped_df.index,
        y=grouped_df['physhlth'],
        name='Physical Unhealthy Days',
        line=dict(color="#E8C6AE", width=4),
        fill='tozeroy',
        fillcolor='rgba(232,198,174, 0.4)',
        yaxis='y2',
        mode='lines+markers',
        marker=dict(size=8),
    ))
    
    # Create axes
    fig.update_layout(
        title="Health Metrics Trends by General Health Rating",
        xaxis=dict(title="General Health Rating (1=Excellent, 5=Poor)"),
        yaxis=dict(
            title="Diabetes Rate (%)",
            titlefont=dict(color="#FBE35A"),
            tickfont=dict(color="#FBE35A"),
        ),
        yaxis2=dict(
            title="Average Days (per month)",
            titlefont=dict(color="#931A23"),
            tickfont=dict(color="#931A23"),
            overlaying="y",
            side="right"
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=500,
        hovermode='x unified',
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


def create_physical_activity_demographics_chart(df):
    """
    Create an interactive chart showing diabetes rates by physical activity
    across demographics (Age Group, Sex, BMI Category).
    (This is the one from the original)
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The diabetes dataset
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Interactive Plotly figure with dropdown
    """
    df = df.copy()
    df.columns = df.columns.str.lower()
    
    def map_age_to_range(age):
        if age <= 2:
            return '18-29'
        elif age <= 4:
            return '30-44'
        elif age <= 6:
            return '45-59'
        elif age <= 12:
            return '60-74'
        else:
            return '75+'
    
    sex_mapping = {0: 'Female', 1: 'Male'}
    
    def categorize_bmi(bmi):
        if bmi < 18.5:
            return 'Underweight'
        elif bmi < 25:
            return 'Normal'
        elif bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'
    
    df['age_group'] = df['age'].apply(map_age_to_range)
    df['sex_label'] = df['sex'].map(sex_mapping)
    df['bmi_category'] = df['bmi'].apply(categorize_bmi)
    df['physactivity_label'] = df['physactivity'].map({0: 'No', 1: 'Yes'})
    
    def calculate_rates(group_by_col):
        results = df.groupby([group_by_col, 'physactivity_label']).agg({
            'diabetes_binary': ['mean', 'count']
        }).reset_index()
        
        results.columns = [group_by_col, 'PhysActivity', 'Diabetes Rate', 'Count']
        results['Diabetes Rate (%)'] = results['Diabetes Rate'] * 100
        
        return results
    
    age_data = calculate_rates('age_group')
    sex_data = calculate_rates('sex_label')
    bmi_data = calculate_rates('bmi_category')
    
    age_order = ['18-29', '30-44', '45-59', '60-74', '75+']
    age_data['age_group'] = pd.Categorical(age_data['age_group'], categories=age_order, ordered=True)
    age_data = age_data.sort_values('age_group')
    
    bmi_order = ['Underweight', 'Normal', 'Overweight', 'Obese']
    bmi_data['bmi_category'] = pd.Categorical(bmi_data['bmi_category'], categories=bmi_order, ordered=True)
    bmi_data = bmi_data.sort_values('bmi_category')
    
    color_no = "#E8C6AE"
    color_yes = "#931A23"
    
    fig = go.Figure()
    
    def add_traces(data, group_col, visible=True, groups_order=None):
        if groups_order is None:
            groups = data[group_col].unique()
        else:
            groups = groups_order
        
        for group in groups:
            group_data = data[data[group_col] == group]
            
            no_activity = group_data[group_data['PhysActivity'] == 'No']
            if not no_activity.empty:
                fig.add_trace(go.Bar(
                    name='No',
                    x=[group],
                    y=no_activity['Diabetes Rate (%)'].values,
                    marker=dict(color=color_no, line=dict(color='white', width=2)),
                    text=[f"{val:.1f}%" for val in no_activity['Diabetes Rate (%)'].values],
                    textposition='outside',
                    customdata=np.column_stack((
                        no_activity['Diabetes Rate (%)'].values,
                        no_activity['Count'].values,
                        [group] * len(no_activity)
                    )),
                    hovertemplate='<b>%{customdata[2]}</b><br>No Physical Activity<br>Diabetes Rate: %{customdata[0]:.1f}%<br>Count: %{customdata[1]:,}<extra></extra>',
                    legendgroup='No',
                    showlegend=(group == groups[0]),
                    visible=visible,
                    offsetgroup=0
                ))
            
            yes_activity = group_data[group_data['PhysActivity'] == 'Yes']
            if not yes_activity.empty:
                fig.add_trace(go.Bar(
                    name='Yes',
                    x=[group],
                    y=yes_activity['Diabetes Rate (%)'].values,
                    marker=dict(color=color_yes, line=dict(color='white', width=2)),
                    text=[f"{val:.1f}%" for val in yes_activity['Diabetes Rate (%)'].values],
                    textposition='outside',
                    customdata=np.column_stack((
                        yes_activity['Diabetes Rate (%)'].values,
                        yes_activity['Count'].values,
                        [group] * len(yes_activity)
                    )),
                    hovertemplate='<b>%{customdata[2]}</b><br>Yes Physical Activity<br>Diabetes Rate: %{customdata[0]:.1f}%<br>Count: %{customdata[1]:,}<extra></extra>',
                    legendgroup='Yes',
                    showlegend=(group == groups[0]),
                    visible=visible,
                    offsetgroup=1
                ))
    
    add_traces(age_data, 'age_group', visible=True, groups_order=age_order)
    age_trace_count = len([t for t in fig.data])
    
    add_traces(sex_data, 'sex_label', visible=False)
    sex_trace_count = len([t for t in fig.data]) - age_trace_count
    
    add_traces(bmi_data, 'bmi_category', visible=False, groups_order=bmi_order)
    bmi_trace_count = len([t for t in fig.data]) - age_trace_count - sex_trace_count
    
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        args=[{"visible": [True] * age_trace_count + [False] * sex_trace_count + [False] * bmi_trace_count},
                              {"xaxis.title": "Age Group"}],
                        label="Age Group",
                        method="update"
                    ),
                    dict(
                        args=[{"visible": [False] * age_trace_count + [True] * sex_trace_count + [False] * bmi_trace_count},
                              {"xaxis.title": "Sex"}],
                        label="Sex",
                        method="update"
                    ),
                    dict(
                        args=[{"visible": [False] * age_trace_count + [False] * sex_trace_count + [True] * bmi_trace_count},
                              {"xaxis.title": "BMI Category"}],
                        label="BMI Category",
                        method="update"
                    ),
                ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.01,
                xanchor="left",
                y=1.15,
                yanchor="top",
                bgcolor="white",
                bordercolor="black",
                borderwidth=1
            ),
        ]
    )
    
    fig.update_layout(
        title={
            'text': 'Physical Activity vs. Diabetes Rate by Demographics',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        xaxis=dict(
            title="Age Group",
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=False
        ),
        yaxis=dict(
            title="Diabetes Rate (%)",
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=False,
            range=[0, 100]
        ),
        barmode='group',
        height=600,
        legend=dict(
            title='Physical Activity',
            orientation='v',
            yanchor='top',
            y=1,
            xanchor='right',
            x=1.08
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='closest',
    )
    
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=False)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=False, range=[0, 100])
    
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