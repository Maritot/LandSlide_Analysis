# Raw Data Cleaning Plan v1

Status: Frozen v1

Frozen on: 2026-07-22

Audience: MR reviewers

Source snapshot: `data/Raw_Data.csv`

## Scope

This plan defines the first approved cleaning pass for the raw landslide dataset. It covers missing values, duplicates, type fixes, category harmonisation, and the null-imputation stance for the current CSV snapshot. The approach is intentionally conservative: preserve rows, preserve the raw table, and only standardize values when the business meaning is clear.

## Baseline Profile

- Rows profiled: `48,108`
- Columns profiled: `52`
- Columns with blanks: `50`
- Fully complete columns: `Event_ID`, `Response_ID`
- Exact duplicate rows: `0`
- Duplicate `Event_ID` values: `0`
- Duplicate `Response_ID` values: `0`
- Malformed `Date` tokens: `0`
- Malformed numeric tokens in typed columns: `0`
- Category inconsistency after trim/case normalization: `0` groups in the audited category fields
- Data exception to treat in v1: `Aid_Amount_INR` has `51` negative values, minimum `-7,713,100.00`

Notes:

- Negative `NDVI` values are valid in the observed range `-0.10` to `0.95`.
- Negative `Temperature_C` values are valid in the observed range `-5.0` to `42.0`.
- Negative `Aid_Amount_INR` values are not accepted as valid aid payments in v1 and will be set to `NULL` pending source verification.

## v1 Cleaning Principles

- Keep `raw_data` unchanged and produce a cleaned layer from it.
- Keep all rows in v1. No records are dropped from the current snapshot.
- Convert blank strings to `NULL`.
- Apply type fixes only where the target type is unambiguous.
- Apply category harmonisation by trimming whitespace and enforcing canonical labels.
- Do not perform statistical null imputation in the base cleaned table.
- Allow only one value-normalization exception in v1: negative `Aid_Amount_INR` becomes `NULL`.
- Defer all analysis-oriented fill strategies to a separate derived layer.

## Duplicate Policy

| Check | Current finding | v1 action |
| --- | --- | --- |
| Exact row duplicate | `0` | No row dropped in the current snapshot. Keep a duplicate check in the pipeline for future loads. |
| `Event_ID` duplicate | `0` | Keep as required business key. If future duplicates appear, quarantine for review instead of keep-first deduping. |
| `Response_ID` duplicate | `0` | Keep as required business key. If future duplicates appear, quarantine for review instead of keep-first deduping. |

## Type Fix Rules

Target date column:

- `Date` -> `DATE`

Target decimal columns:

- `Latitude`, `Longitude`, `Rainfall_mm`, `Elevation_m`, `Slope_Degree`, `NDVI`, `Temperature_C`, `Humidity`, `Distance_to_River_km`, `Roads_Blocked_km`, `Economic_Loss_INR`, `Cropland_Damaged`, `Response_Time_Min`, `Rescue_Duration_Hours`, `Aid_Amount_INR`, `Relief_Materials_Tons`, `Power_Outage_Hours`

Target integer columns:

- `Historical_Landslide_Count`, `Casualties`, `Injured`, `Missing_Persons`, `Families_Affected`, `Population_Affected`, `Houses_Damaged`, `Bridges_Damaged`, `Livestock_Lost`, `Human_Resources_Deployed`, `Rescue_Teams`, `NDRF_Teams`, `SDRF_Teams`, `Volunteers`, `Ambulances`, `Helicopters`, `Excavators`, `JCB_Machines`, `Cranes`, `Relief_Camps`, `Evacuated_People`, `Recovery_Days`

Implementation note:

- Count-style measures are stored as float-style text in the CSV, for example `4.0`. In v1 they are cast to `INT` after trim validation.

## Category Harmonisation Rules

Apply trim and canonical case normalization to all text and category fields. Current audited labels are already consistent after normalization, so v1 only enforces the canonical set below and converts blanks to `NULL`.

Canonical sets:

- `State`: existing 18 state labels are already consistent after trim/case normalization.
- `Season`: `Monsoon`, `Post-Monsoon`, `Pre-Monsoon`, `Winter`
- `Soil_Type`: `Alluvial`, `Clayey`, `Laterite`, `Loamy`, `Rocky`, `Sandy Loam`, `Silty`
- `Land_Use`: `Agricultural`, `Barren/Rocky`, `Forest`, `Mixed Settlement`, `Plantation`, `Residential`, `Road Corridor`
- `Landslide_Occurred`: `Yes`, `No`
- `Landslide_Risk`: `Low`, `Moderate`, `High`, `Very High`
- `Compensation_Provided`: `Yes`, `No`
- `Water_Supply_Disrupted`: `Yes`, `No`
- `Communication_Disruption`: `Yes`, `No`
- `District`: trim only in v1; do not merge district spellings without a geography reference file.

## Null Imputation Strategy

v1 does not impute nulls in the base cleaned table. If we need higher completeness for analytics, imputation should happen only in a derived analysis layer with explicit `_imputed` flags and documented business logic.

| Column group | Recommended strategy | Notes |
| --- | --- | --- |
| Keys and identifiers | No imputation | Never impute `Event_ID` or `Response_ID`. |
| Date and geography | Deterministic only when a trusted source exists | `Season` can be derived from `Date`; coordinates can be backfilled from a verified district reference; `State` and `District` should not be guessed. |
| Environmental predictors | Median by `State + Season`, fallback to state median, then global median | Use only in analysis or modeling layers, not in the base cleaned table. |
| Impact and damage metrics | No default fill | Missing is not proof of zero casualties, zero loss, or zero damage. |
| Response and recovery metrics | No default zero fill | Missing is not proof of no deployment or zero recovery time. |
| Binary service flags | Use `Unknown` only in a derived analysis layer | Do not force `Yes` or `No` in the base cleaned table. |
| Financial anomaly handling | Negative `Aid_Amount_INR` -> `NULL` | Treat as invalid until source confirmation is available. |

## Frozen Rule Buckets

| Rule ID | Affected columns | Keep / drop / impute decision |
| --- | --- | --- |
| `R1` | `Date`, `State`, `District`, `Latitude`, `Longitude`, `Season` | Keep row. Trim and cast. Keep blank values as `NULL`. No v1 imputation. In a derived layer, only deterministic or reference-based backfill is allowed. |
| `R2` | `Soil_Type`, `Land_Use` | Keep row. Harmonize to canonical labels after trim. Keep blanks as `NULL`. No v1 imputation. In a derived layer, `Unknown` may be used if analysis requires completeness. |
| `R3` | `Rainfall_mm`, `Elevation_m`, `Slope_Degree`, `NDVI`, `Temperature_C`, `Humidity`, `Distance_to_River_km` | Keep row. Cast to `DECIMAL`. Keep blanks as `NULL`. No v1 imputation. In a derived layer, median fill by `State + Season` is acceptable with a fallback chain. |
| `R4` | `Historical_Landslide_Count` | Keep row. Cast to `INT`. Keep blanks as `NULL`. Never auto-impute `0`. Optional modeling-only fill may use grouped medians or keep `NULL`. |
| `R5` | `Landslide_Occurred`, `Landslide_Risk` | Keep row. Harmonize category labels. Keep blanks as `NULL`. No class-label imputation in v1. In a derived layer, use `Unknown` rather than forcing a label. |
| `R6` | `Casualties`, `Injured`, `Missing_Persons`, `Families_Affected`, `Population_Affected`, `Houses_Damaged`, `Roads_Blocked_km`, `Bridges_Damaged`, `Economic_Loss_INR`, `Cropland_Damaged`, `Livestock_Lost` | Keep row. Cast to numeric target types. Keep blanks as `NULL`. No default zero fill. Derived-layer imputation must be rule-based or modeling-only and flagged. |
| `R7` | `Response_Time_Min`, `Rescue_Duration_Hours`, `Human_Resources_Deployed`, `Rescue_Teams`, `NDRF_Teams`, `SDRF_Teams`, `Volunteers`, `Ambulances`, `Helicopters`, `Excavators`, `JCB_Machines`, `Cranes`, `Relief_Camps`, `Evacuated_People`, `Relief_Materials_Tons`, `Recovery_Days`, `Power_Outage_Hours` | Keep row. Cast to numeric target types. Keep blanks as `NULL`. No default zero fill. Derived-layer imputation must be explicitly justified and flagged. |
| `R8` | `Aid_Amount_INR`, `Compensation_Provided`, `Water_Supply_Disrupted`, `Communication_Disruption` | Keep row. Harmonize categorical labels and cast `Aid_Amount_INR` to `DECIMAL`. Keep blanks as `NULL`. Set negative `Aid_Amount_INR` values to `NULL`. In a derived layer, binary flags may use `Unknown` if needed. |

