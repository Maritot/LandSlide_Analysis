from __future__ import annotations

import csv
import hashlib
import html
import re
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
RAW_INPUT = ROOT / "data" / "Raw_Data.csv"
USER_INPUT = Path(
    r"C:\Users\tharu\OneDrive\Desktop\SocialPrachar\Projects\LandSlide_Analysis\Merged_Landslide_Data.csv"
)
PLAN_PATH = ROOT / "docs" / "cleaning-plan-v1.docx"
OUTPUT_CSV = ROOT / "data" / "Cleaned_Landslide_Data_v1.csv"
OUTPUT_XLSX = ROOT / "data" / "Cleaned_Landslide_Data_v1.xlsx"
OUTPUT_REPORT = ROOT / "docs" / "Data_Cleaning_Report_v1.md"

EXPECTED_ROW_COUNT = 48_108
EXPECTED_COLUMN_COUNT = 52
EXPECTED_NEGATIVE_AID_COUNT = 51
EXPECTED_MISSING_COUNTS = {
    "Date": 892,
    "State": 896,
    "District": 1861,
    "Latitude": 1107,
    "Longitude": 1135,
    "Season": 936,
    "Rainfall_mm": 2571,
    "Elevation_m": 1490,
    "Slope_Degree": 1537,
    "Soil_Type": 1962,
    "NDVI": 1573,
    "Temperature_C": 959,
    "Humidity": 1108,
    "Distance_to_River_km": 1415,
    "Land_Use": 1925,
    "Historical_Landslide_Count": 1008,
    "Landslide_Occurred": 686,
    "Landslide_Risk": 1490,
    "Casualties": 2174,
    "Injured": 1622,
    "Missing_Persons": 1203,
    "Families_Affected": 1869,
    "Population_Affected": 1463,
    "Houses_Damaged": 2120,
    "Roads_Blocked_km": 2114,
    "Bridges_Damaged": 1689,
    "Economic_Loss_INR": 1976,
    "Cropland_Damaged": 1173,
    "Livestock_Lost": 1850,
    "Response_Time_Min": 1555,
    "Rescue_Duration_Hours": 3615,
    "Human_Resources_Deployed": 2217,
    "Rescue_Teams": 2288,
    "NDRF_Teams": 1826,
    "SDRF_Teams": 1368,
    "Volunteers": 1673,
    "Ambulances": 1049,
    "Helicopters": 2454,
    "Excavators": 2357,
    "JCB_Machines": 2234,
    "Cranes": 1137,
    "Relief_Camps": 2291,
    "Evacuated_People": 1388,
    "Aid_Amount_INR": 1485,
    "Relief_Materials_Tons": 1496,
    "Compensation_Provided": 982,
    "Recovery_Days": 1377,
    "Power_Outage_Hours": 1073,
    "Water_Supply_Disrupted": 1013,
    "Communication_Disruption": 968,
    "Event_ID": 0,
    "Response_ID": 0,
}

HEADERS = [
    "Event_ID",
    "Date",
    "State",
    "District",
    "Latitude",
    "Longitude",
    "Season",
    "Rainfall_mm",
    "Elevation_m",
    "Slope_Degree",
    "Soil_Type",
    "NDVI",
    "Temperature_C",
    "Humidity",
    "Distance_to_River_km",
    "Land_Use",
    "Historical_Landslide_Count",
    "Landslide_Occurred",
    "Landslide_Risk",
    "Casualties",
    "Injured",
    "Missing_Persons",
    "Families_Affected",
    "Population_Affected",
    "Houses_Damaged",
    "Roads_Blocked_km",
    "Bridges_Damaged",
    "Economic_Loss_INR",
    "Cropland_Damaged",
    "Livestock_Lost",
    "Response_ID",
    "Response_Time_Min",
    "Rescue_Duration_Hours",
    "Human_Resources_Deployed",
    "Rescue_Teams",
    "NDRF_Teams",
    "SDRF_Teams",
    "Volunteers",
    "Ambulances",
    "Helicopters",
    "Excavators",
    "JCB_Machines",
    "Cranes",
    "Relief_Camps",
    "Evacuated_People",
    "Aid_Amount_INR",
    "Relief_Materials_Tons",
    "Compensation_Provided",
    "Recovery_Days",
    "Power_Outage_Hours",
    "Water_Supply_Disrupted",
    "Communication_Disruption",
]

DATE_COLUMNS = {"Date"}
DECIMAL_COLUMNS = {
    "Latitude",
    "Longitude",
    "Rainfall_mm",
    "Elevation_m",
    "Slope_Degree",
    "NDVI",
    "Temperature_C",
    "Humidity",
    "Distance_to_River_km",
    "Roads_Blocked_km",
    "Economic_Loss_INR",
    "Cropland_Damaged",
    "Response_Time_Min",
    "Rescue_Duration_Hours",
    "Aid_Amount_INR",
    "Relief_Materials_Tons",
    "Power_Outage_Hours",
}
INTEGER_COLUMNS = {
    "Historical_Landslide_Count",
    "Casualties",
    "Injured",
    "Missing_Persons",
    "Families_Affected",
    "Population_Affected",
    "Houses_Damaged",
    "Bridges_Damaged",
    "Livestock_Lost",
    "Human_Resources_Deployed",
    "Rescue_Teams",
    "NDRF_Teams",
    "SDRF_Teams",
    "Volunteers",
    "Ambulances",
    "Helicopters",
    "Excavators",
    "JCB_Machines",
    "Cranes",
    "Relief_Camps",
    "Evacuated_People",
    "Recovery_Days",
}
TYPED_COLUMNS = DATE_COLUMNS | DECIMAL_COLUMNS | INTEGER_COLUMNS
KEY_COLUMNS = {"Event_ID", "Response_ID"}
TRIM_ONLY_COLUMNS = {"Event_ID", "Response_ID", "District"}

