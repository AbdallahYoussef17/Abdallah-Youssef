import pyodbc
import customtkinter
from tkinter import ttk


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


app = customtkinter.CTk()
app.geometry("900x530")
app.title("E_Commerce")


frame_container = customtkinter.CTkFrame(app)
frame_container.place(relx=.5, rely=0.5, anchor="center")


def clear_frame():
    for widget in frame_container.winfo_children():
        widget.destroy()


def insert_frame():
    clear_frame()
    dynamic_widgets = []

    def clear_widgets():
        for widget in dynamic_widgets:
            widget.destroy()
        dynamic_widgets.clear()

    def update_fields(event=None):
        clear_widgets()
        table_name = entry_table_name.get().strip()

        fields = []
        # Define fields based on the table name
        table_fields = {
            "Customer": [("First Name", "fname"), ("Last Name", "lname"), ("Address", "caddress"), ("Phone", "phone"), ("Email", "email")],
            "OrderCustomer": [("Customer ID", "CID"), ("Order Date", "orderDate"), ("Total Amount", "TotalAmount"), ("Order Status", "OrderStatus")],
            "category": [("Category Name", "CategoryName")],
            "OrderItem": [("Order ID", "Orderid"), ("Product ID", "productid"), ("Quantity", "Quantity"), ("Unit Price", "Unit_Price")],
            "product": [("Product Name", "Pname"), ("Category ID", "Categoryid"), ("Stock Quantity", "Stock_Quantity"), ("Price", "price")],
            "Payment": [("Order ID", "Ordid"), ("Payment Method", "PayMethod"), ("Payment Date", "PayDate"), ("Payment Status", "PayStatus")],
            "ShippingDetails": [("Order ID", "Ord_id"), ("Shipping Address", "SAddress"), ("Carrier", "Carrier"), ("Shipping Date", "ShippingDate"), ("Shipping Status", "ShippingStatus")],
        }

        if table_name in table_fields:
            fields = table_fields[table_name]
        #else:
            #info_label.configure(text="Invalid table name!", fg_color="red")
            #return

        # Create and place new entry fields
        for index, (placeholder, column) in enumerate(fields):
            y_position = 0.3 + (index * 0.08)
            entry = customtkinter.CTkEntry(frame_container, placeholder_text=placeholder, width=300)
            entry.place(relx=0.5, rely=y_position, anchor="center")
            dynamic_widgets.append((entry, column))

    def insert_data():
        try:
            connection = pyodbc.connect(
                'DRIVER={SQL Server};'
                'Server=DESKTOP-L2PQV4G;'
                'Database=E_Commerce;'
                'Trusted_Connection=yes;'
            )
            connection.autocommit = True
            cursor = connection.cursor()

            table_name = entry_table_name.get().strip()
            if not table_name:
                info_label.configure(text="Table name is required!", fg_color="red")
                return

            # Collect values and columns
            columns = [column for _, column in dynamic_widgets]
            values = [entry.get() for entry, _ in dynamic_widgets]

            if not all(values):
                info_label.configure(text="All fields must be filled!", fg_color="red")
                return

            # Build and execute the query
            placeholders = ", ".join("?" for _ in values)
            column_names = ", ".join(columns)
            query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
            cursor.execute(query, values)

            connection.commit()
            info_label.configure(text="Data inserted successfully!", fg_color="green")
        except pyodbc.Error as ex:
            info_label.configure(text=f"Error: {ex}", fg_color="red")

    # UI Elements
    label = customtkinter.CTkLabel(frame_container, text="Insert Data", font=("Arial", 20))
    label.place(relx=0.5, rely=0.1, anchor="center")

    entry_table_name = customtkinter.CTkEntry(frame_container, placeholder_text="Table Name", width=300)
    entry_table_name.place(relx=0.5, rely=0.2, anchor="center")
    entry_table_name.bind("<KeyRelease>", update_fields)

    insert_button = customtkinter.CTkButton(frame_container, text="Insert Data", command=insert_data, fg_color="green", width=150)
    insert_button.place(relx=0.5, rely=0.75, anchor="center")

    info_label = customtkinter.CTkLabel(frame_container, text="", font=("Arial", 12))
    info_label.place(relx=0.5, rely=0.85, anchor="center")

    back_button = customtkinter.CTkButton(frame_container, text="Back", command=main_frame, width=150)
    back_button.place(relx=0.5, rely=0.9, anchor="center")

