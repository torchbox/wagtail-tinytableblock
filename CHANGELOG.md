# Wagtail TinyTableBlock Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [unreleased]

## [0.3.4] - 2025-04-10

## Fixed

- When pasting a table with text/markup before and after it, only the table is kept for formatting purposes.

## [0.3.3] - 2025-04-10

## Changed

- Improved paste handling with line breaks

## [0.3.2] - 2025-04-02

## Fixed

- Line breaks were stripped out ([#11](https://github.com/torchbox/wagtail-tinytableblock/pull/11))


## [0.3.1] - 2025-04-02

## Added

- The missing unlink toolbar icon, when links are enabled

## [0.3] - 2025-04-02

## Added

- The delete cell/row buttons ([#10](https://github.com/torchbox/wagtail-tinytableblock/pull/10))
- Support for cell alignment and width ([#10](https://github.com/torchbox/wagtail-tinytableblock/pull/10))

## [0.2.3] - 2025-03-31

### Changed

- Added cell/row props buttons to the toolbar

## [0.2.2] - 2025-03-19

### Changed

- The TinyMCE contextual menu is disabled by default. ([#8](https://github.com/torchbox/wagtail-tinytableblock/pull/8))
  Pass `enable_context_menu=True` to your block definition to enable the TinyMCE context menu.

## [0.2.2] - 2025-03-18

### Changed

- Added the copy / paste buttons to the toolbar and contextual menu ([#7](https://github.com/torchbox/wagtail-tinytableblock/pull/7))

## [0.2.1] - 2025-03-11

### Changed

- Links are only allowed if the block is configured with (`allow_links=True`) ([#6](https://github.com/torchbox/wagtail-tinytableblock/pull/6))
- Improved sanitization

## [0.2] - 2025-03-09

### Added

- Ability to enable the TinyMCE link plugin ([#5](https://github.com/torchbox/wagtail-tinytableblock/pull/5))
- Better documentation

### Changed

- Improved the table parsing. All cells in a `thead` are now considered header cells ([#5](https://github.com/torchbox/wagtail-tinytableblock/pull/5))

## [0.1] - 2025-03-04

Initial release


[unreleased]: https://github.com/torchbox/wagtail-tinytableblock/compare/v0.2.3...HEAD
[0.3.3]: https://github.com/torchbox/wagtail-tinytableblock/compare/v0.3.3...v0.3.4
[0.3.3]: https://github.com/torchbox/wagtail-tinytableblock/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/torchbox/wagtail-tinytableblock/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/torchbox/wagtail-tinytableblock/compare/v0.3...v0.3.1
[0.3]: https://github.com/torchbox/wagtail-tinytableblock/compare/v0.2.4...v0.3
[0.2.4]: https://github.com/torchbox/wagtail-tinytableblock/compare/v0.2.3...v0.2.4
[0.2.3]: https://github.com/torchbox/wagtail-tinytableblock/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/torchbox/wagtail-tinytableblock/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/torchbox/wagtail-tinytableblock/compare/v0.2...v0.2.1
[0.2]: https://github.com/torchbox/wagtail-tinytableblock/compare/v0.1...v0.2
[0.1]: https://github.com/torchbox/wagtail-tinytableblock/compare/9b5dec2...v0.1
