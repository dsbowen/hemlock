# Changelog

## 0.0.51

- Fixed bug in `make_list` tool
- Added break in `Slider` template to leave space for tooltip by default
- Moved static resources to github.io CDN
- Fixed bug in `likert` when items are reversed

## 0.0.50

- Markdown syntax for page text
- Added and updated value comparisons for validate function bank
- Added value comparisons to submit function bank

## 0.0.49

Lots of updates since 0.0.22. Here are just the few I remember.

- moved from the BeautifulSoup architecture to a classic Jinja architecture for dramatically faster page rendering
- many additional question polymorphs, including Bootstrap range sliders and accompanying Likert functionality
- improved page caching
- improved web socket connectivity
- improved redundancy for workers and long-loading pages
- improved page previewing
- resolved to maintain a better changelog

## 0.0.22

- added support for embedded `dash` apps

## CLI 0.0.17

- added `setup-venv` command for easier virtual environment setup on Windows git bash

## 0.0.20

- fixed `Submit.match` and `Validate.match` bug: now requires full match instead of partial match
- improved number inputs and added `step` attribute