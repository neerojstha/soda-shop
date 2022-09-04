import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('soda_shop')


def get_sales_data():
    """
    Collecting sales details fromm the user
    """
    print("please enter last day sales.")
    print("data should be six numbers and separated by commas.")
    print("Example: 11,22,33,44,55,66\n")

    data_str = input("submit your data here:")
    
    sales_data  = data_str.split(",")
    validate_data(sales_data)

def validate_data(values):
    """
    inside try function check the validity of the data 
    with user submitted data
    """
    try:
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"invalid data: {e}, please try again.\n")
        print(values)
get_sales_data()
