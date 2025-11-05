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

##Graph 1  - Coverage & Cost vs Diabetes
# INCOME 
income_data = df_brfss.groupby('income')['diabetes_binary'].mean() * 100
income_counts = df_brfss.groupby('income').size()
income_df = pd.DataFrame({
    'Income Group ($)': income_data.index.map({1: ' < $10000', 2: ' $10000 - $15000', 3: ' $15000 - $20000', 4: ' $20000 - $25000', 5: ' $25000 - $35000',
                                               6: ' $35000 - $50000', 7: ' $50000 - $75000', 8: ' $75000 >'}),
    'Diabetes Rate (%)': income_data.values,
    'Count': income_counts.values
})

# Calculate coverage vs diabetes rate
coverage_data = df_brfss.groupby('anyhealthcare')['diabetes_binary'].mean() * 100
coverage_counts = df_brfss.groupby('anyhealthcare').size()
coverage_df = pd.DataFrame({
    'Response': coverage_data.index.map({0: ' No', 1: ' Yes'}),
    'Diabetes Rate (%)': coverage_data.values,
    'Count': coverage_counts.values
})

# Calculate cost vs diabetes rate
cost_data = df_brfss.groupby('nodocbccost')['diabetes_binary'].mean() * 100
cost_counts = df_brfss.groupby('nodocbccost').size()
cost_df = pd.DataFrame({
    'Response': cost_data.index.map({0: ' No', 1: ' Yes'}),
    'Diabetes Rate (%)': cost_data.values,
    'Count': cost_counts.values
})

# Create subplots for both variables
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=('Any Healthcare Coverage', 'Cost Barrier to Doctor in Past 12 Months'),
    horizontal_spacing=0.15
)

# Separate No and Yes for coverage
coverage_no = coverage_df[coverage_df['Response'] == ' No']
coverage_yes = coverage_df[coverage_df['Response'] == ' Yes']

# Separate No and Yes for cost
cost_no = cost_df[cost_df['Response'] == ' No']
cost_yes = cost_df[cost_df['Response'] == ' Yes']

# Create the figure
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=('Any Healthcare Coverage', 'Cost Barrier to Doctor in Past 12 Months'),
    horizontal_spacing=0.15
)

# Define income levels
income_levels = {
    1: '< $10000', 2: '$10000 - $15000', 3: '$15000 - $20000', 
    4: '$20000 - $25000', 5: '$25000 - $35000', 6: '$35000 - $50000', 
    7: '$50000 - $75000', 8: '$75000 >'
}

fig.add_trace(go.Bar(
    x=coverage_no['Response'],
    y=coverage_no['Diabetes Rate (%)'],
    name='No',
    marker=dict(color="#E8C6AE", line=dict(color='white', width=2)),
    text=[f"{val:.1f}%" for val in coverage_no['Diabetes Rate (%)']],
    textposition='outside',
    customdata=coverage_no[['Diabetes Rate (%)', 'Count']],
    hovertemplate='%{x} <br> Diabetes Rate: %{customdata[0]:.1f}% <br> Count = %{customdata[1]:,}<extra></extra>',
    hoverlabel=dict(bgcolor="#E8C6AE", font=dict(color='white')),
    legendgroup='response',
    showlegend=True,
    visible=True
), row=1, col=1)

fig.add_trace(go.Bar(
    x=coverage_yes['Response'],
    y=coverage_yes['Diabetes Rate (%)'],
    name='Yes',
    marker=dict(color="#931A23", line=dict(color='white', width=2)),
    text=[f"{val:.1f}%" for val in coverage_yes['Diabetes Rate (%)']],
    textposition='outside',
    customdata=coverage_yes[['Diabetes Rate (%)', 'Count']],
    hovertemplate='%{x} <br> Diabetes Rate: %{customdata[0]:.1f}% <br> Count = %{customdata[1]:,}<extra></extra>',
    hoverlabel=dict(bgcolor="#931A23", font=dict(color='white')),
    legendgroup='response',
    showlegend=True,
    visible=True
), row=1, col=1)

fig.add_trace(go.Bar(
    x=cost_no['Response'],
    y=cost_no['Diabetes Rate (%)'],
    name='No',
    marker=dict(color="#E8C6AE", line=dict(color='white', width=2)),
    text=[f"{val:.1f}%" for val in cost_no['Diabetes Rate (%)']],
    textposition='outside',
    customdata=cost_no[['Diabetes Rate (%)', 'Count']],
    hovertemplate='%{x} <br> Diabetes Rate: %{customdata[0]:.1f}% <br> Count = %{customdata[1]:,}<extra></extra>',
    hoverlabel=dict(bgcolor="#E8C6AE", font=dict(color='white')),
    legendgroup='response',
    showlegend=False,
    visible=True
), row=1, col=2)

