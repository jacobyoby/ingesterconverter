import os
import pdfplumber
import textract
import docx

# Version: 1.0.1
# Description: A script to convert PDF and Word documents to text files
# Future functionality: Add support for .doc and .rtf file formats


def extract_pdf_text(file_path):
    """Extract text from a PDF file.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF file.
    """
    pdf_text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if not page_text:
                # Perform OCR with textract when pdfplumber fails to extract text
                page_text = textract.process(
                    file_path, method='tesseract', encoding='utf-8').decode()
            pdf_text += page_text

    return pdf_text


def extract_word_text(file_path):
    """Extract text from a Word file (.docx).

    Args:
        file_path (str): Path to the Word file.

    Returns:
        str: Extracted text from the Word file.
    """
    doc = docx.Document(file_path)
    word_text = ""

    for para in doc.paragraphs:
        word_text += para.text + "\n"

    return word_text


def main():
    """Main function to process input files and extract text."""
    script_dir = os.path.dirname(os.path.realpath(__file__))

    input_folder = os.path.join(script_dir, "input")
    output_folder = os.path.join(script_dir, "output")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file)
        file_name, file_extension = os.path.splitext(file)

        if file_extension.lower() == '.pdf':
            extracted_text = extract_pdf_text(file_path)
        elif file_extension.lower() == '.docx':
            extracted_text = extract_word_text(file_path)
        # Add support for other file formats (e.g., .doc, .rtf) here
        # elif file_extension.lower() == '.doc':
        #   extracted_text = extract_doc_text(file_path)
        # elif file_extension.lower() == '.rtf':
        #   extracted_text = extract_rtf_text(file_path
        else:
            continue

        with open(os.path.join(output_folder, f"{file_name}.txt"), "w", encoding="utf-8") as text_file:
            text_file.write(extracted_text)


if __name__ == "__main__":
    main()
