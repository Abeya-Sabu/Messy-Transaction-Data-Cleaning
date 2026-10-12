import csv
import json
from collections import Counter
from datetime import datetime
from decimal import Decimal, InvalidOperation

VALID_STATUSES = {"paid", "pending", "cancelled", "refund"}

def clean_name(name):
    return " ".join(name.split()).title()

def clean_date(value):
    value = value.strip()

    formats = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%d-%m-%y"
    ]

    for date_format in formats:
        try:
            date = datetime.strptime(value, date_format)
            return date.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return None

def clean_amount(value):
    value = value.strip().replace(",", "")

    try:
        amount = Decimal(value)

        if not amount.is_finite() or amount <= 0:
            return None

        return amount.quantize(Decimal("0.01"))

    except InvalidOperation:
        return None

def main():

    try:
        with open("input.csv", "r", encoding="utf-8-sig",
                  newline="") as file:
            reader = csv.DictReader(file)

            required_columns = {
                "transaction_id",
                "customer_name",
                "amount",
                "transaction_date",
                "status",
                "order_id"
            }

            if not reader.fieldnames or not required_columns.issubset(
                set(reader.fieldnames)
            ):
                print("Error: CSV column names do not match.")
                print("Please check your input.csv file.")
                return

            rows = list(reader)

    except FileNotFoundError:
        print("Error: input.csv not found.")
        return

    cleaned_rows = []

    for row_number, row in enumerate(rows, start=2):

        transaction_id = (row.get("transaction_id") or "").strip()
        original_name = row.get("customer_name") or ""
        original_date = row.get("transaction_date") or ""
        original_amount = row.get("amount") or ""
        original_status = row.get("status") or ""

        customer_name = clean_name(original_name)
        transaction_date = clean_date(original_date)
        amount = clean_amount(original_amount)
        status = original_status.strip().lower()

        issues = []

        if not transaction_id:
            issues.append("Missing transaction ID")

        if not customer_name:
            issues.append("Missing customer name")

        if transaction_date is None:
            issues.append("Invalid or ambiguous date")

        if amount is None:
            issues.append("Invalid amount")

        if status not in VALID_STATUSES:
            issues.append("Unknown status")
            status = ""

        cleaned_rows.append({
            "row_number": row_number,
            "transaction_id": transaction_id,
            "original_name": original_name,
            "customer_name": customer_name,
            "original_date": original_date,
            "transaction_date": transaction_date or "",
            "original_amount": original_amount,
            "amount": (
                format(amount, ".2f") if amount is not None else ""
            ),
            "status": status,
            "order_id": (row.get("order_id") or "").strip(),
            "validity": "",
            "issues": issues
        })

    id_counts = Counter(
        row["transaction_id"]
        for row in cleaned_rows
        if row["transaction_id"]
    )

    duplicate_id_count = 0

    for row in cleaned_rows:
        transaction_id = row["transaction_id"]

        if transaction_id and id_counts[transaction_id] > 1:
            row["issues"].append("Duplicate transaction ID")
            duplicate_id_count += 1

    transaction_counts = Counter()

    for row in cleaned_rows:
        if (
            row["customer_name"]
            and row["transaction_date"]
            and row["amount"]
            and row["status"]
        ):
            key = (
                row["customer_name"].casefold(),
                row["transaction_date"],
                row["amount"],
                row["status"]
            )
            transaction_counts[key] += 1

    possible_duplicate_count = 0

    for row in cleaned_rows:
        if (
            row["customer_name"]
            and row["transaction_date"]
            and row["amount"]
            and row["status"]
        ):
            key = (
                row["customer_name"].casefold(),
                row["transaction_date"],
                row["amount"],
                row["status"]
            )

            if transaction_counts[key] > 1:
                row["issues"].append("Possible duplicate transaction")
                possible_duplicate_count += 1

    for row in cleaned_rows:
        row["validity"] = (
            "valid" if not row["issues"] else "invalid"
        )

    valid_rows = [
        row for row in cleaned_rows
        if row["validity"] == "valid"
    ]

    invalid_rows = [
        row for row in cleaned_rows
        if row["validity"] == "invalid"
    ]

    total_revenue = Decimal("0.00")

    for row in valid_rows:
        amount = Decimal(row["amount"])

        if row["status"] == "paid":
            total_revenue += amount
        elif row["status"] == "refund":
            total_revenue -= amount

    columns = [
        "row_number",
        "transaction_id",
        "original_name",
        "customer_name",
        "original_date",
        "transaction_date",
        "original_amount",
        "amount",
        "status",
        "order_id",
        "validity",
        "issues"
    ]

    with open("cleaned.csv", "w", encoding="utf-8",
              newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

        for row in cleaned_rows:
            output_row = row.copy()
            output_row["issues"] = "; ".join(row["issues"])
            writer.writerow(output_row)

    report = {
        "input_rows": len(cleaned_rows),
        "valid_rows": len(valid_rows),
        "invalid_rows": len(invalid_rows),
        "duplicate_id_rows": duplicate_id_count,
        "possible_duplicate_rows": possible_duplicate_count,
        "total_revenue": format(total_revenue, ".2f")
    }

    with open("report.json", "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print("Project completed successfully!")
    print("Input rows:", len(cleaned_rows))
    print("Valid rows:", len(valid_rows))
    print("Invalid rows:", len(invalid_rows))
    print("Duplicate ID rows:", duplicate_id_count)
    print("Possible duplicate rows:", possible_duplicate_count)
    print("Total revenue:", format(total_revenue, ".2f"))
    print("Output files: cleaned.csv and report.json")


if __name__ == "__main__":
    main()