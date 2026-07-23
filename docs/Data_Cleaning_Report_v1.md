# Data Cleaning Report

## Report Metadata

- Cleaning plan: `C:\Users\tharu\OneDrive\Desktop\SocialPrachar\Projects\LandSlide_Analysis\LandSlide_Analysis\docs\cleaning-plan-v1.docx`
- Raw source used for cleaning: `C:\Users\tharu\OneDrive\Desktop\SocialPrachar\Projects\LandSlide_Analysis\LandSlide_Analysis\data\Raw_Data.csv`
- User-provided dataset reference: `C:\Users\tharu\OneDrive\Desktop\SocialPrachar\Projects\LandSlide_Analysis\Merged_Landslide_Data.csv`
- Raw source SHA-256: `64e795170b4b330e51fa78a6093bc61c96aef139b87a87c875ac6872fc4065d5`
- User dataset SHA-256: `64e795170b4b330e51fa78a6093bc61c96aef139b87a87c875ac6872fc4065d5`
- User dataset matches workspace snapshot: `True`
- Cleaned CSV sidecar: `C:\Users\tharu\OneDrive\Desktop\SocialPrachar\Projects\LandSlide_Analysis\LandSlide_Analysis\data\Cleaned_Landslide_Data_v1.csv`
- Cleaned Excel output: `C:\Users\tharu\OneDrive\Desktop\SocialPrachar\Projects\LandSlide_Analysis\LandSlide_Analysis\data\Cleaned_Landslide_Data_v1.xlsx`
- Generated report: `C:\Users\tharu\OneDrive\Desktop\SocialPrachar\Projects\LandSlide_Analysis\LandSlide_Analysis\docs\Data_Cleaning_Report_v1.md`
- Generated on: `2026-07-23T14:51:20`

The cleaning run follows the frozen v1 plan exactly: rows were preserved, blanks were normalized to NULL, numeric and date columns were typed, category labels were enforced against the approved canonical sets, and the only invalid-value correction was `Aid_Amount_INR < 0 -> NULL`.

## A. Dataset Summary

| Metric | Value |
| --- | ---: |
| Original number of rows | 48108 |
| Original number of columns | 52 |
| Final number of rows | 48108 |
| Final number of columns | 52 |

## B. Cleaning Activities Performed

