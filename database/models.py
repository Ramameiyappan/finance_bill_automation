"""
Database models defining Invoice and LineItem tables
with a parent-child relationship.
"""
from sqlalchemy import (Column, Integer, String,
    Float, ForeignKey, DateTime, Date)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import UniqueConstraint
import datetime

Base = declarative_base()

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True)
    vendor_name = Column(String, nullable=True)
    invoice_number = Column(String, nullable=True)
    invoice_date = Column(Date, nullable=True)
    due_date = Column(Date, nullable=True)
    total_amount = Column(Float, nullable=True)
    gst_number = Column(String, nullable=True)
    payment_status = Column(String, nullable=True)
    category = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    line_items = relationship("LineItem", back_populates="invoice", cascade="all, delete-orphan")
    __table_args__ = (
        UniqueConstraint(
            "vendor_name", "invoice_number", name="unique_invoice_vendor"),
    )

class LineItem(Base):
    __tablename__ = "line_items"
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    description = Column(String, nullable=True)
    quantity = Column(Float, nullable=True)
    unit_price = Column(Float, nullable=True)
    item_total = Column(Float, nullable=True)
    invoice = relationship("Invoice", back_populates="line_items")