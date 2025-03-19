# A table block for Wagtail StreamField powered by TinyMCE

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD--3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PyPI version](https://img.shields.io/pypi/v/wagtail-tinytableblock.svg?style=flat)](https://pypi.org/project/wagtail-tinytableblock)
[![Build status](https://img.shields.io/github/actions/workflow/status/torchbox/wagtail-tinytableblock/test.yml?branch=main)](https://github.com/torchbox/wagtail-tinytableblock/actions)

## Links

- [Documentation](https://github.com/torchbox/wagtail-tinytableblock/blob/main/README.md)
- [Changelog](https://github.com/torchbox/wagtail-tinytableblock/blob/main/CHANGELOG.md)
- [Contributing](https://github.com/torchbox/wagtail-tinytableblock/blob/main/CONTRIBUTING.md)
- [Discussions](https://github.com/torchbox/wagtail-tinytableblock/discussions)
- [Security](https://github.com/torchbox/wagtail-tinytableblock/security)

TinyTableBlock is a StreamField block powered by [TinyMCE](https://www.tiny.cloud/) and its [table plugin](https://www.tiny.cloud/docs/tinymce/latest/table/).

Wagtail provides [`TableBlock`](https://docs.wagtail.org/en/stable/reference/contrib/table_block.html) and
[`TypedTableBlock`](https://docs.wagtail.org/en/stable/reference/contrib/typed_table_block.html)
which are good options if you want basic tables with some cell merging capability or StreamField-powered cell, but they have their limitations:
- `TableBlock` is using an old version of [handsontable](https://github.com/handsontable/handsontable/tree/6.2.2). It doesn't support multi-row header, column headers, nor pasting complex tables.
- `TypedTableBlock` gets complex quickly depending on the types of blocks you add, and pasting is limited to single cells.
-
Wagtail TinyTableBlock (this package) provides the TinyMCE table editor which has improved copy/paste, multi-row and column headers, external link support and more.
It does not currently support the Wagtail rich text [data format](https://docs.wagtail.org/en/stable/extending/rich_text_internals.html#data-format) for page and document links,
nor does it support embedding images.

## Installation

In your project's Django settings, add the app your `INSTALLED_APPS` list (at the end is fine):

```python
INSTALLED_APPS = [
  # ...
  "wagtail_tinytableblock",
]
```

Add the `TinyTableBlock` model to your StreamField definition. For example

```python
# yourapp/models.py
from wagtail.fields import StreamField
from wagtail.models import Page

from wagtail_tinytableblock import TinyTableBlock


class WonderfulPage(Page):
    body = StreamField([
        # ...
        ("table", TinyTableBlock()),
    ])
```

Finally, run Django's `makemigrations` and `migrate` commands to apply any model field changes to your project

```sh
$ python manage.py makemigrations
$ python manage.py migrate
```

## Configuration

`TinyTableBlock` accepts an `allow_links` keyword argument which allows enabling the TinyMCE link
plugin. Note: this currently only works with external URLs.

```python
from wagtail.blocks import StreamBlock
from wagtail_tinytableblock.blocks import TinyTableBlock

class ContentBlocks(StreamBlock):
    table_block = TinyTableBlock(allow_links=True)
```

By default, we disable the TinyMCE contextual menu to allow the browser native one. If you want to use TinyMCE one,
pass `enable_context_menu=True`:

```python
from wagtail.blocks import StreamBlock
from wagtail_tinytableblock.blocks import TinyTableBlock

class ContentBlocks(StreamBlock):
    table_block = TinyTableBlock(enable_context_menu=True)
```


## Data representation

The table data is saved as a JSON-serialized dictionary with the following keys:

```python
{
   "headers": [],
   "rows": [],
   "html": the_sanitised_html
}
```

`headers` / `rows` are lists of lists with cell values. Each cell is a dictionary with the following keys

 key | value notes
-----|---------
`value` | The cell value
`type` | "td" or "th"
`rowspan` | if set
`colspan` | if set
`scope` | if set
`align` | if set

## Contributing

All contributions are welcome! See [CONTRIBUTING.md](https://github.com/torchbox/wagtail-tinytableblock/blob/main/CONTRIBUTING.md)

Supported versions:

- Python 3.12, 3.13
- Django 4.2, 5.1
- Wagtail 6.3 (LTS), 6.4
