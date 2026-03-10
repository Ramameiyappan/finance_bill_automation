import os
from dotenv import load_dotenv
import json
import logging
import google.generativeai as genai

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

""" congirue the geemini api """
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

def build_prompt(invoice_text):
    """ promt given to gemini """
    prompt = f"""
You are an intelligent invoice parser.

Extract structured information from the invoice text.

Return ONLY valid JSON.

Rules:
- If field not present return null
- If multiple values exist return them separated by comma
- Identify category from:
  Office Expenses, Tools & Software, Travel & Petrol, Utilities, Other
- Extract line items table

Required fields:

vendor_name
invoice_number
invoice_date
due_date
total_amount
gst_number
payment_status
category

line_items:
- description
- quantity
- unit_price
- item_total

Return JSON in this format:

{{
"vendor_name": "",
"invoice_number": "",
"invoice_date": "",
"due_date": "",
"total_amount": "",
"gst_number": "",
"payment_status": "",
"category": "",
"line_items": [
{{
"description": "",
"quantity": "",
"unit_price": "",
"item_total": ""
}}
]
}}

Invoice Text:
{invoice_text}
"""
    return prompt

def extract_invoice_fields(invoice_text):
    """ extract the field """
    prompt = build_prompt(invoice_text)
    for attempt in range(3):
        try:
            response = model.generate_content(prompt)
            result = response.text
            json_start = result.find("{")
            json_end = result.rfind("}")
            if json_start == -1 or json_end == -1:
                raise ValueError("No JSON found in Gemini response")
            json_text = result[json_start:json_end+1]
            data = json.loads(json_text)
            logging.info("Invoice fields extracted successfully")
            return data
        except Exception as e:
            logging.warning(f"Gemini parse failed attempt {attempt+1}")
    logging.error("Gemini extraction failed after retries")
    return None