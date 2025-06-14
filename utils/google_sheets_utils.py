import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


def get_myphones_spreadsheet(range='myphones'):
    # Определяем путь к файлу с токеном
    CREDENTIALS_FILE = os.path.join('config', 'api_google_sheets_token.json')
    spreadsheet_id = '1nJHlfoRuqu3boqb7Bf3ymI-NRdV0kIkzE80PqI5igVg'

    # Загрузка учетных данных из файла токена
    scopes = ['https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)

    # Авторизация и создание сервиса для работы с Google Sheets
    service = build('sheets', 'v4', credentials=credentials)

    # Получение данных из таблицы
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range,
        majorDimension='ROWS',
    ).execute()

    return values