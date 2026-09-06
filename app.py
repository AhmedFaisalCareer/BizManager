import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date
import io

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="BizManager",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

[data-testid="stMetric"] {
    border: 1px solid #dddddd;
    padding: 15px;
    border-radius: 12px;
}

.stButton > button {
    border-radius: 8px;
}

h1, h2, h3 {
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DATABASE
# ============================================================

DB_NAME = "business.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_database():

    conn = get_connection()
    cursor = conn.cursor()

    # Products
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            purchase_price REAL NOT NULL,
            selling_price REAL NOT NULL,
            stock INTEGER NOT NULL,
            low_stock_limit INTEGER DEFAULT 5,
            created_at TEXT
        )
    """)

    # Customers
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            address TEXT,
            created_at TEXT
        )
    """)

    # Sales
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            customer_id INTEGER,
            quantity INTEGER,
            selling_price REAL,
            purchase_price REAL,
            total REAL,
            profit REAL,
            payment_method TEXT,
            sale_date TEXT,
            FOREIGN KEY(product_id) REFERENCES products(id),
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        )
    """)

    conn.commit()
    conn.close()


init_database()


# ============================================================
# DATABASE HELPERS
# ============================================================

def add_product(
    name,
    category,
    purchase_price,
    selling_price,
    stock,
    low_stock_limit
):

    conn = get_connection()

    conn.execute("""
        INSERT INTO products
        (name, category, purchase_price, selling_price,
         stock, low_stock_limit, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        category,
        purchase_price,
        selling_price,
        stock,
        low_stock_limit,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_products():

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM products ORDER BY id DESC",
        conn
    )

    conn.close()

    return df


def update_product(
    product_id,
    name,
    category,
    purchase_price,
    selling_price,
    stock,
    low_stock_limit
):

    conn = get_connection()

    conn.execute("""
        UPDATE products
        SET name=?,
            category=?,
            purchase_price=?,
            selling_price=?,
            stock=?,
            low_stock_limit=?
        WHERE id=?
    """, (
        name,
        category,
        purchase_price,
        selling_price,
        stock,
        low_stock_limit,
        product_id
    ))

    conn.commit()
    conn.close()


def delete_product(product_id):

    conn = get_connection()

    conn.execute(
        "DELETE FROM products WHERE id=?",
        (product_id,)
    )

    conn.commit()
    conn.close()