CANONICAL_SETS = {
    "State": [
        "Andhra Pradesh",
        "Arunachal Pradesh",
        "Assam",
        "Goa",
        "Himachal Pradesh",
        "Jammu and Kashmir",
        "Karnataka",
        "Kerala",
        "Maharashtra",
        "Manipur",
        "Meghalaya",
        "Mizoram",
        "Nagaland",
        "Odisha",
        "Sikkim",
        "Tamil Nadu",
        "Uttarakhand",
        "West Bengal",
    ],
    "Season": ["Monsoon", "Post-Monsoon", "Pre-Monsoon", "Winter"],
    "Soil_Type": ["Alluvial", "Clayey", "Laterite", "Loamy", "Rocky", "Sandy Loam", "Silty"],
    "Land_Use": [
        "Agricultural",
        "Barren/Rocky",
        "Forest",
        "Mixed Settlement",
        "Plantation",
        "Residential",
        "Road Corridor",
    ],
    "Landslide_Occurred": ["Yes", "No"],
    "Landslide_Risk": ["Low", "Moderate", "High", "Very High"],
    "Compensation_Provided": ["Yes", "No"],
    "Water_Supply_Disrupted": ["Yes", "No"],
    "Communication_Disruption": ["Yes", "No"],
}

ROW_RULES = {
    "Date": "R1",
    "State": "R1",
    "District": "R1",
    "Latitude": "R1",
    "Longitude": "R1",
    "Season": "R1",
    "Soil_Type": "R2",
    "Land_Use": "R2",
    "Rainfall_mm": "R3",
    "Elevation_m": "R3",
    "Slope_Degree": "R3",
    "NDVI": "R3",
    "Temperature_C": "R3",
    "Humidity": "R3",
    "Distance_to_River_km": "R3",
    "Historical_Landslide_Count": "R4",
    "Landslide_Occurred": "R5",
    "Landslide_Risk": "R5",
    "Casualties": "R6",
    "Injured": "R6",
    "Missing_Persons": "R6",
    "Families_Affected": "R6",
    "Population_Affected": "R6",
    "Houses_Damaged": "R6",
    "Roads_Blocked_km": "R6",
    "Bridges_Damaged": "R6",
    "Economic_Loss_INR": "R6",
    "Cropland_Damaged": "R6",
    "Livestock_Lost": "R6",
    "Response_Time_Min": "R7",
    "Rescue_Duration_Hours": "R7",
    "Human_Resources_Deployed": "R7",
    "Rescue_Teams": "R7",
    "NDRF_Teams": "R7",
    "SDRF_Teams": "R7",
    "Volunteers": "R7",
    "Ambulances": "R7",
    "Helicopters": "R7",
    "Excavators": "R7",
    "JCB_Machines": "R7",
    "Cranes": "R7",
    "Relief_Camps": "R7",
    "Evacuated_People": "R7",
    "Relief_Materials_Tons": "R7",
    "Recovery_Days": "R7",
    "Power_Outage_Hours": "R7",
    "Aid_Amount_INR": "R8",
    "Compensation_Provided": "R8",
    "Water_Supply_Disrupted": "R8",
    "Communication_Disruption": "R8",
}


def normalize_category_key(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).casefold()


CANONICAL_MAPS = {
    column: {normalize_category_key(value): value for value in values}
    for column, values in CANONICAL_SETS.items()
}


@dataclass
class OperationStat:
    op_id: str
    column_name: str
    cleaning_issue: str
    cleaning_rule_applied: str
    reason_for_cleaning: str
    cleaning_method_used: str
    metric_logic_used: str
    affected_rows: set[int] = field(default_factory=set)
    affected_cells: int = 0
    before_examples: list[str] = field(default_factory=list)
    after_examples: list[str] = field(default_factory=list)

    def add(self, row_number: int, before: str, after: str) -> None:
        self.affected_rows.add(row_number)
        self.affected_cells += 1
        if len(self.before_examples) < 5:
            pair = (before, after)
            existing = list(zip(self.before_examples, self.after_examples))
            if pair not in existing:
                self.before_examples.append(before)
                self.after_examples.append(after)


