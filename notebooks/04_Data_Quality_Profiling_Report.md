# Data Quality Profiling Report

## Scope

- Source reviewed: `data/Raw_Data.csv` (48,108 rows, 52 columns)
- Cleaning target: create a separate `cleaned_raw_data` table from `raw_data`
- Raw table remains untouched; only task-scoped type and quality rules are applied

## Exact Findings

- `Date`: 47216 non-null, 892 null, `0` malformed `YYYY-MM-DD` values
- `Response_Time_Min`: 46553 non-null, 1555 null, `0` malformed numeric values
- `Historical_Landslide_Count`: min `0`, max `12`, negatives `0`, fractional `0`
- `Houses_Damaged`: min `0`, max `65`, negatives `0`, fractional `0`
- `Bridges_Damaged`: min `0`, max `5`, negatives `0`, fractional `0`
- `State`: 18 labels, no inconsistent spellings after trim/case normalization
- `Soil_Type`: 7 labels, no inconsistent spellings after trim/case normalization
- `Human_Resources_Deployed`: 45891 non-null, 2217 null; values are integer-like counts stored as float-style text in the CSV
- No targeted rows need to be dropped; the cleaning pass only standardizes types and trims text

## All Columns and Target Types

- `DATE`: `Date`
- `DECIMAL`: `Latitude`, `Longitude`, `Rainfall_mm`, `Elevation_m`, `Slope_Degree`, `NDVI`, `Temperature_C`, `Humidity`, `Distance_to_River_km`, `Roads_Blocked_km`, `Economic_Loss_INR`, `Cropland_Damaged`, `Response_Time_Min`, `Rescue_Duration_Hours`, `Aid_Amount_INR`, `Relief_Materials_Tons`, `Power_Outage_Hours`
- `INT`: `Historical_Landslide_Count`, `Casualties`, `Injured`, `Missing_Persons`, `Families_Affected`, `Population_Affected`, `Houses_Damaged`, `Bridges_Damaged`, `Livestock_Lost`, `Human_Resources_Deployed`, `Rescue_Teams`, `NDRF_Teams`, `SDRF_Teams`, `Volunteers`, `Ambulances`, `Helicopters`, `Excavators`, `JCB_Machines`, `Cranes`, `Relief_Camps`, `Evacuated_People`, `Recovery_Days`
- `TEXT / ID / CATEGORY`: `Event_ID`, `State`, `District`, `Season`, `Soil_Type`, `Land_Use`, `Landslide_Occurred`, `Landslide_Risk`, `Response_ID`, `Compensation_Provided`, `Water_Supply_Disrupted`, `Communication_Disruption`

## Cleaning Rules

- Create `cleaned_raw_data` and leave `raw_data` unchanged
- Convert numeric-as-text fields to the target MySQL numeric types
- Convert `Date` to `DATE`
- Trim text fields and preserve canonical labels
- Preserve blanks as `NULL`
- Do not impute, deduplicate, or drop rows outside the requested task scope

## Targeted Conclusion

- No malformed `Date` values were found.
- No invalid numeric tokens were found in `Response_Time_Min`.
- No negatives or fractional values were found in `Historical_Landslide_Count`, `Houses_Damaged`, or `Bridges_Damaged`.
- `State` and `Soil_Type` only need trimming, not label consolidation.
- `Human_Resources_Deployed` should be cleaned as an integer measure, not as a category field.