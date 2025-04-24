# Rearrange PDF

A Python tool to rearrange PDF pages for printing booklets.

## Installation

```bash
pip install rearrange-pdf
```

## Usage

### Command Line

```bash
# Rearrange PDF with 4 slides per page (default)
rearrange-pdf your_document.pdf

# Rearrange PDF with 2 slides per page
rearrange-pdf your_document.pdf --per-page 2
```

### Python API

```python
from rearrange_pdf import rearrange_pages

# Rearrange with 4 slides per page
new_pdf = rearrange_pages("your_document.pdf", per_page=4)

# Rearrange with 2 slides per page
new_pdf = rearrange_pages("your_document.pdf", per_page=2)
```

## How it works

This tool rearranges PDF pages to create a booklet layout:

- For 4 slides per page: Pages are rearranged in the order [0, 2, 4, 6, 3, 1, 7, 5]
- For 2 slides per page: Pages are rearranged in the order [0, 2, 1, 3]

If the total number of pages is not divisible by the group size (8 for 4-per-page, 4 for 2-per-page), blank pages are added to complete the group.

## License

MIT
