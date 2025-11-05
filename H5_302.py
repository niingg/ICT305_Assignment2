##imports
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from math import erf, sqrt, log, exp

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
## read dataset
df_brfss = pd.read_csv("diabetes_binary_5050split_health_indicators_BRFSS2015.csv")

## standardising column names 
df_brfss.columns = df_brfss.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-','_')

## Graph 1: Correlation between pre-existing health conditions and diabetes
# Melt the variables into one column for easier plotting
df_melted = df_brfss.melt(
    id_vars='diabetes_binary',
    value_vars=["stroke", "heartdiseaseorattack", "highbp", "highchol"],
    var_name='PreExistingFactors',
    value_name='Value'
)
df_grouped = df_melted.groupby(['PreExistingFactors', 'Value'])['diabetes_binary'].mean().reset_index()
df_grouped['diabetes_rate_pct'] = df_grouped['diabetes_binary'] * 100
df_grouped['Response'] = df_grouped['Value'].map({0: 'No', 1: 'Yes'})
df_grouped['PreExistingFactors'] = df_grouped['PreExistingFactors'].map({
    'stroke': 'Stroke',
    'heartdiseaseorattack': 'Heart Disease',
    'highbp': 'High Blood Pressure',
    'highchol': 'High Cholesterol'
})

# Calculate relative risk for each factor
df_pivot = df_grouped.pivot(index='PreExistingFactors', columns='Response', values='diabetes_rate_pct')
df_pivot['Relative_Risk'] = df_pivot['Yes'] / df_pivot['No']
df_pivot['Prevalence'] = df_pivot['Yes']
df_pivot = df_pivot.reset_index()

prevalence_order = df_pivot.sort_values('Prevalence', ascending=False)['PreExistingFactors'].tolist()

relative_risk_order = df_pivot.sort_values('Relative_Risk', ascending=False)['PreExistingFactors'].tolist()

def prepare_data(order):
    df_no_sorted = df_grouped[df_grouped['Response'] == 'No'].set_index('PreExistingFactors').loc[order].reset_index()
    df_yes_sorted = df_grouped[df_grouped['Response'] == 'Yes'].set_index('PreExistingFactors').loc[order].reset_index()
    return df_no_sorted, df_yes_sorted

fig = go.Figure()

df_no_prev, df_yes_prev = prepare_data(prevalence_order)

fig.add_trace(go.Bar(
    x=df_no_prev['PreExistingFactors'],
    y=df_no_prev['diabetes_rate_pct'],
    name='No',
    marker=dict(color='#EEC8A3'),
    text=[f"{val:.1f}" for val in df_no_prev['diabetes_rate_pct']],
    textposition='outside',
    textfont=dict(size=11),
    hovertemplate='<b>%{x}</b><br>Has Condition: No<br>Diabetes Rate (%): %{y:.1f}<extra></extra>',
    selected=dict(marker=dict(opacity=1)),
    unselected=dict(marker=dict(opacity=0.5)),
    visible=True
))

fig.add_trace(go.Bar(
    x=df_yes_prev['PreExistingFactors'],
    y=df_yes_prev['diabetes_rate_pct'],
    name='Yes',
    marker=dict(color='#931A23'),
    text=[f"{val:.1f}" for val in df_yes_prev['diabetes_rate_pct']],
    textposition='outside',
    textfont=dict(size=11),
    hovertemplate='<b>%{x}</b><br>Has Condition: Yes<br>Diabetes Rate (%): %{y:.1f}<extra></extra>',
    selected=dict(marker=dict(opacity=1)),
    unselected=dict(marker=dict(opacity=0.5)),
    visible=True
))

df_no_rr, df_yes_rr = prepare_data(relative_risk_order)

fig.add_trace(go.Bar(
    x=df_no_rr['PreExistingFactors'],
    y=df_no_rr['diabetes_rate_pct'],
    name='No',
    marker=dict(color='#EEC8A3'),
    text=[f"{val:.1f}" for val in df_no_rr['diabetes_rate_pct']],
    textposition='outside',
    textfont=dict(size=11),
    hovertemplate='<b>%{x}</b><br>Has Condition: No<br>Diabetes Rate (%): %{y:.1f}<extra></extra>',
    selected=dict(marker=dict(opacity=1)),
    unselected=dict(marker=dict(opacity=0.5)),
    visible=False,
    showlegend=False
))

