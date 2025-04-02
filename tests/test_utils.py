from django.test import TestCase

from wagtail_tinytableblock.utils import html_table_to_dict, sanitise_html


class UtilsTestCase(TestCase):
    def test_empty_content_returns_empty_dict(self):
        """Test that empty content returns a dict with empty lists."""
        result = html_table_to_dict("")
        expected = {
            "headers": [],
            "rows": [],
            "html": "",
        }
        self.assertEqual(result, expected)

    def test_content_without_table_returns_empty_dict(self):
        """Test that content without a table returns a dict with empty lists."""
        result = html_table_to_dict("<div>No table here</div>")
        expected = {
            "headers": [],
            "rows": [],
            "html": "",
        }
        self.assertEqual(result, expected)

    def test_simple_table_with_thead(self):
        """Test parsing a simple table with thead and tbody."""
        html = """
        <table>
            <thead>
                <tr>
                    <th>Header 1</th>
                    <td>Header 2</td>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Cell on<br> on two lines</td>
                    <td>Cell 2</td>
                </tr>
            </tbody>
        </table>
        """
        result = html_table_to_dict(html)

        self.assertEqual(len(result["headers"]), 1)
        self.assertListEqual(
            result["headers"][0],
            [
                {
                    "value": "Header 1",
                    "type": "th",
                },
                {
                    "value": "Header 2",
                    "type": "th",
                },
            ],
        )

        self.assertEqual(len(result["rows"]), 1)
        self.assertListEqual(
            result["rows"][0],
            [
                {
                    "value": "Cell on<br/> on two lines",
                    "type": "td",
                },
                {
                    "value": "Cell 2",
                    "type": "td",
                },
            ],
        )

        self.assertEqual(result["html"], html)

    def test_table_with_colspan_and_rowspan(self):
        """Test parsing a table with colspan and rowspan attributes."""
        html = """
        <table>
            <tr>
                <td colspan="2">Spanning 2 columns</td>
            </tr>
            <tr>
                <td rowspan="2">Spanning 2 rows</td>
                <td>Regular cell</td>
            </tr>
            <tr>
                <td>Another cell</td>
                <td>Another cell</td>
            </tr>
        </table>
        """
        result = html_table_to_dict(html)

        # First row - cell with colspan
        self.assertEqual(result["rows"][0][0]["colspan"], 2)
        self.assertEqual(result["rows"][0][0]["value"], "Spanning 2 columns")

        # Second row - cell with rowspan
        self.assertEqual(result["rows"][1][0]["rowspan"], 2)
        self.assertEqual(result["rows"][1][0]["value"], "Spanning 2 rows")

    def test_table_with_alignment_and_scope(self):
        """Test parsing a table with alignment and scope attributes."""
        html = """
        <table>
            <tr>
                <th scope="col" align="left">Header</th>
                <td align="right">Aligned cell</td>
            </tr>
        </table>
        """
        result = html_table_to_dict(html)

        # Header cell with scope
        self.assertEqual(result["rows"][0][0]["type"], "th")
        self.assertEqual(result["rows"][0][0]["scope"], "col")
        self.assertEqual(result["rows"][0][0]["align"], "left")

        # Data cell with alignment
        self.assertEqual(result["rows"][0][1]["align"], "right")

    def test_table_without_thead_tbody(self):
        """Test parsing a table without thead/tbody structure."""
        html = """
        <table>
            <tr>
                <th>Header 1</th>
                <th>Header 2</th>
            </tr>
            <tr>
                <td>Cell 1</td>
                <td>Cell 2</td>
            </tr>
        </table>
        """
        result = html_table_to_dict(html)

        # Should have no headers (as no thead) but two rows
        self.assertEqual(len(result["headers"]), 0)
        self.assertEqual(len(result["rows"]), 2)
        self.assertEqual(result["rows"][0][0]["type"], "th")
        self.assertEqual(result["rows"][1][0]["type"], "td")

    def test_table_with_thead_no_tbody(self):
        """Test parsing a table with thead but no tbody."""
        html = """
        <table>
            <thead>
                <tr>
                    <th>Header 1</th>
                </tr>
            </thead>
            <tr>
                <td>Cell 1</td>
            </tr>
        </table>
        """
        result = html_table_to_dict(html)

        # Should have headers and one row
        self.assertEqual(len(result["headers"]), 1)
        self.assertEqual(len(result["rows"]), 1)
        self.assertEqual(result["headers"][0][0]["value"], "Header 1")
        self.assertEqual(result["rows"][0][0]["value"], "Cell 1")

    def test_table_with_style_attributes(self):
        """Test parsing a simple table with thead and tbody."""
        html = """
        <table>
            <thead>
                <tr>
                    <th style="width: 50px; text-align: left; vertical-align: top; color: red;">Header 1</th>
                    <td align="right" style="width: 10%; text-align: center; display: none;">Header 2</td>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Cell 1</td>
                    <td>Cell 2</td>
                </tr>
            </tbody>
        </table>
        """
        result = html_table_to_dict(html)

        self.assertEqual(len(result["headers"]), 1)
        self.assertListEqual(
            result["headers"][0],
            [
                {
                    "value": "Header 1",
                    "type": "th",
                    "align": "left",
                    "valign": "top",
                    "width": "50px",
                },
                {
                    "value": "Header 2",
                    "type": "th",
                    "align": "center",
                    "width": "10%",
                },
            ],
        )

        self.assertEqual(len(result["rows"]), 1)
        self.assertListEqual(
            result["rows"][0],
            [
                {
                    "value": "Cell 1",
                    "type": "td",
                },
                {
                    "value": "Cell 2",
                    "type": "td",
                },
            ],
        )

        self.assertEqual(result["html"], html)

    def test_multiple_headers_structure(self):
        """Test parsing a table with complex nested structure."""
        html = """
        <table>
            <thead>
                <tr>
                    <th colspan="2">Combined Header</th>
                    <th>Regular Header</th>
                </tr>
                <tr>
                    <th>Sub Header 1</th>
                    <th>Sub Header 2</th>
                    <th>Sub Header 3</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Data 1</td>
                    <td>Data 2</td>
                    <td>Data 3</td>
                </tr>
            </tbody>
        </table>
        """
        result = html_table_to_dict(html)

        # Should have two header rows
        self.assertEqual(len(result["headers"]), 2)

        # First header row has a colspan cell
        self.assertEqual(result["headers"][0][0]["colspan"], 2)
        self.assertEqual(result["headers"][0][0]["value"], "Combined Header")

        # Second header row has three regular cells
        self.assertEqual(len(result["headers"][1]), 3)
        self.assertEqual(result["headers"][1][0]["value"], "Sub Header 1")

    def test_sanitisation__with_links(self):
        html = """
        <h1>H1</h1>
        <table>
            <thead class="foo">
                <tr>
                    <th data-test"foo" valign="middle" colspan="1">Header 1</th>
                    <th class="highlight" align="right">Header 2</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td rowspan="1"><a href="&#106avascript:alert(1)">Cell <strong>1</strong></a></td>
                    <td><a href="#" click='alert(\\'XSS\\')' rel="next">Cell 2</a></td>
                </tr>
            </tbody>
        </table>
        <script>alert("Gotcha!");</script>
        &lt;script&gt;alert('xss');&lt;/script&gt;
        """
        expected = """
        H1
        <table>
            <thead class="foo">
                <tr>
                    <th colspan="1">Header 1</th>
                    <th class="highlight" align="right">Header 2</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td rowspan="1"><a>Cell 1</a></td>
                    <td><a href="#" rel="next">Cell 2</a></td>
                </tr>
            </tbody>
        </table>
        """

        sanitised = sanitise_html(html, allow_links=True)
        self.assertEqual(sanitised.strip(), expected.strip())

    def test_sanitisation__no_links(self):
        html = """
        <table style="width: 100%;">
            <thead class="foo" style="width: 100%;">
                <tr>
                    <th data-test"foo" valign="middle" colspan="1" style="color: red;">Header 1</th>
                    <th class="highlight" align="right">Header 2</th>
                </tr>
            </thead>
            <tbody style="width: 100%;">
                <tr>
                    <td rowspan="1" style="text-align: right;">Cell <strong>1</strong></td>
                    <td><a href="#" click='alert(\\'XSS\\')' rel="next">Cell 2</a></td>
                </tr>
            </tbody>
        </table>
        """
        expected = """
        <table>
            <thead class="foo">
                <tr>
                    <th colspan="1" style="color: red;">Header 1</th>
                    <th class="highlight" align="right">Header 2</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td rowspan="1" style="text-align: right;">Cell 1</td>
                    <td>Cell 2</td>
                </tr>
            </tbody>
        </table>
        """

        sanitised = sanitise_html(html)
        self.assertEqual(sanitised.strip(), expected.strip())
