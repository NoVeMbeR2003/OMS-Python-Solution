
import tkinter as tk
from tkinter import ttk
from backend import get_total_orders , get_total_customers , get_total_product, get_sales_summary ,get_recent_order ,get_data_filter, get_filtered_orders , search_orders

# ---------- Main Window ----------
root = tk.Tk()
root.title("OMS | Admin Panel")
root.geometry("1200x720")
root.minsize(950, 600)
root.configure(bg="#F3F5F9")

# ---------- Colors ----------
SIDEBAR_COLOR = "#172238"
ACCENT_COLOR = "#3767E8"
BG_COLOR = "#F3F5F9"
CARD_COLOR = "#FFFFFF"
TEXT_COLOR = "#1E293B"
MUTED_COLOR = "#64748B"

# ---------- Layout ----------
sidebar = tk.Frame(root, bg=SIDEBAR_COLOR, width=220)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

main = tk.Frame(root, bg=BG_COLOR)
main.pack(side="left", fill="both", expand=True)

# ---------- Sidebar Header ----------
tk.Label(
    sidebar,
    text="OMS",
    font=("Segoe UI", 25, "bold"),
    fg="white",
    bg=SIDEBAR_COLOR
).pack(anchor="w", padx=25, pady=(28, 0))

tk.Label(
    sidebar,
    text="ADMIN PANEL",
    font=("Segoe UI", 9),
    fg="#AAB7CF",
    bg=SIDEBAR_COLOR
).pack(anchor="w", padx=27, pady=(0, 30))

# ---------- Main Content ----------
header = tk.Frame(main, bg=BG_COLOR)
header.pack(fill="x", padx=30, pady=(25, 15))

page_title = tk.Label(
    header,
    text="Dashboard",
    font=("Segoe UI", 23, "bold"),
    fg=TEXT_COLOR,
    bg=BG_COLOR
)
page_title.pack(side="left")

tk.Label(
    header,
    text="Order Management System",
    font=("Segoe UI", 10),
    fg=MUTED_COLOR,
    bg=BG_COLOR
).pack(side="right", pady=10)

content = tk.Frame(main, bg=BG_COLOR)
content.pack(fill="both", expand=True, padx=30, pady=10)