fig.add_trace(go.Bar(
    x=cost_yes['Response'],
    y=cost_yes['Diabetes Rate (%)'],
    name='Yes',
    marker=dict(color="#931A23", line=dict(color='white', width=2)),
    text=[f"{val:.1f}%" for val in cost_yes['Diabetes Rate (%)']],
    textposition='outside',
    customdata=cost_yes[['Diabetes Rate (%)', 'Count']],
    hovertemplate='%{x} <br> Diabetes Rate: %{customdata[0]:.1f}% <br> Count = %{customdata[1]:,}<extra></extra>',
    hoverlabel=dict(bgcolor="#931A23", font=dict(color='white')),
    legendgroup='response',
    showlegend=False,
    visible=True
), row=1, col=2)

for income_code, income_label in income_levels.items():
    df_income = df_brfss[df_brfss['income'] == income_code]
    
    coverage_data_income = df_income.groupby('anyhealthcare')['diabetes_binary'].mean() * 100
    coverage_counts_income = df_income.groupby('anyhealthcare').size()

    cost_data_income = df_income.groupby('nodocbccost')['diabetes_binary'].mean() * 100
    cost_counts_income = df_income.groupby('nodocbccost').size()
    
    for response in [0, 1]:
        response_label = ' No' if response == 0 else ' Yes'
        color = "#E8C6AE" if response == 0 else "#931A23"
        
        if response in coverage_data_income.index:
            fig.add_trace(go.Bar(
                x=[response_label],
                y=[coverage_data_income[response]],
                name='No' if response == 0 else 'Yes',
                marker=dict(color=color, line=dict(color='white', width=2)),
                text=[f"{coverage_data_income[response]:.1f}%"],
                textposition='outside',
                customdata=[[coverage_data_income[response], coverage_counts_income[response]]],
                hovertemplate='%{x} <br> Diabetes Rate: %{customdata[0]:.1f}% <br> Count = %{customdata[1]:,}<extra></extra>',
                hoverlabel=dict(bgcolor=color, font=dict(color='white')),
                legendgroup='response',
                showlegend=False,
                visible=False
            ), row=1, col=1)
        else:
            fig.add_trace(go.Bar(
                x=[response_label],
                y=[0],
                name='No' if response == 0 else 'Yes',
                marker=dict(color=color, line=dict(color='white', width=2)),
                legendgroup='response',
                showlegend=False,
                visible=False
            ), row=1, col=1)
    
    for response in [0, 1]:
        response_label = ' No' if response == 0 else ' Yes'
        color = "#E8C6AE" if response == 0 else "#931A23"
        
        if response in cost_data_income.index:
            fig.add_trace(go.Bar(
                x=[response_label],
                y=[cost_data_income[response]],
                name='No' if response == 0 else 'Yes',
                marker=dict(color=color, line=dict(color='white', width=2)),
                text=[f"{cost_data_income[response]:.1f}%"],
                textposition='outside',
                customdata=[[cost_data_income[response], cost_counts_income[response]]],
                hovertemplate='%{x} <br> Diabetes Rate: %{customdata[0]:.1f}% <br> Count = %{customdata[1]:,}<extra></extra>',
                hoverlabel=dict(bgcolor=color, font=dict(color='white')),
                legendgroup='response',
                showlegend=False,
                visible=False
            ), row=1, col=2)
        else:
            fig.add_trace(go.Bar(
                x=[response_label],
                y=[0],
                name='No' if response == 0 else 'Yes',
                marker=dict(color=color, line=dict(color='white', width=2)),
                legendgroup='response',
                showlegend=False,
                visible=False
            ), row=1, col=2)

# Create dropdown buttons
buttons = []

# Button for "All Income Levels"
buttons.append(dict(
    label='All Income Levels',
    method='update',
    args=[{'visible': [True, True, True, True] + [False] * (len(fig.data) - 4)}]
))

# Button for each income level
for i, (income_code, income_label) in enumerate(income_levels.items()):
    visible_list = [False] * len(fig.data)
    start_idx = 4 + (i * 4)
    visible_list[start_idx:start_idx + 4] = [True, True, True, True]
    
    buttons.append(dict(
        label=income_label,
        method='update',
        args=[{'visible': visible_list}]
    ))

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
    title_text='Diabetes Rate by Healthcare Access Barriers',
    title_x=0.5,
    height=600,
    legend=dict(
        title='Response',
        orientation='v',
        yanchor='top',
        y=1,
        xanchor='right',
        x=1.08
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    hovermode='closest'
)

