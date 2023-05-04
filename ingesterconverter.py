# Import required libraries
import os
import pdfplumber
import textract
import docx
import sqlite3
import logging
import threading
from concurrent.futures import ThreadPoolExecutor

# Configure logging settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Version: 1.0.3
# Description: A script to convert PDF and Word documents to text files
# Future functionality: Add support for .doc and .rtf file formats
# v1.0.2 add sqlite
# v1.0.3 add logging and multithreading

# Function to extract text from PDF files
def extract_pdf_text(file_path):
    pdf_text = ""

    # Open the PDF file with pdfplumber
    with pdfplumber.open(file_path) as pdf:
        # Iterate through the pages in the PDF
        for page in pdf.pages:
            # Extract text from the current page
            page_text = page.extract_text()
            # If pdfplumber fails to extract text, use OCR with Tesseract
            if not page_text:
                page_text = textract.process(file_path, method='tesseract', encoding='utf-8').decode()
            pdf_text += page_text

    return pdf_text

# Function to extract text from Word documents (.docx)
def extract_word_text(file_path):
    # Open the Word document with python-docx
    doc = docx.Document(file_path)
    return "".join(para.text + "\n" for para in doc.paragraphs)

# Function to set up the database for tracking processed files
def setup_database():
    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect("file_history.db")
    cursor = conn.cursor()
    # Create the 'processed_files' table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS processed_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL UNIQUE,
            last_modified TIMESTAMP NOT NULL
        )
        """
    )
    conn.commit()
    return conn

# Function to check if a file has already been processed
def file_processed(conn, file_path, last_modified):
    cursor = conn.cursor()
    # Query the database for the file_path and retrieve the last_modified timestamp
    cursor.execute(
        "SELECT last_modified FROM processed_files WHERE file_path = ?", (file_path,)
    )
    return result[0] == last_modified if (result := cursor.fetchone()) else False

# Function to add a processed file to the database
def add_processed_file(conn, file_path, last_modified):
    cursor = conn.cursor()
    # Insert or replace the file entry in the 'processed_files' table
    cursor.execute(
        "INSERT OR REPLACE INTO processed_files (file_path, last_modified) VALUES (?, ?)",
        (file_path, last_modified),
    )
    conn.commit()

# Function to process a single file
def process_file(file, input_folder, output_folder):
    file_path = os.path.join(input_folder, file)
    file_name, file_extension = os.path.splitext(file)
    last_modified = os.path.getmtime(file_path)

    # Create a new database connection for the current thread
    db_conn = setup_database()

    if not file_processed(db_conn, file_path, last_modified):
        if file_extension.lower() == '.pdf':
            extracted_text = extract_pdf_text(file_path)
        elif file_extension.lower() == '.docx':
            extracted_text = extract_word_text(file_path)
        else:
            return

        with open(os.path.join(output_folder, f"{file_name}.txt"), "w", encoding="utf-8") as text_file:
            text_file.write(extracted_text)

        add_processed_file(db_conn, file_path, last_modified)
        logging.info(f"Finished processing {file}. Output saved in {output_folder}/{file_name}.txt")

    # Close the database connection
    db_conn.close()

# Main function
def main():
    input_folder = "input_folder"
    output_folder = "output_folder"

    # Create input and output folders if they don't exist
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Use a ThreadPoolExecutor to manage multithreading
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(process_file, file, input_folder, output_folder) for file in os.listdir(input_folder)]
        # Wait for all threads to complete
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()
