import pandas as pd
import os

# File path
FILE_PATH = "sales.csv"

# Load dataset or create if not found
if os.path.exists(FILE_PATH):
    df = pd.read_csv(FILE_PATH)
else:
    df = pd.DataFrame(columns=["ID", "Product", "Category", "Quantity", "Price", "Region"])
    df.to_csv(FILE_PATH, index=False)

# -------------------------------
# CREATE Operation
# -------------------------------
def create_record(record):
    """
    Insert a new record into the sales dataset.
    record: dict with keys matching dataset columns
    """
    global df
    df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    df.to_csv(FILE_PATH, index=False)
    print("\n Record added successfully!")


# -------------------------------
# READ Operation
# -------------------------------
def read_record(record_id):
    """
    Retrieve and display record(s) based on ID.
    """
    result = df[df["ID"] == record_id]
    if not result.empty:
        print("\n Record found:\n", result)
    else:
        print("\n No record found with ID:", record_id)


# -------------------------------
# UPDATE Operation
# -------------------------------
def update_record(record_id, column, new_value):
    """
    Update specific field for a record by ID.
    """
    global df
    if record_id in df["ID"].values:
        df.loc[df["ID"] == record_id, column] = new_value
        df.to_csv(FILE_PATH, index=False)
        print(f"\n Record ID {record_id} updated: {column} → {new_value}")
    else:
        print("\n Record not found!")


# -------------------------------
# DELETE Operation
# -------------------------------
def delete_record(record_id):
    """
    Delete record from dataset by ID.
    """
    global df
    if record_id in df["ID"].values:
        df = df[df["ID"] != record_id]
        df.to_csv(FILE_PATH, index=False)
        print(f"\n🗑️ Record ID {record_id} deleted successfully.")
    else:
        print("\n Record not found!")


# -------------------------------
# DEMO EXECUTION
# -------------------------------
if __name__ == "__main__":
    print(" Initial Dataset:\n", df)

    # CREATE
    new_data = {"ID": 4, "Product": "Table", "Category": "Furniture", "Quantity": 3, "Price": 4500, "Region": "West"}
    create_record(new_data)

    # READ
    read_record(2)

    # UPDATE
    update_record(3, "Price", 3500)

    # DELETE
    delete_record(1)

    print("\n Final Dataset:\n", pd.read_csv(FILE_PATH))
