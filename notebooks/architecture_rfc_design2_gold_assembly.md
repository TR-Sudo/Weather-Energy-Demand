## Problem

The current gold-layer build logic is concentrated in a script-shaped module that mixes multiple responsibilities:

- deduplicating and normalizing weather rows,
- aggregating weather into daily GTA summaries,
- joining weather and Ontario demand on `date`,
- computing app-facing derived variables,
- and writing several gold outputs to disk.

This creates architectural friction because the final analysis dataset is the real contract of the project, but that contract is only implicit inside the current script. The Streamlit app depends on a specific schema and feature set, yet there is no stable boundary that owns that schema. As a result:

- the codebase is harder to navigate because understanding the dataset contract requires reading through the entire build script;
- the transformation logic is harder to test because file I/O and assembly logic are intertwined;
- integration risk lives in the seams between aggregation, join logic, feature engineering, and output writing.

## Proposed Interface

Adopt the Design 2 refactor: a small deep module with one pure assembly boundary and one default file-based builder.

Interface shape:

- `GoldBuildConfig`
  - owns input paths, output location, and stable analysis parameters like the reference temperature and high-demand quantile
- `GoldArtifacts`
  - returns the city-level analysis-ready weather table, the daily weather summary, the final joined dataset, plus output-path and metadata information
- `assemble_final_dataset(weather_daily, demand_daily, *, reference_temp_celsius=18.0, high_demand_quantile=0.75) -> GoldArtifacts`
  - pure DataFrame-in/DataFrame-out core for tests
- `build_default_final_dataset(config=GoldBuildConfig()) -> GoldArtifacts`
  - trivial default path for the current repo workflow

Example usage:

```python
artifacts = build_default_final_dataset()
final_df = artifacts.final_dataset
```

This module should hide:

- weather deduplication on `date` and `city`,
- city-level weather feature engineering,
- daily GTA aggregation,
- demand join logic,
- analysis-derived fields such as `temp_extreme_flag`, `temp_deviation_from_18`, `comfort_gap_celsius`, `high_demand_day`, and `demand_direction`,
- and writing multiple gold outputs.

## Dependency Strategy

- **Dependency category**: In-process
- The core assembly boundary should remain pure and operate on already-loaded pandas DataFrames.
- File reads and writes should be pushed to the edges through the default builder.
- The Streamlit app should depend only on the explicit gold-dataset contract, not on internal transformation steps.
- Any threshold or reference values that shape the app-facing schema should be expressed through the config object instead of hidden as script constants.

## Testing Strategy

- **New boundary tests to write**
  - verify that `assemble_final_dataset(...)` returns the expected three tables from representative weather and demand inputs
  - verify that the final dataset includes the required derived columns and uses the configured temperature reference and demand quantile
  - verify that duplicate city-date weather rows are resolved consistently before aggregation
  - verify that the date join produces the expected row count and stable demand-derived features
- **Old tests to delete**
  - none currently exist, but any future shallow tests targeting internal helper functions should be avoided once boundary tests cover the module
- **Test environment needs**
  - in-memory pandas DataFrames only; no external services or live file system dependencies required for the core assembly tests

## Implementation Recommendations

- The module should own the final analysis-ready dataset contract as a first-class concept.
- It should expose a small public interface and keep all pandas shaping details private.
- It should separate pure dataset assembly from repo-specific file I/O.
- The current script entry point should become a thin orchestration layer that delegates to the new module.
- The Streamlit app should continue reading the final gold dataset, but the schema it relies on should be defined and maintained by the deepened assembly boundary.