def build_operation_stat(op_id: str, column_name: str) -> OperationStat:
    rule_id = ROW_RULES.get(column_name, "N/A")
    if op_id == "blank_to_null":
        return OperationStat(
            op_id=op_id,
            column_name=column_name,
            cleaning_issue="Blank string or whitespace-only token",
            cleaning_rule_applied=f"{rule_id}: convert blank strings to NULL and preserve nulls in the base cleaned table",
            reason_for_cleaning="The v1 plan requires blank strings to be normalized to NULL without dropping rows.",
            cleaning_method_used="Strip whitespace, treat empty result as NULL, and write a blank output cell.",
            metric_logic_used="Affected cells count raw values where value.strip() == ''.",
        )
    if op_id == "text_trim":
        return OperationStat(
            op_id=op_id,
            column_name=column_name,
            cleaning_issue="Leading or trailing whitespace in text field",
            cleaning_rule_applied=f"{rule_id}: trim text values; District is trim-only and identifiers are preserved after trim.",
            reason_for_cleaning="The plan allows formatting-only normalization when business meaning remains unchanged.",
            cleaning_method_used="Apply str.strip() and keep the trimmed value.",
            metric_logic_used="Affected cells count non-null text values where trimmed_text != raw_text.",
        )
    if op_id == "category_harmonization":
        return OperationStat(
            op_id=op_id,
            column_name=column_name,
            cleaning_issue="Category normalization against approved canonical labels",
            cleaning_rule_applied=f"{rule_id}: trim and enforce the canonical label set defined in the frozen plan.",
            reason_for_cleaning="The base cleaned layer must standardize categorical labels without introducing new values.",
            cleaning_method_used="Normalize by trim and case, map to approved canonical label, and preserve NULLs.",
            metric_logic_used="Affected cells count non-null category values whose canonical label differs from the raw token.",
        )
    if op_id == "type_conversion_date":
        return OperationStat(
            op_id=op_id,
            column_name=column_name,
            cleaning_issue="Date stored as CSV text",
            cleaning_rule_applied="R1: cast Date to DATE and keep blanks as NULL.",
            reason_for_cleaning="The frozen plan defines Date as the single target date column.",
            cleaning_method_used="Validate ISO-8601 date tokens with date.fromisoformat and emit DATE-typed output.",
            metric_logic_used="Affected cells count all non-null Date values successfully cast to DATE.",
        )
    if op_id == "type_conversion_decimal":
        return OperationStat(
            op_id=op_id,
            column_name=column_name,
            cleaning_issue="Decimal measure stored as CSV text",
            cleaning_rule_applied=f"{rule_id}: cast the column to DECIMAL and keep blanks as NULL.",
            reason_for_cleaning="The v1 schema requires typed decimal measures in the cleaned layer.",
            cleaning_method_used="Validate the trimmed token with Decimal and write a DECIMAL-typed output cell.",
            metric_logic_used="Affected cells count all non-null values successfully cast to DECIMAL.",
        )
    if op_id == "type_conversion_integer":
        return OperationStat(
            op_id=op_id,
            column_name=column_name,
            cleaning_issue="Count-style measure stored as float-style CSV text",
            cleaning_rule_applied=f"{rule_id}: cast the column to INT after trim validation and keep blanks as NULL.",
            reason_for_cleaning="The plan explicitly requires integer casting for count-style measures such as '4.0' -> 4.",
            cleaning_method_used="Validate with Decimal, ensure the value is integral, then cast to INT.",
            metric_logic_used="Affected cells count all non-null values successfully cast to INT.",
        )
    if op_id == "negative_aid_to_null":
        return OperationStat(
            op_id=op_id,
            column_name=column_name,
            cleaning_issue="Invalid negative aid payment",
            cleaning_rule_applied="R8: negative Aid_Amount_INR values must become NULL pending source verification.",
            reason_for_cleaning="The frozen plan allows exactly one invalid-value correction in v1.",
            cleaning_method_used="Parse Aid_Amount_INR as Decimal, detect values below zero, then set them to NULL.",
            metric_logic_used="Affected cells count non-null Aid_Amount_INR values where Decimal(value) < 0.",
        )
    raise ValueError(f"Unsupported operation id: {op_id}")


def get_operation(
    operations: dict[tuple[str, str], OperationStat], op_id: str, column_name: str
) -> OperationStat:
    key = (op_id, column_name)
    if key not in operations:
        operations[key] = build_operation_stat(op_id, column_name)
    return operations[key]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_blank(value: str | None) -> bool:
    return value is None or value.strip() == ""


def parse_decimal(value: str, column_name: str, row_number: int) -> Decimal:
    try:
        return Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(
            f"Malformed decimal token in column '{column_name}' at CSV row {row_number}: {value!r}"
        ) from exc


def parse_integral_string(value: str, column_name: str, row_number: int) -> str:
    number = parse_decimal(value, column_name, row_number)
    if number != number.to_integral_value():
        raise ValueError(
            f"Non-integral token in INT column '{column_name}' at CSV row {row_number}: {value!r}"
        )
    return str(int(number))


def format_report_value(value: str | None) -> str:
    if value is None:
        return "NULL"
    if value == "":
        return '""'
    return value


def quote_values(values: Iterable[str]) -> str:
    values_list = list(values)
    if not values_list:
        return "None"
    return ", ".join(f"`{value}`" for value in values_list)


def digest_row(values: list[str]) -> str:
    return hashlib.sha256("\x1f".join(values).encode("utf-8")).hexdigest()


def excel_column_name(index: int) -> str:
    letters: list[str] = []
    current = index
    while current > 0:
        current, remainder = divmod(current - 1, 26)
        letters.append(chr(65 + remainder))
    return "".join(reversed(letters))


def xml_escape(value: str) -> str:
    return html.escape(value, quote=False)


def excel_serial(value: date) -> int:
    return (value - date(1899, 12, 30)).days


