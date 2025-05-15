
# Scrum

## Scientific Article PDF Parser
This project automatically extracts essential information from scientific articles in PDF format.

## Description
The program analyzes PDF files of scientific articles to extract:

- The original filename (with spaces converted to underscores)
- The title of the article
- The author information
- The abstract of the article
- The introduction
- The main body of the article
- The conclusion
- The discussion
- The bibliography/references

The system lets you select PDF files via a graphical interface and creates an output folder for the processed files (in text or XML format).

## Prerequisites

- Linux operating system
- Python 3.x
- pdftotext utility (from poppler-utils package)
- tkinter (usually included with Python)

## Installation

Clone the repository:

```bash
git remote add origin git@github.com:CaroHP24/Scrum.git
git branch -M Sprint-4
git push -u origin Sprint-4
````

Install the necessary dependencies:

```bash
sudo apt-get install poppler-utils  # For the pdftotext utility
```

## Project Structure

```text
├── extraction.py        # Title, author, abstract, and references extraction
├── extract_corps.py     # Extraction of the main body of the article
├── extract_discussion.py# Extraction of introduction, discussion, and conclusion sections
├── generation.py        # Creation of formatted output files (TXT/XML)
├── deleteTmp.py         # Deletes the temporary directory used during processing
├── xml_parse.py         # XML generation functionality
├── main.py              # Main script integrating all functions and GUI for file selection
├── pdf_input/           # Folder for input PDF files
└── final_output/        # Folder for output (TXT or XML)
```

## Usage

1. Run the main script and select the PDF files via the graphical interface.

2. Run the main script with the desired output format:

* For text output:

```bash
python3 main.py -t
```

* For XML output:

```bash
python3 main.py -x
```

3. Retrieve the results from the `final_output/` folder.

## Output Formats

**Text Format (-t)**
The text output produces `.txt` files with the following content:

```
First line: Original PDF filename
Second line: Article title
Third line: Article abstract
```

**XML Format (-x)**
The XML output produces `.xml` files with the following structure:

```xml
<article>
  <preamble>Original PDF filename</preamble>
  <titre>Article title</titre>
  <auteur>Author information</auteur>
  <abstract>Article abstract</abstract>
  <introduction>Introduction</introduction>
  <corps>Main body of the article</corps>
  <conclusion>Conclusion</conclusion>
  <discussion>Discussion</discussion>
  <biblio>Bibliography/references</biblio>
</article>
```

## Detailed Operation

1. **Input/Output Management (amel.py)**

This module handles:

* Preparing the working directories
* Converting PDFs to temporary text files
* Coordinating the final processing

**Main functions:**

* `clean_and_prepare_dirs()`: Cleans and prepares the working directories
* `convert_pdf_to_text()`: Converts PDFs to plain text
* `final_treatement()`: Applies final processing and generates output files
* `txt_parse()`: Coordinates the text parsing process
* `main()`: Handles command-line arguments and directs processing based on format selection

2. **Information Extraction (extraction.py, extract\_corps.py, extract\_discussion.py)**

These modules analyze text files to extract relevant information.

**Main functions:**

* `extract_title()`: Extracts the article title
* `extract_authors()`: Extracts author information
* `extract_abstract()`: Extracts the article abstract
* `extract_references()`: Extracts bibliography/references
* `extract_corps()`: Extracts the main body of the article
* `extract_introduction()`, `extract_discussion()`, `extract_conclusion()`: Extract corresponding sections

3. **Output File Generation (generation.py)**

This module creates the final text files with the required format.

**Main functions:**

* `parse_filename()`: Formats the filename (replaces spaces with underscores)
* Creates text files with structured information

4. **XML Generation (xml\_parse.py)**

This module creates XML files with structured article information.

**Main function:**

* `generate_article_xml()`: Creates a well-formatted XML file with article components

5. **Temporary Directory Cleanup (deleteTmp.py)**

This module deletes the temporary directory (`pdf_input/tmp_txt`) used during processing.

**Main function:**

* `delete_temp_files()`: Deletes the temporary directory if it exists and prints status messages.

## Notes

* If an output folder already exists, it will be deleted and recreated.
* The program handles cases where certain sections may be missing from the article.
* Extraction is optimized for scientific articles following a standard format.
* XML files are properly formatted with indentation for readability.

## Development

This project was developed using the SCRUM agile methodology. Each version is available in a dedicated branch on GitHub.