| Column Name | Cleaning Issue | Cleaning Rule Applied | Reason for Cleaning | Cleaning Method Used | Metric/Logic Used for Cleaning | Number of affected rows | Number of affected cells | Example values before cleaning | Example values after cleaning |
| --- | --- | --- | --- | --- | --- | ---: | ---: | --- | --- |
| Event_ID | Leading or trailing whitespace in text field | N/A: trim text values; District is trim-only and identifiers are preserved after trim. | The plan allows formatting-only normalization when business meaning remains unchanged. | Apply str.strip() and keep the trimmed value. | Affected cells count non-null text values where trimmed_text != raw_text. | 0 | 0 | n/a | n/a |
| Date | Blank string or whitespace-only token | R1: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 892 | 892 | "" | NULL |
| Date | Date stored as CSV text | R1: cast Date to DATE and keep blanks as NULL. | The frozen plan defines Date as the single target date column. | Validate ISO-8601 date tokens with date.fromisoformat and emit DATE-typed output. | Affected cells count all non-null Date values successfully cast to DATE. | 47216 | 47216 | 2015-05-17<br>2015-02-04<br>2024-12-05<br>2016-10-13<br>2013-10-19 | 2015-05-17 (DATE)<br>2015-02-04 (DATE)<br>2024-12-05 (DATE)<br>2016-10-13 (DATE)<br>2013-10-19 (DATE) |
| State | Blank string or whitespace-only token | R1: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 896 | 896 | "" | NULL |
| State | Category normalization against approved canonical labels | R1: trim and enforce the canonical label set defined in the frozen plan. | The base cleaned layer must standardize categorical labels without introducing new values. | Normalize by trim and case, map to approved canonical label, and preserve NULLs. | Affected cells count non-null category values whose canonical label differs from the raw token. | 0 | 0 | n/a | n/a |
| District | Blank string or whitespace-only token | R1: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1861 | 1861 | "" | NULL |
| District | Leading or trailing whitespace in text field | R1: trim text values; District is trim-only and identifiers are preserved after trim. | The plan allows formatting-only normalization when business meaning remains unchanged. | Apply str.strip() and keep the trimmed value. | Affected cells count non-null text values where trimmed_text != raw_text. | 0 | 0 | n/a | n/a |
| Latitude | Blank string or whitespace-only token | R1: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1107 | 1107 | "" | NULL |
| Latitude | Decimal measure stored as CSV text | R1: cast the column to DECIMAL and keep blanks as NULL. | The v1 schema requires typed decimal measures in the cleaned layer. | Validate the trimmed token with Decimal and write a DECIMAL-typed output cell. | Affected cells count all non-null values successfully cast to DECIMAL. | 47001 | 47001 | 25.67865<br>30.88606<br>34.61433<br>26.16441<br>29.9042 | 25.67865 (DECIMAL)<br>30.88606 (DECIMAL)<br>34.61433 (DECIMAL)<br>26.16441 (DECIMAL)<br>29.9042 (DECIMAL) |
| Longitude | Blank string or whitespace-only token | R1: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1135 | 1135 | "" | NULL |
| Longitude | Decimal measure stored as CSV text | R1: cast the column to DECIMAL and keep blanks as NULL. | The v1 schema requires typed decimal measures in the cleaned layer. | Validate the trimmed token with Decimal and write a DECIMAL-typed output cell. | Affected cells count all non-null values successfully cast to DECIMAL. | 46973 | 46973 | 94.21606<br>77.17932<br>74.51911<br>94.18366<br>79.92994 | 94.21606 (DECIMAL)<br>77.17932 (DECIMAL)<br>74.51911 (DECIMAL)<br>94.18366 (DECIMAL)<br>79.92994 (DECIMAL) |
| Season | Blank string or whitespace-only token | R1: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 936 | 936 | "" | NULL |
| Season | Category normalization against approved canonical labels | R1: trim and enforce the canonical label set defined in the frozen plan. | The base cleaned layer must standardize categorical labels without introducing new values. | Normalize by trim and case, map to approved canonical label, and preserve NULLs. | Affected cells count non-null category values whose canonical label differs from the raw token. | 0 | 0 | n/a | n/a |
| Rainfall_mm | Blank string or whitespace-only token | R3: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 2571 | 2571 | "" | NULL |
| Rainfall_mm | Decimal measure stored as CSV text | R3: cast the column to DECIMAL and keep blanks as NULL. | The v1 schema requires typed decimal measures in the cleaned layer. | Validate the trimmed token with Decimal and write a DECIMAL-typed output cell. | Affected cells count all non-null values successfully cast to DECIMAL. | 45537 | 45537 | 0.0<br>12.2<br>38.2<br>61.1<br>19.5 | 0.0 (DECIMAL)<br>12.2 (DECIMAL)<br>38.2 (DECIMAL)<br>61.1 (DECIMAL)<br>19.5 (DECIMAL) |
| Elevation_m | Blank string or whitespace-only token | R3: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1490 | 1490 | "" | NULL |
| Elevation_m | Decimal measure stored as CSV text | R3: cast the column to DECIMAL and keep blanks as NULL. | The v1 schema requires typed decimal measures in the cleaned layer. | Validate the trimmed token with Decimal and write a DECIMAL-typed output cell. | Affected cells count all non-null values successfully cast to DECIMAL. | 46618 | 46618 | 1374.0<br>917.2<br>1023.6<br>797.8<br>1063.9 | 1374.0 (DECIMAL)<br>917.2 (DECIMAL)<br>1023.6 (DECIMAL)<br>797.8 (DECIMAL)<br>1063.9 (DECIMAL) |
| Slope_Degree | Blank string or whitespace-only token | R3: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1537 | 1537 | "" | NULL |
| Slope_Degree | Decimal measure stored as CSV text | R3: cast the column to DECIMAL and keep blanks as NULL. | The v1 schema requires typed decimal measures in the cleaned layer. | Validate the trimmed token with Decimal and write a DECIMAL-typed output cell. | Affected cells count all non-null values successfully cast to DECIMAL. | 46571 | 46571 | 45.7<br>25.0<br>42.5<br>41.1<br>30.0 | 45.7 (DECIMAL)<br>25.0 (DECIMAL)<br>42.5 (DECIMAL)<br>41.1 (DECIMAL)<br>30.0 (DECIMAL) |
| Soil_Type | Blank string or whitespace-only token | R2: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1962 | 1962 | "" | NULL |
| Soil_Type | Category normalization against approved canonical labels | R2: trim and enforce the canonical label set defined in the frozen plan. | The base cleaned layer must standardize categorical labels without introducing new values. | Normalize by trim and case, map to approved canonical label, and preserve NULLs. | Affected cells count non-null category values whose canonical label differs from the raw token. | 0 | 0 | n/a | n/a |
| NDVI | Blank string or whitespace-only token | R3: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1573 | 1573 | "" | NULL |
| NDVI | Decimal measure stored as CSV text | R3: cast the column to DECIMAL and keep blanks as NULL. | The v1 schema requires typed decimal measures in the cleaned layer. | Validate the trimmed token with Decimal and write a DECIMAL-typed output cell. | Affected cells count all non-null values successfully cast to DECIMAL. | 46535 | 46535 | 0.754<br>0.42<br>0.846<br>0.542<br>0.435 | 0.754 (DECIMAL)<br>0.42 (DECIMAL)<br>0.846 (DECIMAL)<br>0.542 (DECIMAL)<br>0.435 (DECIMAL) |
| Temperature_C | Blank string or whitespace-only token | R3: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 959 | 959 | "" | NULL |
| Temperature_C | Decimal measure stored as CSV text | R3: cast the column to DECIMAL and keep blanks as NULL. | The v1 schema requires typed decimal measures in the cleaned layer. | Validate the trimmed token with Decimal and write a DECIMAL-typed output cell. | Affected cells count all non-null values successfully cast to DECIMAL. | 47149 | 47149 | 26.2<br>14.6<br>22.7<br>26.9<br>17.3 | 26.2 (DECIMAL)<br>14.6 (DECIMAL)<br>22.7 (DECIMAL)<br>26.9 (DECIMAL)<br>17.3 (DECIMAL) |
| Humidity | Blank string or whitespace-only token | R3: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1108 | 1108 | "" | NULL |
| Humidity | Decimal measure stored as CSV text | R3: cast the column to DECIMAL and keep blanks as NULL. | The v1 schema requires typed decimal measures in the cleaned layer. | Validate the trimmed token with Decimal and write a DECIMAL-typed output cell. | Affected cells count all non-null values successfully cast to DECIMAL. | 47000 | 47000 | 71.3<br>66.2<br>48.8<br>81.5<br>74.8 | 71.3 (DECIMAL)<br>66.2 (DECIMAL)<br>48.8 (DECIMAL)<br>81.5 (DECIMAL)<br>74.8 (DECIMAL) |
| Distance_to_River_km | Blank string or whitespace-only token | R3: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1415 | 1415 | "" | NULL |
| Distance_to_River_km | Decimal measure stored as CSV text | R3: cast the column to DECIMAL and keep blanks as NULL. | The v1 schema requires typed decimal measures in the cleaned layer. | Validate the trimmed token with Decimal and write a DECIMAL-typed output cell. | Affected cells count all non-null values successfully cast to DECIMAL. | 46693 | 46693 | 4.03<br>0.82<br>1.06<br>2.5<br>1.08 | 4.03 (DECIMAL)<br>0.82 (DECIMAL)<br>1.06 (DECIMAL)<br>2.5 (DECIMAL)<br>1.08 (DECIMAL) |
| Land_Use | Blank string or whitespace-only token | R2: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1925 | 1925 | "" | NULL |
| Land_Use | Category normalization against approved canonical labels | R2: trim and enforce the canonical label set defined in the frozen plan. | The base cleaned layer must standardize categorical labels without introducing new values. | Normalize by trim and case, map to approved canonical label, and preserve NULLs. | Affected cells count non-null category values whose canonical label differs from the raw token. | 0 | 0 | n/a | n/a |
| Historical_Landslide_Count | Blank string or whitespace-only token | R4: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1008 | 1008 | "" | NULL |
| Historical_Landslide_Count | Count-style measure stored as float-style CSV text | R4: cast the column to INT after trim validation and keep blanks as NULL. | The plan explicitly requires integer casting for count-style measures such as '4.0' -> 4. | Validate with Decimal, ensure the value is integral, then cast to INT. | Affected cells count all non-null values successfully cast to INT. | 47100 | 47100 | 4.0<br>5.0<br>3.0<br>2.0<br>1.0 | 4 (INT)<br>5 (INT)<br>3 (INT)<br>2 (INT)<br>1 (INT) |
| Landslide_Occurred | Blank string or whitespace-only token | R5: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 686 | 686 | "" | NULL |
| Landslide_Occurred | Category normalization against approved canonical labels | R5: trim and enforce the canonical label set defined in the frozen plan. | The base cleaned layer must standardize categorical labels without introducing new values. | Normalize by trim and case, map to approved canonical label, and preserve NULLs. | Affected cells count non-null category values whose canonical label differs from the raw token. | 0 | 0 | n/a | n/a |
| Landslide_Risk | Blank string or whitespace-only token | R5: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1490 | 1490 | "" | NULL |
| Landslide_Risk | Category normalization against approved canonical labels | R5: trim and enforce the canonical label set defined in the frozen plan. | The base cleaned layer must standardize categorical labels without introducing new values. | Normalize by trim and case, map to approved canonical label, and preserve NULLs. | Affected cells count non-null category values whose canonical label differs from the raw token. | 0 | 0 | n/a | n/a |
| Casualties | Blank string or whitespace-only token | R6: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 2174 | 2174 | "" | NULL |
| Casualties | Count-style measure stored as float-style CSV text | R6: cast the column to INT after trim validation and keep blanks as NULL. | The plan explicitly requires integer casting for count-style measures such as '4.0' -> 4. | Validate with Decimal, ensure the value is integral, then cast to INT. | Affected cells count all non-null values successfully cast to INT. | 45934 | 45934 | 0.0<br>3.0<br>4.0<br>8.0<br>5.0 | 0 (INT)<br>3 (INT)<br>4 (INT)<br>8 (INT)<br>5 (INT) |
| Injured | Blank string or whitespace-only token | R6: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1622 | 1622 | "" | NULL |
| Injured | Count-style measure stored as float-style CSV text | R6: cast the column to INT after trim validation and keep blanks as NULL. | The plan explicitly requires integer casting for count-style measures such as '4.0' -> 4. | Validate with Decimal, ensure the value is integral, then cast to INT. | Affected cells count all non-null values successfully cast to INT. | 46486 | 46486 | 0.0<br>5.0<br>10.0<br>16.0<br>4.0 | 0 (INT)<br>5 (INT)<br>10 (INT)<br>16 (INT)<br>4 (INT) |
| Missing_Persons | Blank string or whitespace-only token | R6: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1203 | 1203 | "" | NULL |
| Missing_Persons | Count-style measure stored as float-style CSV text | R6: cast the column to INT after trim validation and keep blanks as NULL. | The plan explicitly requires integer casting for count-style measures such as '4.0' -> 4. | Validate with Decimal, ensure the value is integral, then cast to INT. | Affected cells count all non-null values successfully cast to INT. | 46905 | 46905 | 0.0<br>1.0<br>2.0<br>3.0<br>4.0 | 0 (INT)<br>1 (INT)<br>2 (INT)<br>3 (INT)<br>4 (INT) |
| Families_Affected | Blank string or whitespace-only token | R6: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1869 | 1869 | "" | NULL |
| Families_Affected | Count-style measure stored as float-style CSV text | R6: cast the column to INT after trim validation and keep blanks as NULL. | The plan explicitly requires integer casting for count-style measures such as '4.0' -> 4. | Validate with Decimal, ensure the value is integral, then cast to INT. | Affected cells count all non-null values successfully cast to INT. | 46239 | 46239 | 0.0<br>23.0<br>39.0<br>52.0<br>69.0 | 0 (INT)<br>23 (INT)<br>39 (INT)<br>52 (INT)<br>69 (INT) |
| Population_Affected | Blank string or whitespace-only token | R6: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1463 | 1463 | "" | NULL |
| Population_Affected | Count-style measure stored as float-style CSV text | R6: cast the column to INT after trim validation and keep blanks as NULL. | The plan explicitly requires integer casting for count-style measures such as '4.0' -> 4. | Validate with Decimal, ensure the value is integral, then cast to INT. | Affected cells count all non-null values successfully cast to INT. | 46645 | 46645 | 0.0<br>69.0<br>195.0<br>156.0<br>207.0 | 0 (INT)<br>69 (INT)<br>195 (INT)<br>156 (INT)<br>207 (INT) |
| Houses_Damaged | Blank string or whitespace-only token | R6: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 2120 | 2120 | "" | NULL |
| Houses_Damaged | Count-style measure stored as float-style CSV text | R6: cast the column to INT after trim validation and keep blanks as NULL. | The plan explicitly requires integer casting for count-style measures such as '4.0' -> 4. | Validate with Decimal, ensure the value is integral, then cast to INT. | Affected cells count all non-null values successfully cast to INT. | 45988 | 45988 | 0.0<br>12.0<br>30.0<br>17.0<br>36.0 | 0 (INT)<br>12 (INT)<br>30 (INT)<br>17 (INT)<br>36 (INT) |
| Roads_Blocked_km | Blank string or whitespace-only token | R6: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 2114 | 2114 | "" | NULL |
| Roads_Blocked_km | Decimal measure stored as CSV text | R6: cast the column to DECIMAL and keep blanks as NULL. | The v1 schema requires typed decimal measures in the cleaned layer. | Validate the trimmed token with Decimal and write a DECIMAL-typed output cell. | Affected cells count all non-null values successfully cast to DECIMAL. | 45994 | 45994 | 0.0<br>0.71<br>7.89<br>3.27<br>0.09 | 0.0 (DECIMAL)<br>0.71 (DECIMAL)<br>7.89 (DECIMAL)<br>3.27 (DECIMAL)<br>0.09 (DECIMAL) |
| Bridges_Damaged | Blank string or whitespace-only token | R6: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1689 | 1689 | "" | NULL |
| Bridges_Damaged | Count-style measure stored as float-style CSV text | R6: cast the column to INT after trim validation and keep blanks as NULL. | The plan explicitly requires integer casting for count-style measures such as '4.0' -> 4. | Validate with Decimal, ensure the value is integral, then cast to INT. | Affected cells count all non-null values successfully cast to INT. | 46419 | 46419 | 0.0<br>1.0<br>2.0<br>3.0<br>4.0 | 0 (INT)<br>1 (INT)<br>2 (INT)<br>3 (INT)<br>4 (INT) |
| Economic_Loss_INR | Blank string or whitespace-only token | R6: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1976 | 1976 | "" | NULL |
| Economic_Loss_INR | Decimal measure stored as CSV text | R6: cast the column to DECIMAL and keep blanks as NULL. | The v1 schema requires typed decimal measures in the cleaned layer. | Validate the trimmed token with Decimal and write a DECIMAL-typed output cell. | Affected cells count all non-null values successfully cast to DECIMAL. | 46132 | 46132 | 0.0<br>2839963.0<br>13156623.0<br>10257394.0<br>10897473.0 | 0.0 (DECIMAL)<br>2839963.0 (DECIMAL)<br>13156623.0 (DECIMAL)<br>10257394.0 (DECIMAL)<br>10897473.0 (DECIMAL) |
| Cropland_Damaged | Blank string or whitespace-only token | R6: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1173 | 1173 | "" | NULL |
| Cropland_Damaged | Decimal measure stored as CSV text | R6: cast the column to DECIMAL and keep blanks as NULL. | The v1 schema requires typed decimal measures in the cleaned layer. | Validate the trimmed token with Decimal and write a DECIMAL-typed output cell. | Affected cells count all non-null values successfully cast to DECIMAL. | 46935 | 46935 | 0.0<br>2.5<br>4.2<br>68.8<br>8.2 | 0.0 (DECIMAL)<br>2.5 (DECIMAL)<br>4.2 (DECIMAL)<br>68.8 (DECIMAL)<br>8.2 (DECIMAL) |
| Livestock_Lost | Blank string or whitespace-only token | R6: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1850 | 1850 | "" | NULL |
| Livestock_Lost | Count-style measure stored as float-style CSV text | R6: cast the column to INT after trim validation and keep blanks as NULL. | The plan explicitly requires integer casting for count-style measures such as '4.0' -> 4. | Validate with Decimal, ensure the value is integral, then cast to INT. | Affected cells count all non-null values successfully cast to INT. | 46258 | 46258 | 0.0<br>2.0<br>6.0<br>12.0<br>10.0 | 0 (INT)<br>2 (INT)<br>6 (INT)<br>12 (INT)<br>10 (INT) |
| Response_ID | Leading or trailing whitespace in text field | N/A: trim text values; District is trim-only and identifiers are preserved after trim. | The plan allows formatting-only normalization when business meaning remains unchanged. | Apply str.strip() and keep the trimmed value. | Affected cells count non-null text values where trimmed_text != raw_text. | 0 | 0 | n/a | n/a |
| Response_Time_Min | Blank string or whitespace-only token | R7: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1555 | 1555 | "" | NULL |
| Response_Time_Min | Decimal measure stored as CSV text | R7: cast the column to DECIMAL and keep blanks as NULL. | The v1 schema requires typed decimal measures in the cleaned layer. | Validate the trimmed token with Decimal and write a DECIMAL-typed output cell. | Affected cells count all non-null values successfully cast to DECIMAL. | 46553 | 46553 | 131.2<br>165.1<br>152.4<br>100.6<br>269.3 | 131.2 (DECIMAL)<br>165.1 (DECIMAL)<br>152.4 (DECIMAL)<br>100.6 (DECIMAL)<br>269.3 (DECIMAL) |
| Rescue_Duration_Hours | Blank string or whitespace-only token | R7: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 3615 | 3615 | "" | NULL |
| Rescue_Duration_Hours | Decimal measure stored as CSV text | R7: cast the column to DECIMAL and keep blanks as NULL. | The v1 schema requires typed decimal measures in the cleaned layer. | Validate the trimmed token with Decimal and write a DECIMAL-typed output cell. | Affected cells count all non-null values successfully cast to DECIMAL. | 44493 | 44493 | 2.9<br>4.9<br>3.3<br>2.4<br>3.5 | 2.9 (DECIMAL)<br>4.9 (DECIMAL)<br>3.3 (DECIMAL)<br>2.4 (DECIMAL)<br>3.5 (DECIMAL) |
| Human_Resources_Deployed | Blank string or whitespace-only token | R7: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 2217 | 2217 | "" | NULL |
| Human_Resources_Deployed | Count-style measure stored as float-style CSV text | R7: cast the column to INT after trim validation and keep blanks as NULL. | The plan explicitly requires integer casting for count-style measures such as '4.0' -> 4. | Validate with Decimal, ensure the value is integral, then cast to INT. | Affected cells count all non-null values successfully cast to INT. | 45891 | 45891 | 4.0<br>12.0<br>8.0<br>3.0<br>9.0 | 4 (INT)<br>12 (INT)<br>8 (INT)<br>3 (INT)<br>9 (INT) |
| Rescue_Teams | Blank string or whitespace-only token | R7: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 2288 | 2288 | "" | NULL |
| Rescue_Teams | Count-style measure stored as float-style CSV text | R7: cast the column to INT after trim validation and keep blanks as NULL. | The plan explicitly requires integer casting for count-style measures such as '4.0' -> 4. | Validate with Decimal, ensure the value is integral, then cast to INT. | Affected cells count all non-null values successfully cast to INT. | 45820 | 45820 | 1.0<br>2.0<br>3.0<br>6.0<br>4.0 | 1 (INT)<br>2 (INT)<br>3 (INT)<br>6 (INT)<br>4 (INT) |
| NDRF_Teams | Blank string or whitespace-only token | R7: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1826 | 1826 | "" | NULL |
| NDRF_Teams | Count-style measure stored as float-style CSV text | R7: cast the column to INT after trim validation and keep blanks as NULL. | The plan explicitly requires integer casting for count-style measures such as '4.0' -> 4. | Validate with Decimal, ensure the value is integral, then cast to INT. | Affected cells count all non-null values successfully cast to INT. | 46282 | 46282 | 1.0<br>0.0<br>2.0<br>3.0<br>4.0 | 1 (INT)<br>0 (INT)<br>2 (INT)<br>3 (INT)<br>4 (INT) |
| SDRF_Teams | Blank string or whitespace-only token | R7: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1368 | 1368 | "" | NULL |
| SDRF_Teams | Count-style measure stored as float-style CSV text | R7: cast the column to INT after trim validation and keep blanks as NULL. | The plan explicitly requires integer casting for count-style measures such as '4.0' -> 4. | Validate with Decimal, ensure the value is integral, then cast to INT. | Affected cells count all non-null values successfully cast to INT. | 46740 | 46740 | 0.0<br>1.0<br>7.0<br>4.0<br>5.0 | 0 (INT)<br>1 (INT)<br>7 (INT)<br>4 (INT)<br>5 (INT) |
| Volunteers | Blank string or whitespace-only token | R7: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1673 | 1673 | "" | NULL |
| Volunteers | Count-style measure stored as float-style CSV text | R7: cast the column to INT after trim validation and keep blanks as NULL. | The plan explicitly requires integer casting for count-style measures such as '4.0' -> 4. | Validate with Decimal, ensure the value is integral, then cast to INT. | Affected cells count all non-null values successfully cast to INT. | 46435 | 46435 | 9.0<br>2.0<br>0.0<br>5.0<br>16.0 | 9 (INT)<br>2 (INT)<br>0 (INT)<br>5 (INT)<br>16 (INT) |
| Ambulances | Blank string or whitespace-only token | R7: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1049 | 1049 | "" | NULL |
| Ambulances | Count-style measure stored as float-style CSV text | R7: cast the column to INT after trim validation and keep blanks as NULL. | The plan explicitly requires integer casting for count-style measures such as '4.0' -> 4. | Validate with Decimal, ensure the value is integral, then cast to INT. | Affected cells count all non-null values successfully cast to INT. | 47059 | 47059 | 2.0<br>0.0<br>1.0<br>4.0<br>8.0 | 2 (INT)<br>0 (INT)<br>1 (INT)<br>4 (INT)<br>8 (INT) |
| Helicopters | Blank string or whitespace-only token | R7: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 2454 | 2454 | "" | NULL |
| Helicopters | Count-style measure stored as float-style CSV text | R7: cast the column to INT after trim validation and keep blanks as NULL. | The plan explicitly requires integer casting for count-style measures such as '4.0' -> 4. | Validate with Decimal, ensure the value is integral, then cast to INT. | Affected cells count all non-null values successfully cast to INT. | 45654 | 45654 | 0.0<br>3.0<br>1.0<br>2.0 | 0 (INT)<br>3 (INT)<br>1 (INT)<br>2 (INT) |
| Excavators | Blank string or whitespace-only token | R7: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 2357 | 2357 | "" | NULL |
| Excavators | Count-style measure stored as float-style CSV text | R7: cast the column to INT after trim validation and keep blanks as NULL. | The plan explicitly requires integer casting for count-style measures such as '4.0' -> 4. | Validate with Decimal, ensure the value is integral, then cast to INT. | Affected cells count all non-null values successfully cast to INT. | 45751 | 45751 | 1.0<br>0.0<br>8.0<br>3.0<br>6.0 | 1 (INT)<br>0 (INT)<br>8 (INT)<br>3 (INT)<br>6 (INT) |
| JCB_Machines | Blank string or whitespace-only token | R7: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 2234 | 2234 | "" | NULL |
| JCB_Machines | Count-style measure stored as float-style CSV text | R7: cast the column to INT after trim validation and keep blanks as NULL. | The plan explicitly requires integer casting for count-style measures such as '4.0' -> 4. | Validate with Decimal, ensure the value is integral, then cast to INT. | Affected cells count all non-null values successfully cast to INT. | 45874 | 45874 | 1.0<br>0.0<br>6.0<br>2.0<br>4.0 | 1 (INT)<br>0 (INT)<br>6 (INT)<br>2 (INT)<br>4 (INT) |
| Cranes | Blank string or whitespace-only token | R7: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1137 | 1137 | "" | NULL |
| Cranes | Count-style measure stored as float-style CSV text | R7: cast the column to INT after trim validation and keep blanks as NULL. | The plan explicitly requires integer casting for count-style measures such as '4.0' -> 4. | Validate with Decimal, ensure the value is integral, then cast to INT. | Affected cells count all non-null values successfully cast to INT. | 46971 | 46971 | 0.0<br>4.0<br>3.0<br>1.0<br>2.0 | 0 (INT)<br>4 (INT)<br>3 (INT)<br>1 (INT)<br>2 (INT) |
| Relief_Camps | Blank string or whitespace-only token | R7: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 2291 | 2291 | "" | NULL |
| Relief_Camps | Count-style measure stored as float-style CSV text | R7: cast the column to INT after trim validation and keep blanks as NULL. | The plan explicitly requires integer casting for count-style measures such as '4.0' -> 4. | Validate with Decimal, ensure the value is integral, then cast to INT. | Affected cells count all non-null values successfully cast to INT. | 45817 | 45817 | 0.0<br>3.0<br>4.0<br>2.0<br>9.0 | 0 (INT)<br>3 (INT)<br>4 (INT)<br>2 (INT)<br>9 (INT) |
| Evacuated_People | Blank string or whitespace-only token | R7: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1388 | 1388 | "" | NULL |
| Evacuated_People | Count-style measure stored as float-style CSV text | R7: cast the column to INT after trim validation and keep blanks as NULL. | The plan explicitly requires integer casting for count-style measures such as '4.0' -> 4. | Validate with Decimal, ensure the value is integral, then cast to INT. | Affected cells count all non-null values successfully cast to INT. | 46720 | 46720 | 0.0<br>9.0<br>8.0<br>19.0<br>5.0 | 0 (INT)<br>9 (INT)<br>8 (INT)<br>19 (INT)<br>5 (INT) |
| Aid_Amount_INR | Blank string or whitespace-only token | R8: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1485 | 1485 | "" | NULL |
| Aid_Amount_INR | Decimal measure stored as CSV text | R8: cast the column to DECIMAL and keep blanks as NULL. | The v1 schema requires typed decimal measures in the cleaned layer. | Validate the trimmed token with Decimal and write a DECIMAL-typed output cell. | Affected cells count all non-null values successfully cast to DECIMAL. | 46623 | 46623 | 0.0<br>5521462.0<br>4485236.0<br>2677568.0<br>5118481.0 | 0.0 (DECIMAL)<br>5521462.0 (DECIMAL)<br>4485236.0 (DECIMAL)<br>2677568.0 (DECIMAL)<br>5118481.0 (DECIMAL) |
| Aid_Amount_INR | Invalid negative aid payment | R8: negative Aid_Amount_INR values must become NULL pending source verification. | The frozen plan allows exactly one invalid-value correction in v1. | Parse Aid_Amount_INR as Decimal, detect values below zero, then set them to NULL. | Affected cells count non-null Aid_Amount_INR values where Decimal(value) < 0. | 51 | 51 | -1.0<br>-3952325.0<br>-3810791.0<br>-2255701.0<br>-4053341.0 | NULL<br>NULL<br>NULL<br>NULL<br>NULL |
| Relief_Materials_Tons | Blank string or whitespace-only token | R7: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1496 | 1496 | "" | NULL |
| Relief_Materials_Tons | Decimal measure stored as CSV text | R7: cast the column to DECIMAL and keep blanks as NULL. | The v1 schema requires typed decimal measures in the cleaned layer. | Validate the trimmed token with Decimal and write a DECIMAL-typed output cell. | Affected cells count all non-null values successfully cast to DECIMAL. | 46612 | 46612 | 0.0<br>6.5<br>27.9<br>6.1<br>7.2 | 0.0 (DECIMAL)<br>6.5 (DECIMAL)<br>27.9 (DECIMAL)<br>6.1 (DECIMAL)<br>7.2 (DECIMAL) |
| Compensation_Provided | Blank string or whitespace-only token | R8: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 982 | 982 | "" | NULL |
| Compensation_Provided | Category normalization against approved canonical labels | R8: trim and enforce the canonical label set defined in the frozen plan. | The base cleaned layer must standardize categorical labels without introducing new values. | Normalize by trim and case, map to approved canonical label, and preserve NULLs. | Affected cells count non-null category values whose canonical label differs from the raw token. | 0 | 0 | n/a | n/a |
| Recovery_Days | Blank string or whitespace-only token | R7: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1377 | 1377 | "" | NULL |
| Recovery_Days | Count-style measure stored as float-style CSV text | R7: cast the column to INT after trim validation and keep blanks as NULL. | The plan explicitly requires integer casting for count-style measures such as '4.0' -> 4. | Validate with Decimal, ensure the value is integral, then cast to INT. | Affected cells count all non-null values successfully cast to INT. | 46731 | 46731 | 1.0<br>0.0<br>2.0<br>161.0<br>15.0 | 1 (INT)<br>0 (INT)<br>2 (INT)<br>161 (INT)<br>15 (INT) |
| Power_Outage_Hours | Blank string or whitespace-only token | R7: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1073 | 1073 | "" | NULL |
| Power_Outage_Hours | Decimal measure stored as CSV text | R7: cast the column to DECIMAL and keep blanks as NULL. | The v1 schema requires typed decimal measures in the cleaned layer. | Validate the trimmed token with Decimal and write a DECIMAL-typed output cell. | Affected cells count all non-null values successfully cast to DECIMAL. | 47035 | 47035 | 0.0<br>2.6<br>21.7<br>7.8<br>6.3 | 0.0 (DECIMAL)<br>2.6 (DECIMAL)<br>21.7 (DECIMAL)<br>7.8 (DECIMAL)<br>6.3 (DECIMAL) |
| Water_Supply_Disrupted | Blank string or whitespace-only token | R8: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 1013 | 1013 | "" | NULL |
| Water_Supply_Disrupted | Category normalization against approved canonical labels | R8: trim and enforce the canonical label set defined in the frozen plan. | The base cleaned layer must standardize categorical labels without introducing new values. | Normalize by trim and case, map to approved canonical label, and preserve NULLs. | Affected cells count non-null category values whose canonical label differs from the raw token. | 0 | 0 | n/a | n/a |
| Communication_Disruption | Blank string or whitespace-only token | R8: convert blank strings to NULL and preserve nulls in the base cleaned table | The v1 plan requires blank strings to be normalized to NULL without dropping rows. | Strip whitespace, treat empty result as NULL, and write a blank output cell. | Affected cells count raw values where value.strip() == ''. | 968 | 968 | "" | NULL |
| Communication_Disruption | Category normalization against approved canonical labels | R8: trim and enforce the canonical label set defined in the frozen plan. | The base cleaned layer must standardize categorical labels without introducing new values. | Normalize by trim and case, map to approved canonical label, and preserve NULLs. | Affected cells count non-null category values whose canonical label differs from the raw token. | 0 | 0 | n/a | n/a |

