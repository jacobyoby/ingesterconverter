# ingesterconverter
 
# Document Conversion Tool

This script is a document conversion tool that converts PDF and Word documents (.docx) to text files (.txt). The script also tracks processed files using a SQLite database, allowing for skipping previously processed files with no modifications. Multithreading is used to process multiple files concurrently for improved performance.

## Features

- Convert PDF and Word documents (.docx) to text files
- Keep track of processed files with a SQLite database
- Use multithreading for concurrent file processing
- Log output for easy tracking and debugging

## Requirements
- Python 3.6 or higher
- pdfplumber
- textract
- python-docx
- SQLite (included in Python standard library)

## Installation

1. Clone the repository or download the script.
2. Install the required dependencies using pip:

pip install pdfplumber textract python-docx

## Usage

1. Create a folder named "input_folder" in the same directory as the script.
2. Place the PDF and/or Word documents you want to convert in the "input_folder".
3. Run the script:

python3 convert.py

4. The script will process the documents and create an "output_folder" with the extracted text files.

## Notes

- Currently, the script only supports PDF and .docx files. You can modify the script to support other file formats.
- The script uses multithreading to improve performance, but it may not be ideal for extremely large files or a very high number of files. Adjust the `max_workers` parameter in `ThreadPoolExecutor` according to your needs and system capabilities.
