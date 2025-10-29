# 🧾 Task — CRUD Operations on Sales Dataset  

## 📘 Overview  
This project demonstrates **Create, Read, Update, and Delete (CRUD)** operations on a **Sales dataset** stored in a CSV file using Python and Pandas.  
It provides a simple console-based interface for managing sales data without a database.  

## ⚙️ Features  
- **Create**: Add new sales records.  
- **Read**: Display all or specific records.  
- **Update**: Modify existing entries (like price or quantity).  
- **Delete**: Remove unwanted records.  
- Automatically saves all changes back to the CSV file.  

## 🧩 Tech Stack  
- **Language:** Python 3.x  
- **Libraries:** `pandas`, `os`  

## 📦 Installation  

1. **Navigate to the project directory**  
   ```bash
   cd Task2_CRUD_Operations
   ```

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure sales_data.csv exists**  
   The file should look like:
   ```csv
   ID,Product,Category,Price,Quantity,Date
   1,Laptop,Electronics,55000,2,2025-10-20
   2,Mouse,Accessories,700,10,2025-10-21
   3,Keyboard,Accessories,1200,5,2025-10-22
   ```

## ▶️ Usage  

Run the script:
```bash
python sales_crud.py
```

Example menu:
```
1. Create new record
2. Read records
3. Update record
4. Delete record
5. Exit
```

### Example:
**Create**
```
Enter Product Name: Laptop
Enter Category: Electronics
Enter Price: 55000
Enter Quantity: 2
Enter Date (YYYY-MM-DD): 2025-10-20
✅ Record added successfully!
```

**Read**
```
ID | Product | Category | Price | Quantity | Date
1  | Laptop  | Electronics | 55000 | 2 | 2025-10-20
```

**Update**
```
Enter record ID to update: 1
Enter new price: 60000
✅ Record updated successfully!
```

**Delete**
```
Enter record ID to delete: 2
✅ Record deleted successfully!
```

## 💾 Expected Output  

After performing operations, the `sales_data.csv` file is automatically updated.  
Example final CSV:
```csv
ID,Product,Category,Price,Quantity,Date
1,Laptop,Electronics,60000,2,2025-10-20
3,Keyboard,Accessories,1200,5,2025-10-22
```

## 🧮 Code Explanation  

| Function | Description |
|-----------|--------------|
| `create_record()` | Adds a new sales entry to the CSV file. |
| `read_records()` | Displays all records or filters by ID. |
| `update_record()` | Finds a record by ID and updates fields. |
| `delete_record()` | Deletes a record by ID. |
| `save_data()` | Saves the updated DataFrame back to CSV. |

## 📚 Requirements  
```
pandas
```

## 👨‍💻 Author  
**Ganesh Masavale**  
📅 *Created in 2025*  