def add_customer(name, phone, email, address):

    conn = get_connection()

    conn.execute("""
        INSERT INTO customers
        (name, phone, email, address, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        name,
        phone,
        email,
        address,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_customers():

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM customers ORDER BY id DESC",
        conn
    )

    conn.close()

    return df


def delete_customer(customer_id):

    conn = get_connection()

    conn.execute(
        "DELETE FROM customers WHERE id=?",
        (customer_id,)
    )

    conn.commit()
    conn.close()


def make_sale(
    product_id,
    customer_id,
    quantity,
    payment_method
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT purchase_price, selling_price, stock, name "
        "FROM products WHERE id=?",
        (product_id,)
    )

    product = cursor.fetchone()

    if not product:
        conn.close()
        return False, "Product not found."

    purchase_price = product[0]
    selling_price = product[1]
    stock = product[2]
    product_name = product[3]

    if quantity > stock:
        conn.close()
        return False, f"Only {stock} units available."

    total = selling_price * quantity
    profit = (selling_price - purchase_price) * quantity

    # Reduce stock
    cursor.execute("""
        UPDATE products
        SET stock = stock - ?
        WHERE id=?
    """, (
        quantity,
        product_id
    ))

    # Add sale
    cursor.execute("""
        INSERT INTO sales
        (
            product_id,
            customer_id,
            quantity,
            selling_price,
            purchase_price,
            total,
            profit,
            payment_method,
            sale_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        product_id,
        customer_id,
        quantity,
        selling_price,
        purchase_price,
        total,
        profit,
        payment_method,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return True, f"{product_name} sale recorded successfully."


def get_sales():

    conn = get_connection()

    df = pd.read_sql_query("""
        SELECT
            sales.id,
            products.name AS product,
            customers.name AS customer,
            sales.quantity,
            sales.selling_price,
            sales.total,
            sales.profit,
            sales.payment_method,
            sales.sale_date
        FROM sales
        LEFT JOIN products
            ON sales.product_id = products.id
        LEFT JOIN customers
            ON sales.customer_id = customers.id
        ORDER BY sales.id DESC
    """, conn)

    conn.close()

    return df


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🏪 BizManager")
st.sidebar.caption("Small Business Management System")

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Dashboard",
        "📦 Inventory",
        "💰 New Sale",
        "🧾 Sales History",
        "👥 Customers",
        "📈 Reports",
        "🧾 Invoice"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "Built with Python + Streamlit + SQLite"
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "📊 Dashboard":

    st.title("📊 Business Dashboard")
    st.caption("Overview of your business")

    products = get_products()
    customers = get_customers()
    sales = get_sales()

    total_products = len(products)
    total_customers = len(customers)

    if len(sales) > 0:
        total_sales = sales["total"].sum()
        total_profit = sales["profit"].sum()
        total_orders = len(sales)
    else:
        total_sales = 0
        total_profit = 0
        total_orders = 0

    low_stock = 0

    if len(products) > 0:
        low_stock = len(
            products[
                products["stock"] <= products["low_stock_limit"]
            ]
        )

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "💰 Revenue",
        f"Rs. {total_sales:,.0f}"
    )

    col2.metric(
        "📈 Profit",
        f"Rs. {total_profit:,.0f}"
    )

    col3.metric(
        "🛒 Orders",
        total_orders
    )

    col4.metric(
        "📦 Products",
        total_products
    )

    col5.metric(
        "⚠️ Low Stock",
        low_stock
    )

    st.divider()

    # Low stock
    if low_stock > 0:

        st.subheader("⚠️ Low Stock Products")

        low_stock_df = products[
            products["stock"] <= products["low_stock_limit"]
        ]

        st.dataframe(
            low_stock_df[
                [
                    "name",
                    "category",
                    "stock",
                    "low_stock_limit"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success("✅ No products are currently low on stock.")

    st.divider()

    # Recent sales
    st.subheader("🛒 Recent Sales")

    if len(sales) > 0:

        st.dataframe(
            sales.head(10),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No sales have been recorded yet.")


# ============================================================
# INVENTORY
# ============================================================

elif page == "📦 Inventory":

    st.title("📦 Inventory Management")

    tab1, tab2 = st.tabs([
        "➕ Add Product",
        "📋 Manage Products"
    ])

    # --------------------------------------------------------
    # ADD PRODUCT
    # --------------------------------------------------------

    with tab1:

        st.subheader("Add New Product")

        with st.form("add_product_form"):

            col1, col2 = st.columns(2)

            with col1:

                name = st.text_input(
                    "Product Name"
                )

                category = st.text_input(
                    "Category"
                )

                purchase_price = st.number_input(
                    "Purchase Price",
                    min_value=0.0,
                    step=10.0
                )

            with col2:

                selling_price = st.number_input(
                    "Selling Price",
                    min_value=0.0,
                    step=10.0
                )

                stock = st.number_input(
                    "Stock Quantity",
                    min_value=0,
                    step=1
                )

                low_stock_limit = st.number_input(
                    "Low Stock Alert",
                    min_value=0,
                    value=5,
                    step=1
                )

            submitted = st.form_submit_button(
                "➕ Add Product",
                use_container_width=True
            )

            if submitted:

                if not name.strip():

                    st.error("Product name is required.")

                elif selling_price < purchase_price:

                    st.warning(
                        "Selling price is lower than purchase price."
                    )

                else:

                    add_product(
                        name,
                        category,
                        purchase_price,
                        selling_price,
                        stock,
                        low_stock_limit
                    )

                    st.success(
                        f"{name} added successfully!"
                    )

                    st.rerun()

    # --------------------------------------------------------
    # MANAGE PRODUCTS
    # --------------------------------------------------------

    with tab2:

        products = get_products()

        if len(products) == 0:

            st.info("No products available.")

        else:

            search = st.text_input(
                "🔍 Search products"
            )

            if search:

                filtered = products[
                    products["name"]
                    .str.contains(
                        search,
                        case=False,
                        na=False
                    )
                ]

            else:

                filtered = products

            st.dataframe(
                filtered[
                    [
                        "id",
                        "name",
                        "category",
                        "purchase_price",
                        "selling_price",
                        "stock",
                        "low_stock_limit"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            st.subheader("✏️ Edit Product")

            product_ids = products["id"].tolist()

            selected_id = st.selectbox(
                "Select Product",
                product_ids
            )

            selected = products[
                products["id"] == selected_id
            ].iloc[0]

            with st.form("edit_product"):

                col1, col2 = st.columns(2)

                with col1:

                    edit_name = st.text_input(
                        "Product Name",
                        value=selected["name"]
                    )

                    edit_category = st.text_input(
                        "Category",
                        value=selected["category"]
                        if pd.notna(selected["category"])
                        else ""
                    )

                    edit_purchase = st.number_input(
                        "Purchase Price",
                        value=float(
                            selected["purchase_price"]
                        )
                    )

                with col2:

                    edit_selling = st.number_input(
                        "Selling Price",
                        value=float(
                            selected["selling_price"]
                        )
                    )

                    edit_stock = st.number_input(
                        "Stock",
                        min_value=0,
                        value=int(
                            selected["stock"]
                        )
                    )

                    edit_limit = st.number_input(
                        "Low Stock Limit",
                        min_value=0,
                        value=int(
                            selected["low_stock_limit"]
                        )
                    )

                save = st.form_submit_button(
                    "💾 Save Changes",
                    use_container_width=True
                )

                if save:

                    update_product(
                        selected_id,
                        edit_name,
                        edit_category,
                        edit_purchase,
                        edit_selling,
                        edit_stock,
                        edit_limit
                    )

                    st.success(
                        "Product updated successfully."
                    )

                    st.rerun()

            if st.button(
                "🗑️ Delete Selected Product"
            ):

                delete_product(selected_id)

                st.success(
                    "Product deleted."
                )

                st.rerun()


# ============================================================
# NEW SALE
# ============================================================

elif page == "💰 New Sale":

    st.title("💰 Create New Sale")

    products = get_products()
    customers = get_customers()

    if len(products) == 0:

        st.warning(
            "Add products to inventory before making a sale."
        )

    else:

        product_names = products["name"].tolist()

        selected_product_name = st.selectbox(
            "Select Product",
            product_names
        )

        selected_product = products[
            products["name"] == selected_product_name
        ].iloc[0]

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**Selling Price:** Rs. "
                f"{selected_product['selling_price']:,.2f}"
            )

            st.write(
                f"**Available Stock:** "
                f"{selected_product['stock']}"
            )

        with col2:

            st.write(
                f"**Category:** "
                f"{selected_product['category']}"
            )

        st.divider()

        customer_options = ["Walk-in Customer"]

        customer_map = {
            "Walk-in Customer": None
        }

        for _, customer in customers.iterrows():

            label = (
                f"{customer['name']} "
                f"({customer['phone']})"
            )

            customer_options.append(label)

            customer_map[label] = int(
                customer["id"]
            )

        customer = st.selectbox(
            "Customer",
            customer_options
        )

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            max_value=max(
                1,
                int(selected_product["stock"])
            ),
            value=1
        )

        payment = st.selectbox(
            "Payment Method",
            [
                "Cash",
                "Card",
                "Bank Transfer",
                "Online Payment"
            ]
        )

        total = (
            selected_product["selling_price"]
            * quantity
        )

        profit = (
            selected_product["selling_price"]
            - selected_product["purchase_price"]
        ) * quantity

        st.divider()

        col1, col2 = st.columns(2)

        col1.metric(
            "Total",
            f"Rs. {total:,.2f}"
        )

        col2.metric(
            "Expected Profit",
            f"Rs. {profit:,.2f}"
        )

        if st.button(
            "✅ Complete Sale",
            use_container_width=True
        ):

            success, message = make_sale(
                int(selected_product["id"]),
                customer_map[customer],
                quantity,
                payment
            )

            if success:

                st.success(message)

                st.balloons()

            else:

                st.error(message)


# ============================================================
# SALES HISTORY
# ============================================================

elif page == "🧾 Sales History":

    st.title("🧾 Sales History")

    sales = get_sales()

    if len(sales) == 0:

        st.info("No sales recorded.")

    else:

        search = st.text_input(
            "🔍 Search by product or customer"
        )

        if search:

            sales = sales[
                sales["product"]
                .fillna("")
                .str.contains(
                    search,
                    case=False
                )
                |
                sales["customer"]
                .fillna("")
                .str.contains(
                    search,
                    case=False
                )
            ]

        st.dataframe(
            sales,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader("📥 Export Sales")

        csv = sales.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "Download Sales CSV",
            csv,
            "sales_report.csv",
            "text/csv"
        )


# ============================================================
# CUSTOMERS
# ============================================================

elif page == "👥 Customers":

    st.title("👥 Customer Management")

    tab1, tab2 = st.tabs([
        "➕ Add Customer",
        "📋 Customers"
    ])

    # --------------------------------------------------------
    # ADD CUSTOMER
    # --------------------------------------------------------

    with tab1:

        with st.form("customer_form"):

            name = st.text_input(
                "Customer Name"
            )

            phone = st.text_input(
                "Phone"
            )

            email = st.text_input(
                "Email"
            )

            address = st.text_area(
                "Address"
            )

            submit = st.form_submit_button(
                "➕ Add Customer",
                use_container_width=True
            )

            if submit:

                if not name.strip():

                    st.error(
                        "Customer name is required."
                    )

                else:

                    add_customer(
                        name,
                        phone,
                        email,
                        address
                    )

                    st.success(
                        "Customer added successfully!"
                    )

                    st.rerun()

    # --------------------------------------------------------
    # CUSTOMER LIST
    # --------------------------------------------------------

    with tab2:

        customers = get_customers()

        if len(customers) == 0:

            st.info(
                "No customers registered."
            )

        else:

            search = st.text_input(
                "🔍 Search customers"
            )

            if search:

                filtered = customers[
                    customers["name"]
                    .str.contains(
                        search,
                        case=False,
                        na=False
                    )
                    |
                    customers["phone"]
                    .fillna("")
                    .str.contains(
                        search,
                        case=False,
                        na=False
                    )
                ]

            else:

                filtered = customers

            st.dataframe(
                filtered[
                    [
                        "id",
                        "name",
                        "phone",
                        "email",
                        "address"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            customer_id = st.selectbox(
                "Select customer to delete",
                customers["id"].tolist()
            )

            if st.button(
                "🗑️ Delete Customer"
            ):

                delete_customer(
                    customer_id
                )

                st.success(
                    "Customer deleted."
                )

                st.rerun()


# ============================================================
# REPORTS
# ============================================================

elif page == "📈 Reports":

    st.title("📈 Business Reports")

    sales = get_sales()

    if len(sales) == 0:

        st.info(
            "You need sales data to generate reports."
        )

    else:

        sales["sale_date"] = pd.to_datetime(
            sales["sale_date"]
        )

        # ----------------------------------------------------
        # DATE FILTER
        # ----------------------------------------------------

        min_date = sales["sale_date"].dt.date.min()
        max_date = sales["sale_date"].dt.date.max()

        start_date = st.date_input(
            "Start Date",
            min_date
        )

        end_date = st.date_input(
            "End Date",
            max_date
        )

        filtered = sales[
            (
                sales["sale_date"].dt.date
                >= start_date
            )
            &
            (
                sales["sale_date"].dt.date
                <= end_date
            )
        ]

        st.divider()

        revenue = filtered["total"].sum()
        profit = filtered["profit"].sum()
        orders = len(filtered)
        units = filtered["quantity"].sum()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Revenue",
            f"Rs. {revenue:,.0f}"
        )

        col2.metric(
            "Profit",
            f"Rs. {profit:,.0f}"
        )

        col3.metric(
            "Orders",
            orders
        )

        col4.metric(
            "Units Sold",
            units
        )

        st.divider()

        # ----------------------------------------------------
        # DAILY SALES
        # ----------------------------------------------------

        st.subheader("📊 Sales Over Time")

        daily = (
            filtered
            .groupby(
                filtered["sale_date"].dt.date
            )["total"]
            .sum()
        )

        if len(daily) > 0:

            st.line_chart(daily)

        # ----------------------------------------------------
        # BEST SELLING PRODUCTS
        # ----------------------------------------------------

        st.subheader("🏆 Best-Selling Products")

        best_products = (
            filtered
            .groupby("product")["quantity"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        st.bar_chart(best_products)

        # ----------------------------------------------------
        # PAYMENT METHODS
        # ----------------------------------------------------

        st.subheader("💳 Payment Methods")

        payment_data = (
            filtered
            .groupby(
                "payment_method"
            )["total"]
            .sum()
        )

        st.bar_chart(payment_data)

        # ----------------------------------------------------
        # EXPORT
        # ----------------------------------------------------

        st.divider()

        csv = filtered.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "📥 Download Report",
            csv,
            "business_report.csv",
            "text/csv"
        )


# ============================================================
# INVOICE
# ============================================================

elif page == "🧾 Invoice":

    st.title("🧾 Invoice Generator")

    products = get_products()
    customers = get_customers()

    if len(products) == 0:

        st.warning(
            "Add products before generating an invoice."
        )

    else:

        invoice_number = st.text_input(
            "Invoice Number",
            value=f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )

        col1, col2 = st.columns(2)

        with col1:

            business_name = st.text_input(
                "Business Name",
                value="My Business"
            )

        with col2:

            invoice_date = st.date_input(
                "Invoice Date",
                date.today()
            )

        st.divider()

        customer_name = st.text_input(
            "Customer Name"
        )

        customer_phone = st.text_input(
            "Customer Phone"
        )

        st.divider()

        st.subheader("Products")

        product_names = products["name"].tolist()

        selected = st.selectbox(
            "Product",
            product_names
        )

        product = products[
            products["name"] == selected
        ].iloc[0]

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1
        )

        price = float(
            product["selling_price"]
        )

        subtotal = price * quantity

        discount = st.number_input(
            "Discount",
            min_value=0.0,
            value=0.0
        )

        total = max(
            0,
            subtotal - discount
        )

        st.divider()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Subtotal",
            f"Rs. {subtotal:,.2f}"
        )

        col2.metric(
            "Discount",
            f"Rs. {discount:,.2f}"
        )

        col3.metric(
            "Total",
            f"Rs. {total:,.2f}"
        )

        if st.button(
            "🧾 Generate Invoice",
            use_container_width=True
        ):

            invoice_html = f"""
            <html>
            <head>
            <style>

            body {{
                font-family: Arial;
                padding: 40px;
            }}

            .header {{
                display: flex;
                justify-content: space-between;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 30px;
            }}

            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}

            .total {{
                text-align: right;
                margin-top: 30px;
                font-size: 22px;
                font-weight: bold;
            }}

            </style>
            </head>

            <body>

            <div class="header">

            <div>
                <h1>{business_name}</h1>
                <p>Business Invoice</p>
            </div>

            <div>
                <b>Invoice:</b> {invoice_number}<br>
                <b>Date:</b> {invoice_date}
            </div>

            </div>

            <hr>

            <h3>Customer</h3>

            <p>
            Name: {customer_name}<br>
            Phone: {customer_phone}
            </p>

            <table>

            <tr>
                <th>Product</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Total</th>
            </tr>

            <tr>
                <td>{selected}</td>
                <td>{quantity}</td>
                <td>Rs. {price:,.2f}</td>
                <td>Rs. {subtotal:,.2f}</td>
            </tr>

            </table>

            <div class="total">

            Subtotal: Rs. {subtotal:,.2f}<br>
            Discount: Rs. {discount:,.2f}<br>
            Total: Rs. {total:,.2f}

            </div>

            <hr>

            <p>
            Thank you for your business!
            </p>

            </body>
            </html>
            """

            st.success(
                "Invoice generated!"
            )

            st.components.v1.html(
                invoice_html,
                height=600,
                scrolling=True
            )

            st.download_button(
                "📥 Download Invoice HTML",
                invoice_html,
                f"{invoice_number}.html",
                "text/html"
            )