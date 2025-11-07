"""
Hypothesis 2: Education and Diabetes Prevention
Module for creating visualizations showing the relationship between education and diabetes risk/prevention.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Color Constants
PRIMARY = "#931A23"        # Your brand
SECONDARY = "#E8C6AE"      # Accent
GRID = "rgba(0, 0, 0, 0.08)"
CHART_COLORS = ["#FFF1A4", '#EEC8A3', '#DD9C7C', '#D24C49', '#A64A47', '#931A23']


def create_education_health_behaviors_chart(df):
    """
    Create grouped bar chart showing health behaviors improve with higher education.
    
    Shows prevalence of Healthy Diet, Physical Activity, and Regular Checkups by education level.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The diabetes dataset
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Grouped bar chart showing health behaviors by education
    """
    df = df.copy()
    df.columns = df.columns.str.lower()
    
    edu_col = "educa" if "educa" in df.columns else "education"
    map4 = {1:"Less than HS", 2:"Less than HS", 3:"Less than HS",
            4:"HS Graduate", 5:"Some College", 6:"College Grad"}
    order4 = ["Less than HS","HS Graduate","Some College","College Grad"]
    
    edu_num = pd.to_numeric(df.get(edu_col), errors="coerce")
    df = df.dropna(subset=[edu_col]).copy()
    df["Education"] = pd.Categorical(edu_num.map(map4), categories=order4, ordered=True)
    
    def as01(s):
        s = pd.to_numeric(df.get(s), errors="coerce")
        return s.where(s.isin([0,1])).fillna(0).astype(int)
    
    if {"fruits","veggies"}.issubset(df.columns):
        fruits  = as01("fruits")
        veggies = as01("veggies")
        df["Healthy Diet"] = ((fruits==1) & (veggies==1)).astype(int)
    elif "fruits" in df.columns:
        df["Healthy Diet"] = as01("fruits")
    else:
        df["Healthy Diet"] = as01("veggies") if "veggies" in df.columns else 0
    
    df["Physical Activity"] = as01("physactivity") if "physactivity" in df.columns else 0
    
    if "cholcheck" in df.columns:
        df["Regular Checkups"] = as01("cholcheck")
    elif "anyhealthcare" in df.columns:
        df["Regular Checkups"] = as01("anyhealthcare")
    else:
        df["Regular Checkups"] = 0
    
    agg = (df.groupby("Education", observed=True)[
            ["Healthy Diet","Physical Activity","Regular Checkups"]
          ].mean().mul(100).reset_index())
    
    long = agg.melt(id_vars="Education", var_name="Metric", value_name="Prevalence")
    
    # Colors
    colors = {
        "Healthy Diet":      "#8C1D18",
        "Physical Activity": "#C94B44",
        "Regular Checkups":  "#ECD9C6",
    }
    
    fig = px.bar(
        long, x="Education", y="Prevalence", color="Metric",
        barmode="group", text="Prevalence",
        color_discrete_map=colors,
        title="Higher education predicts better health behaviors across domains",
        labels={"Prevalence":"Prevalence (%)"},
        category_orders={"Education": order4,
                         "Metric": ["Healthy Diet","Physical Activity","Regular Checkups"]},
        template="simple_white"
    )
    
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white',
        yaxis_range=[0, 100],
        hovermode='x unified',
    )
    
    return fig


def create_education_diabetes_trend_chart(df):
    """
    Create line chart showing diabetes rate declines with higher education.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The diabetes dataset
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Line chart showing diabetes trends by education
    """
    df = df.copy()
    df.columns = df.columns.str.lower()
    
    EDU_MAP = {
        1: "Less than HS",
        2: "Less than HS",
        3: "Less than HS",
        4: "HS Graduate",
        5: "Some College",
        6: "College Grad"
    }
    order4 = ["Less than HS","HS Graduate","Some College","College Grad"]
    
    df = df.dropna(subset=["diabetes_binary"])
    
    edu_col = "educa" if "educa" in df.columns else "education"
    edu_num = pd.to_numeric(df.get(edu_col), errors="coerce")
    df = df.dropna(subset=[edu_col]).copy()
    df["edu4"] = pd.Categorical(edu_num.map(EDU_MAP), categories=order4, ordered=True)
    
    diab = (pd.to_numeric(df["diabetes_binary"], errors="coerce") == 1).astype(int)
    g = df.assign(d=diab).groupby("edu4", observed=True)["d"]
    tab = (g.agg(n="count", cases="sum", prev="mean")
             .reset_index()
             .rename(columns={"edu4":"Education"}))
    tab["rate"] = (tab["prev"]*100)
    
    # plot
    x  = tab["Education"].astype(str)
    y  = tab["rate"]
    
    fig = go.Figure()
    
    ymax = min(100.0, max(5.0, float(y.max())*1.25))
    for i, y0 in enumerate(np.arange(0, ymax, 10)):
        if i % 2 == 0:
            fig.add_hrect(y0=y0, y1=min(y0+10, ymax),
                          fillcolor="#F2F4F7", line_width=0, layer="below")
    
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines+markers+text",
        line=dict(color="#A64A47", width=3),
        marker=dict(size=9, color="white", line=dict(color="#A64A47", width=2)),
        text=[f"{v:.1f}%" for v in y],
        textposition="top center",
        hovertemplate="%{x}<br>Diabetes Rate: %{y:.1f}%<br>n=%{customdata[0]}  cases=%{customdata[1]}<extra></extra>",
        customdata=np.c_[tab["n"], tab["cases"]],
        name="Diabetes rate"
    ))
    
    fig.update_layout(
        title="Diabetes Rate Declines with Higher Education (4 groups)",
        template="simple_white",
        margin=dict(l=70, r=30, t=80, b=70),
        xaxis=dict(title="Education Level", showgrid=False),
        yaxis=dict(title="Diabetes Rate (%)", range=[0, ymax], dtick=10, showgrid=False),
        showlegend=False,
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white',
    )
    
    return fig


def create_income_diabetes_by_education_chart(df):
    """
    Create heatmap showing diabetes rates by income and education level.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The diabetes dataset
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Heatmap showing income vs education impact on diabetes
    """
    df = df.copy()
    df.columns = df.columns.str.lower()
    
    INCOME_MAP = {1:"< $10k", 2:"$10–15k", 3:"$15–20k", 4:"$20–25k",
                  5:"$25–35k", 6:"$35–50k", 7:"$50–75k", 8:"≥ $75k"}
    INC_ORDER = [INCOME_MAP[k] for k in (1,2,3,4,5,6,7,8)]
    
    EDU_MAP = {
        1: "K-only",
        2: "Grades 1–8",
        3: "Grades 9–11",
        4: "HS Grad",
        5: "Some College",
        6: "College+",
    }
    EDU_ORDER = [EDU_MAP[k] for k in (1,2,3,4,5,6)]
    
    # Clean data
    db = pd.to_numeric(df.get("diabetes_binary"), errors="coerce")
    df["diabetes"] = (db == 1).astype(int)
    
    edu = pd.to_numeric(df.get("education"), errors="coerce").astype("Int64")
    df["education_lbl"] = pd.Categorical(edu.map(EDU_MAP), categories=EDU_ORDER, ordered=True)
    
    inc = pd.to_numeric(df.get("income"), errors="coerce").astype("Int64")
    df["income_lbl"] = pd.Categorical(inc.map(INCOME_MAP), categories=INC_ORDER, ordered=True)
    
    # Aggregate
    df = df.dropna(subset=["education_lbl", "income_lbl", "diabetes"])
    pivot = (df.groupby(["education_lbl", "income_lbl"], observed=True)["diabetes"]
             .mean()
             .mul(100)
             .reset_index()
             .pivot(index="education_lbl", columns="income_lbl", values="diabetes"))
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale=[[0, "#FFE8E8"], [1, "#931A23"]],
        text=np.round(pivot.values, 1),
        texttemplate="%{text:.1f}%",
        textfont={"size":10},
        colorbar=dict(title="Diabetes<br>Rate (%)"),
        hovertemplate="Education: %{y}<br>Income: %{x}<br>Diabetes Rate: %{z:.1f}%<extra></extra>",
    ))
    
    fig.update_layout(
        title="Diabetes Rate by Income and Education Level",
        xaxis_title="Income Level",
        yaxis_title="Education Level",
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white',
    )
    
    return fig


def create_education_lifestyle_diabetes_chart(df):
    """
    Create line chart showing education's impact on lifestyle factors and diabetes.
    
    Shows trends for physical activity, fruit/veg intake, and diabetes across education levels.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The diabetes dataset
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Multi-line chart with lifestyle and diabetes trends
    """
    df = df.copy()
    df.columns = df.columns.str.lower()
    
    COLOR_ACTIVE = "#386cb0"
    COLOR_FRUIT  = "#66a61e"
    COLOR_VEG    = "#e6ab02"
    COLOR_DIAB   = "#a64a47"
    
    EDU_MAP = {
        1: "K-only",
        2: "Grades 1–8",
        3: "Grades 9–11",
        4: "HS Grad",
        5: "Some College",
        6: "College+",
    }
    EDU_ORDER = [EDU_MAP[k] for k in (1,2,3,4,5,6)]
    
    # Normalize
    edu = pd.to_numeric(df.get("education"), errors="coerce").astype("Int64")
    df["education_lbl"] = edu.map(EDU_MAP)
    df["education_lbl"] = pd.Categorical(df["education_lbl"], categories=EDU_ORDER, ordered=True)
    
    db = pd.to_numeric(df.get("diabetes_binary"), errors="coerce")
    df["diabetes"] = db.astype(int) if db.dropna().isin([0,1]).all() else (db == 1).astype(int)
    
    def _as01(col):
        s = pd.to_numeric(df.get(col), errors="coerce")
        return s.where(s.isin([0,1]), np.nan)
    
    df["phys_ok"]   = _as01("physactivity")   # 1 = active
    df["fruit_ok"]  = _as01("fruits")         # 1 = eats fruit (not low)
    df["veg_ok"]    = _as01("veggies")        # 1 = eats veg (not low)
    
    df = df.dropna(subset=["education_lbl", "diabetes"])
    
    # Aggregate
    grp = (df.groupby("education_lbl", observed=True)
             .agg(n=("diabetes","size"),
                  diab=("diabetes","mean"),
                  phys_rate=("phys_ok","mean"),
                  fruit_rate=("fruit_ok","mean"),
                  veg_rate=("veg_ok","mean"))
             .reset_index())
    
    grp["phys_pct"] = grp["phys_rate"] * 100
    grp["fruit_pct"] = grp["fruit_rate"] * 100
    grp["veg_pct"] = grp["veg_rate"] * 100
    grp["diab_pct"] = grp["diab"] * 100
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=grp["education_lbl"].astype(str), y=grp["phys_pct"],
        mode="lines+markers", name="Physical Activity",
        line=dict(color=COLOR_ACTIVE, width=2.5),
        marker=dict(size=7),
    ))
    
    fig.add_trace(go.Scatter(
        x=grp["education_lbl"].astype(str), y=grp["fruit_pct"],
        mode="lines+markers", name="Eat Fruit",
        line=dict(color=COLOR_FRUIT, width=2.5),
        marker=dict(size=7),
    ))
    
    fig.add_trace(go.Scatter(
        x=grp["education_lbl"].astype(str), y=grp["veg_pct"],
        mode="lines+markers", name="Eat Vegetables",
        line=dict(color=COLOR_VEG, width=2.5),
        marker=dict(size=7),
    ))
    
    fig.add_trace(go.Scatter(
        x=grp["education_lbl"].astype(str), y=grp["diab_pct"],
        mode="lines+markers", name="Diabetes Rate",
        line=dict(color=COLOR_DIAB, width=2.5, dash="dash"),
        marker=dict(size=7),
    ))
    
    fig.update_layout(
        title="Education vs Lifestyle Factors and Diabetes",
        xaxis_title="Education Level",
        yaxis_title="Prevalence (%)",
        template="simple_white",
        hovermode="x unified",
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(x=0.02, y=0.98),
    )
    
    fig.update_yaxes(range=[0, 100])
    
    return fig