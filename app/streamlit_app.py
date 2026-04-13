#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scipy import stats


st.set_page_config(
    page_title="Weather and Ontario Energy Demand",
    layout="wide",
)

DATA_PATH = Path("data/gold/final_dataset.csv")


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date").reset_index(drop=True)


def format_p_value(p_value: float) -> str:
    if p_value < 0.001:
        return "< 0.001"
    return f"{p_value:.4f}"


def interpret_result(p_value: float, alpha: float = 0.05) -> str:
    return "Reject the null hypothesis" if p_value < alpha else "Fail to reject the null hypothesis"


def render_test_result(
    title: str,
    hypotheses: tuple[str, str],
    statistic_label: str,
    statistic_value: float,
    p_value: float,
    justification: str,
    assumptions: str,
    interpretation: str,
) -> None:
    st.subheader(title)
    st.markdown(f"**H0:** {hypotheses[0]}")
    st.markdown(f"**H1:** {hypotheses[1]}")
    col1, col2, col3 = st.columns(3)
    col1.metric(statistic_label, f"{statistic_value:.3f}")
    col2.metric("p-value", format_p_value(p_value))
    col3.metric("Decision", interpret_result(p_value))
    st.caption(f"Why this test fits: {justification}")
    st.caption(f"Assumptions and cautions: {assumptions}")
    st.write(interpretation)