fig.add_trace(go.Bar(
    x=df_yes_rr['PreExistingFactors'],
    y=df_yes_rr['diabetes_rate_pct'],
    name='Yes',
    marker=dict(color='#931A23'),
    text=[f"{val:.1f}" for val in df_yes_rr['diabetes_rate_pct']],
    textposition='outside',
    textfont=dict(size=11),
    hovertemplate='<b>%{x}</b><br>Has Condition: Yes<br>Diabetes Rate (%): %{y:.1f}<extra></extra>',
    selected=dict(marker=dict(opacity=1)),
    unselected=dict(marker=dict(opacity=0.5)),
    visible=False,
    showlegend=False
))

# Create dropdown buttons
buttons = [
    dict(
        label='Sort by Prevalence',
        method='update',
        args=[{'visible': [True, True, False, False]}]
    ),
    dict(
        label='Sort by Relative Risk',
        method='update',
        args=[{'visible': [False, False, True, True]}]
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
        text='Effect of Pre-Existing Factors on Diabetes Rates',
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title='Pre-Existing Factors',
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
        title='Has Condition',
        orientation='v',
        yanchor='top',
        y=1,
        xanchor='right',
        x=1.1
    ),
    height=600,
    hovermode='closest',
    dragmode='select',
    clickmode='event+select'
)

fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=False)
fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=False)

fig.show()

## Graph 2: Correlation between bmi and diabetes
# Create BMI category
df_brfss['bmi_class'] = 0

df_brfss.loc[df_brfss['bmi'] < 18.5, 'bmi_class'] = 0
df_brfss.loc[(df_brfss['bmi'] >= 18.5) & (df_brfss['bmi'] < 25), 'bmi_class'] = 1
df_brfss.loc[(df_brfss['bmi'] >= 25) & (df_brfss['bmi'] < 30), 'bmi_class'] = 2
df_brfss.loc[(df_brfss['bmi'] >= 30) & (df_brfss['bmi'] < 35), 'bmi_class'] = 3
df_brfss.loc[(df_brfss['bmi'] >= 35) & (df_brfss['bmi'] < 40), 'bmi_class'] = 4
df_brfss.loc[(df_brfss['bmi'] >= 40), 'bmi_class'] = 5

# BMI data
bmi_data = df_brfss.groupby('bmi_class')['diabetes_binary'].mean() * 100
bmi_counts = df_brfss.groupby('bmi_class').size()

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
        selected=dict(marker=dict(opacity=1)),
        unselected=dict(marker=dict(opacity=0.3))
    ))

# Update layout
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
    dragmode='select',
    clickmode='event+select',
    legend=dict(
        title='BMI Category',
        orientation='v',
        yanchor='top',
        y=1,
        xanchor='left',
        x=1.02
    )
)

fig.show()

## Graph 3: Correlation between no. of pmhx and diabetes - choose circle or bar
# Create pmhx variable (0-4 barriers)
df_brfss['Conditions'] = 0
df_brfss.loc[df_brfss['highbp'] == 1, 'Conditions'] += 1
df_brfss.loc[df_brfss['highchol'] == 1, 'Conditions'] += 1
df_brfss.loc[df_brfss['heartdiseaseorattack'] == 1, 'Conditions'] += 1
df_brfss.loc[df_brfss['stroke'] == 1, 'Conditions'] += 1
df_brfss.loc[df_brfss['bmi'] > 30, 'Conditions'] += 1

# PMHX data
pmhx_data = df_brfss.groupby('Conditions')['diabetes_binary'].mean() * 100
pmhx_counts = df_brfss.groupby('Conditions').size()

pmhx_df = pd.DataFrame({
    'Conditions': pmhx_data.index.map({
        0: 'No Other Conditions', 
        1: '1 Condition', 
        2: '2 Conditions', 
        3: '3 Conditions', 
        4: '4 Conditions',
        5: '5 Conditions'
    }),
    'Diabetes Rate (%)': pmhx_data.values,
    'Count': pmhx_data.values
})

pmhx_order= [
    'No Other Conditions', 
    '1 Condition', 
    '2 Conditions', 
    '3 Conditions', 
    '4 Conditions',
    '5 Conditions'
]

