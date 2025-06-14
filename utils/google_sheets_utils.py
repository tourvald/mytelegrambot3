import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import os


def get_myphones_spreadsheet(range='myphones'):
    # Определяем путь к файлу с токеном
    CREDENTIALS_FILE = os.path.join('config', 'api_google_sheets_token.json')
    spreadsheet_id = '1nJHlfoRuqu3boqb7Bf3ymI-NRdV0kIkzE80PqI5igVg'

    # Загрузка учетных данных из файла токена
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])

    # Авторизация и создание сервиса для работы с Google Sheets
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    # Получение данных из таблицы
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range,
        majorDimension='ROWS',
    ).execute()

    print(values)
    return values