# 🌐 Task  — Dynamic Web Scraping from E-commerce Websites

## 📘 Overview
This project performs **web scraping** on two e-commerce websites (e.g., Amazon and Flipkart) using **BeautifulSoup** and **Requests**.  
The script allows the user to **dynamically search for any product** and saves the results (name, price, rating, link) into an Excel file.

---

## ⚙️ Features
- 🔍 Accepts dynamic search queries from the user.
- 🛍️ Scrapes product details from **Amazon** and **Flipkart**.
- 📊 Saves scraped data into an Excel file (`product_results.xlsx`).
- 🧠 Handles missing data and exceptions gracefully.

---

## 🧩 Tech Stack
- **Language:** Python 3.x  
- **Libraries:** `requests`, `beautifulsoup4`, `pandas`, `openpyxl`, `re`, `logging`

---

## 📦 Installation
1. Navigate to the project directory:
   ```bash
   cd Task1_WebScraping
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the scraper:
   ```bash
   python web_scraper.py
   ```

---

## 🧮 Example Usage
```
Enter product name to search: laptop
```
✅ The script will fetch results like:
| Website | Product Name | Price | Rating | Link |
|----------|---------------|--------|----------|------|
| Amazon | HP Laptop 15s | ₹45,999 | 4.3 | [Link](https://amazon.in/...) |
| Flipkart | Dell Inspiron 3511 | ₹47,499 | 4.2 | [Link](https://flipkart.com/...) |

Results are saved as:
```
output/product_results_laptop.xlsx
```

---

## 🧩 Code Structure
```
Task1_WebScraping/
│
├── web_scraper.py        # Main scraper script
├── requirements.txt      # Python dependencies
├── README.md             # Documentation
└── output/               # Folder containing Excel results
```

---

## 🧠 Error Handling
- Handles network timeouts and connection errors.
- Skips incomplete entries (missing price or name).
- Waits random time between requests to avoid blocking.

---

## 📚 Requirements
```
requests
beautifulsoup4
pandas
openpyxl
```

---

## 👨‍💻 Author
**Ganesh Masavale**  
📅 *Created in 2025*
