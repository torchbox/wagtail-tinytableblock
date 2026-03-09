import json

from typing import Any

from django import forms
from django.forms import Media
from django.utils.functional import cached_property
from collections.abc import Iterable
from wagtail.blocks import Block, FieldBlock, StructBlock
from wagtail.blocks.field_block import CharBlock, FieldBlockAdapter

from .utils import html_table_to_dict


try:
    from wagtail.admin.telepath import register
except ImportError:
    from wagtail.telepath import register


type BlockDefinitions = Iterable[tuple[str, Block] | list[str | Block]]


class TinyTableFieldBlock(FieldBlock):
    def __init__(
        self, *, required: bool = True, help_text: str | None = None, **kwargs: Any
    ) -> None:
        """CharField's 'label' and 'initial' parameters are not exposed, as Block
        handles that functionality natively (via 'label' and 'default').

        CharField's 'max_length' and 'min_length' parameters are not exposed as table
        data needs to have arbitrary length.
        """
        kwargs["required"] = False
        self.field_options: dict[str, Any] = {
            "required": required,
            "help_text": help_text,
        }

        super().__init__(**kwargs)

    @cached_property
    def field(self) -> forms.CharField:
        return forms.CharField(widget=forms.HiddenInput(), **self.field_options)

    def value_from_form(self, value: str) -> dict:
        try:
            return dict(json.loads(value))
        except (json.decoder.JSONDecodeError, TypeError, ValueError):
            return html_table_to_dict(value, allow_links=self.meta.allow_links)

    def value_for_form(self, value: dict | None) -> str:
        return json.dumps(value)

    def get_form_state(self, value: dict | None) -> str:
        # we return the original html for TinyMCE.
        return value.get("html", "") if value else ""

    class Meta:
        default = None
        icon = "table"


class TinyTableBlockAdapter(FieldBlockAdapter):
    js_constructor = "streamblock.blocks.TinyTableBlockAdapter"

    def js_args(self, block) -> list:
        the_args = super().js_args(block)

        the_args[2]["enableLinks"] = block.meta.allow_links
        the_args[2]["enableContextMenu"] = block.meta.enable_context_menu

        return the_args

    @cached_property
    def media(self) -> Media:
        field_media = super().media
        js = [
            *field_media._js,  # pylint: disable=protected-access
            "wagtail_tinytableblock/js/vendor/tinymce/tinymce.min.js",
            "wagtail_tinytableblock/js/tiny-table-block.js",
        ]
        return Media(js=js)


register(TinyTableBlockAdapter(), TinyTableFieldBlock)


class TinyTableBlock(StructBlock):
    title = CharBlock(required=False)
    caption = CharBlock(required=False)

    def __init__(
        self,
        local_blocks: BlockDefinitions | None = None,
        search_index: bool = True,  # noqa: FBT001,FBT002
        *,
        allow_links: bool = False,
        enable_context_menu: bool = False,
        **kwargs
    ) -> None:
        if local_blocks is None:
            local_blocks = ()

        # Manually define the data block so we can pass on configuration kwargs.
        data_block = TinyTableFieldBlock(
            required=False,
            allow_links=allow_links,
            enable_context_menu=enable_context_menu,
        )

        local_blocks = (*local_blocks, ("data", data_block))
        super().__init__(local_blocks=local_blocks, search_index=search_index, **kwargs)

    class Meta:
        icon = "table"
        template = "wagtail_tinytableblock/table_block.html"
        allow_links = False
        enable_context_menu = False