fig.update_xaxes(title_text="Response", row=1, col=1, showgrid=False, showline=True, linewidth=1, linecolor='black')
fig.update_xaxes(title_text="Response", row=1, col=2, showgrid=False, showline=True, linewidth=1, linecolor='black')
fig.update_yaxes(title_text="Diabetes Rate (%)", row=1, col=1, showgrid=False, showline=True, linewidth=1, linecolor='black', range=[0,100])
fig.update_yaxes(title_text="Diabetes Rate (%)", row=1, col=2, showgrid=False, showline=True, linewidth=1, linecolor='black', range=[0,100])

fig.show()

## Final Graph 2 - Income vs Diabetes Rate
# INCOME 
income_data = df_brfss.groupby('income')['diabetes_binary'].mean() * 100
income_counts = df_brfss.groupby('income').size()
income_df = pd.DataFrame({
    'Income Group ($)': income_data.index.map({1: ' < $10000', 2: ' $10000 - $15000', 3: ' $15000 - $20000', 4: ' $20000 - $25000', 5: ' $25000 - $35000',
                                               6: ' $35000 - $50000', 7: ' $50000 - $75000', 8: ' $75000 >'}),
    'Diabetes Rate (%)': income_data.values,
    'Count': income_counts.values
})

# Create Plotly line chart
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=income_df['Income Group ($)'],
    y=income_df['Diabetes Rate (%)'],
    mode='lines+markers',
    line=dict(color='#931A23', width=3),
    marker=dict(size=10, color='white', line=dict(color='#A64A47', width=2)),
    customdata=income_df[['Income Group ($)', 'Diabetes Rate (%)', 'Count']],
    hovertemplate='Income: %{customdata[0]}<br>Diabetes Rate (%): %{customdata[1]:.1f}<br>Count: %{customdata[2]:,}<extra></extra>'
))

fig.update_layout(
    title=dict(
        text='Diabetes Rate by Income Group',
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title='Income Group',
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        ticks='outside',
        tickmode='linear',
        tick0=1,
        dtick=1
    ),
    yaxis=dict(
        title='Diabetes Rate (%)',
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    height=500,
    plot_bgcolor='white',
    paper_bgcolor='white',
    hovermode='closest',
    hoverlabel=dict(
        bgcolor="white",
        font_color="black",
        bordercolor="gray"
    )
)

fig.show()

## Graph 3 - Rate of coverage ownership by income group
# no coverage vs income
no_coverage = df_brfss[df_brfss['anyhealthcare'] == 0]
coverageincome_data = (
    no_coverage.groupby('income').size() / 
    df_brfss.groupby('income').size() * 100
)
total_counts = df_brfss.groupby('income').size()
no_coverage_counts = no_coverage.groupby('income').size()

coverageincome_df = pd.DataFrame({
    'Income Group ($)': income_data.index.map({1: ' < $10000', 2: ' $10000 - $15000', 3: ' $15000 - $20000', 4: ' $20000 - $25000', 5: ' $25000 - $35000',
                                               6: ' $35000 - $50000', 7: ' $50000 - $75000', 8: ' $75000 >'}),
    'Persons Lacking Coverage (%)': coverageincome_data.values,
    'Total Count': total_counts.values,
    'No Coverage Count': no_coverage_counts.values
})

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=coverageincome_df['Income Group ($)'],
    y=coverageincome_df['Persons Lacking Coverage (%)'],
    mode='lines+markers',
    line=dict(color='#E8C6AE', width=3),
    marker=dict(size=10, color='white', line=dict(color='#E8C6AE', width=2)),
    customdata=coverageincome_df[['Income Group ($)', 'Persons Lacking Coverage (%)', 'No Coverage Count', 'Total Count']],
    hovertemplate='Income: %{customdata[0]}<br>Persons Lacking Coverage (%): %{customdata[1]:.1f}<br>No Coverage: %{customdata[2]:,}<br>Total: %{customdata[3]:,}<extra></extra>'
))

