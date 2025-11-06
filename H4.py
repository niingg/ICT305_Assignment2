## import libraries
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

## read dataset
df_brfss = pd.read_csv("diabetes.csv")

## standardising column names 
df_brfss.columns = df_brfss.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-','_')

## Graph 1: Plotting mental health and physical health against diabetes rate
fig = go.Figure() # Create figure

# Diabetes rate (filled area)
fig.add_trace(go.Scatter(
    x=grouped_df.index,
    y=grouped_df['diabetes_binary'],
    name='Diabetes Rate (%)',
    line=dict(color="#FBE35A", width=4),
    fill='tozeroy',
    fillcolor='rgba(251,227,90, 0.4)',
    yaxis='y'
))

# Mental unhealthy days
fig.add_trace(go.Scatter(
    x=grouped_df.index,
    y=grouped_df['menthlth'],
    name='Mental Unhealthy Days',
    line=dict(color="#931A23", width=4),
    fill='tozeroy',
    fillcolor='rgba(147,26,35, 0.4)',
    yaxis='y2'
))

# Physical unhealthy days
fig.add_trace(go.Scatter(
    x=grouped_df.index,
    y=grouped_df['physhlth'],
    name='Physical Unhealthy Days',
    line=dict(color="#C5944B", width=4),
    fill='tozeroy',
    fillcolor='rgba(238,200,163, 0.4)',
    yaxis='y2'
))

# Legends and Hover
fig.update_layout(
    yaxis=dict(title='Diabetes Rate (%)'),
    yaxis2=dict(title='Healthy Days (per month)', overlaying='y', side='right'),
    legend=dict(x=0.5, y=-0.1, xanchor='center', orientation='h'),
    height=500,
    hovermode="closest",
    template="plotly_white"
)

fig.update_traces(
    hovertemplate='%{y:.1f},'
)

fig.show()

## Graph 2: shows 2 variables, physical activity and difficult walking
# This is to create a new data frame for difficult walking , where we find the diabetes rate
# Group and calculate means for diffwalk
diffwalk_data = df_hypo4.groupby('diffwalk').agg({
    'diabetes_binary': lambda x: x.mean() * 100,
    'diffwalk': 'count'
}).rename(columns={'diffwalk': 'Count', 'diabetes_binary': 'Diabetes Rate (%)'})
diffwalk_data['Response'] = diffwalk_data.index.map({0: 'No Difficulty', 1: 'Difficulty'})


# This is to create a new data frame for physical activity, where we find the diabetes rate
# Group and calculate means for physactivity
physactivity_data = df_hypo4.groupby('physactivity').agg({
    'diabetes_binary': lambda x: x.mean() * 100,
    'physactivity': 'count'
}).rename(columns={'physactivity': 'Count', 'diabetes_binary': 'Diabetes Rate (%)'})
physactivity_data['Response'] = physactivity_data.index.map({0: 'No', 1: 'Yes'})

# Create subplots for both variables
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=('Difficulty Walking', 'Physical Activity in the Past Month'),
    horizontal_spacing=0.15
)

# Separate No and Yes for diffwalk
diffwalk_no = diffwalk_data[diffwalk_data['Response'] == 'No Difficulty']
diffwalk_yes = diffwalk_data[diffwalk_data['Response'] == 'Difficulty']

# Separate No and Yes for physactivity
physactivity_no = physactivity_data[physactivity_data['Response'] == 'No']
physactivity_yes = physactivity_data[physactivity_data['Response'] == 'Yes']

# Plot diffwalk bar chart - No
fig.add_trace(go.Bar(
    x=diffwalk_no['Response'],
    y=diffwalk_no['Diabetes Rate (%)'],
    name='No',
    marker=dict(
        color="#E8C6AE",
        line=dict(color='white', width=2)
    ),
    text=[f"{val:.1f}%" for val in diffwalk_no['Diabetes Rate (%)']],
    textposition='outside',
    customdata=diffwalk_no[['Diabetes Rate (%)', 'Count']],
    hovertemplate='%{x} <br> Diabetes Rate: %{customdata[0]:.1f}% <br> Count = %{customdata[1]:,}<extra></extra>',
    hoverlabel=dict(
        bgcolor="#E8C6AE",
        font=dict(color='white')
    ),
    legendgroup='response',
    showlegend=True,
    unselected=dict(marker=dict(opacity=0.5))
), row=1, col=1)

