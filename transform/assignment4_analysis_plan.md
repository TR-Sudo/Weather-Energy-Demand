# Assignment 4 Analysis Plan

## New Source

- New external source: Ontario IESO hourly Ontario demand report
- Source URL: https://www.ieso.ca/ and the public report archive at `https://reports-public.ieso.ca/public/Demand/`
- Why it belongs: the original project studies GTA weather, and electricity demand is a strong real-world outcome that should respond to heating and cooling conditions.

## Join Key

- Join key: `date`
- Weather data are aggregated from the three GTA cities to one daily GTA summary.
- IESO hourly demand is aggregated to daily Ontario demand metrics before the join.
- Final join strategy: daily GTA weather summary `INNER JOIN` daily Ontario demand on `date`.

## New Variables

- `ontario_demand_avg_mw`: mean hourly Ontario demand for the day
- `ontario_demand_peak_mw`: daily maximum hourly Ontario demand
- `ontario_demand_min_mw`: daily minimum hourly Ontario demand
- `ontario_peak_hour`: hour of the daily demand peak
- `demand_range_mw`: daily peak minus daily minimum demand
- `temp_extreme_flag`: 1 when average GTA conditions imply likely heating or cooling pressure
- `temp_deviation_from_18`: absolute difference between average GTA daily temperature and a mild 18C reference
- `high_demand_day`: 1 when daily peak demand is in the top quartile of the final dataset

## Story

The dashboard tells a continuation story: Assignment 3 showed how GTA weather varies across cities and time. Assignment 4 asks whether those weather patterns line up with meaningful shifts in Ontario electricity demand. The new data source turns the project from a descriptive weather pipeline into an applied statistical analysis about energy usage.

## Planned Analyses

1. One-sample t-test
- Question: Is the mean daily GTA temperature centered around an 18C comfort benchmark?
- Variables: `comfort_gap_celsius`
- Why: a one-sample t-test compares one quantitative sample against a benchmark mean.

2. Two-sample t-test
- Question: Does Ontario peak demand differ on temperature-extreme versus non-extreme days?
- Variables: `ontario_demand_peak_mw` by `temp_extreme_flag`
- Why: compares mean demand across two independent groups.

3. Chi-square test of independence
- Question: Is `high_demand_day` associated with `temp_extreme_flag`?
- Variables: `high_demand_day`, `temp_extreme_flag`
- Why: both variables are categorical and the test compares observed counts to expected counts under independence.

4. Variance comparison
- Question: Is peak-demand variability different on extreme versus non-extreme days?
- Variables: `ontario_demand_peak_mw` by `temp_extreme_flag`
- Why: Levene's test compares group variances with better robustness than a strict F-test.

5. Correlation analysis
- Question: Does demand increase as daily weather moves farther from a mild reference temperature?
- Variables: `temp_deviation_from_18`, `ontario_demand_peak_mw`
- Why: Spearman correlation is appropriate because the relationship is likely monotonic but not perfectly linear.

## Supporting Visuals

- Time-series line chart: average GTA temperature and Ontario peak demand over time
- Grouped boxplot: peak demand by `temp_extreme_flag`
- Grouped bar chart: `high_demand_day` counts by `temp_extreme_flag`
- Scatterplot: `temp_deviation_from_18` versus `ontario_demand_peak_mw`

## Method Notes

- The date join is easy to explain and defend.
- The strongest limitation is scale mismatch: weather is GTA-focused while demand is province-wide.
- The tests support association claims, not causal claims.
