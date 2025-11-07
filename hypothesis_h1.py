"""
Hypothesis 1: Lifestyle Habits and Diabetes
Module for creating visualizations showing the relationship between lifestyle habits and diabetes risk.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Color Constants
PRIMARY = "#931A23"        # Your brand
SECONDARY = "#E8C6AE"      # Accent
BACKGROUND = "white"
GRID = "rgba(0, 0, 0, 0.08)"
CHART_COLORS = ["#FFF1A4", '#EEC8A3', '#DD9C7C', '#D24C49', '#A64A47', '#931A23']


def wilson(success, n, z=1.96):
    """Calculate Wilson score confidence interval"""
    if n == 0:
        return (np.nan, np.nan)
    p = success / n
    denom = 1 + z**2/n
    center = (p + z**2/(2*n)) / denom
    half = (z*np.sqrt((p*(1-p) + z**2/(4*n)) / n)) / denom
    return center - half, center + half


def row_stats(df, col, risk_value):
    """Calculate statistics for a risk factor"""
    # With risk
    a = df[df[col] == risk_value]['diabetes_binary']
    n1, c1 = a.count(), a.sum()
    p1 = c1 / n1 if n1 else np.nan
    lo1, hi1 = wilson(c1, n1)
    
    # Without risk
    b = df[df[col] != risk_value]['diabetes_binary']
    n0, c0 = b.count(), b.sum()
    p0 = c0 / n0 if n0 else np.nan
    lo0, hi0 = wilson(c0, n0)
    
    return p1, lo1, hi1, n1, int(c1), p0, lo0, hi0, n0, int(c0)


def create_individual_lifestyle_factors_chart(df):
    """
    Create grouped bar chart comparing diabetes rates with vs without individual lifestyle risk factors.
    
    Includes confidence intervals (Wilson score) for each estimate.
    
    Factors: Smoking, Physical Activity, Fruit Intake, Vegetable Intake
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The diabetes dataset
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Grouped bar chart with error bars
    """
    df = df.copy()
    df.columns = df.columns.str.lower()
    
    FACTOR_ORDER = [
        ("smoker", "Smoking"),
        ("physactivity", "No Physical Activity"),
        ("fruits", "Low Fruit Intake"),
        ("veggies", "Low Veggie Intake"),
    ]
    RISK_VALUE = {"smoker": 1, "physactivity": 0, "fruits": 0, "veggies": 0}
    
    rows = []
    for col, label in FACTOR_ORDER:
        if col in df.columns:
            p1, lo1, hi1, n1, c1, p0, lo0, hi0, n0, c0 = row_stats(df, col, RISK_VALUE[col])
            rows.append({
                "Factor": label,
                "with_prev": p1, "with_lo": lo1, "with_hi": hi1, "with_n": n1, "with_cases": c1,
                "without_prev": p0, "without_lo": lo0, "without_hi": hi0, "without_n": n0, "without_cases": c0
            })
    
    tbl = pd.DataFrame(rows)
    
    ymax = float(pd.concat([tbl["with_prev"], tbl["without_prev"]]).max()) * 1.25
    ymax = max(0.05, ymax)
    
    fig = go.Figure()
    
    for i, y0 in enumerate(np.arange(0, ymax, 0.10)):
        if i % 2 == 0:
            fig.add_hrect(y0=y0, y1=min(y0+0.10, ymax),
                          fillcolor=BACKGROUND, line_width=0, layer="below")
    
    hover = "Factor: %{x}<br>%{fullData.name}: %{y:.1%}<br>n=%{customdata[0]}  cases=%{customdata[1]}<extra></extra>"
    
    fig.add_bar(
        name="With Risk", legendgroup="With Risk",
        x=tbl["Factor"], y=tbl["with_prev"],
        error_y=dict(type="data", array=tbl["with_hi"]-tbl["with_prev"],
                     arrayminus=tbl["with_prev"]-tbl["with_lo"], thickness=1),
        text=tbl["with_prev"].map(lambda v:f"{v:.1%}"), textposition="outside",
        marker=dict(color=PRIMARY, line=dict(color=GRID, width=1)),
        customdata=np.stack([tbl["with_n"], tbl["with_cases"]], axis=-1),
        hovertemplate=hover,
    )
    
    fig.add_bar(
        name="Without Risk", legendgroup="Without Risk",
        x=tbl["Factor"], y=tbl["without_prev"],
        error_y=dict(type="data", array=tbl["without_hi"]-tbl["without_prev"],
                     arrayminus=tbl["without_prev"]-tbl["without_lo"], thickness=1),
        text=tbl["without_prev"].map(lambda v:f"{v:.1%}"), textposition="outside",
        marker=dict(color=SECONDARY, line=dict(color=GRID, width=1)),
        customdata=np.stack([tbl["without_n"], tbl["without_cases"]], axis=-1),
        hovertemplate=hover,
    )
    
    fig.update_traces(cliponaxis=False, textfont_size=11)
    
    fig.update_layout(
        title=dict(text="Individual Lifestyle Factors<br><sup>Diabetes rate with vs without risk</sup>", x=0.02, xanchor="left"),
        barmode="group", bargap=0.28, bargroupgap=0.14,
        xaxis=dict(title="", showgrid=False, tickangle=0),
        yaxis=dict(title="Diabetes Rate (%)", tickformat=".0%", dtick=0.10,
                   range=[0, ymax], showgrid=False),
        legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.18),
        template="simple_white",
        paper_bgcolor=BACKGROUND, plot_bgcolor=BACKGROUND,
        margin=dict(l=70, r=30, t=80, b=90),
        height=500,
    )
    
    return fig



def create_risk_factors_chart(df):
    """
    Create a bar chart showing diabetes prevalence increases with multiple lifestyle risk factors.
    
    Counts lifestyle risks per person: smoking, inactivity, low fruit/veg, heavy alcohol.
    Shows diabetes prevalence for 0, 1, 2, 3, 4+ factors.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The diabetes dataset
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Bar chart with soft background bands
    """
    df = df.copy()
    df.columns = df.columns.str.lower()
    
    cols = {
        "smoke":    ("smoker",            1),
        "inactive": ("physactivity",      0),
        "lowfruit": ("fruits",            0),
        "lowveg":   ("veggies",           0),
        "heavyalc": ("hvyalcoholconsump", 1),
    }
    
    rb = pd.DataFrame(index=df.index)
    for new, (col, risky) in cols.items():
        if col in df.columns:
            rb[new] = (pd.to_numeric(df[col], errors="coerce") == risky).astype(int)
    
    if rb.shape[1] == 0:
        rb["none"] = 0
    
    df["risk_behaviors"] = rb.sum(axis=1).fillna(0).astype(int)
    
    order = ["0 factors", "1 factor", "2 factors", "3 factors", "4+ factors"]
    labels = lambda k: "4+ factors" if k >= 4 else f"{k} factor{'s' if k != 1 else ''}"
    
    prev_rb = (df.assign(diabetes_binary=(pd.to_numeric(df["diabetes_binary"], errors="coerce") == 1).astype(float))
                 .groupby("risk_behaviors", as_index=False)["diabetes_binary"].mean()
                 .rename(columns={"diabetes_binary":"prevalence"}))
    
    prev_rb["group"] = prev_rb["risk_behaviors"].map(labels)
    prev_rb = (prev_rb.groupby("group", as_index=False)["prevalence"].mean())
    prev_rb["group"] = pd.Categorical(prev_rb["group"], categories=order, ordered=True)
    prev_rb = prev_rb.sort_values("group")
    
    # Plot
    ymax = min(1.0, max(0.05, float(prev_rb["prevalence"].max()) * 1.25))
    step = 0.10
    
    fig = go.Figure(go.Bar(
        x=prev_rb["group"].astype(str),
        y=prev_rb["prevalence"],
        text=(prev_rb["prevalence"]*100).round(1).astype(str) + "%",
        textposition="outside",
        marker=dict(color=CHART_COLORS, line=dict(width=1, color=GRID)),
        hovertemplate="<b>%{x}</b><br>Diabetes rate: %{y:.1%}<extra></extra>",
        cliponaxis=False
    ))
    
    for i, y0 in enumerate(np.arange(0, ymax, step)):
        if i % 2 == 0:
            fig.add_hrect(y0=y0, y1=min(y0+step, ymax),
                          fillcolor=BACKGROUND, line_width=0, layer="below")
    
    fig.update_layout(
        title=dict(text="Diabetes prevalence increases with multiple lifestyle risk factors", x=0.02),
        template="simple_white",
        barmode="group",
        xaxis=dict(title="Number of Risk Factors", showgrid=False),
        yaxis=dict(title="Diabetes Prevalence", range=[0, ymax], dtick=0.1, tickformat=".0%", showgrid=False),
        showlegend=False,
        height=500,
        plot_bgcolor=BACKGROUND,
        paper_bgcolor=BACKGROUND,
    )
    
    return fig


def create_physical_activity_by_demographics_chart(df, demographic="Age Group"):
    """
    Create an interactive chart showing diabetes rates by physical activity
    across a selected demographic.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The diabetes dataset
    demographic : str
        One of: "Age Group", "Sex", "BMI Category"
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Plotly figure showing the selected demographic view
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
    
    # Select data based on demographic parameter
    if demographic == "Age Group":
        data = age_data
        group_col = 'age_group'
        groups_order = age_order
        x_title = "Age Group"
    elif demographic == "Sex":
        data = sex_data
        group_col = 'sex_label'
        groups_order = None
        x_title = "Sex"
    else:  # BMI Category
        data = bmi_data
        group_col = 'bmi_category'
        groups_order = bmi_order
        x_title = "BMI Category"
    
    color_no = "#E8C6AE"
    color_yes = "#931A23"
    
    fig = go.Figure()
    
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
                offsetgroup=1
            ))
    
    fig.update_layout(
        title={
            'text': 'Physical Activity vs. Diabetes Rate by Demographics',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        xaxis=dict(
            title=x_title,
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

