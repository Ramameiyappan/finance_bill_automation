"""
Main pipeline for the Finance Automation system.

Handles email monitoring, invoice processing,
database storage, and report generation.
"""

import os
import logging
from monitor_email import monitor_inbox
from text_extracted import extract_text
from invoice_parser import extract_invoice_fields
from database.db_manager import save_invoice, init_db
from excel_report import generate_excel_report
from export_database import export_csv 

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

BILLS_FOLDER = "bills"

def get_all_files():
    """"Scan the bills directory and return all supported invoice files."""
    files = []
    for root, dirs, filenames in os.walk(BILLS_FOLDER):
        for f in filenames:
            if f.lower().endswith((".pdf", ".png", ".jpg", ".jpeg")):
                files.append(os.path.join(root, f))
    return files

def process_invoices():
    """Extract text, parse invoice fields, and store results in the database."""
    files = get_all_files()
    logging.info(f"Total documents found: {len(files)}")
    for file_path in files:
        try:
            logging.info(f"Processing file: {file_path}")
            text = extract_text(file_path)
            if not text:
                logging.warning("No text extracted")
                continue
            data = extract_invoice_fields(text)
            if not data:
                logging.warning("Gemini extraction failed")
                continue
            save_invoice(data, file_path)
        except Exception as e:
            logging.error(f"Error processing {file_path}: {e}")

def run_pipeline():
    """Run the complete finance automation workflow."""
    logging.info("Starting Finance Automation Pipeline")
    init_db()
    monitor_inbox()
    process_invoices()
    generate_excel_report()
    export_csv()
    logging.info("Pipeline completed successfully")

if __name__ == "__main__":
    run_pipeline()