def update_frame():
    clear_frame()

    # Title Label
    label = customtkinter.CTkLabel(frame_container, text="Update Data", font=("Arial", 20))
    label.place(relx=0.5, rely=0.1, anchor="center")

    # Dropdown for Table Name
    table_options = ("Customer", "OrderCustomer", "category", "OrderItem", "product", "Payment", "ShippingDetails")
    table_menu = customtkinter.CTkOptionMenu(frame_container, values=table_options)
    table_menu.place(relx=0.5, rely=0.2, anchor="center")

    # Entry for Column to Update
    entry_column = customtkinter.CTkEntry(frame_container, placeholder_text="Column to Update", width=300)
    entry_column.place(relx=0.5, rely=0.3, anchor="center")

    # Entry for New Value
    value_column = customtkinter.CTkEntry(frame_container, placeholder_text="New Value", width=300)
    value_column.place(relx=0.5, rely=0.4, anchor="center")

    # Entry for Condition Column
    entry_condition = customtkinter.CTkEntry(frame_container, placeholder_text="Condition Column", width=300)
    entry_condition.place(relx=0.5, rely=0.5, anchor="center")

    # Entry for Condition Value
    value_condition = customtkinter.CTkEntry(frame_container, placeholder_text="Condition Value", width=300)
    value_condition.place(relx=0.5, rely=0.6, anchor="center")

    # Function to Update Data
    def update_data():
        try:
            connection = pyodbc.connect(
                'DRIVER={SQL Server};'
                'Server=DESKTOP-L2PQV4G;'
                'Database=E_Commerce;'
                'Trusted_Connection=yes;'
            )
            connection.autocommit = True
            cursor = connection.cursor()

            # Execute Update Query
            cursor.execute(f"UPDATE {table_menu.get()} SET {entry_column.get()} = ? WHERE {entry_condition.get()} = ?",
                           (value_column.get(), value_condition.get()))
            connection.commit()
            info_label.configure(text="Data Updated Successfully!", fg_color="green")
        except pyodbc.Error as ex:
            info_label.configure(text=f"Failed to update: {ex}", fg_color="red")

    # Update Button
    update_button = customtkinter.CTkButton(frame_container, text="Update Data", command=update_data, fg_color="blue", width=150)
    update_button.place(relx=0.5, rely=0.7, anchor="center")

    # Info Label
    info_label = customtkinter.CTkLabel(frame_container, text="", font=("Arial", 12))
    info_label.place(relx=0.5, rely=0.8, anchor="center")

    # Back Button
    back_button = customtkinter.CTkButton(frame_container, text="Back", command=main_frame, width=150)
    back_button.place(relx=0.5, rely=0.9, anchor="center")


def delete_frame():
    clear_frame()

    # Title Label
    label = customtkinter.CTkLabel(frame_container, text="Delete Data", font=("Arial", 20))  
    label.place(relx=0.5, rely=0.1, anchor="center")

    # Dropdown for Table Name
    table_options = ("Customer", "OrderCustomer", "category", "OrderItem", "product", "Payment", "ShippingDetails")
    table_menu = customtkinter.CTkOptionMenu(frame_container, values=table_options)
    table_menu.place(relx=0.5, rely=0.2, anchor="center")

    # Entry for Condition Column
    entry_condition = customtkinter.CTkEntry(frame_container, placeholder_text="Condition Column", width=300)
    entry_condition.place(relx=0.5, rely=0.3, anchor="center")

    # Entry for Condition Value
    value_condition = customtkinter.CTkEntry(frame_container, placeholder_text="Condition Value", width=300)
    value_condition.place(relx=0.5, rely=0.4, anchor="center")

    # Function to Delete Data
    def delete_data():
        try:
            connection = pyodbc.connect(
                'DRIVER={SQL Server};'
                'Server=DESKTOP-L2PQV4G;'
                'Database=E_Commerce;'
                'Trusted_Connection=yes;'
            )
            connection.autocommit = True
            cursor = connection.cursor()

            # Execute Delete Query
            cursor.execute(f"DELETE FROM {table_menu.get()} WHERE {entry_condition.get()} = ?",
                           (value_condition.get(),))
            connection.commit()
            info_label.configure(text="Data Deleted Successfully!", fg_color="green")
        except pyodbc.Error as ex:
            info_label.configure(text=f"Failed to delete: {ex}", fg_color="red")

    # Delete Button
    delete_button = customtkinter.CTkButton(frame_container, text="Delete Data", command=delete_data, fg_color="red", width=150)
    delete_button.place(relx=0.5, rely=0.6, anchor="center")

    # Info Label
    info_label = customtkinter.CTkLabel(frame_container, text="", font=("Arial", 12))
    info_label.place(relx=0.5, rely=0.7, anchor="center")

    # Back Button
    back_button = customtkinter.CTkButton(frame_container, text="Back", command=main_frame, width=150)
    back_button.place(relx=0.5, rely=0.8, anchor="center")