fig.update_layout(
    title=dict(
        text='Lack of Coverage at each Income Group',
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title='Income Group',
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        ticks='outside',
        tickmode='linear',
        tick0=1,
        dtick=1
    ),
    yaxis=dict(
        title='Persons Lacking Coverage (%)',
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    height=500,
    plot_bgcolor='white',
    paper_bgcolor='white',
    hovermode='closest',
    hoverlabel=dict(
        bgcolor="white",
        font_color="black",
        bordercolor="gray"
    )
)

fig.show()

## Graph 4 - Diabetes vs No. of Access Barriers\
# Create access barrier variable (0, 1, or 2 barriers)
df_brfss['access_barriers'] = 0
df_brfss.loc[df_brfss['anyhealthcare'] == 0, 'access_barriers'] += 1
df_brfss.loc[df_brfss['nodocbccost'] == 1, 'access_barriers'] += 1

# Calculate diabetes rate for each barrier level
barrier_data = df_brfss.groupby('access_barriers')['diabetes_binary'].mean() * 100
barrier_df = pd.DataFrame({
    'Access Barriers': barrier_data.index.map({
        0: '0 Barriers',
        1: '1 Barrier',
        2: '2 Barriers'
    }),
    'Diabetes Rate (%)': barrier_data.values
})

# Prepare data
barrier_df['Access Barriers'] = pd.Categorical(
    barrier_df['Access Barriers'],
    categories=['0 Barriers', '1 Barrier', '2 Barriers'],
    ordered=True
)
barrier_df = barrier_df.sort_values('Access Barriers')

# Create bar chart
fig = go.Figure()

# Create separate trace for each barrier category
colors = ['#931A23', '#E8C6AE', '#DD9C7C']

for i, (idx, row) in enumerate(barrier_df.iterrows()):
    fig.add_trace(go.Bar(
        x=[row['Access Barriers']],
        y=[row['Diabetes Rate (%)']],
        name=row['Access Barriers'],
        marker=dict(
            color=colors[i],
            line=dict(color='white', width=2)
        ),
        text=[f"{row['Diabetes Rate (%)']:.1f}%"],
        textposition='outside',
        textfont=dict(size=12),
        hovertemplate=f"<b>{row['Access Barriers']}</b><br>Diabetes Rate: {row['Diabetes Rate (%)']:.2f}%<extra></extra>",
        showlegend=True
    ))

fig.update_layout(
    title=dict(
        text='Diabetes Rate by Number of Healthcare Access Barriers',
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title='Healthcare Access Barriers',
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        ticks='outside',
        ticklen=5,
        tickwidth=1,
        tickcolor='black',
        categoryorder='array',
        categoryarray=['0 Barriers', '1 Barrier', '2 Barriers']
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
    height=600,
    plot_bgcolor='white',
    paper_bgcolor='white',
    hovermode='closest',
    legend=dict(
        title='Healthcare Access Barriers',
        orientation='v',
        yanchor='top',
        y=1,
        xanchor='right',
        x=1.25
    )
)

fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=False)
fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=False)

fig.show()

# Create donut chart with percentage (hyp 4)
barrier_df['Access Barriers'] = pd.Categorical(
    barrier_df['Access Barriers'],
    categories=['0 Barriers', '1 Barrier', '2 Barriers'],
    ordered=True
)
barrier_df = barrier_df.sort_values('Access Barriers')

fig = go.Figure(data=[go.Pie(
    labels=barrier_df['Access Barriers'],
    values=barrier_df['Diabetes Rate (%)'],
    hole=0.33,
    marker=dict(
        colors=['#931A23', '#E8C6AE', '#DD9C7C'],
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
        text='Diabetes Rate by Number of Healthcare Access Barriers',
        x=0.45,
        xanchor='center'
    ),
    width=700,
    height=700,
    showlegend=True,
    legend=dict(
        title='Healthcare Access Barriers',
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

# Create donut chart no percentage (hyp 4)
barrier_df['Access Barriers'] = pd.Categorical(
    barrier_df['Access Barriers'],
    categories=['0 Barriers', '1 Barrier', '2 Barriers'],
    ordered=True
)
barrier_df = barrier_df.sort_values('Access Barriers')

fig = go.Figure(data=[go.Pie(
    labels=barrier_df['Access Barriers'],
    values=barrier_df['Diabetes Rate (%)'],
    hole=0.33,
    marker=dict(
        colors=['#931A23', '#E8C6AE', '#DD9C7C'],
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
        text='Diabetes Rate by Number of Healthcare Access Barriers',
        x=0.45,
        xanchor='center'
    ),
    width=700,
    height=700,
    showlegend=True,
    legend=dict(
        title='Healthcare Access Barriers',
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