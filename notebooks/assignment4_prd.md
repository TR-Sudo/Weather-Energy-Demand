# Product Requirements Document

## Problem Statement

The project needs to show that the Assignment 3 weather pipeline can support a stronger, more complete analytics product in Assignment 4. The current need is not just to display cleaned weather data, but to extend that dataset with a meaningful external source, turn the result into an analysis-ready product, and help a user understand the data story from preparation through statistical interpretation.

From the user's perspective, the problem is:

- the original GTA weather dataset is useful but incomplete for deeper analysis;
- the assignment requires a new external source that creates stronger comparisons;
- the final result must support interactive exploration, multiple statistical tests, and plain-language interpretation;
- the project must feel like a continuation of Assignment 3 rather than a separate unrelated app.

## Solution

Build an interactive Streamlit dashboard that extends the GTA weather project with Ontario IESO electricity-demand data. The app should combine daily weather summaries and daily Ontario demand metrics through a simple `date` join, create derived variables that support the required tests, and guide a user through:

- the project story,
- the final joined dataset,
- motivating visualizations,
- the required hypothesis tests,
- and a reflection on assumptions and limitations.

The user experience should make it easy to see how temperature patterns may be associated with electricity demand while clearly distinguishing association from causation.

## User Stories

1. As a student, I want the Assignment 4 project to clearly continue Assignment 3, so that the submission feels coherent and defensible.
2. As a student, I want to add a real-world external data source, so that the project shows meaningful dataset extension rather than extra columns for their own sake.
3. As a student, I want a simple join strategy based on `date`, so that I can explain and defend the data integration clearly.
4. As a viewer, I want to understand the original weather dataset and the new demand dataset, so that I can follow the analytical story from start to finish.
5. As a viewer, I want to see why Ontario electricity demand belongs in a weather project, so that the extension feels justified.
6. As a viewer, I want to understand what new derived variables were created, so that the later tests feel motivated.
7. As a student, I want the final dataset to include continuous, binary, and categorical variables, so that all required statistical methods are supported.
8. As a user, I want to preview the final dataset in the app, so that I can inspect the structure before looking at results.
9. As a user, I want summary statistics in the app, so that I can quickly understand the scale and spread of the variables.
10. As a user, I want column descriptions for key variables, so that the dataset is easy to interpret.
11. As a user, I want date filtering, so that I can narrow the analysis to specific periods.
12. As a user, I want season filtering, so that I can compare how the relationship behaves across parts of the year.
13. As a viewer, I want a time-series chart of weather and demand, so that I can visually assess whether major temperature shifts align with changes in electricity demand.
14. As a viewer, I want a grouped demand chart by temperature condition, so that I can see why a group-comparison test is appropriate.
15. As a viewer, I want a categorical count chart, so that I can see why a chi-square analysis is appropriate.
16. As a viewer, I want a scatterplot for the demand relationship, so that I can see why a correlation analysis is appropriate.
17. As a student, I want at least one one-sample t-test, so that the app satisfies the assignment requirements.
18. As a student, I want at least one two-sample t-test, so that the app satisfies the assignment requirements.
19. As a student, I want one chi-square-family analysis, so that the app satisfies the assignment requirements.
20. As a student, I want one variance-comparison analysis, so that the app satisfies the assignment requirements.
21. As a student, I want one correlation analysis, so that the app satisfies the assignment requirements.
22. As a user, I want each analysis to state the null and alternative hypotheses, so that the statistical question is explicit.
23. As a user, I want to see the test statistic and p-value, so that the result is transparent.
24. As a user, I want a short justification for each method, so that I understand why the test matches the variables.
25. As a user, I want assumptions and cautions presented beside each test, so that the app does not overstate certainty.
26. As a user, I want plain-language interpretations of results, so that I do not need to translate raw output myself.
27. As a student, I want the final app to read from a gold dataset stored in the repo, so that the dashboard is reproducible and simple to deploy.
28. As a developer, I want ingestion scripts for both source systems, so that the pipeline can be rerun cleanly.
29. As a developer, I want silver transformations that standardize and aggregate both data sources, so that the gold layer is stable and analysis-ready.
30. As a developer, I want the weather data expanded to a one-year window, so that the statistical tests are more credible than they would be on a one-week sample.
31. As a viewer, I want the app to explain that the weather data represent the GTA while demand represents Ontario, so that the geographic mismatch is not hidden.
32. As a viewer, I want the app to explain that significance does not imply practical importance or causation, so that the conclusions stay responsible.
33. As a student, I want supporting markdown documents for planning and reflection, so that the written deliverables align with the app.
34. As a student, I want the README to describe the new pipeline and app, so that the repo is submission-ready.
35. As a demo presenter, I want a clean final dataset and app flow, so that I can record a clear short walkthrough.

