# Assignment 4 Reflection

## What Worked Well

- Extending the Assignment 3 weather pipeline with IESO demand made the project feel like a true continuation instead of a restart.
- The `date` join was simple, explainable, and easy to validate.
- The final dataset supports all required analyses without forcing unrelated variables together.

## What Was Difficult

- The original Assignment 3 window was too short for credible statistical testing, so the project had to be expanded to a full year.
- Matching GTA weather with Ontario-wide demand introduces a geographic mismatch that had to be acknowledged clearly.
- Temperature and demand do not follow a perfectly linear relationship, so the correlation design needed a better feature than raw temperature alone.

## Hardest Assumptions to Defend

- Daily rows are not fully independent because both weather and electricity demand are seasonal and autocorrelated.
- The 18C benchmark used for the one-sample test is practical rather than theoretical.
- `temp_extreme_flag` is a simplified rule and cannot capture every factor that affects electricity usage.

## What I Would Improve

- Add holiday and weekday-workload context to separate weather effects from calendar effects.
- Expand beyond three GTA cities or use province-level weather summaries to better match the demand geography.
- Add lagged features and seasonal modeling to handle autocorrelation more carefully.
- Include deployment and demo polish such as richer chart annotations and downloadable analysis outputs.