## C. Missing Value Summary

| Column | Missing values before cleaning | Missing values after cleaning | Action taken | Imputation technique used |
| --- | ---: | ---: | --- | --- |
| Event_ID | 0 | 0 | Kept as NULL | None in v1 |
| Date | 892 | 892 | Kept as NULL | None in v1 |
| State | 896 | 896 | Kept as NULL | None in v1 |
| District | 1861 | 1861 | Kept as NULL | None in v1 |
| Latitude | 1107 | 1107 | Kept as NULL | None in v1 |
| Longitude | 1135 | 1135 | Kept as NULL | None in v1 |
| Season | 936 | 936 | Kept as NULL | None in v1 |
| Rainfall_mm | 2571 | 2571 | Kept as NULL | None in v1 |
| Elevation_m | 1490 | 1490 | Kept as NULL | None in v1 |
| Slope_Degree | 1537 | 1537 | Kept as NULL | None in v1 |
| Soil_Type | 1962 | 1962 | Kept as NULL | None in v1 |
| NDVI | 1573 | 1573 | Kept as NULL | None in v1 |
| Temperature_C | 959 | 959 | Kept as NULL | None in v1 |
| Humidity | 1108 | 1108 | Kept as NULL | None in v1 |
| Distance_to_River_km | 1415 | 1415 | Kept as NULL | None in v1 |
| Land_Use | 1925 | 1925 | Kept as NULL | None in v1 |
| Historical_Landslide_Count | 1008 | 1008 | Kept as NULL | None in v1 |
| Landslide_Occurred | 686 | 686 | Kept as NULL | None in v1 |
| Landslide_Risk | 1490 | 1490 | Kept as NULL | None in v1 |
| Casualties | 2174 | 2174 | Kept as NULL | None in v1 |
| Injured | 1622 | 1622 | Kept as NULL | None in v1 |
| Missing_Persons | 1203 | 1203 | Kept as NULL | None in v1 |
| Families_Affected | 1869 | 1869 | Kept as NULL | None in v1 |
| Population_Affected | 1463 | 1463 | Kept as NULL | None in v1 |
| Houses_Damaged | 2120 | 2120 | Kept as NULL | None in v1 |
| Roads_Blocked_km | 2114 | 2114 | Kept as NULL | None in v1 |
| Bridges_Damaged | 1689 | 1689 | Kept as NULL | None in v1 |
| Economic_Loss_INR | 1976 | 1976 | Kept as NULL | None in v1 |
| Cropland_Damaged | 1173 | 1173 | Kept as NULL | None in v1 |
| Livestock_Lost | 1850 | 1850 | Kept as NULL | None in v1 |
| Response_ID | 0 | 0 | Kept as NULL | None in v1 |
| Response_Time_Min | 1555 | 1555 | Kept as NULL | None in v1 |
| Rescue_Duration_Hours | 3615 | 3615 | Kept as NULL | None in v1 |
| Human_Resources_Deployed | 2217 | 2217 | Kept as NULL | None in v1 |
| Rescue_Teams | 2288 | 2288 | Kept as NULL | None in v1 |
| NDRF_Teams | 1826 | 1826 | Kept as NULL | None in v1 |
| SDRF_Teams | 1368 | 1368 | Kept as NULL | None in v1 |
| Volunteers | 1673 | 1673 | Kept as NULL | None in v1 |
| Ambulances | 1049 | 1049 | Kept as NULL | None in v1 |
| Helicopters | 2454 | 2454 | Kept as NULL | None in v1 |
| Excavators | 2357 | 2357 | Kept as NULL | None in v1 |
| JCB_Machines | 2234 | 2234 | Kept as NULL | None in v1 |
| Cranes | 1137 | 1137 | Kept as NULL | None in v1 |
| Relief_Camps | 2291 | 2291 | Kept as NULL | None in v1 |
| Evacuated_People | 1388 | 1388 | Kept as NULL | None in v1 |
| Aid_Amount_INR | 1485 | 1536 | Kept as NULL; plus 51 invalid negatives converted to NULL | None in v1 |
| Relief_Materials_Tons | 1496 | 1496 | Kept as NULL | None in v1 |
| Compensation_Provided | 982 | 982 | Kept as NULL | None in v1 |
| Recovery_Days | 1377 | 1377 | Kept as NULL | None in v1 |
| Power_Outage_Hours | 1073 | 1073 | Kept as NULL | None in v1 |
| Water_Supply_Disrupted | 1013 | 1013 | Kept as NULL | None in v1 |
| Communication_Disruption | 968 | 968 | Kept as NULL | None in v1 |