def select_frame():
    clear_frame()
    label = customtkinter.CTkLabel(frame_container, text="Select Data", font=("Arial", 20))
    label.pack(pady=10)

    # Dropdown for table selection
    table_options = ("Customer", "OrderCustomer", "category", "OrderItem", "product", "Payment", "ShippingDetails")
    table_menu = customtkinter.CTkOptionMenu(frame_container, values=table_options)
    table_menu.pack(pady=5)

    # Entry for column name and value for filtering (optional)
    filter_frame = customtkinter.CTkFrame(frame_container)
    filter_frame.pack(pady=5)

    column_name_entry = customtkinter.CTkEntry(filter_frame, placeholder_text="Column Name (optional)", width=150)
    column_name_entry.pack(side="left", padx=5)

    column_value_entry = customtkinter.CTkEntry(filter_frame, placeholder_text="Value (optional)", width=150)
    column_value_entry.pack(side="left", padx=5)

    # Display Data in Table
    output_frame = customtkinter.CTkFrame(frame_container, height=300, width=800)
    output_frame.pack(pady=10)
    treeview = ttk.Treeview(output_frame, show='headings', height=10)
    treeview.pack(fill="both", expand=True)

    def select_data():
        table_name = table_menu.get()
        column_name = column_name_entry.get().strip()
        column_value = column_value_entry.get().strip()

        # Build the query string
        query = f"SELECT * FROM {table_name}"

        # Add filter based on column name and value (optional)
        if column_name and column_value:
            query += f" WHERE {column_name} = ?"  # Parameter placeholder without circular brackets

        try:
            connection = pyodbc.connect(
                'DRIVER={SQL Server};'
                'Server=DESKTOP-L2PQV4G;'
                'Database=E_Commerce;'
                'Trusted_Connection=yes;'
            )
            cursor = connection.cursor()

            # Execute query with parameters
            if column_name and column_value:
                cursor.execute(query, column_value)  # No parentheses around column_value
            else:
                cursor.execute(query)
            rows = cursor.fetchall()

            # Clear previous data
            treeview.delete(*treeview.get_children())

            # Fetch column names
            cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
            columns = [col[0] for col in cursor.fetchall()]

            # Configure treeview columns
            treeview["columns"] = columns
            for col in columns:
                treeview.heading(col, text=col)
            
            # Insert rows into treeview
            for row in rows:
                treeview.insert("", "end", values=[str(item).strip("(),'") for item in row])  # Remove extra brackets and quotes
        except pyodbc.Error as ex:
            print(f"Error: {ex}")

    select_button = customtkinter.CTkButton(frame_container, text="Select Data", command=select_data, width=420, height=70)  # Adjusted size
    select_button.pack(pady=10)

    back_button = customtkinter.CTkButton(frame_container, text="Back", command=main_frame, width=150)
    back_button.pack(pady=10)







def main_frame():
    clear_frame()
    label = customtkinter.CTkLabel(frame_container, text="Select Operation", font=("Arial", 20))
    label.pack(pady=10)

    insert_button = customtkinter.CTkButton(frame_container, text="Insert Data", command=insert_frame, width=720,height=70)
    insert_button.pack(pady=5)

    update_button = customtkinter.CTkButton(frame_container, text="Update Data", command=update_frame, width=720,height=70)
    update_button.pack(pady=5)

    delete_button = customtkinter.CTkButton(frame_container, text="Delete Data", command=delete_frame, width=720,height=70)
    delete_button.pack(pady=5)

    select_button = customtkinter.CTkButton(frame_container, text="Select Data", command=select_frame, width=720,height=70)
    select_button.pack(pady=5)

# Show the main frame initially
main_frame()
app.mainloop()
