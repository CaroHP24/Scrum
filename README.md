# Scrum

## Scientific Article PDF Parser
This project automatically extracts essential information (title and abstract) from scientific articles in PDF format.

## Description
The program analyzes PDF files of scientific articles to extract:

1. The original filename (with spaces converted to underscores)
2. The title of the article
3. The abstract of the article

The system takes as input a folder containing PDF files and creates an output folder for the processed text files.

## Prerequisites

- Linux operating system
- Python 3.x
- pdftotext utility (from poppler-utils package)

## Installation

To push an existing repository from the command line:

```bash
git remote add origin git@github.com:CaroHP24/Scrum.git
git branch -M Dev
git push -u origin Dev
```

Install the necessary dependencies:

```bash
sudo apt-get install poppler-utils  # For the pdftotext utility
```

## Project Structure
```text
├── amel.py         # Input/output management and PDF→TXT conversion
├── extraction.py   # Title and abstract extraction
├── generation.py   # Creation of formatted output files
├── deleteTmp.py    # Deletes the temporary directory used during processing
├── main.py         # Main script integrating all functions
├── pdf_input/      # Folder for input PDF files
└── final_output/   # Folder for output TXT files
```
## Usage

Place your PDF files in the `pdf_input/` folder.

Run the main script:

```bash
python3 main.py
```

Retrieve the results from the final_output/ folder

# Detailed Operation
1. **Input/Output Management (amel.py)**

This module handles:

+ Preparing the working directories
+ Converting PDFs to temporary text files
+ Coordinating the final processing

**Main functions:**

- clean_and_prepare_dirs(): Cleans and prepares the working directories
- convert_pdf_to_text(): Converts PDFs to plain text
- final_treatement(): Applies final processing and generates output files

2. **Information Extraction (extraction.py)**

This module analyzes text files to extract relevant information.

**Main functions:**

+ is_affiliation_line(): Detects lines containing affiliations
+ is_likely_author(): Identifies lines likely containing authors
+ extract_title(): Extracts the article title
+ extract_abstract(): Extracts the article abstract

3. **Output File Generation (generation.py)**

This module creates the final text files with the required format.

**Main functions:**

+ parse_filename(): Formats the filename (replaces spaces with underscores)
+ create_txt(): Generates the final text file with structured information

4. **Temporary Directory Cleanup (deleteTmp.py)**

This module deletes the temporary directory (pdf_input/tmp_txt) used during processing.

**Main function:**

+ delete_temp_files(): Deletes the temporary directory if it exists. Prints a message indicating whether the directory was deleted or if it was not found.

# Notes

If an output folder already exists, it will be deleted and recreated
The program handles cases where certain sections (title or abstract) are not present in the article
The extraction is optimized for scientific articles following a standard format

# Development
This project was developed using the SCRUM agile methodology. Each version is available in a dedicated branch on GitHub.