def write_xlsx_from_csv(csv_path: Path, xlsx_path: Path, headers: list[str]) -> None:
    row_count = sum(1 for _ in csv_path.open("r", encoding="utf-8-sig", newline="")) - 1
    total_rows = row_count + 1
    last_column = excel_column_name(len(headers))
    worksheet_ref = f"A1:{last_column}{total_rows}"

    xlsx_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(xlsx_path, "w", compression=zipfile.ZIP_DEFLATED) as workbook:
        workbook.writestr(
            "[Content_Types].xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>""",
        )
        workbook.writestr(
            "_rels/.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>""",
        )
        created_iso = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        workbook.writestr(
            "docProps/app.xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>OpenAI Codex</Application>
</Properties>""",
        )
        workbook.writestr(
            "docProps/core.xml",
            f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Cleaned Landslide Data v1</dc:title>
  <dc:creator>OpenAI Codex</dc:creator>
  <cp:lastModifiedBy>OpenAI Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{created_iso}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{created_iso}</dcterms:modified>
</cp:coreProperties>""",
        )
        workbook.writestr(
            "xl/workbook.xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Cleaned_Data" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>""",
        )
        workbook.writestr(
            "xl/_rels/workbook.xml.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>""",
        )
        workbook.writestr(
            "xl/styles.xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <numFmts count="1">
    <numFmt numFmtId="164" formatCode="yyyy-mm-dd"/>
  </numFmts>
  <fonts count="1">
    <font>
      <sz val="11"/>
      <name val="Calibri"/>
      <family val="2"/>
    </font>
  </fonts>
  <fills count="2">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
  </fills>
  <borders count="1">
    <border><left/><right/><top/><bottom/><diagonal/></border>
  </borders>
  <cellStyleXfs count="1">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0"/>
  </cellStyleXfs>
  <cellXfs count="2">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="164" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>
  </cellXfs>
  <cellStyles count="1">
    <cellStyle name="Normal" xfId="0" builtinId="0"/>
  </cellStyles>
</styleSheet>""",
        )

        with workbook.open("xl/worksheets/sheet1.xml", "w") as sheet_stream:
            def write_line(value: str) -> None:
                sheet_stream.write(value.encode("utf-8"))

            write_line("""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>""")
            write_line(
                """<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">"""
            )
            write_line(f"""<dimension ref="{worksheet_ref}"/>""")
            write_line("""<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>""")
            write_line("<sheetData>")

            header_cells = []
            for column_index, header in enumerate(headers, start=1):
                cell_ref = f"{excel_column_name(column_index)}1"
                header_cells.append(
                    f'<c r="{cell_ref}" t="inlineStr"><is><t>{xml_escape(header)}</t></is></c>'
                )
            write_line(f'<row r="1">{"".join(header_cells)}</row>')

            with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
                reader = csv.DictReader(handle)
                for row_index, row in enumerate(reader, start=2):
                    cells: list[str] = []
                    for column_index, header in enumerate(headers, start=1):
                        value = row[header]
                        if value == "":
                            continue
                        cell_ref = f"{excel_column_name(column_index)}{row_index}"
                        if header in DATE_COLUMNS:
                            parsed_date = date.fromisoformat(value)
                            cells.append(
                                f'<c r="{cell_ref}" s="1"><v>{excel_serial(parsed_date)}</v></c>'
                            )
                        elif header in INTEGER_COLUMNS or header in DECIMAL_COLUMNS:
                            cells.append(f'<c r="{cell_ref}"><v>{value}</v></c>')
                        else:
                            cells.append(
                                f'<c r="{cell_ref}" t="inlineStr"><is><t>{xml_escape(value)}</t></is></c>'
                            )
                    write_line(f'<row r="{row_index}">{"".join(cells)}</row>')

            write_line("</sheetData>")
            write_line(f'<autoFilter ref="{worksheet_ref}"/>')
            write_line("</worksheet>")


