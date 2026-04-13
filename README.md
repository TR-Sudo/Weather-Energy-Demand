# Assignment 4: Weather and Ontario Energy Demand Analysis

This project extends the original Assignment 3 GTA weather pipeline into an interactive Assignment 4 statistical analysis app.

## Project Story

Assignment 3 focused on daily weather patterns for Toronto, Oshawa, and Barrie using the Open-Meteo archive API. Assignment 4 adds a new external source from the Ontario Independent Electricity System Operator (IESO) so the project can ask a stronger applied question:

**How are GTA temperature conditions associated with Ontario electricity demand?**

The final app uses a one-year window from `2025-04-01` to `2026-03-31`, joins daily GTA weather summaries to daily Ontario demand metrics on `date`, and supports visual exploration plus required hypothesis tests.

## Data Sources

- Weather: Open-Meteo Historical Weather API
  - https://open-meteo.com/en/docs/historical-weather-api
- Electricity demand: Ontario IESO public demand reports
  - https://www.ieso.ca/
  - https://reports-public.ieso.ca/public/Demand/

## Repository Structure

```text
Asmt3_Stat/
├── README.md
├── requirements.txt
├── .env.example
├── data/
│   ├── raw/
│   │   ├── weather/
│   │   └── ieso/
│   ├── clean/
│   └── gold/
├── ingest/
│   ├── ingest_weather.py
│   └── ingest_ieso_demand.py
├── transform/
│   ├── transform_weather.py
│   ├── transform_ieso_demand.py
│   └── create_gold.py
├── app/
│   └── streamlit_app.py
├── notebooks/
├── assignment4_analysis_plan.md
└── assignment4_reflection.md
```

## Final Dataset

Primary app dataset:

- `data/gold/final_dataset.csv`

Key variables include:

- `avg_temp_mean_celsius`
- `temp_extreme_flag`
- `temp_deviation_from_18`
- `ontario_demand_avg_mw`
- `ontario_demand_peak_mw`
- `high_demand_day`

## Statistical Analyses

The Streamlit app includes:

- One-sample t-test
- Two-sample t-test
- Chi-square test of independence
- Variance comparison with Levene's test
- Spearman correlation analysis

## How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Rebuild the pipeline if needed:

```bash
python ingest/ingest_weather.py
python ingest/ingest_ieso_demand.py
python transform/transform_weather.py
python transform/transform_ieso_demand.py
python transform/create_gold.py
```

3. Launch the app:

```bash
streamlit run app/streamlit_app.py
```

## Public Deployment

### Streamlit Community Cloud
1. Push this repository to GitHub.
2. Visit https://share.streamlit.io and connect your GitHub account.
3. Select this repository, branch, and `app/streamlit_app.py` as the app file.
4. Deploy and share the generated public URL.

### Local public hosting
If you want to expose the app from a server or VM, run:

```bash
streamlit run app/streamlit_app.py --server.address 0.0.0.0 --server.port 8501
```

Ensure your host firewall or router allows incoming traffic on port `8501`.

### Notes
- The app uses `data/gold/final_dataset.csv`, so include that file in the repo or the deployment environment.
- The repository now includes `.streamlit/config.toml` with `server.address = "0.0.0.0"` for public hosting and `enableCORS = false`.

## Join Strategy

- Weather is collected at the city-date level for Toronto, Oshawa, and Barrie.
- Those city rows are aggregated to one GTA daily summary.
- IESO hourly demand is aggregated to daily Ontario demand metrics.
- The final join uses `date` as the shared key.

This join is simple and explainable, but it also introduces a limitation: the weather data represent the GTA while demand represents the whole province.

## Limitations

- Statistical significance does not imply causation.
- Weather and demand both have seasonality and autocorrelation.
- Ontario demand is influenced by many other factors, including work schedules and non-weather behavior.
- The one-sample benchmark of 18C is a practical comfort reference rather than a natural constant.