# ---------- Orders Page GUI ----------
def show_orders():
    # Page description
    tk.Label(
        content,
        text="Manage and explore customer orders",
        font=("Segoe UI", 11),
        fg=MUTED_COLOR,
        bg=BG_COLOR
    ).pack(anchor="w", pady=(0, 15))

    # ---------- Filters Card ----------
    filters = tk.Frame(
        content,
        bg=CARD_COLOR,
        highlightbackground="#E1E6EF",
        highlightthickness=1
    )
    filters.pack(fill="x", pady=(0, 15))

    tk.Label(
        filters,
        text="Filter Orders",
        font=("Segoe UI", 14, "bold"),
        fg=TEXT_COLOR,
        bg=CARD_COLOR
    ).grid(
        row=0, column=0, columnspan=4,
        sticky="w", padx=18, pady=(15, 12)
    )

    # ---------- Search Selection ----------
    tk.Label(
        filters,
        text="Order / Customer ID",
        font=("Segoe UI", 10),
        fg=MUTED_COLOR,
        bg=CARD_COLOR
    ).grid(row=1, column=0, sticky="w", padx=18)

    search_var = tk.StringVar()

    ttk.Entry(
        filters,
        textvariable=search_var,
        width=25
    ).grid(
        row=2, column=0,
        sticky="ew", padx=18, pady=(5, 15)
    )

    # ---------- Order Status ----------
    tk.Label(
        filters,
        text="Order Status",
        font=("Segoe UI", 10),
        fg=MUTED_COLOR,
        bg=CARD_COLOR
    ).grid(row=1, column=1, sticky="w", padx=10)

    order_status_var = tk.StringVar(value="All")

    ttk.Combobox(
        filters,
        textvariable=order_status_var,
        values=[
            "All",
            "Pending",
            "Processing",
            "Shipped",
            "Delivered",
            "Cancelled"
        ],
        state="readonly",
        width=18
    ).grid(
        row=2, column=1,
        sticky="ew", padx=10, pady=(5, 15)
    )

    # ---------- Payment Status ----------
    tk.Label(
        filters,
        text="Payment Status",
        font=("Segoe UI", 10),
        fg=MUTED_COLOR,
        bg=CARD_COLOR
    ).grid(row=1, column=2, sticky="w", padx=10)

    payment_status_var = tk.StringVar(value="All")

    ttk.Combobox(
        filters,
        textvariable=payment_status_var,
        values=[
            "All",
            "Paid",
            "Pending",
            "Failed",
            "Refunded"
        ],
        state="readonly",
        width=18
    ).grid(
        row=2, column=2,
        sticky="ew", padx=10, pady=(5, 15)
    )

    # ---------- Order Date ----------
    tk.Label(
        filters,
        text="Order Date",
        font=("Segoe UI", 10),
        fg=MUTED_COLOR,
        bg=CARD_COLOR
    ).grid(row=1, column=3, sticky="w", padx=10)

    date_filter_var = tk.StringVar(value="All Dates")

    date_filter_dropdown = ttk.Combobox(
        filters,
        textvariable=date_filter_var,
        values=[
            "All Dates",
            "Today",
            "Year 2025",
            "Year 2024",
            "Year 2023",
            "Custom Range"
        ],
        state="readonly",
        width=18
    )

    date_filter_dropdown.grid(
        row=2, column=3,
        sticky="ew", padx=10, pady=(5, 15)
    )

    # ---------- Custom Date Range Section ----------
    custom_date_frame = tk.LabelFrame(
        filters,
        text="Custom Order Date Range",
        font=("Segoe UI", 10, "bold"),
        fg=TEXT_COLOR,
        bg=CARD_COLOR,
        padx=10,
        pady=10
    )

    # Start Date
    tk.Label(
        custom_date_frame,
        text="Start Date (YYYY-MM-DD)",
        font=("Segoe UI", 9),
        fg=MUTED_COLOR,
        bg=CARD_COLOR
    ).grid(row=0, column=0, sticky="w", padx=8, pady=5)

    start_date_var = tk.StringVar()

    start_date_entry = ttk.Entry(
        custom_date_frame,
        textvariable=start_date_var,
        width=20
    )
    start_date_entry.grid(
        row=1, column=0,
        sticky="ew", padx=8, pady=(0, 5)
    )

    # End Date
    tk.Label(
        custom_date_frame,
        text="End Date (YYYY-MM-DD)",
        font=("Segoe UI", 9),
        fg=MUTED_COLOR,
        bg=CARD_COLOR
    ).grid(row=0, column=1, sticky="w", padx=8, pady=5)

    end_date_var = tk.StringVar()

    end_date_entry = ttk.Entry(
        custom_date_frame,
        textvariable=end_date_var,
        width=20
    )
    end_date_entry.grid(
        row=1, column=1,
        sticky="ew", padx=8, pady=(0, 5)
    )

    custom_date_frame.grid_columnconfigure(0, weight=1)
    custom_date_frame.grid_columnconfigure(1, weight=1)

    # Show or hide the custom date fields
    def toggle_custom_date(event=None):
        if date_filter_var.get() == "Custom Range":
            custom_date_frame.grid(
                row=3, column=0, columnspan=4,
                sticky="ew", padx=18, pady=(0, 12)
            )
        else:
            custom_date_frame.grid_remove()

    date_filter_dropdown.bind(
        "<<ComboboxSelected>>",
        toggle_custom_date
    )

    # ---------- Filter Buttons ----------
    filter_buttons = tk.Frame(filters, bg=CARD_COLOR)

    filter_buttons.grid(
        row=4, column=0, columnspan=4,
        sticky="e", padx=18, pady=(0, 15)
    )

    apply_button = tk.Button(
        filter_buttons,
        text="Apply Filters",
        font=("Segoe UI", 10, "bold"),
        bg=ACCENT_COLOR,
        fg="white",
        activebackground="#2853C7",
        activeforeground="white",
        relief="flat",
        padx=18,
        pady=8,
        cursor="hand2",
        command=None
    )
    apply_button.pack(side="left", padx=(0, 8))

    def reset_filters():
        search_var.set("")
        order_status_var.set("All")
        payment_status_var.set("All")
        date_filter_var.set("All Dates")
        start_date_var.set("")
        end_date_var.set("")
        custom_date_frame.grid_remove()

    reset_button = tk.Button(
        filter_buttons,
        text="Reset",
        font=("Segoe UI", 10),
        bg="#E9EDF5",
        fg=TEXT_COLOR,
        relief="flat",
        padx=18,
        pady=8,
        cursor="hand2",
        command=reset_filters
    )
    reset_button.pack(side="left")

    for column in range(4):
        filters.grid_columnconfigure(column, weight=1)

    # ---------- Orders Table Card ----------
    orders_card = tk.Frame(
        content,
        bg=CARD_COLOR,
        highlightbackground="#E1E6EF",
        highlightthickness=1
    )
    orders_card.pack(fill="both", expand=True)

    # Table heading
    table_header = tk.Frame(orders_card, bg=CARD_COLOR)
    table_header.pack(fill="x", padx=18, pady=15)

    tk.Label(
        table_header,
        text="Order Records",
        font=("Segoe UI", 15, "bold"),
        fg=TEXT_COLOR,
        bg=CARD_COLOR
    ).pack(side="left")

    results_label = tk.Label(
        table_header,
        text="Orders: —",
        font=("Segoe UI", 10),
        fg=MUTED_COLOR,
        bg=CARD_COLOR
    )
    results_label.pack(side="right")
   
   
   

    # ---------- Table and Scrollbar ----------
    table_frame = tk.Frame(orders_card, bg=CARD_COLOR)
    table_frame.pack(fill="both", expand=True, padx=18)

    columns = (
        "order_id",
        "customer_id",
        "order_date",
        "order_status",
        "payment_status"
    )

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=12
    )

    headings = {
        "order_id": "Order ID",
        "customer_id": "Customer ID",
        "order_date": "Order Date",
        "order_status": "Order Status",
        "payment_status": "Payment Status"
    }

    for column, heading in headings.items():
        table.heading(column, text=heading)
        table.column(column, width=150, anchor="w")

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=table.yview
    )

    table.configure(yscrollcommand=scrollbar.set)

    table.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ---------- Pagination Controls ----------
    pagination = tk.Frame(orders_card, bg=CARD_COLOR)
    pagination.pack(fill="x", padx=18, pady=15)

    page_label = tk.Label(
        pagination,
        text="Page — of —",
        font=("Segoe UI", 10),
        fg=MUTED_COLOR,
        bg=CARD_COLOR
    )
    page_label.pack(side="left")

    ttk.Button(
        pagination,
        text="Previous",
        command=lambda: None
    ).pack(side="right", padx=(8, 0))

    ttk.Button(
        pagination,
        text="Next",
        command=lambda: None
    ).pack(side="right")

    # ---------- GUI References ----------
    orders_gui = {
        "search": search_var,
        "order_status": order_status_var,
        "payment_status": payment_status_var,
        "date_filter": date_filter_var,
        "start_date": start_date_var,
        "end_date": end_date_var,
        "custom_date_frame": custom_date_frame,
        "table": table,
        "results_label": results_label,
        "page_label": page_label,
        "apply_button": apply_button,
        "reset_button": reset_button
    }
    def apply_order_date_filters():
    
     date_option= orders_gui["date_filter"].get()
     date_query=get_data_filter(date_option)

     orders=get_filtered_orders(date_query)
     table= orders_gui["table"]
     for order in orders:
        table.insert(
            "",
            "end",
            values=(
                order.get("order_id", ""),
                order.get("customer_id", ""),
                order.get("order_date", ""),
                order.get("order_status", ""),
                order.get("payment_status", "")
            )
        )

     orders_gui["results_label"].config(
        text=f"Orders: {len(orders)}"
     )
    apply_button.configure(command=apply_order_date_filters)     
    def search_order_records():
     search_text = orders_gui["search"].get().strip()

     orders = search_orders(search_text)

     print(orders)
    search_order_records()
    
    
    
    return orders_gui