# Plot diffwalk bar chart - Yes
fig.add_trace(go.Bar(
    x=diffwalk_yes['Response'],
    y=diffwalk_yes['Diabetes Rate (%)'],
    name='Yes',
    marker=dict(
        color="#931A23",
        line=dict(color='white', width=2)
    ),
    text=[f"{val:.1f}%" for val in diffwalk_yes['Diabetes Rate (%)']],
    textposition='outside',
    customdata=diffwalk_yes[['Diabetes Rate (%)', 'Count']],
    hovertemplate='%{x} <br> Diabetes Rate: %{customdata[0]:.1f}% <br> Count = %{customdata[1]:,}<extra></extra>',
    hoverlabel=dict(
        bgcolor="#931A23",
        font=dict(color='white')
    ),
    legendgroup='response',
    showlegend=True,
    unselected=dict(marker=dict(opacity=0.5))
), row=1, col=1)

# Plot physactivity bar chart - No
fig.add_trace(go.Bar(
    x=physactivity_no['Response'],
    y=physactivity_no['Diabetes Rate (%)'],
    name='No',
    marker=dict(
        color="#E8C6AE",
        line=dict(color='white', width=2)
    ),
    text=[f"{val:.1f}%" for val in physactivity_no['Diabetes Rate (%)']],
    textposition='outside',
    customdata=physactivity_no[['Diabetes Rate (%)', 'Count']],
    hovertemplate='%{x} <br> Diabetes Rate: %{customdata[0]:.1f}% <br> Count = %{customdata[1]:,}<extra></extra>',
    hoverlabel=dict(
        bgcolor="#E8C6AE",
        font=dict(color='white')
    ),
    legendgroup='response',
    showlegend=False,
    unselected=dict(marker=dict(opacity=0.5))
), row=1, col=2)

# Plot physactivity bar chart - Yes
fig.add_trace(go.Bar(
    x=physactivity_yes['Response'],
    y=physactivity_yes['Diabetes Rate (%)'],
    name='Yes',
    marker=dict(
        color="#931A23",
        line=dict(color='white', width=2)
    ),
    text=[f"{val:.1f}%" for val in physactivity_yes['Diabetes Rate (%)']],
    textposition='outside',
    customdata=physactivity_yes[['Diabetes Rate (%)', 'Count']],
    hovertemplate='%{x} <br> Diabetes Rate: %{customdata[0]:.1f}% <br> Count = %{customdata[1]:,}<extra></extra>',
    hoverlabel=dict(
        bgcolor="#931A23",
        font=dict(color='white')
    ),
    legendgroup='response',
    showlegend=False,
    unselected=dict(marker=dict(opacity=0.5))
), row=1, col=2)

# Update layout
fig.update_xaxes(title_text="Response", row=1, col=1, showgrid=False)
fig.update_xaxes(title_text="Response", row=1, col=2, showgrid=False)
fig.update_yaxes(title_text="Diabetes Rate (%)", row=1, col=1, showgrid=False)
fig.update_yaxes(title_text="Diabetes Rate (%)", row=1, col=2, showgrid=False)

fig.update_layout(
    title_text='Diabetes Rate by Difficulty Walking and Physical Activity',
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
    hovermode='closest',
    dragmode='select',
    clickmode='event+select'
)

fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=False)
fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=False,range=[0,100])

fig.show()

## Graph 3
# Creating the 'Limitations' column

df_brfss['Limitations'] = 0
df_brfss.loc[df_brfss['genhlth'] < 5, 'Limitations'] += 1
df_brfss.loc[df_brfss['physactivity'] == 0, 'Limitations'] += 1
df_brfss.loc[df_brfss['diffwalk'] == 1, 'Limitations'] += 1
df_brfss.loc[df_brfss['physhlth'] < 15, 'Limitations'] += 1
df_brfss.loc[df_brfss['menthlth'] < 15, 'Limitations'] += 1

