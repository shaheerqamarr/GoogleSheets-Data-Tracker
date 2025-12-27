# Google Sheets Data Tracker

A Python script that automatically tracks and detects new rows added to a Google Sheet. Perfect for monitoring data updates, processing new entries, or triggering workflows based on new data.

## Features

- ✅ Connects to Google Sheets via API
- ✅ Tracks which rows have been processed
- ✅ Detects only new rows added since last run
- ✅ Stores progress in a local text file
- ✅ Displays both all rows and new rows for comparison
- ✅ Automatically updates tracking after each run
- ✅ Uses environment variables for secure configuration
- ✅ Clear debug output and statistics

## Prerequisites

- Python 3.7+
- A Google Cloud Project with Sheets API enabled
- Service account credentials (JSON file)
- Access to the Google Sheet you want to track

## Installation

1. **Clone or download this project**

2. **Install required packages:**
```bash
pip install gspread google-auth python-dotenv
```

3. **Set up Google Cloud credentials:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable **Google Sheets API** and **Google Drive API**
   - Create a **Service Account**
   - Download the credentials JSON file
   - Save it in the project folder (e.g., `credentials.json`)

4. **Share your Google Sheet:**
   - Open your `credentials.json` file
   - Find the `client_email` field (e.g., `your-service@project.iam.gserviceaccount.com`)
   - Open your Google Sheet
   - Click "Share" and add that email with **Editor** access

## Configuration

Create a `.env` file in the project root with the following variables:

```env
CREDENTIALS_FILE=credentials.json
SPREADSHEET_ID=your_spreadsheet_id_here
TRACKING_FILE=last_processed_row.txt
```

**Finding your Spreadsheet ID:**

The ID is in your Google Sheets URL:
```
https://docs.google.com/spreadsheets/d/1qzlx0ZT-3Qtj2Mwe1zN71Bm07H8EOMcILnkVBZ4myXg/edit
                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                      This is your SPREADSHEET_ID
```

## Usage

### Basic Usage

Run the script:
```bash
python main.py
```

### First Run
- Processes all existing rows as "new"
- Creates `last_processed_row.txt` to track progress
- Displays all data from the sheet

### Subsequent Runs
- Only shows rows added since the last run
- Updates the tracking file automatically
- Perfect for scheduled runs (cron jobs, task scheduler)

### Reset Tracking
To start fresh and reprocess all rows:
```bash
# Windows
del last_processed_row.txt

# Mac/Linux
rm last_processed_row.txt
```

## Example Output

```
Connecting to Google Sheets...

============================================================
TRACKING INFORMATION
============================================================
Total rows in sheet: 15
Last processed row: 10
New rows detected: 5

============================================================
ALL DATA ROWS (Total: 14)
============================================================
Headers: ['Name', 'Email', 'Date', 'Status']
Row 2: ['John Doe', 'john@example.com', '2024-01-15', 'Active']
Row 3: ['Jane Smith', 'jane@example.com', '2024-01-16', 'Active']
...

============================================================
NEW ROWS ONLY (Total: 5)
============================================================
Headers: ['Name', 'Email', 'Date', 'Status']
Row 11: ['New User', 'new@example.com', '2024-01-20', 'Pending']
Row 12: ['Another User', 'another@example.com', '2024-01-21', 'Active']
...

✓ Tracking file updated: last processed row is now 15

============================================================
PROCESSING NEW ROWS
============================================================
Processing new row 1: ['New User', 'new@example.com', '2024-01-20', 'Pending']
Processing new row 2: ['Another User', 'another@example.com', '2024-01-21', 'Active']
```

## Customization

Add your own processing logic in the `if __name__ == "__main__"` section:

```python
if new_rows:
    for idx, row in enumerate(new_rows, start=1):
        print(f"Processing new row {idx}: {row}")
        
        # Add your custom logic here:
        # - Send email notifications
        # - Save to database
        # - Trigger webhooks
        # - Update another sheet
        # - Generate reports
        # - Parse specific columns: name = row[0], email = row[1], etc.
```

