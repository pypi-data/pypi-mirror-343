import click
import llm
import arxiv
# Keep specific import for this one as it seemed to work
from arxiv import UnexpectedEmptyPageError, HTTPError
import fitz  # PyMuPDF
import tempfile
import os
import re
from typing import List, Union
import base64 # For image encoding


@llm.hookimpl
def register_commands(cli):
    return
    # @cli.command()
    # def hello_world():
    #     "Say hello world"
    #     click.echo("Hello world!")


@llm.hookimpl
def register_fragment_loaders(register):
    register("arxiv", arxiv_loader)


def extract_arxiv_id(argument: str) -> Union[str, None]:
    """Extracts arXiv ID from URL or returns the argument if it looks like an ID."""
    # Check for URL pattern: https://arxiv.org/abs/xxxx.xxxxx or /pdf/xxxx.xxxxx.pdf
    # Allows for optional 'v' followed by digits for versions
    match_url = re.match(r"https?://arxiv\.org/(?:abs|pdf)/(\d{4,}\.\d{4,}(?:v\d+)?)(?:\.pdf)?$", argument)
    if match_url:
        return match_url.group(1)

    # Check for ID pattern: xxxx.xxxxx or xxxx.xxxxxvN (enforce lengths)
    match_id = re.match(r"^(\d{4,}\.\d{4,}(?:v\d+)?)$", argument)
    if match_id:
        return match_id.group(1)

    # Check for older ID pattern: category/xxxxxxx (7 digits)
    match_old_id = re.match(r"^[a-z-]+(?:\.[A-Z]{2})?/\d{7}$", argument)
    if match_old_id:
        return argument # Return the full old ID including category

    return None


def arxiv_loader(argument: str) -> List[llm.Fragment]:
    """
    Load text and images from an arXiv paper PDF.

    Returns a list of fragments: first is text, subsequent are base64 images.
    Text fragment contains placeholders like [IMAGE: source_url] for images found on each page.

    Argument is an arXiv ID (e.g., 2310.06825, hep-th/0101001)
    or an arXiv URL (e.g., https://arxiv.org/abs/2310.06825).
    """
    arxiv_id = extract_arxiv_id(argument)
    if not arxiv_id:
        raise ValueError(
            f"Invalid arXiv identifier or URL: {argument}. "
            "Expected format like '2310.06825', 'cs.CL/1234567', or 'https://arxiv.org/abs/...'."
        )

    try:
        search = arxiv.Search(id_list=[arxiv_id], max_results=1)
        results = list(search.results())
        if not results:
            raise ValueError(f"No paper found for arXiv ID: {arxiv_id}")
        paper = results[0]
        paper_source_url = paper.entry_id
        
        # Store image fragments separately first
        image_fragments = [] 
        full_text_parts = [] # Collect text parts page by page

        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_path = paper.download_pdf(dirpath=temp_dir)
            try:
                doc = fitz.open(pdf_path)
                for page_num, page in enumerate(doc):
                    # 1. Extract text for the current page
                    page_text = page.get_text()
                    full_text_parts.append(page_text)
                    
                    # 2. Extract images and create image fragments + placeholders
                    image_list = page.get_images(full=True)
                    page_image_placeholders = []
                    for img_index, img_info in enumerate(image_list):
                        xref = img_info[0]
                        try:
                            base_image = doc.extract_image(xref)
                        except Exception:
                            # Ignore images that cannot be extracted
                            continue 
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"]
                        img_base64 = base64.b64encode(image_bytes).decode('utf-8')
                        
                        # Generate source URL for both placeholder and fragment
                        img_source = f"{paper_source_url}/page_{page_num + 1}_img_{img_index + 1}.{image_ext}"
                        
                        # Add placeholder to list for this page
                        page_image_placeholders.append(f"\n[IMAGE: {img_source}]\n")
                        
                        # Add image fragment to the main list
                        image_fragments.append(llm.Fragment(img_base64, source=img_source))
                    
                    # 3. Append placeholders to the text collected for this page
                    if page_image_placeholders:
                        full_text_parts.append("".join(page_image_placeholders))
                        
                doc.close()
            except Exception as e:
                if 'doc' in locals() and doc.is_open:
                    doc.close()
                raise ValueError(f"Failed to extract content from PDF {pdf_path}: {e}") from e

        # Combine all text parts
        full_text = "".join(full_text_parts)
        
        # Create final list of fragments
        fragments = [llm.Fragment(full_text, source=paper_source_url)] + image_fragments
        return fragments

    except UnexpectedEmptyPageError as e:
         raise ValueError(f"arXiv search returned an unexpected empty page for ID: {arxiv_id}. Check the ID. Error: {e}") from e
    except HTTPError as e:
        raise ValueError(f"Failed to fetch paper details from arXiv for ID {arxiv_id}: {e}") from e
    except Exception as e:
        raise ValueError(f"Error processing arXiv paper {arxiv_id}: {str(e)}") from e
