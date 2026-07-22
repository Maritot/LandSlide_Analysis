from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parent.parent
MARKDOWN_PATH = ROOT / "docs" / "cleaning-plan-v1.md"
DOCX_PATH = ROOT / "docs" / "cleaning-plan-v1.docx"

LANDSCAPE_PAGE_WIDTH = 15840
LANDSCAPE_PAGE_HEIGHT = 12240
LEFT_RIGHT_MARGIN = 1440
CONTENT_WIDTH = LANDSCAPE_PAGE_WIDTH - (LEFT_RIGHT_MARGIN * 2)


def esc(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def render_runs(text: str, *, size: int = 22, bold: bool = False) -> str:
    parts = re.split(r"(`[^`]+`)", text)
    runs: list[str] = []
    for part in parts:
        if not part:
            continue

        if part.startswith("`") and part.endswith("`"):
            code = part[1:-1]
            runs.append(
                "<w:r>"
                "<w:rPr>"
                '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>'
                '<w:sz w:val="20"/>'
                '<w:szCs w:val="20"/>'
                '<w:color w:val="1F1F1F"/>'
                "</w:rPr>"
                f'<w:t xml:space="preserve">{esc(code)}</w:t>'
                "</w:r>"
            )
            continue

        run_props: list[str] = [f'<w:sz w:val="{size}"/>', f'<w:szCs w:val="{size}"/>']
        if bold:
            run_props.append("<w:b/>")
        runs.append(
            "<w:r>"
            f"<w:rPr>{''.join(run_props)}</w:rPr>"
            f'<w:t xml:space="preserve">{esc(part)}</w:t>'
            "</w:r>"
        )

    return "".join(runs) or "<w:r><w:t></w:t></w:r>"


def paragraph(text: str, kind: str = "normal") -> str:
    size = 22
    bold = False
    ppr: list[str] = []

    if kind == "title":
        size = 32
        bold = True
        ppr.append('<w:spacing w:before="120" w:after="220"/>')
    elif kind == "heading2":
        size = 26
        bold = True
        ppr.append('<w:spacing w:before="180" w:after="120"/>')
    elif kind == "heading3":
        size = 24
        bold = True
        ppr.append('<w:spacing w:before="160" w:after="100"/>')
    elif kind == "bullet":
        ppr.append('<w:spacing w:after="80"/>')
        ppr.append('<w:ind w:left="720" w:hanging="360"/>')
        text = f"- {text}"
    else:
        ppr.append('<w:spacing w:after="120"/>')

    ppr_xml = f"<w:pPr>{''.join(ppr)}</w:pPr>" if ppr else ""
    return f"<w:p>{ppr_xml}{render_runs(text, size=size, bold=bold)}</w:p>"


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator_row(line: str) -> bool:
    cells = split_row(line)
    if not cells:
        return False
    return all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells)


def table_widths(headers: list[str]) -> list[int]:
    normalized = [header.casefold() for header in headers]

    if normalized == ["column", "nulls", "missing %", "rule id", "v1 action / impute stance"]:
        return [2100, 900, 1100, 1000, 7860]

    if normalized == ["rule id", "affected columns", "keep / drop / impute decision"]:
        return [1100, 3600, 8260]

    if normalized == ["column group", "recommended strategy", "notes"]:
        return [2600, 3600, 6760]

    if normalized == ["check", "current finding", "v1 action"]:
        return [2200, 1800, 8960]

    if normalized == ["column", "current quality status", "v1 action"]:
        return [2200, 3500, 7260]

    col_count = max(1, len(headers))
    even = int(CONTENT_WIDTH / col_count)
    return [even] * col_count


def table_cell(text: str, *, width: int, header: bool = False) -> str:
    shading = '<w:shd w:fill="F2F2F2"/>' if header else ""
    return (
        "<w:tc>"
        f'<w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{shading}</w:tcPr>'
        "<w:p>"
        '<w:pPr><w:spacing w:after="0"/></w:pPr>'
        f"{render_runs(text, size=20, bold=header)}"
        "</w:p>"
        "</w:tc>"
    )