## D. Duplicate Summary

- Duplicate rows detected in raw snapshot: 0
- Duplicate rows removed: 0
- Duplicate rows detected after cleaning normalization: 0
- Duplicate Event_ID values: 0
- Duplicate Response_ID values: 0
- Actions taken: no rows were dropped in v1; duplicate checks were executed and all current counts passed the frozen-plan acceptance criteria.

## E. Data Type Conversion Summary

| Column | Original data type | New data type | Reason for conversion | Number of values converted |
| --- | --- | --- | --- | ---: |
| Date | CSV string token | DATE | Target type is explicitly defined in the frozen v1 plan. | 47216 |
| Latitude | CSV string token | DECIMAL | Target type is explicitly defined in the frozen v1 plan. | 47001 |
| Longitude | CSV string token | DECIMAL | Target type is explicitly defined in the frozen v1 plan. | 46973 |
| Rainfall_mm | CSV string token | DECIMAL | Target type is explicitly defined in the frozen v1 plan. | 45537 |
| Elevation_m | CSV string token | DECIMAL | Target type is explicitly defined in the frozen v1 plan. | 46618 |
| Slope_Degree | CSV string token | DECIMAL | Target type is explicitly defined in the frozen v1 plan. | 46571 |
| NDVI | CSV string token | DECIMAL | Target type is explicitly defined in the frozen v1 plan. | 46535 |
| Temperature_C | CSV string token | DECIMAL | Target type is explicitly defined in the frozen v1 plan. | 47149 |
| Humidity | CSV string token | DECIMAL | Target type is explicitly defined in the frozen v1 plan. | 47000 |
| Distance_to_River_km | CSV string token | DECIMAL | Target type is explicitly defined in the frozen v1 plan. | 46693 |
| Historical_Landslide_Count | CSV string token | INT | Target type is explicitly defined in the frozen v1 plan. | 47100 |
| Casualties | CSV string token | INT | Target type is explicitly defined in the frozen v1 plan. | 45934 |
| Injured | CSV string token | INT | Target type is explicitly defined in the frozen v1 plan. | 46486 |
| Missing_Persons | CSV string token | INT | Target type is explicitly defined in the frozen v1 plan. | 46905 |
| Families_Affected | CSV string token | INT | Target type is explicitly defined in the frozen v1 plan. | 46239 |
| Population_Affected | CSV string token | INT | Target type is explicitly defined in the frozen v1 plan. | 46645 |
| Houses_Damaged | CSV string token | INT | Target type is explicitly defined in the frozen v1 plan. | 45988 |
| Roads_Blocked_km | CSV string token | DECIMAL | Target type is explicitly defined in the frozen v1 plan. | 45994 |
| Bridges_Damaged | CSV string token | INT | Target type is explicitly defined in the frozen v1 plan. | 46419 |
| Economic_Loss_INR | CSV string token | DECIMAL | Target type is explicitly defined in the frozen v1 plan. | 46132 |
| Cropland_Damaged | CSV string token | DECIMAL | Target type is explicitly defined in the frozen v1 plan. | 46935 |
| Livestock_Lost | CSV string token | INT | Target type is explicitly defined in the frozen v1 plan. | 46258 |
| Response_Time_Min | CSV string token | DECIMAL | Target type is explicitly defined in the frozen v1 plan. | 46553 |
| Rescue_Duration_Hours | CSV string token | DECIMAL | Target type is explicitly defined in the frozen v1 plan. | 44493 |
| Human_Resources_Deployed | CSV string token | INT | Target type is explicitly defined in the frozen v1 plan. | 45891 |
| Rescue_Teams | CSV string token | INT | Target type is explicitly defined in the frozen v1 plan. | 45820 |
| NDRF_Teams | CSV string token | INT | Target type is explicitly defined in the frozen v1 plan. | 46282 |
| SDRF_Teams | CSV string token | INT | Target type is explicitly defined in the frozen v1 plan. | 46740 |
| Volunteers | CSV string token | INT | Target type is explicitly defined in the frozen v1 plan. | 46435 |
| Ambulances | CSV string token | INT | Target type is explicitly defined in the frozen v1 plan. | 47059 |
| Helicopters | CSV string token | INT | Target type is explicitly defined in the frozen v1 plan. | 45654 |
| Excavators | CSV string token | INT | Target type is explicitly defined in the frozen v1 plan. | 45751 |
| JCB_Machines | CSV string token | INT | Target type is explicitly defined in the frozen v1 plan. | 45874 |
| Cranes | CSV string token | INT | Target type is explicitly defined in the frozen v1 plan. | 46971 |
| Relief_Camps | CSV string token | INT | Target type is explicitly defined in the frozen v1 plan. | 45817 |
| Evacuated_People | CSV string token | INT | Target type is explicitly defined in the frozen v1 plan. | 46720 |
| Aid_Amount_INR | CSV string token | DECIMAL | Target type is explicitly defined in the frozen v1 plan. | 46623 |
| Relief_Materials_Tons | CSV string token | DECIMAL | Target type is explicitly defined in the frozen v1 plan. | 46612 |
| Recovery_Days | CSV string token | INT | Target type is explicitly defined in the frozen v1 plan. | 46731 |
| Power_Outage_Hours | CSV string token | DECIMAL | Target type is explicitly defined in the frozen v1 plan. | 47035 |

