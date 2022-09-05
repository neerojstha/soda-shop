import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
    Collecting sales details from the user
    """
    while True:
        print("please enter last day sales.")
        print("data should be five numbers and separated by commas.")
        print("Example: 11,22,33,44,55\n")

        data_str = input("submit your data here:\n")
    
        sales_data  = data_str.split(",")
        if validate_data(sales_data):
            print("Data is valid")
            break
    return sales_data

def validate_data(values):
    """
    inside try function check the validity of the data 
    with user submitted data
    """
  
    try:
        if len(values) != 5:
            raise ValueError(
                f"Exactly 5 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"invalid data: {e}, please try again.\n")
        return False

    return True
       

def update_worksheet(data, worksheet):
    """
    updating relevant worksheet with recent data
    """
    print(f"updatinng {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")

def calculate_excess_data(sales_row):
    """
    compare sales and inventory for future order.
    future order inventory limit of 99
    """

    print("calculating order data...\n")
    inventory = SHEET.worksheet("inventory").get_all_values()
    inventory_row = inventory[-1]
    
    excess_data = []
    for inventory, sales in zip(sales_row, sales_row):
        excess = int(inventory) - sales
        excess_data.append(excess)
    return excess_data   

def get_last_6_entries_sales():
    """
    collecting last 6 entries from the book.
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 6):
        column = sales.col_values(ind)
        columns.append(column[-6:])

    return columns

def calculate_inventory_data(data):
    """ 
    calculate the average inventory for each item, adding 15%
    """
    print("calculating inventory data...\n")
    new_inventory_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        inventory_num = average * 1.15
        new_inventory_data.append(round(inventory_num))

    return new_inventory_data    
        

def main():
    """
    all function working
    """    
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_excess_data = calculate_excess_data(sales_data)
    update_worksheet(new_excess_data, "excess")
    sales_columns = get_last_6_entries_sales()
    inventory_data = calculate_inventory_data(sales_columns)
    update_worksheet(inventory_data, "inventory")



print("Soda shop data Automation") 
main()