# Create Bar Chart for the limitations 

#donut_data
donut_data = df_brfss.groupby('Limitations')['diabetes_binary'].mean() * 100
donut_counts = df_brfss.groupby('Limitations').size()

donut_df = pd.DataFrame({
    'Limitations': donut_data.index.map({
        0: 'No Other Limitations', 
        1: '1 Limitations', 
        2: '2 Limitations', 
        3: '3 Limitations', 
        4: '4 Limitations',
        5: '5 Limitations'
    }),
    'Diabetes Rate (%)': donut_data.values,
    'Count': donut_data.values
})

donut_order= [
    'No Other Limitations', 
    '1 Limitations', 
    '2 Limitations', 
    '3 Limitations', 
    '4 Limitations',
    '5 Limitations'
]

donut_df['Limitations'] = pd.Categorical(donut_df['Limitations'], categories=donut_order, ordered=True)
donut_df = donut_df.sort_values('Limitations')

fig = go.Figure()

# Add bars with different colors for each category
colors = ["#FFF1A4", '#EEC8A3', '#DD9C7C', '#D24C49', '#A64A47', '#931A23']

for i, (idx, row) in enumerate(donut_df.iterrows()):
    fig.add_trace(go.Bar(
        x=[row['Limitations']],
        y=[row['Diabetes Rate (%)']],
        name=row['Limitations'],
        marker=dict(color=colors[i]),
        text=[f"{row['Diabetes Rate (%)']:.1f}"],
        textposition='outside',
        textfont=dict(size=10),
        customdata=[[row['Limitations'], row['Diabetes Rate (%)'], row['Count']]],
        hovertemplate='<b>%{customdata[0]}</b><br>Diabetes Rate (%): %{customdata[1]:.1f}<br>Count: %{customdata[2]:,}<extra></extra>',
        showlegend=True,
        selected=dict(marker=dict(opacity=1)),
        unselected=dict(marker=dict(opacity=0.3))
    ))

# Update layout
fig.update_layout(
    title=dict(
        text='Diabetes Rate by No. of Pre-Existing Limitations',
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title='No. of Pre-Existing Conditions<br>(Physical Activity, General Health, Mental Health, Physical Health, Difficulty Walking)',
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        ticks='outside',
        ticklen=5,
        tickwidth=1,
        tickcolor='black',
        tickangle=0     
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
# Change the y-axis (diabetes range) to 100
fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=False)
fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=False,range=[0,100])

fig.show()

## Graph 4: compares the physical activity to the diabetes rates over 3 variables, BMI, Sex, and Age
# Create 5 age groups based on the original age categories
def map_age_to_range(age_cat):
    if age_cat in [1, 2]:  # 18-24, 25-29
        return '18-29'
    elif age_cat in [3, 4, 5]:  # 30-34, 35-39, 40-44
        return '30-44'
    elif age_cat in [6, 7, 8]:  # 45-49, 50-54, 55-59
        return '45-59'
    elif age_cat in [9, 10, 11]:  # 60-64, 65-69, 70-74
        return '60-74'
    else:  # 12, 13 (75-79, 80+)
        return '75+'

# Map sex categories
sex_mapping = {0: 'Female', 1: 'Male'}

# Create BMI categories for grouping
df_brfss['bmi_category'] = pd.cut(df_brfss['bmi'], 
                                    bins=[0, 18.5, 25, 30, 100],
                                    labels=['Underweight', 'Normal', 'Overweight', 'Obese'])

# Map all categories
df_brfss['age_group'] = df_brfss['age'].apply(map_age_to_range)
df_brfss['sex_label'] = df_brfss['sex'].map(sex_mapping)
df_brfss['physactivity_label'] = df_brfss['physactivity'].map({0: 'No', 1: 'Yes'})

# Function to calculate diabetes rate by physical activity and grouping variable
def calculate_rates(group_by_col):
    results = df_brfss.groupby([group_by_col, 'physactivity_label']).agg({
        'diabetes_binary': ['mean', 'count']
    }).reset_index()
    
    results.columns = [group_by_col, 'PhysActivity', 'Diabetes Rate', 'Count']
    results['Diabetes Rate (%)'] = results['Diabetes Rate'] * 100
    
    return results

