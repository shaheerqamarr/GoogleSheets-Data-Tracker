import gspread
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv
load_dotenv()

def get_last_processed_row():
    """Read the last processed row number from tracking file"""
    if os.path.exists(os.getenv("TRACKING_FILE")):
        with open(os.getenv("TRACKING_FILE"), 'r') as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0

def save_last_processed_row(row_number):
    """Save the last processed row number to tracking file"""
    with open(os.getenv("TRACKING_FILE"), 'w') as f:
        f.write(str(row_number))

def connect_to_sheet():
    """Connect to Google Sheets and return the worksheet"""
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    creds = Credentials.from_service_account_file(os.getenv("CREDENTIALS_FILE"), scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(os.getenv("SPREADSHEET_ID")).sheet1
    
    return sheet

def get_new_rows():
    """Main function to detect and return new rows"""
    
    print("Connecting to Google Sheets...")
    sheet = connect_to_sheet()
    
    all_data = sheet.get_all_values()
    
    if not all_data:
        print("Sheet is empty!")
        return [], []
    
    last_processed_row = get_last_processed_row()
    total_rows = len(all_data)
    
    print(f"\n{'='*60}")
    print(f"TRACKING INFORMATION")
    print(f"{'='*60}")
    print(f"Total rows in sheet: {total_rows}")
    print(f"Last processed row: {last_processed_row}")
    print(f"New rows detected: {max(0, total_rows - last_processed_row)}")
    
    headers = all_data[0] if all_data else []
    all_rows = all_data[1:] if len(all_data) > 1 else []

    if last_processed_row == 0:
        new_rows = all_rows
    else:
        start_index = last_processed_row - 1
        new_rows = all_rows[start_index:] if start_index < len(all_rows) else []
    
    print(f"\n{'='*60}")
    print(f"ALL DATA ROWS (Total: {len(all_rows)})")
    print(f"{'='*60}")
    if headers:
        print(f"Headers: {headers}")
    for idx, row in enumerate(all_rows, start=2):  
        print(f"Row {idx}: {row}")
    
    print(f"\n{'='*60}")
    print(f"NEW ROWS ONLY (Total: {len(new_rows)})")
    print(f"{'='*60}")
    if new_rows:
        if headers:
            print(f"Headers: {headers}")
        for idx, row in enumerate(new_rows, start=last_processed_row + 2):
            print(f"Row {idx}: {row}")
    else:
        print("No new rows found.")
    
    save_last_processed_row(total_rows)
    print(f"\n✓ Tracking file updated: last processed row is now {total_rows}")
    
    return all_rows, new_rows

if __name__ == "__main__":
    try:
        all_rows, new_rows = get_new_rows()
        
        if new_rows:
            print(f"\n{'='*60}")
            print(f"PROCESSING NEW ROWS")
            print(f"{'='*60}")
            for idx, row in enumerate(new_rows, start=1):
                print(f"Processing new row {idx}: {row}")
        
    except FileNotFoundError:
        print(f"Error: {os.getenv("CREDENTIALS_FILE")} not found!")
        print("Make sure your credentials file is in the same directory.")
    except gspread.exceptions.APIError as e:
        print(f"Google Sheets API Error: {e}")
        print("Make sure the sheet is shared with your service account email.")
    except Exception as e:
        print(f"Error: {e}")