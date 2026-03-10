import os
import base64
import datetime
from email.utils import parseaddr
import logging

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

ALLOWED_EXTENSIONS = (".pdf", ".png", ".jpg", ".jpeg")
BILLS_FOLDER = "bills"
LOG_FILE = "email_monitor.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def authenticate_gmail():
    ''' Authenticate Gmail API using OAuth '''
    creds = None
    # check for stored credentials
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # if credentials are expired or not present
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    # connect user google gmail api
    service = build("gmail", "v1", credentials=creds)
    logging.info("Gmail authentication successful")
    return service

def get_vendor_name(headers):
    """Extract sender_vendor name"""
    sender = ""
    for header in headers:
        if header["name"] == "From":
            sender = header["value"]
            break
    name, email = parseaddr(sender)
    email_name = email.split("@")[0]
    if name:
        vendor = f"{name}_{email_name}"
    else:
        vendor = email_name
    vendor = vendor.replace(" ", "_")
    return vendor

def save_attachment(filename, data, vendor):
    """Save attachment to bills/YYYY-MM/vendor_name/"""
    today = datetime.datetime.now()
    month_folder = today.strftime("%Y-%m")
    path = os.path.join(BILLS_FOLDER, month_folder, vendor)
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, filename)
    with open(file_path, "wb") as f:
        f.write(data)
    logging.info(f"Saved attachment: {file_path}")

def process_parts(parts, service, msg_id, vendor):
    """ Recursively process message parts to extract attachments """
    has_attachment = False
    for part in parts:
        filename = part.get("filename")
        body = part.get("body", {})
        if filename and filename.lower().endswith(ALLOWED_EXTENSIONS):
            if "attachmentId" in body:
                attachment = service.users().messages().attachments().get(
                    userId="me",
                    messageId=msg_id,
                    id=body["attachmentId"]
                ).execute()
                data = base64.urlsafe_b64decode(attachment["data"])
                save_attachment(filename, data, vendor)
                has_attachment = True
        if "parts" in part:
            if process_parts(part["parts"], service, msg_id, vendor):
                has_attachment = True
    return has_attachment

def download_attachments(service, msg_id):
    """Download attachments from a message"""
    # get the entire message from mail id, thread id, snippet, payload
    message = service.users().messages().get(
        userId="me",
        id=msg_id
    ).execute()

    headers = message["payload"]["headers"]
    vendor = get_vendor_name(headers)
    payload = message.get("payload", {})
    parts = payload.get("parts", [])
    if not parts:
        parts = [payload]
    has_attachment = process_parts(parts, service, msg_id, vendor)
    return has_attachment

def mark_email_as_read(service, msg_id):
    service.users().messages().modify(
        userId="me",
        id=msg_id,
        body={
            "removeLabelIds": ["UNREAD"]
        }
    ).execute()
    logging.info(f"Marked email {msg_id} as read")

def get_unread_messages(service):
    messages = []
    next_page = None
    while True:
        response = service.users().messages().list(
            userId="me",
            labelIds=["INBOX"],
            q="is:unread has:attachment",
            pageToken=next_page
        ).execute()
        messages.extend(response.get("messages", []))
        next_page = response.get("nextPageToken")
        if not next_page:
            break
    logging.info(f"Total unread emails found: {len(messages)}")
    return messages

def monitor_inbox():
    """Check inbox and download attachments"""
    service = authenticate_gmail()
    # get all message id from the inbox along with nextPageToken, resultSizeEstimate
    messages = get_unread_messages(service)
    if not messages:
        logging.info("No unread emails with attachments found")
        return
    # get all attachment from the mail id that are filtered
    for msg in messages:
        msg_id = msg["id"]
        try:
            has_attachment = download_attachments(service, msg_id)
            if has_attachment:
                mark_email_as_read(service, msg_id)
        except Exception as e:
            logging.error(f"Error processing email {msg_id}: {str(e)}")