# ---------- Page Navigation ----------
def show_page(page_name):
    page_title.config(text=page_name)

    for widget in content.winfo_children():
        widget.destroy()

    if page_name == "Dashboard":
        show_dashboard()
    elif page_name == "Orders":
        show_orders()    
    else:
        tk.Label(
            content,
            text=f"{page_name} page",
            font=("Segoe UI", 20, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(anchor="w", pady=10)

        tk.Label(
            content,
            text="Your backend and MongoDB queries will be connected here.",
            font=("Segoe UI", 11),
            bg=BG_COLOR,
            fg=MUTED_COLOR
        ).pack(anchor="w")

# ---------- Dashboard ----------
def show_dashboard():
    total_order=get_total_orders()
    total_customer=get_total_customers()
    total_product=get_total_product()
    total_revenue=get_sales_summary()
    stats = [
        ("Total Orders", f"{total_order:,}"),
        ("Customers", f"{total_customer}"),
        ("Products", f"{total_product}"),
        ("Total Revenue", f"{total_revenue}")
    ]

    cards = tk.Frame(content, bg=BG_COLOR)
    cards.pack(fill="x", pady=10)

    for title, value in stats:
        card = tk.Frame(
            cards,
            bg=CARD_COLOR,
            highlightbackground="#E1E6EF",
            highlightthickness=1
        )
        card.pack(side="left", fill="x", expand=True, padx=6)

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 10),
            fg=MUTED_COLOR,
            bg=CARD_COLOR
        ).pack(anchor="w", padx=18, pady=(18, 8))

        tk.Label(
            card,
            text=value,
            font=("Segoe UI", 23, "bold"),
            fg=ACCENT_COLOR,
            bg=CARD_COLOR
        ).pack(anchor="w", padx=18, pady=(0, 18))

    # Recent orders section
    recent = tk.Frame(
        content,
        bg=CARD_COLOR,
        highlightbackground="#E1E6EF",
        highlightthickness=1
    )
    recent.pack(fill="both", expand=True, pady=(20, 10))

    tk.Label(
        recent,
        text="Recent Orders",
        font=("Segoe UI", 15, "bold"),
        fg=TEXT_COLOR,
        bg=CARD_COLOR
    ).pack(anchor="w", padx=18, pady=15)

    columns = ("order_id", "customer_id", "status", "payment")

    table = ttk.Treeview(
        recent,
        columns=columns,
        show="headings",
        height=10
    )

    headings = {
        "order_id": "Order ID",
        "customer_id": "Customer ID",
        "status": "Order Status",
        "payment": "Payment Status"
    }

    for column, heading in headings.items():
        table.heading(column, text=heading)
        table.column(column, width=170, anchor="w")

    table.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    recent_orders = get_recent_order()

    for order in recent_orders:
      table.insert(
        "",
        "end",
        values=(
            order.get("order_id", ""),
            order.get("customer_id", ""),
            order.get("order_status", ""),
            order.get("payment_status", "")
        )
    )

# ---------- Sidebar Navigation ----------
pages = [
    "Dashboard",
    "Orders",
    "Customers",
    "Products",
    "Data Quality"
]

for page in pages:
    tk.Button(
        sidebar,
        text=f"   {page}",
        font=("Segoe UI", 11),
        fg="white",
        bg=SIDEBAR_COLOR,
        activebackground=ACCENT_COLOR,
        activeforeground="white",
        relief="flat",
        bd=0,
        anchor="w",
        padx=18,
        pady=12,
        cursor="hand2",
        command=lambda name=page: show_page(name)
    ).pack(fill="x", padx=10, pady=3)

# ---------- Initial Page ----------
show_page("Dashboard")

root.mainloop()
