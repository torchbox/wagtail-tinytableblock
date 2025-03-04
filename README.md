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

## Contributing

All contributions are welcome! See [CONTRIBUTING.md](https://github.com/torchbox/wagtail-tinytableblock/blob/main/CONTRIBUTING.md)

Supported versions:

- Python 3.12, 3.13
- Django 4.2, 5.1
- Wagtail 6.3 (LTS), 6.4
