import pytest
from pathlib import Path
from pdf_to_cards import pdf_OCR
from image_to_text import image_OCR
from text_to_cards import text_to_card

SAMPLES_DIR = Path(__file__).parent / "samples"
SAMPLE_PDF = SAMPLES_DIR / "sample.pdf"
SAMPLE_IMG = SAMPLES_DIR / "sample.jpg"

EXPECTED_IMG_TEXT = "THIS IS A TEST IMAGE"
EXPECTED_PDF_TEXT = "This is a pdf test page 1"

@pytest.fixture
def cleanup_files():
    """Clean input_note.txt and response.txt before/after tests"""
    for f in ["input_note.txt", "response.txt"]:
        p = Path(f)
        if p.exists():
            p.unlink()
    yield
    for f in ["input_note.txt", "response.txt"]:
        p = Path(f)
        if p.exists():
            p.unlink()

def test_text_conversion_api(cleanup_files):
    with open("input_note.txt", "w") as f:
        f.write("This is a test note for Gemini API.")

    text_to_card()
    with open("response.txt") as f:
        content = f.read()
    print("Text-to-card Output:\n", content)

    assert content.strip() != ""

def test_image_conversion_api(cleanup_files):
    # result = image_OCR(str(SAMPLE_IMG))
    image_OCR(str(SAMPLE_IMG))
    with open("input_note.txt") as f:
        content = f.read()
    print("Image OCR Output:\n", content)

    assert content.strip() == EXPECTED_IMG_TEXT
    #assert result.strip() == EXPECTED_IMG_TEXT

def test_pdf_conversion_api(cleanup_files):
    # result = pdf_OCR(str(SAMPLE_PDF))
    pdf_OCR(str(SAMPLE_PDF))
    with open("input_note.txt") as f:
        content=f.read()
    print("PDF OCR Output:\n", content)

    assert content.strip() == EXPECTED_PDF_TEXT
    #assert result.strip() == EXPECTED_PDF_TEXT
