import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Café MRP System",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  PLACEHOLDER DATA  (will come from data_loader.py later)
# ─────────────────────────────────────────────
MENU_ITEMS = ["Burgers", "Subs", "Tacos", "Spaghetti", "Pizzas"]

WEEK_LABELS = [
    "W - 12", "W - 11", "W - 10", "W - 9", "W - 8",
    "W - 7",  "W - 6",  "W - 5",  "W - 4", "W - 3",
    "W - 2",  "Last Week",
]

FORECAST_WEEKS = [
    "This Week", "Next Week", "W + 2", "W + 3", "W + 4", "W + 5"
]

# Placeholder historical demand (burgers — matches your Excel data)
PLACEHOLDER_HISTORICAL = {
    "Burgers":    [189, 190, 195, 165, 225, 276, 254, 322, 331, 189, 211, 396],
    "Subs":       [87,  71,  89,  114, 107, 59,  56,  104, 63,  73,  52,  61 ],
    "Tacos":      [101, 148, 118, 104, 122, 121, 149, 140, 130, 140, 147, 131],
    "Spaghetti":  [54,  63,  44,  37,  36,  41,  30,  39,  40,  40,  31,  30 ],
    "Pizzas":     [37,  46,  39,  42,  39,  67,  80,  57,  90,  113, 68,  135],
}

# Placeholder "most recent forecast" (this week's forecast — from Excel)
PLACEHOLDER_LAST_FORECAST = {
    "Burgers":    [193, 197, 259, 299, 321, 292],
    "Subs":       [90,  78,  90,  75,  79,  75 ],
    "Tacos":      [116, 135, 130, 106, 113, 144],
    "Spaghetti":  [51,  43,  35,  43,  42,  40 ],
    "Pizzas":     [33,  47,  66,  73,  71,  59 ],
}

# Placeholder forecast accuracy (will be calculated later)
PLACEHOLDER_ACCURACY = {
    "Burgers":    {"MAE": 42.3, "MAPE": "14.2%", "Bias": -8.1},
    "Subs":       {"MAE": 18.7, "MAPE": "22.6%", "Bias":  3.4},
    "Tacos":      {"MAE": 21.5, "MAPE": "16.8%", "Bias": -2.9},
    "Spaghetti":  {"MAE":  7.2, "MAPE": "18.4%", "Bias":  1.1},
    "Pizzas":     {"MAE": 24.6, "MAPE": "31.2%", "Bias": -5.7},
}

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/emoji/96/coffee.png", width=60)
    st.title("Café MRP")
    st.caption("Supply Chain Management System")
    st.divider()

    st.subheader("📋 Module")
    # Navigation placeholder — will become st.navigation() or st.page_link() later
    st.info("📈 Forecasting  ← You are here", icon=None)
    st.markdown("📊 Planning")
    st.markdown("📦 Inventory")
    st.markdown("🛒 Purchasing")

    st.divider()

    st.subheader("🍽️ Menu Item")
    selected_item = st.selectbox(
        label="Select item to forecast",
        options=MENU_ITEMS,
        index=0,
        label_visibility="collapsed",
    )

    st.divider()

    # Quick stats for selected item
    hist = PLACEHOLDER_HISTORICAL[selected_item]
    acc  = PLACEHOLDER_ACCURACY[selected_item]

    st.subheader(f"{selected_item} — Quick Stats")
    col_a, col_b = st.columns(2)
    col_a.metric("Last Week Actual", hist[-1])
    col_b.metric("4-Wk Average", int(sum(hist[-4:]) / 4))

    st.caption("Forecast Accuracy (last 8 wks)")
    col_c, col_d, col_e = st.columns(3)
    col_c.metric("MAE",  acc["MAE"])
    col_d.metric("MAPE", acc["MAPE"])
    col_e.metric("Bias", acc["Bias"])


# ─────────────────────────────────────────────
#  MAIN CONTENT
# ─────────────────────────────────────────────
st.title(f"📈 Forecasting — {selected_item}")
st.caption(
    "Review historical demand, enter your forecast for the next 6 weeks, "
    "and track forecast accuracy over time."
)
st.divider()

# ── Section 1: Historical Demand Chart + Forecast Entry ──────────────────────
col_chart, col_form = st.columns([3, 2], gap="large")

