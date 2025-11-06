##imports
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from ipywidgets import VBox, HBox, Dropdown, ToggleButtons, Output
from IPython.display import display

## read dataset
df_brfss = pd.read_csv("diabetes.csv")

## standardising column names 
df_brfss.columns = df_brfss.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-','_')

## higher education levels predict better health behaiviours accroos domains
df = df_brfss.copy()
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

# Plot 
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

fig.update_layout(shapes=[
    dict(type="rect", xref="paper", x0=0, x1=1, y0=y, y1=min(y+20,100),
         layer="below", line=dict(width=0), fillcolor="#F2F4F7")
    for i, y in enumerate(np.arange(0, 100, 20)) if i % 2 == 0
])

fig.update_traces(
    texttemplate="%{text:.0f}%",
    textposition="outside",
    cliponaxis=False,
    hovertemplate="<b>%{x}</b><br>%{fullData.name}: %{y:.0f}%<extra></extra>"
)

fig.update_layout(
    yaxis=dict(range=[0,100], dtick=20, title="Prevalence (%)", showgrid=False),
    xaxis=dict(title="Education Level", showgrid=False),
    legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.22),
    bargap=0.28, bargroupgap=0.16,
    margin=dict(l=70, r=40, t=80, b=100),
    uniformtext_minsize=10, uniformtext_mode="hide",
    paper_bgcolor="white", plot_bgcolor="white"
)

fig.show()

## diabetes rate declines with higher education abt the disease
df = df_brfss.dropna(subset=["diabetes_binary"]).copy()
df.columns = df.columns.str.lower()

edu_col = "educa" if "educa" in df.columns else "education"
map4   = {1:"Less than HS", 2:"Less than HS", 3:"Less than HS",
          4:"HS Graduate",  5:"Some College", 6:"College Grad"}
order4 = ["Less than HS","HS Graduate","Some College","College Grad"]

edu_num = pd.to_numeric(df.get(edu_col), errors="coerce")
df = df.dropna(subset=[edu_col]).copy()
df["edu4"] = pd.Categorical(edu_num.map(map4), categories=order4, ordered=True)

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
    showlegend=False
)

fig.show()

## Income vs Diabetes by Education Group 
INCOME_MAP = {1:"< $10k", 2:"$10–15k", 3:"$15–20k", 4:"$20–25k",
              5:"$25–35k", 6:"$35–50k", 7:"$50–75k", 8:"≥ $75k"}
INC_ORDER = [INCOME_MAP[k] for k in (1,2,3,4,5,6,7,8)]

AGE_ORDER  = ["18–29","30–44","45–59","60–74","75+"]
RED_PALETTE = ["#fde0dd", "#fcbba1", "#fc9272", "#fb6a4a", "#ef3b2c", "#cb181d"]

