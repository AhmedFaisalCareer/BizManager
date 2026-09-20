# 🏪 BizManager

**BizManager** is a small business management system built with **Python, Streamlit, SQLite, and Pandas**.

It helps small businesses manage products, inventory, customers, sales, reports, and invoices from one simple dashboard.

---

## 🌐 Live Demo

**Streamlit App:**
`https://bizmanager-3xb6kwahrpgnyhgjsedkus.streamlit.app/

> Replace the placeholder with your deployed Streamlit application URL.

---

## ✨ Features

### 📊 Business Dashboard

The dashboard provides a quick overview of business activity.

It displays:

* 💰 Total revenue
* 📈 Total profit
* 🛒 Number of orders
* 📦 Total products
* ⚠️ Low-stock products
* 🛒 Recent sales

The dashboard also highlights products that have reached their configured low-stock limit.

---

### 📦 Inventory Management

Manage your products from the inventory section.

You can:

* Add products
* View products
* Search products
* Edit product information
* Update stock
* Set low-stock limits
* Delete products

Each product stores:

* Product name
* Category
* Purchase price
* Selling price
* Stock quantity
* Low-stock limit
* Creation date

---

### 💰 New Sales

Create sales directly from the application.

The sales system supports:

* Product selection
* Customer selection
* Walk-in customers
* Quantity selection
* Payment method
* Automatic total calculation
* Expected profit calculation
* Automatic stock reduction

### 💳 Payment Methods

The application supports:

* Cash
* Card
* Bank Transfer
* Online Payment

When a sale is completed, the product stock is automatically reduced and the sale is stored in the database.

---

### 🧾 Sales History

View previously recorded sales in one place.

Sales history includes:

* Product
* Customer
* Quantity
* Selling price
* Total
* Profit
* Payment method
* Sale date

You can also search sales by:

* Product name
* Customer name

### 📥 Export Sales

Sales data can be exported as a CSV file.

---

### 👥 Customer Management

Manage customer information through the customer section.

You can:

* Add customers
* Search customers
* View customer information
* Delete customers

Customer records include:

* Name
* Phone
* Email
* Address
* Creation date

---

## 📈 Business Reports

The Reports section provides sales analytics for a selected date range.

### 📊 Available Metrics

* Revenue
* Profit
* Orders
* Units sold

### 📉 Sales Analytics

The application provides charts for:

* Sales over time
* Best-selling products
* Payment methods

Reports can also be downloaded as CSV files.

---

## 🧾 Invoice Generator

BizManager includes a basic invoice generator.

You can enter:

* Invoice number
* Business name
* Invoice date
* Customer name
* Customer phone
* Product
* Quantity
* Discount

The application automatically calculates:

```text
Subtotal
    ↓
Discount
    ↓
Final Total
```

The generated invoice includes:

* Business information
* Invoice number
* Date
* Customer information
* Product information
* Quantity
* Price
* Subtotal
* Discount
* Final total

The invoice can be downloaded as an HTML file.

---

## 🗄️ Database

BizManager uses **SQLite** for local data storage.

The database file is:

```text
business.db
```

### Database Tables

#### `products`

Stores inventory information:

* Product name
* Category
* Purchase price
* Selling price
* Stock
* Low-stock limit
* Creation date

#### `customers`

Stores customer information:

* Name
* Phone
* Email
* Address
* Creation date

#### `sales`

Stores sales transactions:

* Product
* Customer
* Quantity
* Selling price
* Purchase price
* Total
* Profit
* Payment method
* Sale date

---

## 🔄 Sales Workflow

```text
Add Product
     ↓
Add Customer
     ↓
Create Sale
     ↓
Stock Automatically Decreases
     ↓
Sale Saved in Database
     ↓
Dashboard Updated
     ↓
Reports Updated
```

---

## 📊 Profit Calculation

BizManager calculates profit automatically.

The basic calculation is:

```text
Profit = (Selling Price - Purchase Price) × Quantity
```

For example:

```text
Selling Price = Rs. 500
Purchase Price = Rs. 350
Quantity = 3

Profit = (500 - 350) × 3
       = Rs. 450
```

---

## ⚠️ Low Stock Management

Each product has a configurable low-stock limit.

For example:

```text
Stock: 4
Low Stock Limit: 5
```

The product will appear in the dashboard's **Low Stock Products** section.

This helps identify inventory that may need restocking.

---

## 🛠️ Technology Stack

| Technology | Purpose                                 |
| ---------- | --------------------------------------- |
| Python     | Application logic                       |
| Streamlit  | Web application interface               |
| SQLite     | Local database                          |
| Pandas     | Data processing and tables              |
| HTML/CSS   | Invoice and selected interface elements |

### Python Libraries

The application uses:

```text
streamlit
sqlite3
pandas
datetime
io
```

`sqlite3`, `datetime`, and `io` are part of Python's standard library.

---

## 📁 Project Structure

```text
BizManager/
│
├── app.py
├── requirements.txt
├── README.md
└── business.db
```

> `business.db` is created automatically when the application initializes the database.

---

## 📦 Requirements

The main external packages required by the application are:

```txt
streamlit
pandas
```

The complete `requirements.txt` can contain:

```txt
streamlit
pandas
```

---

## 🖥️ Application Navigation

The sidebar provides access to:

```text
🏪 BizManager
│
├── 📊 Dashboard
├── 📦 Inventory
├── 💰 New Sale
├── 🧾 Sales History
├── 👥 Customers
├── 📈 Reports
└── 🧾 Invoice
```

---

## 🎯 Who Is It For?

BizManager is designed as a simple management solution for small businesses that need to keep track of:

* Products
* Inventory
* Customers
* Sales
* Revenue
* Profit
* Reports
* Invoices

It can be adapted for different types of small businesses.

---

## 💡 Possible Use Cases

BizManager can be adapted for businesses such as:

* 🛍️ Retail shops
* 📱 Electronics stores
* 👕 Clothing stores
* 📚 Stationery shops
* 🧴 General stores
* 🧰 Small equipment businesses
* 🛒 Small e-commerce operations

---

## 🔮 Future Improvements

Possible future versions could include:

* Customer purchase history
* Product categories with filters
* Multiple products in a single invoice
* PDF invoice generation
* Stock purchase records
* Supplier management
* Expense tracking
* Employee management
* Monthly profit reports
* Sales forecasting
* User authentication
* Admin and staff accounts
* Cloud database
* Cloud backup
* Online deployment
* Mobile-friendly improvements

---

## 🎯 Project Goal

The goal of BizManager is to provide small businesses with a straightforward digital system for managing everyday business operations.

Instead of maintaining separate spreadsheets for products, customers, and sales, BizManager brings these core functions together in one Streamlit application.

---

## 👨‍💻 Developer

**Ahmed Dev Studio**

Building custom:

* 🐍 Python Applications
* 🌐 Web Applications
* 🚀 Streamlit Applications
* 📊 Business Dashboards
* 🤖 AI Applications
* ⚙️ Automation Solutions
* 🔗 API Integrations

---

# 🏪 BizManager

**Manage Products. Track Sales. Understand Your Business.**
