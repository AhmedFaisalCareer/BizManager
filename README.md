🏪 BizManager — Small Business Management Dashboard

A simple and professional Small Business Management Dashboard built with Python, Streamlit, SQLite, and Pandas.

BizManager helps small businesses manage products, inventory, sales, customers, invoices, and business reports from one dashboard.

✨ Features

📊 Dashboard

Total revenue

Total profit

Number of orders

Total products

Low-stock alerts

Recent sales

📦 Inventory Management

Add products

Edit products

Delete products

Product categories

Purchase and selling prices

Stock quantity

Custom low-stock limit

Product search

💰 Sales Management

Create new sales

Select products and customers

Automatic total calculation

Automatic profit calculation

Multiple payment methods

Automatic stock reduction

🧾 Sales History

View previous sales

Search sales by product or customer

Export sales data as CSV

👥 Customer Management

Add customers

Store phone, email, and address

Search customers

Delete customers

📈 Reports

Filter sales by date

Revenue and profit summaries

Sales-over-time chart

Best-selling products

Payment method analysis

Download reports as CSV

🧾 Invoice Generator

Generate invoice numbers

Add business and customer information

Select products and quantities

Add discounts

Automatic subtotal and total calculation

Display a professional invoice

Download invoice as HTML

🛠️ Technologies Used

Python

Streamlit

SQLite

Pandas

HTML/CSS

No AI or external AI APIs are required.

📁 Project Structure

BizManager/
│
├── app.py
├── requirements.txt
├── README.md
└── business.db          # Created automatically when the app runs

⚙️ Installation

1. Clone the repository

git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY

2. Create a virtual environment (recommended)

Windows:

python -m venv venv
venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Run the application

streamlit run app.py

The application will open in your browser.

🗄️ Database

BizManager uses SQLite for local data storage.

The database file:

business.db

is created automatically when the application starts.

The database stores:

Products

Customers

Sales

💡 Example Use Case

A small electronics shop can use BizManager to:

Add products such as laptops, keyboards, and mice.

Set purchase and selling prices.

Track available stock.

Add customers.

Record sales.

Automatically calculate revenue and profit.

Monitor low-stock products.

Generate invoices.

View business reports.

Export sales information.

🔐 Important Note

This project is designed as a local/demo business management application.

Before using it for a real business with sensitive or important data, consider adding:

User authentication

Database backups

Data validation

Role-based permissions

Secure deployment

PDF invoice generation

Cloud database support

🚀 Future Improvements

Possible future features:

🔐 Login and user accounts

🏢 Business profile/settings

🧾 Multi-product invoices

📄 PDF invoice generation

💸 Expense management

🚚 Supplier management

👨‍💼 Employee management

📦 Purchase orders

💾 Database backup/restore

📊 Advanced profit/loss reports

☁️ Cloud database

📱 Better mobile layout

👨‍💻 Author

Ahmed Faisal

Built as a Python and Streamlit business-management project.

📄 License

This project is available for learning and personal use. You can modify it for your own projects.
