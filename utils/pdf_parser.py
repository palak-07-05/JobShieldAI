def sanitize_unicode(text: str) -> str:
    """Replace invalid surrogate characters that can crash Streamlit widgets."""
    if text is None:
        return ""
    return str(text).encode("utf-8", "replace").decode("utf-8")


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract plain text from an uploaded PDF file.

    Args:
        uploaded_file: A Streamlit UploadedFile object.

    Returns:
        Extracted text as a string.

    Raises:
        RuntimeError if pypdf is not installed or extraction fails.
    """
    try:
        import pypdf
    except ImportError:
        raise RuntimeError(
            "pypdf is not installed. Run: pip install pypdf"
        )

    try:
        reader = pypdf.PdfReader(uploaded_file)
        pages_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages_text.append(sanitize_unicode(text))
        return sanitize_unicode("\n".join(pages_text))
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF: {e}")
