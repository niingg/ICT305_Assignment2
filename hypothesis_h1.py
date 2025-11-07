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
        marker=dict(color=PRIMARY, line=dict(width=1, color=GRID)),
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


def create_physical_activity_by_demographics_chart(df, facet_type="education"):
    """
    Create faceted bar charts showing physical activity vs diabetes by education, age, or sex.
    
    Shows diabetes rates for active vs inactive people across different demographic groups.
    Each demographic is shown in its own facet for easy comparison.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The diabetes dataset
    facet_type : str
        Which demographic to facet by: "education", "age", or "sex"
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Faceted bar charts
    """
    df = df.copy()
    df.columns = df.columns.str.lower()
    
    import plotly.express as px
    
    EDU_MAP = {
        1: "K-only / None",
        2: "Grades 1–8",
        3: "Grades 9–11",
        4: "HS Grad / GED",
        5: "Some College / AA",
        6: "College 4+",
    }
    EDU_ORDER = [EDU_MAP[k] for k in (1,2,3,4,5,6)]
    AGE_ORDER = ["18–29","30–44","45–59","60–74","75+"]
    
    COLOR_NO  = PRIMARY   # inactive
    COLOR_YES = SECONDARY  # active
    
    # Normalize data
    db = pd.to_numeric(df.get("diabetes_binary"), errors="coerce")
    df["diabetes"] = (db == 1).astype(float)
    
    # physactivity -> Yes/No
    pa = pd.to_numeric(df.get("physactivity"), errors="coerce")
    pa = pa.where(pa.isin([0,1]), np.where(pa == 1, 1, 0))
    df["phys_lbl"] = np.where(pa == 1, "Yes", "No")
    
    # Age groups
    age = pd.to_numeric(df.get("age"), errors="coerce")
    if age.dropna().between(1,13).all():
        def map_agecode(a):
            if a in (1,2): return "18–29"
            if a in (3,4,5): return "30–44"
            if a in (6,7,8): return "45–59"
            if a in (9,10,11): return "60–74"
            if a in (12,13): return "75+"
            return np.nan
        df["agegroup"] = age.astype("Int64").map(map_agecode)
    else:
        df["agegroup"] = pd.cut(age, [18,30,45,60,75,np.inf],
                                labels=AGE_ORDER, right=False, include_lowest=True)
    
    # Education
    edu = pd.to_numeric(df.get("education"), errors="coerce").astype("Int64")
    df["education_lbl"] = pd.Categorical(edu.map(EDU_MAP),
                                         categories=EDU_ORDER, ordered=True)
    
    # Sex
    s = pd.to_numeric(df.get("sex"), errors="coerce")
    if s.dropna().isin([0,1]).all():
        df["sex_lbl"] = s.map({0:"Female", 1:"Male"})
    elif s.dropna().isin([1,2]).all():
        df["sex_lbl"] = s.map({1:"Male", 2:"Female"})
    else:
        df["sex_lbl"] = np.nan
    
    # Helper function to make table
    def make_table(df_in, facet_var):
        sub = df_in.dropna(subset=["diabetes","phys_lbl", facet_var]).copy()
        g = (sub.groupby([facet_var, "phys_lbl"], observed=True)
               .agg(n=("diabetes","size"), cases=("diabetes","sum"))
               .reset_index())
        g["prev"] = g["cases"] / g["n"]
        g["phys_lbl"] = pd.Categorical(g["phys_lbl"], ["No","Yes"], ordered=True)
        if facet_var == "agegroup":
            g["agegroup"] = pd.Categorical(g["agegroup"], AGE_ORDER, ordered=True)
        if facet_var == "education_lbl":
            g["education_lbl"] = pd.Categorical(g["education_lbl"], EDU_ORDER, ordered=True)
        return g.sort_values([facet_var, "phys_lbl"]).reset_index(drop=True)
    
    # Select which table to use
    if facet_type == "education":
        tbl = make_table(df, "education_lbl")
        facet_var = "education_lbl"
        title_note = "Education"
    elif facet_type == "age":
        tbl = make_table(df, "agegroup")
        facet_var = "agegroup"
        title_note = "Age Group"
    else:  # sex
        tbl = make_table(df, "sex_lbl")
        facet_var = "sex_lbl"
        title_note = "Sex"
    
    # Create faceted plot
    fig = px.bar(
        tbl, x="phys_lbl", y="prev",
        facet_col=facet_var, facet_col_wrap=3,
        color="phys_lbl",
        color_discrete_map={"No": COLOR_NO, "Yes": COLOR_YES},
        text=tbl["prev"].map(lambda v: f"{v:.0%}"),
        title=f"Physical Activity vs Diabetes by {title_note}<br><sup>% with diabetes — faceted</sup>"
    )
    fig.update_traces(
        marker_line_width=1, marker_line_color=GRID,
        textposition="outside",
        hovertemplate="%{x}<br>%{y:.1%}<extra></extra>",
        showlegend=False,
    )
    fig.for_each_yaxis(lambda a: a.update(title="% Diabetes", tickformat=".0%", dtick=0.10, range=[0,1], gridcolor=GRID))
    fig.for_each_xaxis(lambda a: a.update(title="Physically Active"))
    fig.update_layout(
        template="simple_white", 
        bargap=0.35, 
        showlegend=False,
        margin=dict(l=50, r=20, t=90, b=50),
        height=600,
        plot_bgcolor=BACKGROUND,
        paper_bgcolor=BACKGROUND,
    )
    
    return fig