with col_chart:
    st.subheader("Historical Demand & Current Forecast")

    hist_vals     = PLACEHOLDER_HISTORICAL[selected_item]
    forecast_vals = PLACEHOLDER_LAST_FORECAST[selected_item]

    # Build chart: historical bars + forecast line
    fig = make_subplots()

    # Historical bars
    fig.add_trace(go.Bar(
        x=WEEK_LABELS,
        y=hist_vals,
        name="Actual Demand",
        marker_color="#2E86AB",
        opacity=0.8,
    ))

    # Suggested forecast line (static placeholder — will be calculated later)
    suggested_vals = [int(sum(hist_vals[-4:]) / 4)] * 6   # simple 4-week avg
    fig.add_trace(go.Scatter(
        x=FORECAST_WEEKS,
        y=suggested_vals,
        name="Suggested Forecast",
        mode="lines+markers",
        line=dict(color="#F6AE2D", dash="dash", width=2),
        marker=dict(size=7),
    ))

    # Prior forecast line
    fig.add_trace(go.Scatter(
        x=FORECAST_WEEKS,
        y=forecast_vals,
        name="Last Committed Forecast",
        mode="lines+markers",
        line=dict(color="#E84855", width=2),
        marker=dict(size=7),
    ))

    fig.update_layout(
        height=350,
        margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        xaxis_title="Week",
        yaxis_title="Units",
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font=dict(color="#fafafa"),
        xaxis=dict(gridcolor="#2a2a2a"),
        yaxis=dict(gridcolor="#2a2a2a"),
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "🟡 Suggested forecast = simple 4-week moving average  |  "
        "🔴 Last committed forecast = values entered last week"
    )


with col_form:
    st.subheader("Enter This Week's Forecast")

    # Auto-suggestion callout
    suggested = int(sum(PLACEHOLDER_HISTORICAL[selected_item][-4:]) / 4)
    st.info(
        f"💡 **Suggested forecast:** {suggested} units/week  \n"
        f"Based on a 4-week moving average. Adjust as needed.",
        icon=None,
    )

    with st.form(key="forecast_form"):
        st.markdown("**Units forecasted per week:**")

        forecast_inputs = {}
        for i, week in enumerate(FORECAST_WEEKS):
            # Pre-populate with suggested value; student can override
            forecast_inputs[week] = st.number_input(
                label=week,
                min_value=0,
                max_value=2000,
                value=suggested,
                step=1,
                key=f"forecast_{week}",
            )

        st.markdown("")  # spacer

        col_sub, col_clr = st.columns(2)
        submitted = col_sub.form_submit_button(
            "✅ Commit Forecast",
            use_container_width=True,
            type="primary",
        )
        cleared = col_clr.form_submit_button(
            "↩️ Reset to Suggested",
            use_container_width=True,
        )

    # Feedback after submission (static placeholder)
    if submitted:
        st.success(
            f"✅ Forecast for **{selected_item}** committed successfully!  \n"
            f"Values saved for weeks: {', '.join(FORECAST_WEEKS)}.",
            icon=None,
        )
        # Show summary table of what was entered
        summary_df = pd.DataFrame({
            "Week": list(forecast_inputs.keys()),
            "Forecasted Units": list(forecast_inputs.values()),
        })
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

    if cleared:
        st.info("Form reset to suggested values. Re-enter and commit when ready.")


# ── Section 2: Forecast Accuracy ──────────────────────────────────────────────
st.divider()
st.subheader("📊 Forecast Accuracy — All Items")
st.caption(
    "Tracking forecast accuracy helps identify which items need more attention "
    "and whether forecasting is improving over time."
)

# Accuracy comparison table (placeholder)
accuracy_data = []
for item in MENU_ITEMS:
    acc = PLACEHOLDER_ACCURACY[item]
    hist = PLACEHOLDER_HISTORICAL[item]
    accuracy_data.append({
        "Menu Item":     item,
        "Last Week Actual": hist[-1],
        "4-Wk Avg":     int(sum(hist[-4:]) / 4),
        "MAE":           acc["MAE"],
        "MAPE":          acc["MAPE"],
        "Bias":          acc["Bias"],
        "Trend":         "📈" if acc["Bias"] > 0 else "📉",
    })

accuracy_df = pd.DataFrame(accuracy_data)

# Highlight the currently selected item
def highlight_selected(row):
    if row["Menu Item"] == selected_item:
        return ["background-color: #1a3a4a"] * len(row)
    return [""] * len(row)

styled_df = accuracy_df.style.apply(highlight_selected, axis=1)

st.dataframe(styled_df, use_container_width=True, hide_index=True)

# Accuracy bar chart — MAPE by item
st.markdown("")
mape_vals = [float(PLACEHOLDER_ACCURACY[item]["MAPE"].strip("%")) for item in MENU_ITEMS]

fig2 = go.Figure(go.Bar(
    x=MENU_ITEMS,
    y=mape_vals,
    marker_color=["#E84855" if v > 25 else "#F6AE2D" if v > 15 else "#44BBA4" for v in mape_vals],
    text=[f"{v:.1f}%" for v in mape_vals],
    textposition="outside",
))

fig2.update_layout(
    title="Mean Absolute Percentage Error (MAPE) by Item  |  🟢 <15%   🟡 15-25%   🔴 >25%",
    height=280,
    margin=dict(l=0, r=0, t=50, b=0),
    yaxis_title="MAPE (%)",
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font=dict(color="#fafafa"),
    xaxis=dict(gridcolor="#2a2a2a"),
    yaxis=dict(gridcolor="#2a2a2a"),
    showlegend=False,
)

st.plotly_chart(fig2, use_container_width=True)

# ── Footer ──────────────────────────────────────────────────────────────────
st.divider()
st.caption("☕ Café MRP System  |  SCM 478  |  BYU-Idaho  |  Static shell — data layer coming next")
