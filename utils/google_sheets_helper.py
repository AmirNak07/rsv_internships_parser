import gspread
from oauth2client.service_account import ServiceAccountCredentials


def authorize_google_sheets() -> gspread.Client:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("config/credentials.json", scope)
    client = gspread.authorize(creds)
    return client


def write_to_google_sheet(client: gspread.Client, spreadsheet_id: str, sheet_name: str, data: list) -> None:
    sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)

    sheet.clear()

    headers = ["title", "instituteName", "region", "industryName", "skills", "duration", "participationFormatName", "paymentAmount", "link"]
    rows = [headers] + data

    sheet.append_rows(values=rows)
