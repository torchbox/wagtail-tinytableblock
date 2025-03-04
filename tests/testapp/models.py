from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from wagtail_tinytableblock.blocks import TinyTableBlock


class TablePage(Page):
    body = StreamField([("table", TinyTableBlock())])

    content_panels = Page.content_panels + [FieldPanel("body")]