## Implementation Decisions

- The project remains centered on the original GTA weather pipeline and keeps the same city focus from Assignment 3.
- The new external data source is Ontario IESO hourly Ontario demand data.
- The weather window is expanded to one full year from April 1, 2025 through March 31, 2026 to provide seasonal variation and a defensible sample size.
- Weather is ingested at the city-day level for Toronto, Oshawa, and Barrie.
- IESO demand is ingested at the hourly level and then aggregated to daily metrics before joining.
- The final integration key is `date`.
- Weather data are aggregated into a GTA daily summary before the join so the final analysis dataset has one row per day.
- The gold dataset includes both raw daily metrics and derived variables needed for testing.
- Derived variables include a temperature-extreme flag, a high-demand-day flag, a comfort-gap measure, and a temperature-deviation-from-18C measure.
- The app is organized into five sections: project overview, data preview, visual storytelling, hypothesis testing, and reflection/limitations.
- The statistical design uses:
  - a one-sample t-test for the centered temperature benchmark;
  - a two-sample Welch t-test for demand on extreme versus non-extreme days;
  - a chi-square test of independence for `high_demand_day` and `temp_extreme_flag`;
  - Levene's test for a robust variance comparison;
  - Spearman correlation for temperature deviation versus peak demand.
- The app uses repo-stored gold data rather than calling raw APIs during runtime.
- The interaction model is intentionally guided rather than fully open-ended so the assignment story stays focused and understandable.

## Testing Decisions

- A good test should verify observable behavior and output correctness rather than implementation details.
- Pipeline validation should focus on whether ingestion produces expected raw files, whether transformations create stable tabular outputs, and whether the final gold dataset contains the required columns and row structure.
- App validation should focus on whether the final dataset loads successfully, whether each analysis can run against the available fields, and whether the visual and analytical sections render from the gold data source.
- The most important modules to test are:
  - weather ingestion behavior,
  - IESO demand ingestion behavior,
  - daily aggregation logic for demand,
  - gold-layer feature engineering,
  - and the statistical-analysis helpers used by the app.
- Tests should prefer checking schema, row counts, grouping behavior, and stable analysis outputs over testing internal pandas steps line-by-line.
- Since the repo had minimal prior formal tests, the strongest prior art in the codebase is behavior-based verification through generated CSV outputs and successful end-to-end execution of the pipeline.

## Out of Scope

- Forecasting future electricity demand
- Causal modeling of weather effects on demand
- Province-wide weather coverage beyond the original three-city GTA scope
- Holiday, pricing, industrial-load, or calendar enrichment beyond the selected IESO extension
- Production-grade deployment infrastructure
- Authentication, multi-user features, or persistent user state
- Advanced time-series modeling to correct for autocorrelation

## Further Notes

- The strongest design tradeoff is geographic mismatch: the weather features represent GTA conditions while the demand outcome is province-wide.
- The one-sample benchmark of 18C is a practical interpretive reference, not a theoretical constant.
- The project is intentionally designed to satisfy the assignment requirements while still telling a coherent applied story.
- This PRD reflects the current implemented scope only and does not include future expansion work.
