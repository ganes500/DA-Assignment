# 📊 Task — Descriptive & Predictive Sales Analysis Dashboard

## 📘 Overview
This project performs **descriptive** and **predictive** analysis on a sales dataset, visualized through an **interactive dashboard** built using **Plotly Dash**.

---

## ⚙️ Features
- 📈 Descriptive Analysis (Total Sales, Average Order Value, Top Products)
- 🤖 Predictive Analysis (Linear Regression to forecast future sales)
- 🧭 Interactive Dashboard (Cross-filtering, dynamic graphs)
- 🎨 Visualizations: Bar Chart, Pie Chart, Line Chart

---

## 🧩 Tech Stack
- **Python 3.x**
- **Libraries:** pandas, plotly, dash, scikit-learn, numpy

---

## 📦 Installation
1. Navigate to the project directory:
   ```bash
   cd Task3_SalesDashboard
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the dashboard:
   ```bash
   python sales_dashboard.py
   ```

---

## 🧮 Dataset Example (`sales_data.csv`)
| Date       | Product   | Sales | Quantity |
|-------------|-----------|--------|-----------|
| 2025-01-01  | Laptop    | 55000  | 2         |
| 2025-01-02  | Keyboard  | 1200   | 4         |
| 2025-01-03  | Mouse     | 800    | 6         |
| 2025-01-04  | Monitor   | 15000  | 3         |

---

## 📊 Expected Output
Once the dashboard runs, you can access it at:
```
http://127.0.0.1:8050/
```
The dashboard includes:
- Interactive **bar charts** for product-wise sales.
- **Pie charts** showing category contributions.
- **Line charts** forecasting future sales.

---

## 🧮 Predictive Model
Uses **Linear Regression** from scikit-learn to predict future sales based on date and total revenue trends.

---

## 📚 Requirements
```
pandas
plotly
dash
scikit-learn
numpy
```

---

## 👨‍💻 Author
**Ganesh Masavale**  
📅 *Created in 2025*