## F. Category Harmonisation Summary

### State
- Original categories: `Andhra Pradesh`, `Arunachal Pradesh`, `Assam`, `Goa`, `Himachal Pradesh`, `Jammu and Kashmir`, `Karnataka`, `Kerala`, `Maharashtra`, `Manipur`, `Meghalaya`, `Mizoram`, `Nagaland`, `Odisha`, `Sikkim`, `Tamil Nadu`, `Uttarakhand`, `West Bengal`
- Canonical categories: `Andhra Pradesh`, `Arunachal Pradesh`, `Assam`, `Goa`, `Himachal Pradesh`, `Jammu and Kashmir`, `Karnataka`, `Kerala`, `Maharashtra`, `Manipur`, `Meghalaya`, `Mizoram`, `Nagaland`, `Odisha`, `Sikkim`, `Tamil Nadu`, `Uttarakhand`, `West Bengal`
- Number of category values modified: 0
- Harmonisation rules applied: Trim and case-normalize against the frozen canonical label set.

### District
- Original categories: `Aizawl`, `Alluri Sitharama Raju`, `Cachar`, `Chamoli`, `Chikmagalur`, `Churachandpur`, `Coimbatore`, `Dakshina Kannada`, `Darjeeling`, `Doda`, `East Khasi Hills`, `East Sikkim`, `Gajapati`, `Gangtok`, `Idukki`, `Kalimpong`, `Kanyakumari`, `Karbi Anglong`, `Kinnaur`, `Kishtwar`, `Kodagu`, `Kohima`, `Koraput`, `Kottayam`, `Kozhikode`, `Kullu`, `Lunglei`, `Mandi`, `Nilgiris`, `North Goa`, `North Sikkim`, `Papum Pare`, `Phek`, `Pithoragarh`, `Raigad`, `Ramban`, `Ratnagiri`, `Rudraprayag`, `Satara`, `Shimla`, `South Goa`, `Tehri Garhwal`, `Ukhrul`, `Uttarkashi`, `Visakhapatnam`, `Wayanad`, `West Garo Hills`, `West Kameng`
- Canonical categories: `Aizawl`, `Alluri Sitharama Raju`, `Cachar`, `Chamoli`, `Chikmagalur`, `Churachandpur`, `Coimbatore`, `Dakshina Kannada`, `Darjeeling`, `Doda`, `East Khasi Hills`, `East Sikkim`, `Gajapati`, `Gangtok`, `Idukki`, `Kalimpong`, `Kanyakumari`, `Karbi Anglong`, `Kinnaur`, `Kishtwar`, `Kodagu`, `Kohima`, `Koraput`, `Kottayam`, `Kozhikode`, `Kullu`, `Lunglei`, `Mandi`, `Nilgiris`, `North Goa`, `North Sikkim`, `Papum Pare`, `Phek`, `Pithoragarh`, `Raigad`, `Ramban`, `Ratnagiri`, `Rudraprayag`, `Satara`, `Shimla`, `South Goa`, `Tehri Garhwal`, `Ukhrul`, `Uttarkashi`, `Visakhapatnam`, `Wayanad`, `West Garo Hills`, `West Kameng`
- Number of category values modified: 0
- Harmonisation rules applied: Trim only in v1; do not merge district spellings without a geography reference file.

