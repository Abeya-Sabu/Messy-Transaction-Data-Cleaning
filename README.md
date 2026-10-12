Messy Transactions Data Cleaning

1. Description

This project is a Python-based data cleaning and validation program. It reads transaction records from `input.csv`, cleans the data, identifies invalid records and duplicate transactions, and generates output files.

2. Technologies Used

- Python 3
- CSV module
- JSON module
- Datetime module

3. Input File

`input.csv` contains transaction records with the following fields:

- Transaction ID
- Customer Name
- Amount
- Transaction Date
- Status
- Order ID

4. Features

- Standardizes customer names.
- Converts dates into `YYYY-MM-DD` format.
- Converts transaction amounts into numeric values.
- Normalizes transaction statuses.
- Validates records and explains data issues.
- Detects duplicate transaction IDs and possible duplicate transactions.
- Calculates total net revenue.
- Generates `cleaned.csv` and `report.json`.

5. How to Run

**Requirements:** Python 3 installed on your computer.

1. Place `main.py` and `input.csv` in the same folder.
2. Open the project folder in PyCharm.
3. Open the terminal.
4. Run the following command:

   `python main.py`

The program generates `cleaned.csv` and `report.json` in the project folder.

6. Output Files

- `cleaned.csv`: Contains cleaned transaction data, validity status, and explanations of issues.
- `report.json`: Contains the number of input, valid, and invalid rows, duplicate counts, and total revenue.

7. Assumptions

- Customer names are trimmed and converted to title case.
- Dates that cannot be interpreted confidently are considered invalid.
- Transaction amounts must be positive numeric values.
- Accepted statuses are `paid`, `pending`, `cancelled`, and `refund`.
- Repeated transaction IDs are flagged as duplicates.
- Transactions with matching customer names, dates, amounts, and statuses are flagged as possible duplicates.
- Net revenue is calculated as valid paid amounts minus valid refund amounts. Refund amounts are assumed to be positive.

8. Edge Case Tested

An invalid date such as `31/13/2026` is tested. Since the date is impossible, the program marks the record as invalid and records the reason in the issues field.

9. Conclusion

This project demonstrates basic Python programming, data cleaning, data validation, duplicate detection, CSV file handling, and JSON report generation.