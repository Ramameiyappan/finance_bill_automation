"""
Database manager for storing invoices and line items
using SQLAlchemy with SQLite.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from database.models import Base, Invoice, LineItem

DATABASE_URL = "sqlite:///finance.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Initialize database tables if they do not exist."""
    Base.metadata.create_all(engine)

def to_date(value):
    """Convert string value into a valid date format."""
    if not value:
        return None
    formats = ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"]
    for fmt in formats:
        try:
            dt = datetime.strptime(value, fmt)
            return dt.date()
        except:
            continue
    return None

def to_float(value):
    """Convert numeric values to float safely."""
    if value is None:
        return None
    try:
        return float(str(value).replace(",", ""))
    except:
        return None

def save_invoice(data, file_path):
    """Store invoice and line items into the database."""
    session = SessionLocal()
    try:
        existing = session.query(Invoice).filter_by(
            vendor_name=data.get("vendor_name"),
            invoice_number=data.get("invoice_number")
        ).first()
        if existing:
            print("Duplicate invoice detected. Skipping.")
            session.close()
            return

        invoice = Invoice(
            vendor_name=data.get("vendor_name"),
            invoice_number=data.get("invoice_number"),
            invoice_date=to_date(data.get("invoice_date")),
            due_date=to_date(data.get("due_date")),
            total_amount=to_float(data.get("total_amount")),
            gst_number=data.get("gst_number"),
            payment_status=data.get("payment_status"),
            category=data.get("category"),
            file_path=file_path
        )
        session.add(invoice)
        session.commit()

        line_items = data.get("line_items", [])
        for item in line_items:
            line = LineItem(
                invoice_id=invoice.id,
                description=item.get("description"),
                quantity=to_float(item.get("quantity")),
                unit_price=to_float(item.get("unit_price")),
                item_total=to_float(item.get("item_total"))
            )
            session.add(line)
        session.commit()
        print("Invoice saved successfully")
    except Exception as e:
        session.rollback()
        print("Error saving invoice:", e)
    finally:
        session.close()