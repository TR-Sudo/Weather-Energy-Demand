# GitHub Issue Drafts for Assignment 4 PRD

These drafts cover the GitHub issue creation portion of the `prd-to-issues` workflow.

Replace the placeholders below before posting:

- `#<PRD-ISSUE-NUMBER>` with the parent PRD issue number
- `#<ISSUE-1>` / `#<ISSUE-2>` / etc. with the real blocker issue numbers as you create them

Suggested creation order:

1. Issue 1
2. Issue 2
3. Issue 3
4. Issue 4
5. Issue 5
6. Issue 6

## Proposed Vertical Slices

1. **Title**: Build the joined gold dataset from GTA weather and Ontario demand
   **Type**: AFK
   **Blocked by**: None
   **User stories covered**: 1, 2, 3, 6, 7, 27, 28, 29, 30, 35

2. **Title**: Ship the app overview, data preview, and filtering flow
   **Type**: AFK
   **Blocked by**: Issue 1
   **User stories covered**: 1, 4, 5, 8, 9, 10, 11, 12, 31, 35

3. **Title**: Add visual storytelling charts for weather-demand exploration
   **Type**: AFK
   **Blocked by**: Issue 2
   **User stories covered**: 13, 14, 15, 16, 35

4. **Title**: Add one-sample and two-sample t-test analysis sections
   **Type**: AFK
   **Blocked by**: Issue 2
   **User stories covered**: 17, 18, 22, 23, 24, 25, 26, 32

5. **Title**: Add chi-square and variance-comparison analysis sections
   **Type**: AFK
   **Blocked by**: Issue 2
   **User stories covered**: 19, 20, 22, 23, 24, 25, 26, 32

6. **Title**: Add correlation analysis and final documentation polish
   **Type**: AFK
   **Blocked by**: Issue 3, Issue 4, Issue 5
   **User stories covered**: 21, 22, 23, 24, 25, 26, 31, 32, 33, 34, 35

---

## Issue 1

**Title**: Build the joined gold dataset from GTA weather and Ontario demand

```md
## Parent PRD

#<PRD-ISSUE-NUMBER>

## What to build

Create the reproducible end-to-end data path that extends the Assignment 3 weather project with Ontario IESO demand data and produces a repo-stored gold dataset ready for the Assignment 4 app. This slice should cover ingestion, daily standardization, a simple `date` join, and the derived variables needed for later analyses so the project has a single stable analysis-ready dataset.

Reference the parent PRD sections on Problem Statement, Solution, Implementation Decisions, and Testing Decisions rather than re-describing the full project here.

## Acceptance criteria

- [ ] Weather ingestion supports the one-year window from `2025-04-01` through `2026-03-31` for Toronto, Oshawa, and Barrie and writes raw files into the repo
- [ ] IESO demand ingestion writes raw Ontario demand files that can be reprocessed into stable tabular outputs
- [ ] Clean transformations produce cleaned daily weather data and daily Ontario demand metrics that can be joined on `date`
- [ ] Gold-layer generation creates a single repo-stored final dataset with one row per day and the required derived variables, including continuous, binary, and categorical fields for downstream tests
- [ ] The final gold dataset can be loaded locally without calling source APIs at runtime

## Blocked by

None - can start immediately

## User stories addressed

- User story 1
- User story 2
- User story 3
- User story 6
- User story 7
- User story 27
- User story 28
- User story 29
- User story 30
- User story 35
```

## Issue 2

**Title**: Ship the app overview, data preview, and filtering flow

```md
## Parent PRD

#<PRD-ISSUE-NUMBER>

## What to build

Add the first interactive app slice that reads the repo-stored gold dataset and lets a viewer understand the project story, inspect the final joined data, and narrow the analysis window before looking at results. This slice should make the Assignment 4 continuation from Assignment 3 obvious, explain why Ontario demand was added to the weather project, and expose the key dataset fields, summary statistics, and filters in a guided layout.

Reference the parent PRD sections on Solution and Implementation Decisions for the five-section app structure and guided interaction model.

## Acceptance criteria

- [ ] The Streamlit app loads the gold dataset from the repo and renders successfully without live API calls
- [ ] The app includes a project overview that explains the weather-plus-demand story and the `date` join clearly
- [ ] Users can preview the final dataset, summary statistics, and short descriptions for key columns
- [ ] Users can filter the app by date range and season and the displayed dataset metrics respond to those filters
- [ ] The app explicitly notes that weather represents the GTA while demand represents Ontario

## Blocked by

- Blocked by #<ISSUE-1>

## User stories addressed

- User story 1
- User story 4
- User story 5
- User story 8
- User story 9
- User story 10
- User story 11
- User story 12
- User story 31
- User story 35
```

## Issue 3

**Title**: Add visual storytelling charts for weather-demand exploration