## Column-Level Inventory

| Column | Nulls | Missing % | Rule ID | v1 action / impute stance |
| --- | ---: | ---: | --- | --- |
| `Date` | 892 | 1.85% | `R1` | Cast `DATE`; keep `NULL`; no v1 impute |
| `State` | 896 | 1.86% | `R1` | Trim canonical; keep `NULL`; no v1 impute |
| `District` | 1861 | 3.87% | `R1` | Trim only; keep `NULL`; no v1 impute |
| `Latitude` | 1107 | 2.30% | `R1` | Cast `DECIMAL`; keep `NULL`; no v1 impute |
| `Longitude` | 1135 | 2.36% | `R1` | Cast `DECIMAL`; keep `NULL`; no v1 impute |
| `Season` | 936 | 1.95% | `R1` | Trim canonical; keep `NULL`; derive only from `Date` in derived layer |
| `Rainfall_mm` | 2571 | 5.34% | `R3` | Cast `DECIMAL`; keep `NULL`; derived-layer median fill only |
| `Elevation_m` | 1490 | 3.10% | `R3` | Cast `DECIMAL`; keep `NULL`; derived-layer median fill only |
| `Slope_Degree` | 1537 | 3.19% | `R3` | Cast `DECIMAL`; keep `NULL`; derived-layer median fill only |
| `Soil_Type` | 1962 | 4.08% | `R2` | Trim canonical; keep `NULL`; optional `Unknown` in derived layer |
| `NDVI` | 1573 | 3.27% | `R3` | Cast `DECIMAL`; keep `NULL`; derived-layer median fill only |
| `Temperature_C` | 959 | 1.99% | `R3` | Cast `DECIMAL`; keep `NULL`; derived-layer median fill only |
| `Humidity` | 1108 | 2.30% | `R3` | Cast `DECIMAL`; keep `NULL`; derived-layer median fill only |
| `Distance_to_River_km` | 1415 | 2.94% | `R3` | Cast `DECIMAL`; keep `NULL`; derived-layer median fill only |
| `Land_Use` | 1925 | 4.00% | `R2` | Trim canonical; keep `NULL`; optional `Unknown` in derived layer |
| `Historical_Landslide_Count` | 1008 | 2.10% | `R4` | Cast `INT`; keep `NULL`; never auto-fill `0` |
| `Landslide_Occurred` | 686 | 1.43% | `R5` | Trim canonical; keep `NULL`; use `Unknown` only in derived layer |
| `Landslide_Risk` | 1490 | 3.10% | `R5` | Trim canonical; keep `NULL`; use `Unknown` only in derived layer |
| `Casualties` | 2174 | 4.52% | `R6` | Cast `INT`; keep `NULL`; no default zero fill |
| `Injured` | 1622 | 3.37% | `R6` | Cast `INT`; keep `NULL`; no default zero fill |
| `Missing_Persons` | 1203 | 2.50% | `R6` | Cast `INT`; keep `NULL`; no default zero fill |
| `Families_Affected` | 1869 | 3.89% | `R6` | Cast `INT`; keep `NULL`; no default zero fill |
| `Population_Affected` | 1463 | 3.04% | `R6` | Cast `INT`; keep `NULL`; no default zero fill |
| `Houses_Damaged` | 2120 | 4.41% | `R6` | Cast `INT`; keep `NULL`; no default zero fill |
| `Roads_Blocked_km` | 2114 | 4.39% | `R6` | Cast `DECIMAL`; keep `NULL`; no default zero fill |
| `Bridges_Damaged` | 1689 | 3.51% | `R6` | Cast `INT`; keep `NULL`; no default zero fill |
| `Economic_Loss_INR` | 1976 | 4.11% | `R6` | Cast `DECIMAL`; keep `NULL`; no default zero fill |
| `Cropland_Damaged` | 1173 | 2.44% | `R6` | Cast `DECIMAL`; keep `NULL`; no default zero fill |
| `Livestock_Lost` | 1850 | 3.85% | `R6` | Cast `INT`; keep `NULL`; no default zero fill |
| `Response_Time_Min` | 1555 | 3.23% | `R7` | Cast `DECIMAL`; keep `NULL`; no default zero fill |
| `Rescue_Duration_Hours` | 3615 | 7.51% | `R7` | Cast `DECIMAL`; keep `NULL`; no default zero fill |
| `Human_Resources_Deployed` | 2217 | 4.61% | `R7` | Cast `INT`; keep `NULL`; no default zero fill |
| `Rescue_Teams` | 2288 | 4.76% | `R7` | Cast `INT`; keep `NULL`; no default zero fill |
| `NDRF_Teams` | 1826 | 3.80% | `R7` | Cast `INT`; keep `NULL`; no default zero fill |
| `SDRF_Teams` | 1368 | 2.84% | `R7` | Cast `INT`; keep `NULL`; no default zero fill |
| `Volunteers` | 1673 | 3.48% | `R7` | Cast `INT`; keep `NULL`; no default zero fill |
| `Ambulances` | 1049 | 2.18% | `R7` | Cast `INT`; keep `NULL`; no default zero fill |
| `Helicopters` | 2454 | 5.10% | `R7` | Cast `INT`; keep `NULL`; no default zero fill |
| `Excavators` | 2357 | 4.90% | `R7` | Cast `INT`; keep `NULL`; no default zero fill |
| `JCB_Machines` | 2234 | 4.64% | `R7` | Cast `INT`; keep `NULL`; no default zero fill |
| `Cranes` | 1137 | 2.36% | `R7` | Cast `INT`; keep `NULL`; no default zero fill |
| `Relief_Camps` | 2291 | 4.76% | `R7` | Cast `INT`; keep `NULL`; no default zero fill |
| `Evacuated_People` | 1388 | 2.89% | `R7` | Cast `INT`; keep `NULL`; no default zero fill |
| `Aid_Amount_INR` | 1485 | 3.09% | `R8` | Cast `DECIMAL`; keep `NULL`; negatives -> `NULL` |
| `Relief_Materials_Tons` | 1496 | 3.11% | `R7` | Cast `DECIMAL`; keep `NULL`; no default zero fill |
| `Compensation_Provided` | 982 | 2.04% | `R8` | Trim canonical; keep `NULL`; optional `Unknown` in derived layer |
| `Recovery_Days` | 1377 | 2.86% | `R7` | Cast `INT`; keep `NULL`; no default zero fill |
| `Power_Outage_Hours` | 1073 | 2.23% | `R7` | Cast `DECIMAL`; keep `NULL`; no default zero fill |
| `Water_Supply_Disrupted` | 1013 | 2.11% | `R8` | Trim canonical; keep `NULL`; optional `Unknown` in derived layer |
| `Communication_Disruption` | 968 | 2.01% | `R8` | Trim canonical; keep `NULL`; optional `Unknown` in derived layer |

## Columns With No Missing Values

| Column | Current quality status | v1 action |
| --- | --- | --- |
| `Event_ID` | Complete and unique in the profiled snapshot | Keep as required event key; no imputation |
| `Response_ID` | Complete and unique in the profiled snapshot | Keep as required response key; no imputation |

## Acceptance Criteria For v1

- Cleaned row count remains `48,108`.
- No exact row is dropped in the current snapshot.
- `Event_ID` and `Response_ID` remain non-null and unique.
- Blank strings are normalized to `NULL`.
- Date and numeric fields load into their target types without malformed-token failures.
- Category fields are limited to the canonical label sets listed above.
- Nulls are preserved in the base cleaned table unless the value is explicitly invalid.
- Negative `Aid_Amount_INR` values are converted to `NULL` and reported for source follow-up.

## Deferred To v2

- Geographic backfill for missing `State`, `District`, `Latitude`, and `Longitude`
- Deterministic season backfill from `Date`
- Reference-based district spelling merges
- Derived-layer imputation with `_imputed` flags
- Statistical imputation for modeling datasets
- Cross-field inference rules such as converting blank impact metrics to zero from surrounding evidence