def _clean_ei(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = df_raw.copy()
    df.columns = df.columns.str.lower()

    db = pd.to_numeric(df.get("diabetes_binary"), errors="coerce")
    df["diabetes"] = (db == 1).astype(int)

    edu = pd.to_numeric(df.get("education"), errors="coerce").astype("Int64")
    df["education_lbl"] = pd.Categorical(edu.map(EDU_MAP), categories=EDU_ORDER, ordered=True)

    inc = pd.to_numeric(df.get("income"), errors="coerce").astype("Int64")
    df["income_lbl"] = pd.Categorical(inc.map(INCOME_MAP), categories=INC_ORDER, ordered=True)

    sex_raw = df.get("sex")
    if sex_raw is not None:
        s = pd.to_numeric(sex_raw, errors="coerce")
        if s.dropna().isin([0,1]).all():
            df["sex_lbl"] = s.map({0:"Female", 1:"Male"})
        elif s.dropna().isin([1,2]).all():
            df["sex_lbl"] = s.map({1:"Male", 2:"Female"})
        else:
            v = sex_raw.astype(str).str.lower().str.strip()
            df["sex_lbl"] = np.where(v.isin(["f","female"]), "Female",
                              np.where(v.isin(["m","male"]), "Male", np.nan))
    else:
        df["sex_lbl"] = np.nan

    age = pd.to_numeric(df.get("age"), errors="coerce")
    if age.dropna().between(1,13).all():
        def _five(a):
            if a in (1,2):   return "18–29"
            if a in (3,4,5): return "30–44"
            if a in (6,7,8): return "45–59"
            if a in (9,10,11): return "60–74"
            if a in (12,13):  return "75+"
            return np.nan
        df["agegroup"] = age.astype("Int64").map(_five)
    else:
        df["agegroup"] = pd.cut(age, [18,30,45,60,75,np.inf],
                                labels=AGE_ORDER, right=False, include_lowest=True)

    return df.dropna(subset=["diabetes","education_lbl","income_lbl"])

def _aggregate_ei(df: pd.DataFrame) -> pd.DataFrame:
    g = (df.groupby(["education_lbl","income_lbl"], observed=True)
           .agg(n=("diabetes","size"),
                cases=("diabetes","sum"),
                prev=("diabetes","mean"))
           .reset_index())
    g["text"] = (g["prev"]*100).round(0).astype(int).astype(str) + "%"
    return g

# Bars 
def _bars(tbl: pd.DataFrame):
    fig = px.bar(
        tbl, x="income_lbl", y="prev", color="education_lbl",
        category_orders={"income_lbl": INC_ORDER, "education_lbl": EDU_ORDER},
        barmode="group", text="text",
        color_discrete_sequence=RED_PALETTE,
        title="Income vs Diabetes — Grouped by Education"
    )
    fig.update_traces(
        textposition="outside",
        marker_line_width=1, marker_line_color="rgba(0,0,0,0.18)",
        customdata=np.c_[tbl["n"]],
        hovertemplate="<b>%{fullData.name}</b><br>"
                      "Income: %{x}<br>"
                      "Diabetes: %{y:.1%}<br>"
                      "n=%{customdata[0]}<extra></extra>"
    )
    fig.update_layout(
        template="simple_white",
        xaxis_title="Income Scale",
        yaxis=dict(title="% with Diabetes", tickformat=".0%", dtick=0.10, range=[0,1]),
        bargap=0.2, bargroupgap=0.12,
        legend_title="Education",
        margin=dict(l=70, r=20, t=70, b=60)
    )
    return fig

# Heatmap
def _heat(tbl: pd.DataFrame):
    mat = (tbl.pivot(index="education_lbl", columns="income_lbl", values="prev")
               .reindex(index=EDU_ORDER, columns=INC_ORDER))
    n   = (tbl.pivot(index="education_lbl", columns="income_lbl", values="n")
               .reindex(index=EDU_ORDER, columns=INC_ORDER))

    hover = mat.copy().astype(object)
    for i, er in enumerate(EDU_ORDER):
        for j, inc in enumerate(INC_ORDER):
            p = mat.iloc[i,j]; nn = n.iloc[i,j]
            hover.iloc[i,j] = (
                f"<b>{er}</b><br>{inc}<br>"
                + (f"Diabetes: {p:.1%}" if pd.notna(p) else "Diabetes: —")
                + (f"<br>n={int(nn)}" if pd.notna(nn) else "")
            )

    vmax = 1.0 if not np.isfinite(np.nanmax(mat.values)) else max(0.20, float(np.nanmax(mat.values)))
    fig = go.Figure(go.Heatmap(
        z=mat.values, x=INC_ORDER, y=EDU_ORDER,
        colorscale="Reds",
        zmin=0, zmax=vmax,
        colorbar=dict(title="% Diabetes", tickformat=".0%"),
        hoverinfo="text", text=hover.values, hovertemplate="%{text}<extra></extra>"
    ))
    fig.update_layout(
        title="Diabetes Rate Heatmap — Education × Income",
        template="simple_white",
        xaxis=dict(title="Income Scale"),
        yaxis=dict(title="Education Level", autorange="reversed"),
        margin=dict(l=80, r=80, t=70, b=70)
    )
    return fig

def show_income_vs_diabetes_by_education(df_brfss: pd.DataFrame):
    base = _clean_ei(df_brfss)

    view_dd  = ToggleButtons(options=[("Grouped Bars","bars"), ("Heatmap","heat")],
                             value="bars", description="View:")
    slice_dd = Dropdown(options=[("All","__all__"), ("Sex","sex_lbl"), ("Age Group","agegroup")],
                        value="__all__", description="Slice:")
    value_dd = Dropdown(options=[("All","__all__")], value="__all__", description="Value:")
    out = Output()

    def _options(col):
        if col == "__all__":
            return [("All","__all__")]
        vals = base[col].dropna().astype(str)
        order = [v for v in AGE_ORDER if col=="agegroup" and v in set(vals)]
        if not order:
            order = sorted(vals.unique().tolist())
        return [("All","__all__")] + [(v, v) for v in order]

    def _apply_slice(df):
        if slice_dd.value == "__all__" or value_dd.value == "__all__":
            return df
        return df[df[slice_dd.value].astype(str) == str(value_dd.value)]

    def render(*_):
        sub = _apply_slice(base)
        tbl = _aggregate_ei(sub)
        fig = _bars(tbl) if view_dd.value == "bars" else _heat(tbl)
        out.clear_output(wait=True)
        with out: fig.show()

    def on_slice_change(_):
        value_dd.options = _options(slice_dd.value)
        value_dd.value = "__all__"
        render()

    slice_dd.observe(on_slice_change, names="value")
    value_dd.observe(render, names="value")
    view_dd.observe(render, names="value")

    on_slice_change(None)
    display(VBox([HBox([view_dd, slice_dd, value_dd]), out]))

show_income_vs_diabetes_by_education(df_brfss)

## Education vs Lifestyle Factors and Diabetes
# Colors for lines 
COLOR_ACTIVE = "#386cb0"
COLOR_FRUIT  = "#66a61e"
COLOR_VEG    = "#e6ab02"
COLOR_DIAB   = "#a64a47"  # diabetes line

def _normalize(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Clean/label columns; compute helper columns."""
    df = df_raw.copy()
    df.columns = df.columns.str.lower()

    edu = pd.to_numeric(df.get("education", np.nan), errors="coerce").astype("Int64")
    df["education_lbl"] = edu.map(EDU_MAP)
    df["education_lbl"] = pd.Categorical(df["education_lbl"], categories=EDU_ORDER, ordered=True)

    db = pd.to_numeric(df.get("diabetes_binary", np.nan), errors="coerce")
    df["diabetes"] = db.astype(int) if db.dropna().isin([0,1]).all() else (db == 1).astype(int)

    sex_raw = df.get("sex", np.nan)
    sex_num = pd.to_numeric(sex_raw, errors="coerce")
    if sex_num.dropna().isin([0,1]).all():
        df["sex_lbl"] = sex_num.map({0:"Female", 1:"Male"})
    elif sex_num.dropna().isin([1,2]).all():
        df["sex_lbl"] = sex_num.map({1:"Male", 2:"Female"})
    else:
        val = pd.Series(sex_raw, dtype="object").astype(str).str.strip().str.lower()
        df["sex_lbl"] = np.where(val.isin(["f","female"]), "Female",
                          np.where(val.isin(["m","male"]), "Male", "All"))

    def _as01(col):
        s = pd.to_numeric(df.get(col, np.nan), errors="coerce")
        return s.where(s.isin([0,1]), np.nan)

    df["phys_ok"]   = _as01("physactivity")   # 1 = active
    df["fruit_ok"]  = _as01("fruits")         # 1 = eats fruit (not low)
    df["veg_ok"]    = _as01("veggies")        # 1 = eats veg (not low)

    df = df.dropna(subset=["education_lbl", "diabetes"])
    return df

def _aggregate(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate lifestyle % and diabetes % by Education (and Sex slice if already filtered)."""
    grp = (df.groupby("education_lbl", observed=True)
             .agg(n=("diabetes","size"),
                  diab=("diabetes","mean"),
                  phys_rate=("phys_ok","mean"),
                  fruit_rate=("fruit_ok","mean"),
                  veg_rate=("veg_ok","mean"))
             .reset_index())
    return grp

def _build_multiline(tbl: pd.DataFrame, show_diab_line: bool) -> go.Figure:
    """Create the multi-line chart; hover shows lifestyle % and diabetes %."""
    x = tbl["education_lbl"].astype(str).tolist()

    traces = []
    def add_line(ycol, name, color):
        if ycol not in tbl or tbl[ycol].notna().sum() == 0:
            return
        y = tbl[ycol].values
        diab = tbl["diab"].values
        hover = [
            f"<b>{name}</b><br>Education: {edu}"
            f"<br>{name}: {0 if pd.isna(yv) else yv:.1%}"
            f"<br>Diabetes: {0 if pd.isna(dv) else dv:.1%}"
            for edu, yv, dv in zip(x, y, diab)
        ]
        traces.append(go.Scatter(
            x=x, y=y, mode="lines+markers", name=name,
            line=dict(width=3, color=color),
            marker=dict(size=7, line=dict(width=1, color="rgba(0,0,0,0.25)")),
            hoverinfo="text", hovertext=hover
        ))

    add_line("phys_rate",  "Physically Active", COLOR_ACTIVE)
    add_line("fruit_rate", "Fruit Intake",      COLOR_FRUIT)
    add_line("veg_rate",   "Vegetable Intake",  COLOR_VEG)

    if show_diab_line and ("diab" in tbl):
        traces.append(go.Scatter(
            x=x, y=tbl["diab"].values, mode="lines+markers",
            name="Diabetes Prevalence",
            line=dict(width=3, color=COLOR_DIAB, dash="dash"),
            marker=dict(size=7, line=dict(width=1, color="rgba(0,0,0,0.25)")),
            hovertemplate="<b>Diabetes</b><br>Education: %{x}<br>%{y:.1%}<extra></extra>",
            yaxis="y2"
        ))

    fig = go.Figure(data=traces)
    fig.update_layout(
        title="Education vs Lifestyle Factors and Diabetes",
        template="simple_white",
        xaxis=dict(title="Education Level", categoryorder="array", categoryarray=EDU_ORDER),
        yaxis=dict(title="% Engaged in Healthy Behaviours", tickformat=".0%", dtick=0.10, range=[0,1], gridcolor="#e9eef3"),
        yaxis2=dict(title="% with Diabetes", overlaying="y", side="right", tickformat=".0%", dtick=0.10, range=[0,1]),
        legend_title="Factor",
        margin=dict(l=70, r=70, t=70, b=60),
        hoverlabel_align="left"
    )
    return fig

def show_education_vs_lifestyle(df_brfss: pd.DataFrame):
    df = _normalize(df_brfss)

    sex_opts = [("All","__all__")]
    uniq_sex = [s for s in ["Female","Male"] if (df["sex_lbl"].astype(str) == s).any()]
    sex_opts += [(s, s) for s in uniq_sex]
    sex_dd = Dropdown(options=sex_opts, value="__all__", description="Sex:")

    axis_toggle = ToggleButtons(
        options=[("Lifestyle only","life"), ("Overlay diabetes","dual")],
        value="life", description="Y-axis:"
    )
    out = Output()

    def apply_slice(_df):
        if sex_dd.value == "__all__":
            return _df
        return _df[_df["sex_lbl"].astype(str) == sex_dd.value]

    def render(*_):
        sub = apply_slice(df)
        tbl = _aggregate(sub)
        fig = _build_multiline(tbl, show_diab_line=(axis_toggle.value == "dual"))
        out.clear_output(wait=True)
        with out:
            fig.show()

    sex_dd.observe(render, names="value")
    axis_toggle.observe(render, names="value")

    render()
    display(VBox([HBox([sex_dd, axis_toggle]), out]))

show_education_vs_lifestyle(df_brfss)