def render_table(rows: list[list[str]]) -> str:
    widths = table_widths(rows[0])
    col_count = len(widths)
    grid = "".join(f'<w:gridCol w:w="{width}"/>' for width in widths)
    rendered_rows: list[str] = []

    for index, row in enumerate(rows):
        padded = row + [""] * (col_count - len(row))
        cells = "".join(
            table_cell(cell, width=widths[cell_index], header=(index == 0))
            for cell_index, cell in enumerate(padded[:col_count])
        )
        rendered_rows.append(f"<w:tr>{cells}</w:tr>")

    return (
        "<w:tbl>"
        "<w:tblPr>"
        '<w:tblW w:w="0" w:type="auto"/>'
        "<w:tblBorders>"
        '<w:top w:val="single" w:sz="8" w:space="0" w:color="808080"/>'
        '<w:left w:val="single" w:sz="8" w:space="0" w:color="808080"/>'
        '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="808080"/>'
        '<w:right w:val="single" w:sz="8" w:space="0" w:color="808080"/>'
        '<w:insideH w:val="single" w:sz="6" w:space="0" w:color="BFBFBF"/>'
        '<w:insideV w:val="single" w:sz="6" w:space="0" w:color="BFBFBF"/>'
        "</w:tblBorders>"
        "<w:tblCellMar>"
        '<w:top w:w="90" w:type="dxa"/>'
        '<w:left w:w="90" w:type="dxa"/>'
        '<w:bottom w:w="90" w:type="dxa"/>'
        '<w:right w:w="90" w:type="dxa"/>'
        "</w:tblCellMar>"
        "</w:tblPr>"
        f"<w:tblGrid>{grid}</w:tblGrid>"
        f"{''.join(rendered_rows)}"
        "</w:tbl>"
    )


def parse_markdown(markdown: str) -> str:
    lines = markdown.splitlines()
    blocks: list[str] = []
    index = 0

    def is_heading(line: str) -> bool:
        return bool(re.match(r"#{1,6} ", line))

    def is_bullet(line: str) -> bool:
        return line.startswith("- ")

    def is_table(line: str) -> bool:
        stripped = line.strip()
        return stripped.startswith("|") and stripped.endswith("|")

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if not stripped:
            index += 1
            continue

        if is_heading(stripped):
            hashes, heading_text = stripped.split(" ", 1)
            kind = "title" if len(hashes) == 1 else "heading2" if len(hashes) == 2 else "heading3"
            blocks.append(paragraph(heading_text, kind=kind))
            index += 1
            continue

        if is_table(stripped):
            table_lines: list[str] = []
            while index < len(lines) and is_table(lines[index].strip()):
                table_lines.append(lines[index].strip())
                index += 1
            rows = [split_row(row) for row in table_lines if not is_separator_row(row)]
            if rows:
                blocks.append(render_table(rows))
            continue

        if is_bullet(stripped):
            while index < len(lines) and is_bullet(lines[index].strip()):
                blocks.append(paragraph(lines[index].strip()[2:].strip(), kind="bullet"))
                index += 1
            continue

        blocks.append(paragraph(stripped, kind="normal"))
        index += 1

    return "".join(blocks)


def build_document_xml(markdown: str) -> str:
    body_xml = parse_markdown(markdown) + (
        "<w:sectPr>"
        f'<w:pgSz w:w="{LANDSCAPE_PAGE_WIDTH}" w:h="{LANDSCAPE_PAGE_HEIGHT}" w:orient="landscape"/>'
        f'<w:pgMar w:top="1440" w:right="{LEFT_RIGHT_MARGIN}" w:bottom="1440" w:left="{LEFT_RIGHT_MARGIN}" '
        'w:header="720" w:footer="720" w:gutter="0"/>'
        "</w:sectPr>"
    )

    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{body_xml}</w:body>"
        "</w:document>"
    )


def write_docx(document_xml: str) -> None:
    content_types_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
        "</Types>"
    )

    rels_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
        "</Relationships>"
    )

    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    core_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties '
        'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:dcmitype="http://purl.org/dc/dcmitype/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        "<dc:title>Raw Data Cleaning Plan v1</dc:title>"
        "<dc:creator>OpenAI Codex</dc:creator>"
        "<cp:lastModifiedBy>OpenAI Codex</cp:lastModifiedBy>"
        f'<dcterms:created xsi:type="dcterms:W3CDTF">{timestamp}</dcterms:created>'
        f'<dcterms:modified xsi:type="dcterms:W3CDTF">{timestamp}</dcterms:modified>'
        "</cp:coreProperties>"
    )

    app_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        "<Application>OpenAI Codex</Application>"
        "</Properties>"
    )

    with ZipFile(DOCX_PATH, "w", compression=ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", content_types_xml)
        docx.writestr("_rels/.rels", rels_xml)
        docx.writestr("word/document.xml", document_xml)
        docx.writestr("docProps/core.xml", core_xml)
        docx.writestr("docProps/app.xml", app_xml)

    with ZipFile(DOCX_PATH, "r") as verify_zip:
        if verify_zip.testzip() is not None:
            raise RuntimeError("Generated DOCX archive failed validation.")


def main() -> None:
    markdown = MARKDOWN_PATH.read_text(encoding="utf-8")
    document_xml = build_document_xml(markdown)
    write_docx(document_xml)
    print(DOCX_PATH)


if __name__ == "__main__":
    main()