def main() -> None:
    st.title("GTA Weather and Ontario Demand Explorer")
    st.markdown(
        "This dashboard links GTA weather averages with Ontario IESO electricity demand "
        "to explore how temperature extremes align with provincial peak usage."
    )

    df = load_data()

    with st.sidebar:
        st.header("Filters")
        min_date = df["date"].min().date()
        max_date = df["date"].max().date()
        date_range = st.date_input(
            "Date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )
        season_options = sorted(df["season"].unique())
        selected_seasons = st.multiselect("Season", season_options, default=season_options)

    if len(date_range) != 2:
        st.warning("Select both a start and end date to continue.")
        return

    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered = df[
        (df["date"] >= start_date)
        & (df["date"] <= end_date)
        & (df["season"].isin(selected_seasons))
    ].copy()

    if filtered.empty:
        st.warning("No rows match the current filters.")
        return

    st.header("1. Project Overview / Data Story")
    st.write(
        "This project combines GTA weather metrics for Toronto, Oshawa, and Barrie with Ontario demand data from the Independent Electricity System Operator (IESO). "
        "Daily demand is aggregated and joined to the GTA weather summary by `date` to explore how temperature extremes relate to peak load."
    )
    st.write(
        "The core question is whether extreme temperature conditions are associated with higher electricity demand and "
        "whether demand becomes more variable when temperatures move away from a mild 18C reference point."
    )

    st.header("2. Data Preview")
    metric1, metric2, metric3, metric4 = st.columns(4)
    metric1.metric("Rows", f"{len(filtered)}")
    metric2.metric("Avg peak demand (MW)", f"{filtered['ontario_demand_peak_mw'].mean():,.0f}")
    metric3.metric("Avg daily temp (C)", f"{filtered['avg_temp_mean_celsius'].mean():.1f}")
    metric4.metric("High-demand days", f"{filtered['high_demand_day'].sum()}")

    st.dataframe(filtered.head(10), use_container_width=True)
    st.dataframe(filtered.describe(include="all").transpose(), use_container_width=True)

    column_descriptions = pd.DataFrame(
        [
            ("avg_temp_mean_celsius", "Average of the three city daily mean temperatures."),
            ("temp_extreme_flag", "1 when the day is cold enough for heating pressure or hot enough for cooling pressure."),
            ("ontario_demand_peak_mw", "Highest hourly Ontario demand on that date from the IESO feed."),
            ("high_demand_day", "1 when peak demand is in the top 25% of days in the final dataset."),
            ("temp_deviation_from_18", "Absolute distance from a mild 18C reference temperature."),
        ],
        columns=["column", "description"],
    )
    st.dataframe(column_descriptions, use_container_width=True)

    st.header("3. Visual Storytelling")
    line_fig = go.Figure()
    line_fig.add_trace(
        go.Scatter(
            x=filtered["date"],
            y=filtered["avg_temp_mean_celsius"],
            name="Avg GTA temp (C)",
            mode="lines",
        )
    )
    line_fig.add_trace(
        go.Scatter(
            x=filtered["date"],
            y=filtered["ontario_demand_peak_mw"],
            name="Ontario peak demand (MW)",
            mode="lines",
            yaxis="y2",
        )
    )
    line_fig.update_layout(
        title="Temperature and peak demand over time",
        yaxis=dict(title="Temperature (C)"),
        yaxis2=dict(title="Demand (MW)", overlaying="y", side="right"),
        legend=dict(orientation="h"),
    )
    st.plotly_chart(line_fig, use_container_width=True)
    st.caption("Cold and hot periods tend to line up with higher demand, which motivates the later tests.")

    box_fig = px.box(
        filtered,
        x="temp_extreme_flag",
        y="ontario_demand_peak_mw",
        labels={"temp_extreme_flag": "Temperature extreme flag", "ontario_demand_peak_mw": "Peak demand (MW)"},
        title="Peak demand on extreme vs non-extreme temperature days",
    )
    st.plotly_chart(box_fig, use_container_width=True)

    count_df = (
        filtered.groupby(["temp_extreme_flag", "high_demand_day"])
        .size()
        .reset_index(name="days")
    )
    count_fig = px.bar(
        count_df,
        x="temp_extreme_flag",
        y="days",
        color="high_demand_day",
        barmode="group",
        title="High-demand day counts by temperature-extreme status",
        labels={"temp_extreme_flag": "Temperature extreme flag", "high_demand_day": "High demand day"},
    )
    st.plotly_chart(count_fig, use_container_width=True)

    scatter_fig = px.scatter(
        filtered,
        x="temp_deviation_from_18",
        y="ontario_demand_peak_mw",
        color="season",
        title="Demand rises as weather moves away from a mild 18C reference",
        labels={
            "temp_deviation_from_18": "Absolute temperature deviation from 18C",
            "ontario_demand_peak_mw": "Peak demand (MW)",
        },
    )
    trend_x = filtered["temp_deviation_from_18"].to_numpy()
    trend_y = filtered["ontario_demand_peak_mw"].to_numpy()
    slope, intercept = np.polyfit(trend_x, trend_y, 1)
    scatter_fig.add_trace(
        go.Scatter(
            x=trend_x,
            y=slope * trend_x + intercept,
            mode="lines",
            name="Linear trend",
        )
    )
    st.plotly_chart(scatter_fig, use_container_width=True)

    st.header("4. Hypothesis Testing")
    analysis = st.selectbox(
        "Choose an analysis",
        [
            "One-sample t-test: comfort gap vs 0",
            "Two-sample t-test: demand on extreme vs non-extreme days",
            "Chi-square test: high-demand day vs temperature extreme",
            "Variance comparison: demand variability by temperature extreme",
            "Spearman correlation: temperature deviation vs peak demand",
        ],
    )

    if analysis == "One-sample t-test: comfort gap vs 0":
        sample = filtered["comfort_gap_celsius"].dropna()
        test = stats.ttest_1samp(sample, popmean=0)
        render_test_result(
            title="One-sample t-test",
            hypotheses=(
                "The mean daily GTA temperature equals 18C after centering.",
                "The mean daily GTA temperature differs from 18C after centering.",
            ),
            statistic_label="t-statistic",
            statistic_value=float(test.statistic),
            p_value=float(test.pvalue),
            justification="A one-sample t-test fits because the sample is one quantitative series compared against a single benchmark mean.",
            assumptions="Daily observations are treated as approximately independent, but weather has seasonality and autocorrelation. The 18C benchmark is a practical comfort reference, not a natural law.",
            interpretation=(
                "This checks whether the filtered period is centered around a mild 18C day. "
                "If the null is rejected, the selected period leans meaningfully cooler or warmer than that neutral reference."
            ),
        )

    elif analysis == "Two-sample t-test: demand on extreme vs non-extreme days":
        extreme = filtered.loc[filtered["temp_extreme_flag"] == 1, "ontario_demand_peak_mw"]
        normal = filtered.loc[filtered["temp_extreme_flag"] == 0, "ontario_demand_peak_mw"]
        test = stats.ttest_ind(extreme, normal, equal_var=False, nan_policy="omit")
        render_test_result(
            title="Welch two-sample t-test",
            hypotheses=(
                "Mean peak demand is the same on extreme and non-extreme temperature days.",
                "Mean peak demand differs between extreme and non-extreme temperature days.",
            ),
            statistic_label="t-statistic",
            statistic_value=float(test.statistic),
            p_value=float(test.pvalue),
            justification="Welch's t-test compares the means of two independent groups without assuming equal variances.",
            assumptions="The groups should be reasonably independent and not too skewed. Daily demand still has serial dependence, so this is an association test rather than causal evidence.",
            interpretation=(
                "This asks whether electricity usage tends to shift upward on very cold or very hot days compared with milder days."
            ),
        )

    elif analysis == "Chi-square test: high-demand day vs temperature extreme":
        contingency = pd.crosstab(filtered["temp_extreme_flag"], filtered["high_demand_day"])
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency)
        st.subheader("Chi-square test of independence")
        st.markdown("**H0:** High-demand status is independent of temperature-extreme status.")
        st.markdown("**H1:** High-demand status and temperature-extreme status are associated.")
        col1, col2, col3 = st.columns(3)
        col1.metric("Chi-square", f"{chi2:.3f}")
        col2.metric("p-value", format_p_value(float(p_value)))
        col3.metric("Degrees of freedom", f"{dof}")
        st.caption(
            "Why this test fits: both variables are categorical and the test compares observed cell counts with the counts expected under independence."
        )
        st.caption(
            "Assumptions and cautions: expected counts should be reasonably large. If a filtered view becomes very small, the result is less trustworthy."
        )
        st.write(
            "A significant result would suggest that high-demand days are not randomly distributed across extreme and non-extreme temperature conditions."
        )
        st.dataframe(contingency, use_container_width=True)
        st.dataframe(
            pd.DataFrame(expected, index=contingency.index, columns=contingency.columns),
            use_container_width=True,
        )

    elif analysis == "Variance comparison: demand variability by temperature extreme":
        extreme = filtered.loc[filtered["temp_extreme_flag"] == 1, "ontario_demand_peak_mw"]
        normal = filtered.loc[filtered["temp_extreme_flag"] == 0, "ontario_demand_peak_mw"]
        test = stats.levene(extreme, normal, center="median")
        render_test_result(
            title="Levene variance comparison",
            hypotheses=(
                "Peak-demand variance is equal on extreme and non-extreme temperature days.",
                "Peak-demand variance differs between the two groups.",
            ),
            statistic_label="Levene statistic",
            statistic_value=float(test.statistic),
            p_value=float(test.pvalue),
            justification="Levene's test is a variance-comparison method that is more robust than a classic F-test when data are not perfectly normal.",
            assumptions="Observations should be roughly independent within groups. Variance differences can reflect seasonality or calendar structure, not only temperature.",
            interpretation=(
                "This tests whether demand becomes more or less volatile when weather conditions are extreme."
            ),
        )

    else:
        sample = filtered[["temp_deviation_from_18", "ontario_demand_peak_mw"]].dropna()
        corr, p_value = stats.spearmanr(
            sample["temp_deviation_from_18"],
            sample["ontario_demand_peak_mw"],
        )
        render_test_result(
            title="Spearman correlation",
            hypotheses=(
                "There is no monotonic association between temperature deviation and peak demand.",
                "There is a monotonic association between temperature deviation and peak demand.",
            ),
            statistic_label="Spearman rho",
            statistic_value=float(corr),
            p_value=float(p_value),
            justification="Spearman correlation fits because absolute deviation from 18C is quantitative and likely related to demand in a monotonic but not perfectly linear way.",
            assumptions="Spearman handles non-normal data better than Pearson, but repeated daily observations can still contain seasonal clustering.",
            interpretation=(
                "A positive correlation means demand tends to rise as weather moves farther away from a mild temperature."
            ),
        )

    st.header("5. Reflection / Limitations")
    st.write(
        "The `date` join is simple and explainable, but it also compresses three-city weather into one GTA average while demand is province-wide, "
        "so there is unavoidable geographic mismatch."
    )
    st.write(
        "The app highlights associations, not causation. Electricity demand also depends on work schedules, holidays, industrial activity, daylight, and pricing behavior."
    )
    st.write(
        "Daily data still carry temporal dependence, so p-values should be interpreted as useful evidence rather than final proof."
    )
    st.header("6. Insight")
    st.write(
        "The analysis suggests that extreme temperature days tend to coincide with higher Ontario peak demand, and that demand variability can be meaningfully different "
        "on days with strong temperature extremes. These patterns support the idea that weather-based demand pressure is a useful, if not complete, lens for understanding daily energy peaks."
    )


if __name__ == "__main__":
    main()
