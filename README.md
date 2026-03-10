# Finance Bill Automation

Finance Bill Automation is an end-to-end pipeline that automatically reads invoices received via email, extracts structured information using OCR and AI, stores the data in a database, and generates Excel reports with expense summaries and charts.

The system removes the need for manual invoice entry by automatically processing bills from multiple vendors.

---

## Features

* Automatic email monitoring using Gmail API
* Download invoice attachments (PDF, JPG, PNG)
* OCR extraction for scanned invoices using Tesseract
* AI-based field extraction using Gemini API
* SQLite database storage with relational structure
* Parent–Child tables for invoices and line items
* Automatic expense categorization
* Excel report generation with charts

---

## Technology Stack

* **Python** – Core programming language
* **Gmail API** – Email inbox access
* **PyMuPDF** – Extract text from digital PDFs
* **pdf2image** – Convert scanned PDFs to images
* **Tesseract OCR** – Extract text from images
* **Google Gemini API** – Extract structured invoice fields
* **SQLite + SQLAlchemy** – Database storage
* **OpenPyXL** – Excel report generation with charts

---

## Project Structure

```
finance_automation

├── monitor_email.py
│   Handles Gmail authentication and downloads invoice attachments
│
├── text_extracted.py
│   Extracts text from PDFs and images using OCR
│
├── invoice_parser.py
│   Uses Gemini AI to extract structured invoice fields
│
├── excel_report.py
│   Generates Excel reports with charts
│
├── main_pipeline.py
│   Runs the full automation pipeline
│
├── database/
│   ├── models.py
│   └── db_manager.py
│
├── bills/
│   Stores downloaded invoice attachments
│
├── output/
│   Stores generated Excel reports
│
├── finance.db
│   SQLite database
│
├── README.md
│   Project documentation
│
├── .env.example
│   Example environment configuration
│
├── requirements.txt
│   Project dependencies
│
└── .gitignore
```

---

## Prerequisites

Before running the project install the following tools.

### 1. Install Python

Install **Python 3.10 or later**

Verify installation:

```
python --version
```

---

### 2. Install Tesseract OCR

Download Tesseract from:

https://github.com/UB-Mannheim/tesseract/wiki

After installation add the installation folder to your system **PATH**.

Example:

```
C:\Program Files\Tesseract-OCR
```

---

### 3. Install Poppler

Poppler is required for converting scanned PDFs to images.

Download Poppler from:

https://github.com/oschwartz10612/poppler-windows/releases

Extract the downloaded file and add the **bin folder** to your PATH.

Example:

```
C:\poppler\Library\bin
```

---

## Installation

Clone the repository:

```
git clone https://github.com/Ramameiyappan/finance_bill_automation.git
```

Navigate to the project folder:

```
cd finance_bill_automation
```

---

## Create Virtual Environment

```
python -m venv virtual_environment
```

Activate the environment.

### Windows

```
virtual_environment\Scripts\activate
```

### Linux / Mac

```
source virtual_environment/bin/activate
```

---

## Install Dependencies

```
pip install -r requirements.txt
```

---

## Environment Setup

Create a `.env` file in the project root.

Example:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## Gmail API Setup

1. Open **Google Cloud Console**
2. Create a new project
3. Enable **Gmail API**
4. Create **OAuth Credentials**
5. Download the credentials file

Rename the downloaded file to:

```
credentials.json
```

Place the file in the project root directory.

When the program runs for the first time it will automatically generate:

```
token.json
```

---

## Running the Pipeline

Run the automation pipeline:

```
python main_pipeline.py
```

The system will perform the following steps:

1. Connect to Gmail inbox
2. Detect unread emails containing attachments
3. Download invoice files to the bills folder
4. Extract text using OCR and PDF readers
5. Parse invoice data using Gemini AI
6. Store extracted data in SQLite database
7. Generate Excel report with expense summary

---

## Output

Downloaded invoices are stored in:

```
bills/YYYY-MM/vendor_name/
```

Generated reports are stored in:

```
output/
```

Example report:

```
output/2026_03_expense_report.xlsx
```

---

## Excel Report Structure

The generated Excel report contains **three sheets**.

### Sheet 1 – Invoices

Complete list of invoices with vendor details, dates, amounts, and categories.

### Sheet 2 – Line Items

All extracted line items from invoices.

### Sheet 3 – Category Summary

Expense totals grouped by category with charts.

Charts included:

* Bar chart showing monthly expense by category
* Pie chart showing expense distribution

---

## Supported Document Types

The system supports multiple invoice formats:

* Digital PDFs
* Scanned PDFs
* Image receipts (PNG, JPG, JPEG)

---

## Workflow

```
Email Inbox
      ↓
Download Attachment
      ↓
Save to bills folder
      ↓
OCR Text Extraction
      ↓
Gemini AI Field Extraction
      ↓
Store Data in SQLite
      ↓
Generate Excel Report
```
