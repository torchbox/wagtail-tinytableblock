/* global tinymce */
class TinyTableBlockDefinition extends window.wagtailStreamField.blocks.FieldBlockDefinition {
  render(placeholder, prefix, initialState, initialError) {
    const block = super.render(placeholder, prefix, initialState, initialError);

    let plugins = "table autoresize";
    let toolbar = "undo redo | tablerowheader tablecolheader tablemergecells tablesplitcells tablecellprops tablerowprops | tableinsertcolbefore tableinsertcolafter tableinsertrowbefore tableinsertrowafter | tabledeletecol tabledeleterow tabledelete";
    let contextmenu = "table";
    let valid_elements = "br,table[border|width|height|align|summary|style],tr[align|valign|style],td[align|valign|width|colspan|rowspan|style],th[align|valign|width|colspan|rowspan|scope|style],thead,tbody";
    const valid_styles = {
      "th": "text-align,vertical-align,width",
      "td": "text-align,vertical-align,width",
      "tr": "text-align,width"
    }

    if (this.meta.enableLinks) {
      plugins += " link autolink";
      toolbar += " | link unlink";
      contextmenu += " link";
      valid_elements += ",a[href|target|rel]";
    }

    let contextmenu_never_use_native = true;
    if (!this.meta.enableContextMenu) {
      contextmenu = false;
      contextmenu_never_use_native = false;
    }

    tinymce.init({
      selector: "#" + prefix,
      plugins: plugins,
      menubar: "",
      toolbar: toolbar,
      contextmenu: contextmenu,
      valid_elements: valid_elements,
      valid_styles: valid_styles,
      table_toolbar: "",  // disable the floating toolbar
      table_advtab: false,
      table_appearance_options: false,
      table_cell_advtab: false,
      table_row_advtab: false,
      table_sizing_mode: 'responsive',
      table_resize_bars: false,
      object_resizing: false,
      newline_behavior: "linebreak",
      contextmenu_never_use_native: contextmenu_never_use_native,
      skin: (window.matchMedia("(prefers-color-scheme: dark)").matches ? "oxide-dark" : "oxide"),
      content_css: (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "default"),
      content_style: 'thead th, thead td { font-weight: 700; }',
      statusbar: false,
      branding: false,
      promotion: false,
      license_key: "gpl",
      setup: (editor) => {
        let tableExists = false;

        editor.on("init", () => {
          tableExists = editor.getBody().getElementsByTagName("table").length > 0;
          if (!tableExists) {
              editor.execCommand("mceInsertTable", false, { rows: 2, columns: 2 });
          }
        });

        editor.on("change NodeChange SetContent", () => {
          // Check for tables after content changes
          tableExists = editor.getBody().getElementsByTagName('table').length > 0;
          // propagate the changes to the hidden input.
          editor.save();
        });

        editor.on("BeforeExecCommand", (e) => {
          // Don't allow inserting a table if one exists.
          if (e.command === 'mceInsertTable' && tableExists) {
            e.preventDefault();
          }
        });

        editor.on("ExecCommand", (e) => {
            if (e.command === "mceTableDelete") {
                // re-add empty table on delete
                editor.execCommand("mceInsertTable", false, {rows: 2, columns: 2});
            }
        });

        editor.on("PastePreProcess keydown", (e) => {
            // Only allow adding content into the one table
            const activeNode = editor.selection.getNode();
            const isCell = activeNode.nodeName === "TD" || activeNode.nodeName === "TH";
            const isParentCell = activeNode.parentNode.nodeName === "TD" || activeNode.parentNode.nodeName === "TH";
            if (!isCell && !isParentCell && e.keyCode !== 9) {
              e.preventDefault();
            }
        });
      },
      paste_preprocess: function(editor, args) {
        if (editor.dom.getParent(editor.selection.getNode(), "td,th")) {
          // If there is a table, strip out but the table.
          const tableMatch = args.content.match(/<table[\s\S]*?<\/table>/i);
          if (tableMatch) {
              args.content = tableMatch[0];
          }

          // Unwrap any paragraphs/divs that might come with the paste
          args.content = args.content.replace(/<p>(.*?)<\/p>/g, "$1<br>");
          args.content = args.content.replace(/<div>(.*?)<\/div>/g, "$1<br>");

          let match_caption = args.content.match(/<caption[^>]*>(.*?)<\/caption>/i);
          if (match_caption) {
            // Get our block's caption element and set it.
            let caption = document.getElementById(prefix.replace("-data", "-caption"));
            if (caption) {
             caption.value = match_caption[1].replace(/<[^>]*>/gm, "");
            }
          }
          args.content = args.content.replace(/<caption[^>]*>(.*?)<\/caption>/g, "");
        }
      },
      paste_postprocess: function(editor, args) {
        if (editor.dom.getParent(editor.selection.getNode(), "td,th")) {
          // Replace newlines with <br> tags, and remove the trailing <br>
          args.node.innerHTML = args.node.innerHTML.replace(/\n/g, "<br>");
          args.node.innerHTML = args.node.innerHTML.replace(/<br>$/, "");
        }
      }
    });

    return block;
  }
}

window.telepath.register("streamblock.blocks.TinyTableBlockAdapter", TinyTableBlockDefinition);