def main() -> None:
    if not RAW_INPUT.exists():
        raise FileNotFoundError(f"Raw input not found: {RAW_INPUT}")
    if not PLAN_PATH.exists():
        raise FileNotFoundError(f"Cleaning plan not found: {PLAN_PATH}")

    input_hash = sha256_file(RAW_INPUT)
    user_input_hash = sha256_file(USER_INPUT) if USER_INPUT.exists() else None
    user_input_matches = user_input_hash == input_hash if user_input_hash else None

    operations: dict[tuple[str, str], OperationStat] = {}
    raw_missing_counts = Counter()
    cleaned_missing_counts = Counter()
    raw_category_values = {column: set() for column in CANONICAL_SETS}
    cleaned_category_values = {column: set() for column in CANONICAL_SETS}
    raw_district_values: set[str] = set()
    cleaned_district_values: set[str] = set()
    type_conversion_counts = Counter()
    invalid_correction_counts = Counter()
    column_modified_rows: dict[str, set[int]] = defaultdict(set)
    column_modified_cells = Counter()
    changed_rows: set[int] = set()
    raw_duplicate_hashes: set[str] = set()
    cleaned_duplicate_hashes: set[str] = set()
    raw_duplicate_rows = 0
    cleaned_duplicate_rows = 0
    seen_event_ids: set[str] = set()
    duplicate_event_ids: set[str] = set()
    seen_response_ids: set[str] = set()
    duplicate_response_ids: set[str] = set()
    negative_aid_count = 0
    nulls_added_by_invalid_correction = 0

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with RAW_INPUT.open("r", encoding="utf-8-sig", newline="") as raw_handle, OUTPUT_CSV.open(
        "w", encoding="utf-8", newline=""
    ) as cleaned_handle:
        reader = csv.DictReader(raw_handle)
        if reader.fieldnames != HEADERS:
            raise ValueError("Unexpected CSV header order; the frozen v1 script expects the profiled snapshot schema.")

        writer = csv.DictWriter(cleaned_handle, fieldnames=HEADERS)
        writer.writeheader()

        row_count = 0
        for csv_row_number, raw_row in enumerate(reader, start=2):
            row_count += 1
            raw_row_values = [raw_row[header] for header in HEADERS]
            raw_row_hash = digest_row(raw_row_values)
            if raw_row_hash in raw_duplicate_hashes:
                raw_duplicate_rows += 1
            else:
                raw_duplicate_hashes.add(raw_row_hash)

            cleaned_row: dict[str, str] = {}
            for header in HEADERS:
                raw_value = raw_row[header]
                raw_text = raw_value if raw_value is not None else ""
                raw_trimmed = raw_text.strip()
                is_missing_before = raw_trimmed == ""
                if is_missing_before:
                    raw_missing_counts[header] += 1
                    get_operation(operations, "blank_to_null", header).add(
                        csv_row_number,
                        format_report_value(raw_text),
                        "NULL",
                    )
                    cleaned_value: str | None = None
                else:
                    cleaned_value = raw_trimmed

                    if header in TRIM_ONLY_COLUMNS and cleaned_value != raw_text:
                        get_operation(operations, "text_trim", header).add(
                            csv_row_number,
                            format_report_value(raw_text),
                            format_report_value(cleaned_value),
                        )

                    if header in CANONICAL_MAPS:
                        canonical_map = CANONICAL_MAPS[header]
                        normalized_key = normalize_category_key(cleaned_value)
                        if normalized_key not in canonical_map:
                            raise ValueError(
                                f"Unexpected category value in column '{header}' at CSV row {csv_row_number}: {raw_text!r}"
                            )
                        canonical_value = canonical_map[normalized_key]
                        if canonical_value != raw_text:
                            get_operation(operations, "category_harmonization", header).add(
                                csv_row_number,
                                format_report_value(raw_text),
                                format_report_value(canonical_value),
                            )
                        cleaned_value = canonical_value

                    if header == "Date":
                        try:
                            date.fromisoformat(cleaned_value)
                        except ValueError as exc:
                            raise ValueError(
                                f"Malformed date token at CSV row {csv_row_number}: {cleaned_value!r}"
                            ) from exc
                        type_conversion_counts[header] += 1
                        get_operation(operations, "type_conversion_date", header).add(
                            csv_row_number,
                            format_report_value(raw_text),
                            f"{cleaned_value} (DATE)",
                        )

                    elif header in DECIMAL_COLUMNS:
                        parsed_decimal = parse_decimal(cleaned_value, header, csv_row_number)
                        type_conversion_counts[header] += 1
                        get_operation(operations, "type_conversion_decimal", header).add(
                            csv_row_number,
                            format_report_value(raw_text),
                            f"{cleaned_value} (DECIMAL)",
                        )
                        if header == "Aid_Amount_INR" and parsed_decimal < 0:
                            negative_aid_count += 1
                            invalid_correction_counts[header] += 1
                            nulls_added_by_invalid_correction += 1
                            get_operation(operations, "negative_aid_to_null", header).add(
                                csv_row_number,
                                format_report_value(raw_text),
                                "NULL",
                            )
                            cleaned_value = None

                    elif header in INTEGER_COLUMNS:
                        int_string = parse_integral_string(cleaned_value, header, csv_row_number)
                        type_conversion_counts[header] += 1
                        get_operation(operations, "type_conversion_integer", header).add(
                            csv_row_number,
                            format_report_value(raw_text),
                            f"{int_string} (INT)",
                        )
                        cleaned_value = int_string

                if cleaned_value is None:
                    cleaned_missing_counts[header] += 1
                    cleaned_output = ""
                else:
                    cleaned_output = cleaned_value

                if header in CANONICAL_SETS and raw_trimmed != "":
                    raw_category_values[header].add(raw_text)
                if header in CANONICAL_SETS and cleaned_output != "":
                    cleaned_category_values[header].add(cleaned_output)
                if header == "District" and raw_trimmed != "":
                    raw_district_values.add(raw_text)
                if header == "District" and cleaned_output != "":
                    cleaned_district_values.add(cleaned_output)

                cell_changed = False
                if cleaned_value is None:
                    cell_changed = is_missing_before or (header == "Aid_Amount_INR" and raw_trimmed != "")
                elif cleaned_output != raw_text:
                    cell_changed = True
                elif header in TYPED_COLUMNS:
                    cell_changed = True

                if cell_changed:
                    changed_rows.add(csv_row_number)
                    column_modified_rows[header].add(csv_row_number)
                    column_modified_cells[header] += 1

                cleaned_row[header] = cleaned_output

            event_id = cleaned_row["Event_ID"]
            response_id = cleaned_row["Response_ID"]
            if event_id == "" or response_id == "":
                raise ValueError("Event_ID and Response_ID must remain non-null in the cleaned output.")
            if event_id in seen_event_ids:
                duplicate_event_ids.add(event_id)
            else:
                seen_event_ids.add(event_id)
            if response_id in seen_response_ids:
                duplicate_response_ids.add(response_id)
            else:
                seen_response_ids.add(response_id)

            cleaned_row_hash = digest_row([cleaned_row[header] for header in HEADERS])
            if cleaned_row_hash in cleaned_duplicate_hashes:
                cleaned_duplicate_rows += 1
            else:
                cleaned_duplicate_hashes.add(cleaned_row_hash)

            writer.writerow(cleaned_row)

    if row_count != EXPECTED_ROW_COUNT:
        raise ValueError(f"Unexpected row count {row_count}; expected {EXPECTED_ROW_COUNT} for the frozen v1 snapshot.")
    if len(HEADERS) != EXPECTED_COLUMN_COUNT:
        raise ValueError(
            f"Unexpected column count {len(HEADERS)}; expected {EXPECTED_COLUMN_COUNT} for the frozen v1 snapshot."
        )
    if raw_duplicate_rows != 0:
        raise ValueError(f"Expected 0 exact raw duplicate rows but found {raw_duplicate_rows}.")
    if duplicate_event_ids:
        raise ValueError(f"Expected unique Event_ID values but found duplicates: {sorted(duplicate_event_ids)[:5]}")
    if duplicate_response_ids:
        raise ValueError(
            f"Expected unique Response_ID values but found duplicates: {sorted(duplicate_response_ids)[:5]}"
        )
    if negative_aid_count != EXPECTED_NEGATIVE_AID_COUNT:
        raise ValueError(
            f"Unexpected negative Aid_Amount_INR count {negative_aid_count}; expected {EXPECTED_NEGATIVE_AID_COUNT}."
        )
    for header, expected_missing in EXPECTED_MISSING_COUNTS.items():
        actual_missing = raw_missing_counts[header]
        if actual_missing != expected_missing:
            raise ValueError(
                f"Unexpected missing count for {header}: found {actual_missing}, expected {expected_missing}."
            )

    for column in TRIM_ONLY_COLUMNS:
        operations.setdefault(("text_trim", column), build_operation_stat("text_trim", column))
    for column in CANONICAL_SETS:
        operations.setdefault(
            ("category_harmonization", column), build_operation_stat("category_harmonization", column)
        )

    write_xlsx_from_csv(OUTPUT_CSV, OUTPUT_XLSX, HEADERS)

    total_cells = EXPECTED_ROW_COUNT * EXPECTED_COLUMN_COUNT
    total_columns_affected = len(column_modified_rows)
    total_rows_affected = len(changed_rows)
    total_cells_modified = sum(column_modified_cells.values())
    total_missing_before = sum(raw_missing_counts.values())
    total_missing_after = sum(cleaned_missing_counts.values())
    total_missing_handled = total_missing_before + nulls_added_by_invalid_correction
    total_invalid_values_corrected = sum(invalid_correction_counts.values())
    percentage_affected = (total_cells_modified / total_cells) * 100
    rows_dropped = 0
    rows_retained = EXPECTED_ROW_COUNT
    columns_modified_list = [header for header in HEADERS if header in column_modified_rows]

    category_columns = [
        "State",
        "District",
        "Season",
        "Soil_Type",
        "Land_Use",
        "Landslide_Occurred",
        "Landslide_Risk",
        "Compensation_Provided",
        "Water_Supply_Disrupted",
        "Communication_Disruption",
    ]
    category_modified_counts = {
        column: operations.get(("category_harmonization", column), build_operation_stat("category_harmonization", column)).affected_cells
        for column in CANONICAL_SETS
    }
    category_modified_counts["District"] = operations.get(
        ("text_trim", "District"), build_operation_stat("text_trim", "District")
    ).affected_cells

    report_lines: list[str] = []
    report_lines.append("# Data Cleaning Report")
    report_lines.append("")
    report_lines.append("## Report Metadata")
    report_lines.append("")
    report_lines.append(f"- Cleaning plan: `{PLAN_PATH}`")
    report_lines.append(f"- Raw source used for cleaning: `{RAW_INPUT}`")
    if USER_INPUT.exists():
        report_lines.append(f"- User-provided dataset reference: `{USER_INPUT}`")
        report_lines.append(f"- Raw source SHA-256: `{input_hash}`")
        report_lines.append(f"- User dataset SHA-256: `{user_input_hash}`")
        report_lines.append(f"- User dataset matches workspace snapshot: `{user_input_matches}`")
    else:
        report_lines.append(f"- Raw source SHA-256: `{input_hash}`")
    report_lines.append(f"- Cleaned CSV sidecar: `{OUTPUT_CSV}`")
    report_lines.append(f"- Cleaned Excel output: `{OUTPUT_XLSX}`")
    report_lines.append(f"- Generated report: `{OUTPUT_REPORT}`")
    report_lines.append(f"- Generated on: `{datetime.now().isoformat(timespec='seconds')}`")
    report_lines.append("")
    report_lines.append("The cleaning run follows the frozen v1 plan exactly: rows were preserved, blanks were normalized to NULL, numeric and date columns were typed, category labels were enforced against the approved canonical sets, and the only invalid-value correction was `Aid_Amount_INR < 0 -> NULL`.")
    report_lines.append("")

    report_lines.append("## A. Dataset Summary")
    report_lines.append("")
    report_lines.append("| Metric | Value |")
    report_lines.append("| --- | ---: |")
    report_lines.append(f"| Original number of rows | {EXPECTED_ROW_COUNT} |")
    report_lines.append(f"| Original number of columns | {EXPECTED_COLUMN_COUNT} |")
    report_lines.append(f"| Final number of rows | {EXPECTED_ROW_COUNT} |")
    report_lines.append(f"| Final number of columns | {EXPECTED_COLUMN_COUNT} |")
    report_lines.append("")

    report_lines.append("## B. Cleaning Activities Performed")
    report_lines.append("")
    report_lines.append("| Column Name | Cleaning Issue | Cleaning Rule Applied | Reason for Cleaning | Cleaning Method Used | Metric/Logic Used for Cleaning | Number of affected rows | Number of affected cells | Example values before cleaning | Example values after cleaning |")
    report_lines.append("| --- | --- | --- | --- | --- | --- | ---: | ---: | --- | --- |")
    operation_sort_order = {
        "blank_to_null": 1,
        "text_trim": 2,
        "category_harmonization": 3,
        "type_conversion_date": 4,
        "type_conversion_decimal": 4,
        "type_conversion_integer": 4,
        "negative_aid_to_null": 5,
    }
    sorted_operations = sorted(
        operations.values(),
        key=lambda item: (HEADERS.index(item.column_name), operation_sort_order[item.op_id], item.op_id),
    )
    for operation in sorted_operations:
        before_examples = "<br>".join(format_report_value(value) for value in operation.before_examples) or "n/a"
        after_examples = "<br>".join(format_report_value(value) for value in operation.after_examples) or "n/a"
        report_lines.append(
            f"| {operation.column_name} | {operation.cleaning_issue} | {operation.cleaning_rule_applied} | {operation.reason_for_cleaning} | {operation.cleaning_method_used} | {operation.metric_logic_used} | {len(operation.affected_rows)} | {operation.affected_cells} | {before_examples} | {after_examples} |"
        )
    report_lines.append("")

    report_lines.append("## C. Missing Value Summary")
    report_lines.append("")
    report_lines.append("| Column | Missing values before cleaning | Missing values after cleaning | Action taken | Imputation technique used |")
    report_lines.append("| --- | ---: | ---: | --- | --- |")
    for header in HEADERS:
        action_taken = "Kept as NULL"
        if header == "Aid_Amount_INR" and nulls_added_by_invalid_correction:
            action_taken = "Kept as NULL; plus 51 invalid negatives converted to NULL"
        report_lines.append(
            f"| {header} | {raw_missing_counts[header]} | {cleaned_missing_counts[header]} | {action_taken} | None in v1 |"
        )
    report_lines.append("")

    report_lines.append("## D. Duplicate Summary")
    report_lines.append("")
    report_lines.append(f"- Duplicate rows detected in raw snapshot: {raw_duplicate_rows}")
    report_lines.append("- Duplicate rows removed: 0")
    report_lines.append(f"- Duplicate rows detected after cleaning normalization: {cleaned_duplicate_rows}")
    report_lines.append(f"- Duplicate Event_ID values: {len(duplicate_event_ids)}")
    report_lines.append(f"- Duplicate Response_ID values: {len(duplicate_response_ids)}")
    report_lines.append("- Actions taken: no rows were dropped in v1; duplicate checks were executed and all current counts passed the frozen-plan acceptance criteria.")
    report_lines.append("")

    report_lines.append("## E. Data Type Conversion Summary")
    report_lines.append("")
    report_lines.append("| Column | Original data type | New data type | Reason for conversion | Number of values converted |")
    report_lines.append("| --- | --- | --- | --- | ---: |")
    for header in HEADERS:
        if header in DATE_COLUMNS:
            new_type = "DATE"
        elif header in DECIMAL_COLUMNS:
            new_type = "DECIMAL"
        elif header in INTEGER_COLUMNS:
            new_type = "INT"
        else:
            continue
        report_lines.append(
            f"| {header} | CSV string token | {new_type} | Target type is explicitly defined in the frozen v1 plan. | {type_conversion_counts[header]} |"
        )
    report_lines.append("")

    report_lines.append("## F. Category Harmonisation Summary")
    report_lines.append("")
    for column in category_columns:
        report_lines.append(f"### {column}")
        if column == "District":
            original_values = sorted(raw_district_values)
            canonical_values = sorted(cleaned_district_values)
            rule_text = "Trim only in v1; do not merge district spellings without a geography reference file."
        else:
            original_values = sorted(raw_category_values[column])
            canonical_values = CANONICAL_SETS[column]
            rule_text = "Trim and case-normalize against the frozen canonical label set."
        report_lines.append(f"- Original categories: {quote_values(original_values)}")
        report_lines.append(f"- Canonical categories: {quote_values(canonical_values)}")
        report_lines.append(f"- Number of category values modified: {category_modified_counts[column]}")
        report_lines.append(f"- Harmonisation rules applied: {rule_text}")
        report_lines.append("")

    report_lines.append("## G. Invalid Value Corrections")
    report_lines.append("")
    report_lines.append("| Column name | Invalid value detected | Validation rule used | Correction applied | Number of affected rows |")
    report_lines.append("| --- | --- | --- | --- | ---: |")
    report_lines.append(
        f"| Aid_Amount_INR | Negative aid payment value | Negative Aid_Amount_INR is invalid in v1; NDVI and Temperature_C negatives remain valid by plan. | Set negative values to NULL pending source verification | {invalid_correction_counts['Aid_Amount_INR']} |"
    )
    report_lines.append("")

    report_lines.append("## H. Dataset Validation")
    report_lines.append("")
    validation_status = "Pass"
    report_lines.append(f"- Final row count: {EXPECTED_ROW_COUNT}")
    report_lines.append(f"- Final column count: {EXPECTED_COLUMN_COUNT}")
    report_lines.append(f"- Rows retained: {rows_retained}")
    report_lines.append(f"- Rows dropped: {rows_dropped}")
    report_lines.append(f"- Columns modified: {total_columns_affected} ({', '.join(columns_modified_list)})")
    report_lines.append(f"- Total cells modified: {total_cells_modified}")
    report_lines.append(f"- Exact duplicate rows after cleaning: {cleaned_duplicate_rows}")
    report_lines.append(f"- Duplicate Event_ID values after cleaning: {len(duplicate_event_ids)}")
    report_lines.append(f"- Duplicate Response_ID values after cleaning: {len(duplicate_response_ids)}")
    report_lines.append("- Data types: all DATE, DECIMAL, and INT target columns validated successfully with zero malformed-token failures.")
    report_lines.append("- Category consistency: all audited category fields resolved to the approved canonical sets; District remained trim-only as required.")
    report_lines.append("- Missing values: nulls were preserved in the base cleaned table; no statistical imputation was performed.")
    report_lines.append(f"- Validation status: {validation_status}")
    report_lines.append("")

    report_lines.append("## I. Cleaning Metrics")
    report_lines.append("")
    report_lines.append(f"- Total cleaning operations performed: {len(sorted_operations)}")
    report_lines.append(f"- Total columns affected: {total_columns_affected}")
    report_lines.append(f"- Total rows affected: {total_rows_affected}")
    report_lines.append(f"- Total cells modified: {total_cells_modified}")
    report_lines.append(f"- Total duplicate rows removed: 0")
    report_lines.append(f"- Total invalid values corrected: {total_invalid_values_corrected}")
    report_lines.append(f"- Total missing values handled: {total_missing_handled}")
    report_lines.append(
        f"- Percentage of dataset affected by cleaning: {percentage_affected:.2f}% of {total_cells:,} cells"
    )
    report_lines.append("")

    report_lines.append("## J. Change Log")
    report_lines.append("")
    report_lines.append("| Step number | Operation performed | Columns affected | Number of rows affected | Reason for the transformation |")
    report_lines.append("| ---: | --- | --- | ---: | --- |")
    blank_rows_affected = len(
        set().union(
            *[
                operations[("blank_to_null", header)].affected_rows
                for header in HEADERS
                if ("blank_to_null", header) in operations
            ]
        )
    )
    trim_rows_affected = len(
        set().union(
            *[
                operations[key].affected_rows
                for key in operations
                if key[0] in {"text_trim", "category_harmonization"}
            ]
        )
    )
    date_rows_affected = len(operations[("type_conversion_date", "Date")].affected_rows)
    decimal_rows_affected = len(
        set().union(
            *[
                operations[("type_conversion_decimal", header)].affected_rows
                for header in DECIMAL_COLUMNS
                if ("type_conversion_decimal", header) in operations
            ]
        )
    )
    integer_rows_affected = len(
        set().union(
            *[
                operations[("type_conversion_integer", header)].affected_rows
                for header in INTEGER_COLUMNS
                if ("type_conversion_integer", header) in operations
            ]
        )
    )
    invalid_rows_affected = len(operations[("negative_aid_to_null", "Aid_Amount_INR")].affected_rows)
    report_lines.append(
        "| 1 | Verified the frozen snapshot profile and schema before transformation | All columns | 48108 | Confirm the input matches the authoritative cleaning plan v1 snapshot. |"
    )
    report_lines.append(
        f"| 2 | Normalized blank strings to NULL | {', '.join([header for header in HEADERS if ('blank_to_null', header) in operations])} | {blank_rows_affected} | The plan requires NULL preservation without row drops or fill-ins. |"
    )
    report_lines.append(
        f"| 3 | Applied trim and canonical text harmonisation | {', '.join(sorted(TRIM_ONLY_COLUMNS | set(CANONICAL_SETS)))} | {trim_rows_affected} | The plan permits formatting-only normalization and canonical category enforcement. |"
    )
    report_lines.append(
        f"| 4 | Cast Date to DATE | Date | {date_rows_affected} | Date is the only target DATE field in v1. |"
    )
    report_lines.append(
        f"| 5 | Cast decimal measures to DECIMAL | {', '.join(sorted(DECIMAL_COLUMNS))} | {decimal_rows_affected} | The plan defines these continuous measures as DECIMAL. |"
    )
    report_lines.append(
        f"| 6 | Cast count-style measures to INT | {', '.join(sorted(INTEGER_COLUMNS))} | {integer_rows_affected} | The plan defines these columns as integer counts, even when the CSV stores tokens like 4.0. |"
    )
    report_lines.append(
        f"| 7 | Converted invalid negative Aid_Amount_INR values to NULL | Aid_Amount_INR | {invalid_rows_affected} | Negative aid payments are the only explicit invalid-value exception allowed in v1. |"
    )
    report_lines.append(
        "| 8 | Revalidated row counts, key uniqueness, duplicate rows, target types, category sets, and null preservation | All columns | 48108 | Ensure the cleaned layer passes every acceptance criterion from the frozen plan. |"
    )
    report_lines.append("")

    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_REPORT.write_text("\n".join(report_lines), encoding="utf-8")

    print(f"Cleaned CSV: {OUTPUT_CSV}")
    print(f"Cleaned XLSX: {OUTPUT_XLSX}")
    print(f"Cleaning report: {OUTPUT_REPORT}")
    print(f"Rows: {EXPECTED_ROW_COUNT}")
    print(f"Columns: {EXPECTED_COLUMN_COUNT}")
    print(f"Total cells modified: {total_cells_modified}")
    print(f"Negative Aid_Amount_INR values nulled: {invalid_correction_counts['Aid_Amount_INR']}")
    print(f"Validation status: {validation_status}")


if __name__ == "__main__":
    main()
