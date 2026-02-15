import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats
from plotly.io import write_html

# -----------------------------
# Data Generation
# -----------------------------
np.random.seed(42)

data = {
    "date": pd.date_range(start="2025-01-01", periods=90, freq="D"),
    "discount": np.random.uniform(5, 30, 90),
    "product_category": np.random.choice(
        ["Electronics", "Clothing", "Food"], 90
    ),
    "region": np.random.choice(["North", "South", "East"], 90),
}

df = pd.DataFrame(data)

# -----------------------------
# 1. Daily Average Discount
# -----------------------------
daily_avg_discount = df.groupby("date", as_index=False)["discount"].mean()

fig_line = go.Figure()
fig_line.add_trace(
    go.Scatter(
        x=daily_avg_discount["date"],
        y=daily_avg_discount["discount"],
        mode="lines+markers",
        fill="tozeroy",
        name="Average Discount",
    )
)

fig_line.update_layout(
    title="Average Discount Trend Over Time",
    xaxis_title="Date",
    yaxis_title="Average Discount (%)",
)

# -----------------------------
# 2. Area Chart
# -----------------------------
fig_area = px.area(
    daily_avg_discount,
    x="date",
    y="discount",
    title="Average Discount Trend (Area Chart)",
)

# -----------------------------
# 3. Category-wise Trend
# -----------------------------
category_trend = df.groupby(
    ["date", "product_category"], as_index=False
)["discount"].mean()

fig_multi = px.line(
    category_trend,
    x="date",
    y="discount",
    color="product_category",
    title="Discount Trend by Product Category",
)

# -----------------------------
# 4. Monthly Statistics
# -----------------------------
df["month"] = df["date"].dt.to_period("M")

monthly_stats = (
    df.groupby("month")["discount"]
    .agg(["mean", "min", "max", "std"])
    .reset_index()
)

monthly_stats.columns = [
    "month",
    "avg_discount",
    "min_discount",
    "max_discount",
    "std_discount",
]

monthly_stats["month"] = monthly_stats["month"].astype(str)

fig_combo = go.Figure()

fig_combo.add_trace(
    go.Bar(
        x=monthly_stats["month"],
        y=monthly_stats["std_discount"],
        name="Discount Variability",
        opacity=0.4,
    )
)

fig_combo.add_trace(
    go.Scatter(
        x=monthly_stats["month"],
        y=monthly_stats["avg_discount"],
        mode="lines+markers",
        name="Average Discount",
        yaxis="y2",
    )
)

fig_combo.update_layout(
    title="Monthly Average Discount with Variability",
    yaxis2=dict(
        title="Average Discount (%)",
        overlaying="y",
        side="right",
    ),
)

# -----------------------------
# 5. Linear Trend Analysis
# -----------------------------
x_numeric = np.arange(len(daily_avg_discount))

slope, intercept, r_value, p_value, std_err = stats.linregress(
    x_numeric,
    daily_avg_discount["discount"],
)

trend_line = slope * x_numeric + intercept

fig_trend = go.Figure()

fig_trend.add_trace(
    go.Scatter(
        x=daily_avg_discount["date"],
        y=daily_avg_discount["discount"],
        mode="lines",
        name="Daily Average",
    )
)

fig_trend.add_trace(
    go.Scatter(
        x=daily_avg_discount["date"],
        y=trend_line,
        mode="lines",
        line=dict(dash="dash"),
        name=f"Trend (R² = {r_value**2:.3f})",
    )
)

fig_trend.update_layout(
    title="Discount Trend with Linear Regression",
    xaxis_title="Date",
    yaxis_title="Average Discount (%)",
)

# -----------------------------
# SAVE GRAPHS AS HTML (AUTO OPEN)
# -----------------------------
write_html(fig_line, "graph1_daily_avg.html", auto_open=True)
write_html(fig_area, "graph2_area.html", auto_open=True)
write_html(fig_multi, "graph3_category.html", auto_open=True)
write_html(fig_combo, "graph4_monthly.html", auto_open=True)
write_html(fig_trend, "graph5_trend.html", auto_open=True)

# -----------------------------
# Export for Power BI
# -----------------------------
daily_avg_discount.to_csv("discount_trends.csv", index=False)
category_trend.to_csv("discount_by_category.csv", index=False)
monthly_stats.to_csv("monthly_discount_stats.csv", index=False)

print("✅ ALL 5 GRAPHS OPENED IN BROWSER")
print("✅ CSV FILES EXPORTED SUCCESSFULLY")