pmhx_df['Conditions'] = pd.Categorical(pmhx_df['Conditions'], categories=pmhx_order, ordered=True)
pmhx_df = pmhx_df.sort_values('Conditions')

fig = go.Figure()

# Add bars with different colors for each category
colors = ["#FFF1A4", '#EEC8A3', '#DD9C7C', '#D24C49', '#A64A47', '#931A23']

for i, (idx, row) in enumerate(pmhx_df.iterrows()):
    fig.add_trace(go.Bar(
        x=[row['Conditions']],
        y=[row['Diabetes Rate (%)']],
        name=row['Conditions'],
        marker=dict(color=colors[i]),
        text=[f"{row['Diabetes Rate (%)']:.1f}"],
        textposition='outside',
        textfont=dict(size=11),
        customdata=[[row['Conditions'], row['Diabetes Rate (%)'], row['Count']]],
        hovertemplate='<b>%{customdata[0]}</b><br>Diabetes Rate (%): %{customdata[1]:.1f}<br>Count: %{customdata[2]:,}<extra></extra>',
        showlegend=True,
        selected=dict(marker=dict(opacity=1)),
        unselected=dict(marker=dict(opacity=0.3))
    ))

# Update layout
fig.update_layout(
    title=dict(
        text='Diabetes Rate by No. of Pre-Existing Conditions',
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title='No. of Pre-Existing Conditions<br>(Heart Disease, High Blood Pressure, High Cholesterol, Stroke, Obesity)',
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
    height=500,
    plot_bgcolor='white',
    paper_bgcolor='white',
    hovermode='closest',
    dragmode='select',
    clickmode='event+select',
    legend=dict(
        title='Number of Conditions',
        orientation='v',
        yanchor='top',
        y=1,
        xanchor='left',
        x=1.02
    )
)

fig.show()

# donut chart
# PMHX data
pmhx_data = df_brfss.groupby('Conditions')['diabetes_binary'].mean() * 100
pmhx_counts = df_brfss.groupby('Conditions').size()

pmhx_df = pd.DataFrame({
    'Conditions': pmhx_data.index.map({
        0: 'No Other Conditions', 
        1: '1 Condition', 
        2: '2 Conditions', 
        3: '3 Conditions', 
        4: '4 Conditions',
        5: '5 Conditions'
    }),
    'Diabetes Rate (%)': pmhx_data.values,
    'Count': pmhx_data.values
})

pmhx_order= [
    'No Other Conditions', 
    '1 Condition', 
    '2 Conditions', 
    '3 Conditions', 
    '4 Conditions',
    '5 Conditions'
]

pmhx_df['Conditions'] = pd.Categorical(pmhx_df['Conditions'], categories=pmhx_order, ordered=True)
pmhx_df = pmhx_df.sort_values('Conditions')

fig = go.Figure(data=[go.Pie(
    labels=pmhx_df['Conditions'],
    values=pmhx_df['Diabetes Rate (%)'],
    hole=0.33,
    marker=dict(
        colors=["#FBE35A", '#EEC8A3', '#DD9C7C', '#D24C49', '#A64A47', '#931A23'],
        line=dict(color='white', width=2)
    ),
    textinfo='label+percent',
    textposition='inside',
    textfont=dict(size=14, color='white', family='Arial', weight='bold'),
    hovertemplate='<b>%{label}</b><br>Diabetes Rate: %{value:.2f}%<extra></extra>',
    sort=False
)])

fig.update_layout(
    title=dict(
        text='Diabetes Rate by Number of Pre-Existing Conditions',
        x=0.45,
        xanchor='center'
    ),
    width=700,
    height=700,
    showlegend=True,
    legend=dict(
        title='Number of Conditions',
        orientation='v',
        yanchor='middle',
        y=0.5,
        xanchor='left',
        x=1.02
    ),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

fig.show()

# donut without percentage inside it
# PMHX data
pmhx_data = df_brfss.groupby('Conditions')['diabetes_binary'].mean() * 100
pmhx_counts = df_brfss.groupby('Conditions').size()

pmhx_df = pd.DataFrame({
    'Conditions': pmhx_data.index.map({
        0: 'No Other Conditions', 
        1: '1 Condition', 
        2: '2 Conditions', 
        3: '3 Conditions', 
        4: '4 Conditions',
        5: '5 Conditions'
    }),
    'Diabetes Rate (%)': pmhx_data.values,
    'Count': pmhx_data.values
})

pmhx_order= [
    'No Other Conditions', 
    '1 Condition', 
    '2 Conditions', 
    '3 Conditions', 
    '4 Conditions',
    '5 Conditions'
]

pmhx_df['Conditions'] = pd.Categorical(pmhx_df['Conditions'], categories=pmhx_order, ordered=True)
pmhx_df = pmhx_df.sort_values('Conditions')

fig = go.Figure(data=[go.Pie(
    labels=pmhx_df['Conditions'],
    values=pmhx_df['Diabetes Rate (%)'],
    hole=0.33,
    marker=dict(
        colors=["#FBE35A", '#EEC8A3', '#DD9C7C', '#D24C49', '#A64A47', '#931A23'],
        line=dict(color='white', width=2)
    ),
    textinfo='label',
    textposition='inside',
    textfont=dict(size=14, color='white', family='Arial', weight='bold'),
    hovertemplate='<b>%{label}</b><br>Diabetes Rate: %{value:.2f}%<extra></extra>',
    sort=False
)])

fig.update_layout(
    title=dict(
        text='Diabetes Rate by Number of Pre-Existing Conditions',
        x=0.45,
        xanchor='center'
    ),
    width=700,
    height=700,
    showlegend=True,
    legend=dict(
        title='Number of Conditions',
        orientation='v',
        yanchor='middle',
        y=0.5,
        xanchor='left',
        x=1.02
    ),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

fig.show()

## Graph 4: Correlation between age, no. of pmhx and diabetes
# Create yes/no conditions variable (0-1 no yes)
df_brfss['conditions_binary'] = 0
df_brfss.loc[df_brfss['Conditions'] > 0, 'conditions_binary'] += 1

# Create age groups
df_brfss['age_group'] = pd.cut(
    df_brfss['age'], 
    bins=[0, 2, 5, 8, 11, 13],
    labels=['18-29', '30-44', '45-59', '60-74', '75+'],
    include_lowest=True
)

# Age groups
age_conditions_grouped = df_brfss.groupby(['age_group', 'conditions_binary'], observed=True)['diabetes_binary'].mean().reset_index()
age_conditions_grouped['diabetes_rate_pct'] = age_conditions_grouped['diabetes_binary'] * 100
age_conditions_grouped['Response'] = age_conditions_grouped['conditions_binary'].map({0: 'No', 1: 'Yes'})
age_conditions_counts = df_brfss.groupby(['age_group', 'conditions_binary'], observed=True).size().reset_index(name='Count')
age_conditions_grouped = age_conditions_grouped.merge(age_conditions_counts, on=['age_group', 'conditions_binary'])

df_age_no = age_conditions_grouped[age_conditions_grouped['Response'] == 'No']
df_age_yes = age_conditions_grouped[age_conditions_grouped['Response'] == 'Yes']

# Sex groups
sex_conditions_grouped = df_brfss.groupby(['sex', 'conditions_binary'], observed=True)['diabetes_binary'].mean().reset_index()
sex_conditions_grouped['diabetes_rate_pct'] = sex_conditions_grouped['diabetes_binary'] * 100
sex_conditions_grouped['Response'] = sex_conditions_grouped['conditions_binary'].map({0: 'No', 1: 'Yes'})
sex_conditions_grouped['sex_label'] = sex_conditions_grouped['sex'].map({0: 'Female', 1: 'Male'})
sex_conditions_counts = df_brfss.groupby(['sex', 'conditions_binary'], observed=True).size().reset_index(name='Count')
sex_conditions_grouped = sex_conditions_grouped.merge(sex_conditions_counts, on=['sex', 'conditions_binary'])

df_sex_no = sex_conditions_grouped[sex_conditions_grouped['Response'] == 'No']
df_sex_yes = sex_conditions_grouped[sex_conditions_grouped['Response'] == 'Yes']

fig = go.Figure()

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
    showlegend=True,  # Changed to True
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
    showlegend=True,  # Changed to True
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
    dragmode='select',
    clickmode='event+select'
)

fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=False)
fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=False)

fig.show()

