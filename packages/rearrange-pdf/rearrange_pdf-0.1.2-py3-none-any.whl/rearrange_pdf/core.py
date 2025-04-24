from PyPDF2 import PdfReader, PdfWriter, PageObject


def add_blank_pages(writer, num_pages):
    """
    Add blank pages to a PDF writer.
    
    Args:
        writer: PdfWriter instance
        num_pages: Number of blank pages to add
    """
    blank_page = PageObject.create_blank_page(width=842, height=595)
    for _ in range(num_pages):
        writer.add_page(blank_page)


def get_new_order(per_page):
    """
    Get the new page order based on per_page setting.
    
    Args:
        per_page: Number of slides per page (2 or 4)
        
    Returns:
        List of indices representing the new page order
        
    Raises:
        ValueError: If per_page is not 2 or 4
    """
    if per_page == 4:
        return [0, 2, 4, 6, 3, 1, 7, 5]  # 每頁四張，一組8頁
    elif per_page == 2:
        return [0, 2, 1, 3]  # 每頁兩張，一組4頁（1,2,3,4 -> 1,3,2,4）
    else:
        raise ValueError("Only per-page 2 or 4 is supported")


def rearrange_pages(filename, per_page=4):
    """
    Rearrange pages in a PDF file for booklet printing.
    
    Args:
        filename: Path to the input PDF file
        per_page: Number of slides per page (2 or 4, default=4)
        
    Returns:
        Path to the rearranged PDF file
        
    Raises:
        ValueError: If per_page is not 2 or 4
    """
    reader = PdfReader(filename)
    original_pages = reader.pages
    total_pages = len(original_pages)

    group_size = per_page * 2
    remainder = total_pages % group_size
    blank_pages = group_size - remainder if remainder != 0 else 0

    writer = PdfWriter()
    for page in original_pages:
        writer.add_page(page)
    if blank_pages > 0:
        add_blank_pages(writer, blank_pages)
        total_pages += blank_pages

    rearranged_writer = PdfWriter()
    new_order = get_new_order(per_page)

    for start in range(0, total_pages, group_size):
        for index in new_order:
            if (start + index) < total_pages:
                rearranged_writer.add_page(writer.pages[start + index])

    new_filename = f"rearranged_p{per_page}_" + filename.split("/")[-1]
    with open(new_filename, "wb") as f:
        rearranged_writer.write(f)

    return new_filename
