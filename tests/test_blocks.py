from django.test import TestCase

from wagtail_tinytableblock.blocks import TinyTableBlock


class BlockTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.simple_table_data = {
            "headers": [[{"value": "header cell", "type": "th"}]],
            "rows": [[{"value": "row cell", "type": "td"}]],
        }
        cls.full_data = {
            "title": "The table",
            "caption": "The caption",
            "data": cls.simple_table_data,
        }
        cls.data_with_empty_table = {
            "title": "The table",
            "caption": "The caption",
            "data": {
                "headers": [],
                "rows": [],
            },
        }

        cls.block = TinyTableBlock()

    def test_render_block__full(self):
        rendered = self.block.render(self.full_data)
        self.assertIn(f"<h2>{self.full_data['title']}</h2>", rendered)
        self.assertIn(f"<caption>{self.full_data['caption']}</caption>", rendered)
        self.assertIn("<table>", rendered)
        self.assertIn("header cell", rendered)
        self.assertIn("row cell", rendered)

    def test_render_block__no_table(self):
        rendered = self.block.render(self.data_with_empty_table)
        self.assertNotIn(self.full_data["title"], rendered)
        self.assertNotIn(self.full_data["caption"], rendered)
        self.assertNotIn("<table>", rendered)
        self.assertNotIn("header cell", rendered)
        self.assertNotIn("row cell", rendered)

    def test_render_block__optional_elements(self):
        rendered = self.block.render(
            {"data": self.simple_table_data, "title": "The title"}
        )
        self.assertIn("<h2>The title</h2>", rendered)
        self.assertNotIn("<caption>", rendered)

        rendered = self.block.render(
            {"data": self.simple_table_data, "caption": "Caption this!"}
        )
        self.assertIn("<caption>Caption this!</caption>", rendered)
        self.assertNotIn("<h2>", rendered)