## Scheduling (Optional)

### Windows Task Scheduler
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., every hour)
4. Action: Start a program
5. Program: `python`
6. Arguments: `C:\path\to\your\main.py`
7. Start in: `C:\path\to\your\project\folder`

### Linux/Mac Cron Job
```bash
# Edit crontab
crontab -e

# Run every hour
0 * * * * cd /path/to/project && /usr/bin/python3 main.py >> tracker.log 2>&1

# Run every 15 minutes
*/15 * * * * cd /path/to/project && /usr/bin/python3 main.py >> tracker.log 2>&1
```

## File Structure

```
project/
│
├── main.py                      # Main script
├── .env                         # Environment variables (don't commit!)
├── credentials.json             # Google service account credentials (don't commit!)
├── last_processed_row.txt       # Auto-generated tracking file
├── README.md                    # This file
├── requirements.txt             # Python dependencies
└── .gitignore                   # Git ignore file
```

## Creating requirements.txt

Create a `requirements.txt` file for easy dependency installation:

```txt
gspread==5.12.0
google-auth==2.23.4
python-dotenv==1.0.0
```

Install all dependencies at once:
```bash
pip install -r requirements.txt
```

## Troubleshooting

### "Spreadsheet not found"
- Make sure the sheet is shared with your service account email
- Check that the `SPREADSHEET_ID` in `.env` is correct
- Verify the sheet exists and you have access

### "Request had insufficient authentication scopes"
- Ensure both Google Sheets API and Google Drive API are enabled in Google Cloud Console
- Check that scopes in the code include both spreadsheets and drive

### "No new rows found" (always)
- Delete `last_processed_row.txt` and run again
- Check that new data exists in your sheet beyond the header row
- Verify the tracking file is being created and updated

### "PermissionError" or "[403]"
- Share the Google Sheet with the service account email from `credentials.json`
- Give it **Editor** permissions (not just Viewer)

### "credentials.json not found"
- Check that the file path in `.env` matches your actual file location
- Ensure the file is in the same directory as specified

### Environment variables not loading
- Make sure `.env` file is in the same directory as `main.py`
- Check that variable names match exactly (case-sensitive)
- Verify `python-dotenv` is installed

## Security Notes

### Create a .gitignore file

Never commit sensitive files to version control. Create a `.gitignore` file:

```gitignore
# Credentials and secrets
credentials.json
.env

# Tracking files
last_processed_row.txt
*.log

# Python
*.pyc
__pycache__/
*.py[cod]
*$py.class

# Virtual environment
venv/
.venv/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
```

### Best Practices
- **Never commit `credentials.json` or `.env` to version control**
- Keep your credentials file secure and don't share it
- Use environment-specific `.env` files for different deployments
- Rotate service account keys periodically
- Use separate service accounts for development and production

## How It Works

1. **Initial Run**: Reads all rows from the sheet, marks all as "new", saves total count
2. **Tracking**: Stores the last processed row number in `last_processed_row.txt`
3. **Subsequent Runs**: Only processes rows added after the last saved row number
4. **Update**: After processing, updates the tracking file with the new total

## Example Use Cases

- **Data Pipeline**: Automatically process new form responses
- **Notifications**: Send emails when new entries are added
- **Database Sync**: Keep a database in sync with sheet updates
- **Analytics**: Generate reports on new data entries
- **Workflow Automation**: Trigger actions based on new rows
- **Monitoring**: Track when new data arrives for dashboards

## License

This project is open source and available for personal and commercial use.

## Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Verify your Google Cloud setup is complete
3. Ensure the sheet is properly shared with your service account
4. Check that all environment variables are set correctly in `.env`
5. Review error messages for specific guidance

---

**Happy tracking! 🚀**