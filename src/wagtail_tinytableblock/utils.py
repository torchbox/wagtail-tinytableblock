from html import unescape
from typing import TYPE_CHECKING, Literal

import nh3

from bs4 import BeautifulSoup


if TYPE_CHECKING:
    from bs4.element import Tag

Cell = Literal["td", "th"]


def sanitise_html(content: str, *, allow_links: bool = False) -> str:
    tags: set[str] = {"table", "tr", "th", "td", "thead", "tbody", "caption"}
    attributes: dict[str, set[str]] = {
        "*": {"class"},
        "th": {"colspan", "rowspan", "align", "scope"},
        "td": {"colspan", "rowspan", "align", "scope"},
    }
    if allow_links:
        tags |= {"a"}
        attributes["a"] = {"href", "rel", "title"}

    return nh3.clean(  # pylint: disable=no-member
        unescape(content),
        tags=tags,
        attributes=attributes,
        link_rel=None,
    )


def get_cell_data(cell: "Tag", forced_type: Cell | None = None) -> dict[str, str | int]:
    value = "".join(str(child) for child in cell.children)
    cell_data = {"value": value, "type": forced_type or cell.name}

    if (rowspan := int(cell.get("rowspan", 1))) > 1:
        cell_data["rowspan"] = rowspan
    if (colspan := int(cell.get("colspan", 1))) > 1:
        cell_data["colspan"] = colspan
    if scope := cell.get("scope"):
        cell_data["scope"] = scope
    if align := cell.get("align"):
        cell_data["align"] = align

    return cell_data


def check_all_cells_are_empty(rows: list[list[dict[str, str | int]]]) -> bool:
    for row in rows:
        for cell in row:
            if cell["value"]:
                return False
    return True


def html_table_to_dict(content: str, *, allow_links: bool = False) -> dict:
    """Take an HTML table and convert it to a dictionary.

    The dictionary has the following structure:
    - headers - a list of header row lists, each containing the cell info
    - rows - a list of row lists, each containing the cell info
    - html - the original html
    """
    content = sanitise_html(content, allow_links=allow_links)
    soup = BeautifulSoup(content, "html.parser")

    table = soup.find("table")
    if not table:
        return {
            "headers": [],
            "rows": [],
            "html": "",
        }

    # Extract headers
    headers = []
    if thead := table.find("thead"):
        for header_row in thead.find_all("tr"):
            # find all cells in thead and store them as th
            headers.append(
                [
                    get_cell_data(cell, forced_type="th")
                    for cell in header_row.find_all(["th", "td"])
                ]
            )

        if tbody_rows := table.find("tbody"):
            table_rows = tbody_rows.find_all("tr")
        else:
            # If there's a thead but no tbody, get all rows not in thead
            table_rows = [row for row in table.find_all("tr") if row.parent != thead]
    else:
        table_rows = table.find_all("tr")
        # TODO: extract headers from tr if all cells are th?

    # Extract row data and convert to list of dictionaries
    rows = []
    for row in table_rows:
        rows.append([get_cell_data(cell) for cell in row.find_all(["td", "th"])])

    # given we start with an empty 2x2 table, if that is submitted, then we have something like
    # [[{'type': 'td', 'value': ''}, {'type': 'td', 'value': ''}]], but we want []
    if check_all_cells_are_empty(headers):
        headers = []

    if check_all_cells_are_empty(rows):
        rows = []

    data = {
        "headers": headers,
        "rows": rows,
        "html": content,
    }

    return data