### Season
- Original categories: `Monsoon`, `Post-Monsoon`, `Pre-Monsoon`, `Winter`
- Canonical categories: `Monsoon`, `Post-Monsoon`, `Pre-Monsoon`, `Winter`
- Number of category values modified: 0
- Harmonisation rules applied: Trim and case-normalize against the frozen canonical label set.

### Soil_Type
- Original categories: `Alluvial`, `Clayey`, `Laterite`, `Loamy`, `Rocky`, `Sandy Loam`, `Silty`
- Canonical categories: `Alluvial`, `Clayey`, `Laterite`, `Loamy`, `Rocky`, `Sandy Loam`, `Silty`
- Number of category values modified: 0
- Harmonisation rules applied: Trim and case-normalize against the frozen canonical label set.

### Land_Use
- Original categories: `Agricultural`, `Barren/Rocky`, `Forest`, `Mixed Settlement`, `Plantation`, `Residential`, `Road Corridor`
- Canonical categories: `Agricultural`, `Barren/Rocky`, `Forest`, `Mixed Settlement`, `Plantation`, `Residential`, `Road Corridor`
- Number of category values modified: 0
- Harmonisation rules applied: Trim and case-normalize against the frozen canonical label set.

### Landslide_Occurred
- Original categories: `No`, `Yes`
- Canonical categories: `Yes`, `No`
- Number of category values modified: 0
- Harmonisation rules applied: Trim and case-normalize against the frozen canonical label set.