# Calculate for all three grouping options
age_data = calculate_rates('age_group')
sex_data = calculate_rates('sex_label')
bmi_data = calculate_rates('bmi_category')

# Order age groups properly
age_order = ['18-29', '30-44', '45-59', '60-74', '75+']
age_data['age_group'] = pd.Categorical(age_data['age_group'], categories=age_order, ordered=True)
age_data = age_data.sort_values('age_group')

# Define colors
color_no = "#E8C6AE"
color_yes = "#931A23"

# Create figure with dropdown
fig = go.Figure()

# Function to add traces for a grouping
def add_traces(data, group_col, visible=True):
    if group_col == 'age_group':
        groups = age_order
    else:
        groups = data[group_col].unique()
    
    for group in groups:
        group_data = data[data[group_col] == group]
        
        # No Physical Activity bars
        no_activity = group_data[group_data['PhysActivity'] == 'No']
        if not no_activity.empty:
            fig.add_trace(go.Bar(
                name='No',
                x=[group],
                y=no_activity['Diabetes Rate (%)'].values,
                marker=dict(color=color_no, line=dict(color='white', width=2)),
                text=[f"{val:.1f}%" for val in no_activity['Diabetes Rate (%)'].values],
                textposition='outside',
                customdata=np.column_stack((no_activity['Diabetes Rate (%)'].values, 
                                           no_activity['Count'].values,
                                           [group] * len(no_activity))),
                hovertemplate='<b>%{customdata[2]}</b><br>No Physical Activity<br>Diabetes Rate: %{customdata[0]:.1f}%<br>Count: %{customdata[1]:,}<extra></extra>',
                hoverlabel=dict(bgcolor=color_no, font=dict(color='white')),
                legendgroup='No',
                showlegend=(group == groups[0]),
                visible=visible,
                offsetgroup=0
            ))
        
        # Yes Physical Activity bars
        yes_activity = group_data[group_data['PhysActivity'] == 'Yes']
        if not yes_activity.empty:
            fig.add_trace(go.Bar(
                name='Yes',
                x=[group],
                y=yes_activity['Diabetes Rate (%)'].values,
                marker=dict(color=color_yes, line=dict(color='white', width=2)),
                text=[f"{val:.1f}%" for val in yes_activity['Diabetes Rate (%)'].values],
                textposition='outside',
                customdata=np.column_stack((yes_activity['Diabetes Rate (%)'].values,
                                           yes_activity['Count'].values,
                                           [group] * len(yes_activity))),
                hovertemplate='<b>%{customdata[2]}</b><br>Yes Physical Activity<br>Diabetes Rate: %{customdata[0]:.1f}%<br>Count: %{customdata[1]:,}<extra></extra>',
                hoverlabel=dict(bgcolor=color_yes, font=dict(color='white')),
                legendgroup='Yes',
                showlegend=(group == groups[0]),
                visible=visible,
                offsetgroup=1
            ))

# Add traces for Age Group (visible by default)
add_traces(age_data, 'age_group', visible=True)

# Count traces for age group
age_trace_count = len([t for t in fig.data])

# Add traces for Sex (hidden initially)
add_traces(sex_data, 'sex_label', visible=False)
sex_trace_count = len([t for t in fig.data]) - age_trace_count

# Add traces for BMI (hidden initially)
add_traces(bmi_data, 'bmi_category', visible=False)
bmi_trace_count = len([t for t in fig.data]) - age_trace_count - sex_trace_count

# Create dropdown menu
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
            x=0.15,
            xanchor="right",
            y=1.15,
            yanchor="top",
            bgcolor="white",
            bordercolor="black",
            borderwidth=1
        ),
    ]
)

# Update layout
fig.update_layout(
    title={
        'text': 'Physical Activity vs. Diabetes Rate by Demographic Groups',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 20, 'color': '#2C3E50'}
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
        mirror=False
    ),
    barmode='group',
    height=600,
    width=1000,
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
    hoverlabel=dict(
        font_size=12
    )
)

# Change the y-axis (diabetes range) to 100
fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=False)
fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=False,range=[0,100])

fig.show()


