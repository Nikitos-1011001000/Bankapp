from file_parser import read_csv_transactions, read_excel_transactions

if __name__ == "__main__":
    csv_data = read_csv_transactions("transactions.csv")
    excel_data = read_excel_transactions("transactions_excel.xlsx")

    print(f"CSV: {len(csv_data)} транзакций")
    print(f"Excel: {len(excel_data)} транзакций")
