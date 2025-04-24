import argparse
from .core import rearrange_pages


def main():
    """
    Command-line interface for rearrange-pdf.
    """
    parser = argparse.ArgumentParser(description="Rearrange PDF pages for booklet printing")
    parser.add_argument("filename", help="Input PDF file")
    parser.add_argument("--per-page", type=int, choices=[2, 4], default=4,
                        help="Number of slides per physical page (2 or 4, default=4)")
    args = parser.parse_args()

    new_pdf = rearrange_pages(args.filename, args.per_page)
    print(f"Rearranged PDF saved as {new_pdf}")


if __name__ == "__main__":
    main()