### Landslide_Risk
- Original categories: `High`, `Low`, `Moderate`, `Very High`
- Canonical categories: `Low`, `Moderate`, `High`, `Very High`
- Number of category values modified: 0
- Harmonisation rules applied: Trim and case-normalize against the frozen canonical label set.

### Compensation_Provided
- Original categories: `No`, `Yes`
- Canonical categories: `Yes`, `No`
- Number of category values modified: 0
- Harmonisation rules applied: Trim and case-normalize against the frozen canonical label set.

### Water_Supply_Disrupted
- Original categories: `No`, `Yes`
- Canonical categories: `Yes`, `No`
- Number of category values modified: 0
- Harmonisation rules applied: Trim and case-normalize against the frozen canonical label set.

### Communication_Disruption
- Original categories: `No`, `Yes`
- Canonical categories: `Yes`, `No`
- Number of category values modified: 0
- Harmonisation rules applied: Trim and case-normalize against the frozen canonical label set.

## G. Invalid Value Corrections

| Column name | Invalid value detected | Validation rule used | Correction applied | Number of affected rows |
| --- | --- | --- | --- | ---: |
| Aid_Amount_INR | Negative aid payment value | Negative Aid_Amount_INR is invalid in v1; NDVI and Temperature_C negatives remain valid by plan. | Set negative values to NULL pending source verification | 51 |

