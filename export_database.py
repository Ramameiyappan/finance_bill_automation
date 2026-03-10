"""
Export invoice and line item data from the database
into CSV files.
"""
import csv
from database.db_manager import SessionLocal
from database.models import Invoice, LineItem
import os

def export_csv():
    """Export invoices and line items into CSV files."""
    session = SessionLocal()
    OUTPUT_FOLDER = "output"
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    invoice_csv = os.path.join(OUTPUT_FOLDER, "invoices.csv")
    line_items_csv = os.path.join(OUTPUT_FOLDER, "line_items.csv")

    invoices = session.query(Invoice).all()
    with open(invoice_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "id", "vendor_name", "invoice_number",
            "invoice_date", "due_date", "total_amount", "gst_number",
            "payment_status", "category", "file_path", "created_at"])

        for inv in invoices:
            writer.writerow([
                inv.id, inv.vendor_name, inv.invoice_number,
                inv.invoice_date, inv.due_date, inv.total_amount, inv.gst_number,
                inv.payment_status, inv.category, inv.file_path, inv.created_at])

    items = session.query(LineItem).all()
    with open(line_items_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            "id", "invoice_id", "description",
            "quantity", "unit_price", "item_total"])

        for item in items:
            writer.writerow([ item.id, item.invoice_id, item.description,
                item.quantity, item.unit_price, item.item_total])

    session.close()
    print("CSV export completed")