```md
## Parent PRD

#<PRD-ISSUE-NUMBER>

## What to build

Add the visual storytelling slice that helps a viewer understand why the selected statistical tests are reasonable before they reach the analysis section. This slice should connect the joined dataset to an interpretable narrative with time-series and comparison charts that show how temperature patterns line up with Ontario demand and how the categorical groupings support later tests.

Reference the parent PRD sections on Solution, User Stories, and Implementation Decisions for the required visualization set.

## Acceptance criteria

- [ ] The app includes a time-series chart that shows temperature and demand over time in a way that makes major shifts visually comparable
- [ ] The app includes a grouped or distribution-focused chart comparing demand on extreme versus non-extreme temperature days
- [ ] The app includes a categorical count chart that motivates the later chi-square analysis
- [ ] The app includes a scatterplot that motivates the later correlation analysis
- [ ] Each chart renders from the filtered gold dataset and supports the analytical story without overstating causation

## Blocked by

- Blocked by #<ISSUE-2>

## User stories addressed

- User story 13
- User story 14
- User story 15
- User story 16
- User story 35
```

## Issue 4

**Title**: Add one-sample and two-sample t-test analysis sections

```md
## Parent PRD

#<PRD-ISSUE-NUMBER>

## What to build

Add the first hypothesis-testing slice to the app with a one-sample t-test and a two-sample Welch t-test, each presented with clear hypotheses, statistical output, method justification, caution text, and plain-language interpretation. This slice should make the app satisfy part of the assignment's required methods while keeping the explanation accessible to a viewer.

Reference the parent PRD sections on Solution, User Stories, and the statistical design decisions for the selected tests.

## Acceptance criteria

- [ ] The app includes a one-sample t-test using the chosen benchmark-centered weather measure
- [ ] The app includes a two-sample Welch t-test comparing demand across extreme and non-extreme temperature groups
- [ ] Each analysis states the null and alternative hypotheses explicitly
- [ ] Each analysis shows the test statistic and p-value and includes a short method justification
- [ ] Each analysis includes assumptions, cautions, and a plain-language interpretation that distinguishes association from causation

## Blocked by

- Blocked by #<ISSUE-2>

## User stories addressed

- User story 17
- User story 18
- User story 22
- User story 23
- User story 24
- User story 25
- User story 26
- User story 32
```

## Issue 5

**Title**: Add chi-square and variance-comparison analysis sections

```md
## Parent PRD

#<PRD-ISSUE-NUMBER>

## What to build

Add the categorical and variability-testing slice to the app with a chi-square-family analysis and a robust variance-comparison analysis. This slice should show how the derived categorical fields and grouped demand behavior from the final dataset support the assignment's remaining required methods, while keeping the results interpretable and responsibly framed.

Reference the parent PRD sections on Solution, User Stories, and the statistical design decisions for chi-square and Levene-style variance testing.

## Acceptance criteria

- [ ] The app includes a chi-square-family analysis for the selected categorical weather-demand relationship
- [ ] The app includes a variance-comparison analysis for demand across the selected groups
- [ ] Each analysis states the null and alternative hypotheses explicitly
- [ ] Each analysis shows the test statistic and p-value and includes a short method justification
- [ ] Each analysis includes assumptions, cautions, and a plain-language interpretation that makes the result understandable without overclaiming certainty

## Blocked by

- Blocked by #<ISSUE-2>

## User stories addressed

- User story 19
- User story 20
- User story 22
- User story 23
- User story 24
- User story 25
- User story 26
- User story 32
```

## Issue 6

**Title**: Add correlation analysis and final documentation polish

```md
## Parent PRD

#<PRD-ISSUE-NUMBER>

## What to build

Finish the project with the correlation-analysis slice plus the final explanation and documentation updates needed for a coherent submission. This slice should complete the statistical method set, reinforce the project limitations and responsible interpretation language, and align the README and supporting markdown documents with the final app and pipeline behavior.

Reference the parent PRD sections on Solution, User Stories, Testing Decisions, Further Notes, and the out-of-scope boundaries.

## Acceptance criteria

- [ ] The app includes the required correlation analysis for the selected weather-demand relationship with clear hypotheses, statistic output, method justification, cautions, and interpretation
- [ ] The app includes a reflection or limitations section that explains geographic mismatch, non-causal interpretation, and practical limits of the results
- [ ] Supporting markdown deliverables are updated so planning and reflection match the implemented app
- [ ] The README describes the final pipeline, gold dataset, and app flow in a submission-ready way
- [ ] The final app flow is coherent enough to support a short walkthrough or demo

## Blocked by

- Blocked by #<ISSUE-3>
- Blocked by #<ISSUE-4>
- Blocked by #<ISSUE-5>

## User stories addressed

- User story 21
- User story 22
- User story 23
- User story 24
- User story 25
- User story 26
- User story 31
- User story 32
- User story 33
- User story 34
- User story 35
```