## H. Dataset Validation

- Final row count: 48108
- Final column count: 52
- Rows retained: 48108
- Rows dropped: 0
- Columns modified: 50 (Date, State, District, Latitude, Longitude, Season, Rainfall_mm, Elevation_m, Slope_Degree, Soil_Type, NDVI, Temperature_C, Humidity, Distance_to_River_km, Land_Use, Historical_Landslide_Count, Landslide_Occurred, Landslide_Risk, Casualties, Injured, Missing_Persons, Families_Affected, Population_Affected, Houses_Damaged, Roads_Blocked_km, Bridges_Damaged, Economic_Loss_INR, Cropland_Damaged, Livestock_Lost, Response_Time_Min, Rescue_Duration_Hours, Human_Resources_Deployed, Rescue_Teams, NDRF_Teams, SDRF_Teams, Volunteers, Ambulances, Helicopters, Excavators, JCB_Machines, Cranes, Relief_Camps, Evacuated_People, Aid_Amount_INR, Relief_Materials_Tons, Compensation_Provided, Recovery_Days, Power_Outage_Hours, Water_Supply_Disrupted, Communication_Disruption)
- Total cells modified: 1937039
- Exact duplicate rows after cleaning: 0
- Duplicate Event_ID values after cleaning: 0
- Duplicate Response_ID values after cleaning: 0
- Data types: all DATE, DECIMAL, and INT target columns validated successfully with zero malformed-token failures.
- Category consistency: all audited category fields resolved to the approved canonical sets; District remained trim-only as required.
- Missing values: nulls were preserved in the base cleaned table; no statistical imputation was performed.
- Validation status: Pass

## I. Cleaning Metrics

- Total cleaning operations performed: 103
- Total columns affected: 50
- Total rows affected: 48108
- Total cells modified: 1937039
- Total duplicate rows removed: 0
- Total invalid values corrected: 51
- Total missing values handled: 79701
- Percentage of dataset affected by cleaning: 77.43% of 2,501,616 cells

## J. Change Log

| Step number | Operation performed | Columns affected | Number of rows affected | Reason for the transformation |
| ---: | --- | --- | ---: | --- |
| 1 | Verified the frozen snapshot profile and schema before transformation | All columns | 48108 | Confirm the input matches the authoritative cleaning plan v1 snapshot. |
| 2 | Normalized blank strings to NULL | Date, State, District, Latitude, Longitude, Season, Rainfall_mm, Elevation_m, Slope_Degree, Soil_Type, NDVI, Temperature_C, Humidity, Distance_to_River_km, Land_Use, Historical_Landslide_Count, Landslide_Occurred, Landslide_Risk, Casualties, Injured, Missing_Persons, Families_Affected, Population_Affected, Houses_Damaged, Roads_Blocked_km, Bridges_Damaged, Economic_Loss_INR, Cropland_Damaged, Livestock_Lost, Response_Time_Min, Rescue_Duration_Hours, Human_Resources_Deployed, Rescue_Teams, NDRF_Teams, SDRF_Teams, Volunteers, Ambulances, Helicopters, Excavators, JCB_Machines, Cranes, Relief_Camps, Evacuated_People, Aid_Amount_INR, Relief_Materials_Tons, Compensation_Provided, Recovery_Days, Power_Outage_Hours, Water_Supply_Disrupted, Communication_Disruption | 39171 | The plan requires NULL preservation without row drops or fill-ins. |
| 3 | Applied trim and canonical text harmonisation | Communication_Disruption, Compensation_Provided, District, Event_ID, Land_Use, Landslide_Occurred, Landslide_Risk, Response_ID, Season, Soil_Type, State, Water_Supply_Disrupted | 0 | The plan permits formatting-only normalization and canonical category enforcement. |
| 4 | Cast Date to DATE | Date | 47216 | Date is the only target DATE field in v1. |
| 5 | Cast decimal measures to DECIMAL | Aid_Amount_INR, Cropland_Damaged, Distance_to_River_km, Economic_Loss_INR, Elevation_m, Humidity, Latitude, Longitude, NDVI, Power_Outage_Hours, Rainfall_mm, Relief_Materials_Tons, Rescue_Duration_Hours, Response_Time_Min, Roads_Blocked_km, Slope_Degree, Temperature_C | 48108 | The plan defines these continuous measures as DECIMAL. |
| 6 | Cast count-style measures to INT | Ambulances, Bridges_Damaged, Casualties, Cranes, Evacuated_People, Excavators, Families_Affected, Helicopters, Historical_Landslide_Count, Houses_Damaged, Human_Resources_Deployed, Injured, JCB_Machines, Livestock_Lost, Missing_Persons, NDRF_Teams, Population_Affected, Recovery_Days, Relief_Camps, Rescue_Teams, SDRF_Teams, Volunteers | 48108 | The plan defines these columns as integer counts, even when the CSV stores tokens like 4.0. |
| 7 | Converted invalid negative Aid_Amount_INR values to NULL | Aid_Amount_INR | 51 | Negative aid payments are the only explicit invalid-value exception allowed in v1. |
| 8 | Revalidated row counts, key uniqueness, duplicate rows, target types, category sets, and null preservation | All columns | 48108 | Ensure the cleaned layer passes every acceptance criterion from the frozen plan. |
