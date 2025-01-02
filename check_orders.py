import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import date
from calendar import month_name

class check_orders_Frame(tk.Frame):
    def __init__(self, parent, controller, csv_file="orders.csv"):
        super().__init__(parent)
        self.controller = controller
        self.csv_file = csv_file
        self.orders = self.load_orders()

        # Title
        tk.Label(self, text="All Orders", font=("Arial", 16)).pack(pady=10)

        # Filters
        self.create_filters()

        # Treeview
        self.create_treeview()

        # Buttons
        self.create_buttons()

        # Initial load
        self.refresh_treeview()

    def load_orders(self):
        if not os.path.exists(self.csv_file):
            return []
        with open(self.csv_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return list(reader)

    def save_orders(self):
        with open(self.csv_file, "w", newline="", encoding="utf-8") as file:
            if not self.orders:
                return
            fieldnames = self.orders[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.orders)

    def create_filters(self):
        filter_frame = tk.Frame(self)
        filter_frame.pack(pady=5)

        # Supplier filter
        tk.Label(filter_frame, text="Supplier:").pack(side=tk.LEFT, padx=5)
        self.supplier_filter = ttk.Combobox(filter_frame, state="readonly")
        self.supplier_filter.pack(side=tk.LEFT, padx=5)

        suppliers = ["All"] + sorted(set(order["Supplier"] for order in self.orders))
        self.supplier_filter["values"] = suppliers
        self.supplier_filter.set("All")
        self.supplier_filter.bind("<<ComboboxSelected>>", lambda _: self.refresh_treeview())

        # Delivery Option filter
        tk.Label(filter_frame, text="Delivery Option:").pack(side=tk.LEFT, padx=5)
        self.delivery_filter = ttk.Combobox(filter_frame, state="readonly")
        self.delivery_filter.pack(side=tk.LEFT, padx=5)

        delivery_methods = ["All"] + sorted(set(order["Delivery Option"] for order in self.orders))
        self.delivery_filter["values"] = delivery_methods
        self.delivery_filter.set("All")
        self.delivery_filter.bind("<<ComboboxSelected>>", lambda _: self.refresh_treeview())

        # Provider filter
        tk.Label(filter_frame, text="Provider:").pack(side=tk.LEFT, padx=5)
        self.provider_filter = ttk.Combobox(filter_frame, state="readonly")
        self.provider_filter.pack(side=tk.LEFT, padx=5)

        providers = ["All"] + sorted(set(order["Provider"] for order in self.orders))
        self.provider_filter["values"] = providers
        self.provider_filter.set("All")
        self.provider_filter.bind("<<ComboboxSelected>>", lambda _: self.refresh_treeview())

        # Ordered Month filter
        tk.Label(filter_frame, text="Ordered Month:").pack(side=tk.LEFT, padx=5)
        self.month_filter = ttk.Combobox(filter_frame, state="readonly")
        self.month_filter.pack(side=tk.LEFT, padx=5)

        months = ["All"] + list(month_name[1:])  # All months + month names
        self.month_filter["values"] = months
        self.month_filter.set("All")
        self.month_filter.bind("<<ComboboxSelected>>", lambda _: self.refresh_treeview())

    def create_treeview(self):
        # Define the columns to be displayed
        columns = (
            "Order Number", "Patient Name", "Order Date", "Marked Ordered", "Marked Delivered"
        )

        # Create the Treeview widget
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=20)
        
        # Configure the columns and headings
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.W)
            self.tree.column(col, anchor=tk.W, width=120)

        self.tree.pack(pady=10)

        # Style for bold headers
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        
        # Insert data into the treeview
        self.refresh_treeview()

    def refresh_treeview(self):
        # Get the selected filter values
        selected_supplier = self.supplier_filter.get()
        selected_delivery = self.delivery_filter.get()
        selected_provider = self.provider_filter.get()
        selected_month = self.month_filter.get()

        # Filter orders based on selected filters
        filtered_orders = self.orders

        if selected_supplier != "All":
            filtered_orders = [order for order in filtered_orders if order["Supplier"] == selected_supplier]

        if selected_delivery != "All":
            filtered_orders = [order for order in filtered_orders if order["Delivery Option"] == selected_delivery]

        if selected_provider != "All":
            filtered_orders = [order for order in filtered_orders if order["Provider"] == selected_provider]

        if selected_month != "All":
            # Get the month number corresponding to the selected month
            month_number = str(list(month_name).index(selected_month)).zfill(2)
            
            # Filter orders by the selected month
            filtered_orders = [order for order in filtered_orders if order["Order Date"].split("-")[1] == month_number]

        # Sort the orders by Order Date (most recent first)
        filtered_orders.sort(key=lambda x: x["Order Date"], reverse=True)

        # Delete all existing rows from the treeview
        self.tree.delete(*self.tree.get_children())

        # Loop through all filtered orders and insert them into the treeview
        for order in filtered_orders:
            # Combine first and last name into a single column
            patient_name = f"{order['Patient First Name']} {order['Patient Last Name']}"
            row_values = (
                order["Order Number"],
                patient_name,
                order["Order Date"],
                order["Marked Ordered Date"],
                order["Marked Delivered Date"]
            )

                # Insert the row into the treeview and get the item ID
            item = self.tree.insert("", tk.END, values=row_values)

            # If "Delivery Option" is "Drop Shipping", change the row text color to red
            if order["Delivery Option"] == "Drop Shipping":
                # Apply the "drop_shipping" tag to this item
                self.tree.item(item, tags=("drop_shipping",))

            # Apply tags for styling (after all items have been inserted)
            self.tree.tag_configure("drop_shipping", foreground="red")


    def create_buttons(self):
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Examine Order", command=self.examine_order, bg="blue", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Back", command=lambda: self.controller.show_frame('main_menu'), bg="red", fg="white").pack(side=tk.LEFT, padx=5)

    def examine_order(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        selected_values = self.tree.item(selected_item, "values")
        order_number = selected_values[0]
        patient_name = f"{selected_values[1]}"

        # Find the order corresponding to the selected order number
        for order in self.orders:
            if order["Order Number"] == order_number:
                # Build the order details string, including blank values
                order_details = f"Order Number: {order_number}\nPatient Name: {patient_name}\n\n"
                
                # List of all the field names to display, in the order you want them shown
                fields = [
                    ("Order Date", order["Order Date"]),
                    ("Provider", order["Provider"]),
                    ("Patient First Name", order["Patient First Name"]),
                    ("Patient Last Name", order["Patient Last Name"]),
                    ("Date of Birth", order["Date of Birth"]),
                    ("Insurance", order["Insurance"]),
                    ("Supplier", order["Supplier"]),
                    ("Model", order["Model"]),
                    ("Garment Type", order["Garment Type"]),
                    ("Body Location", order["Body Location"]),
                    ("Compression Level", order["Compression Level"]),
                    ("Size", order["Size"]),
                    ("Length", order["Length"]),
                    ("Strap", order["Strap"]),
                    ("Toe", order["Toe"]),
                    ("Color", order["Color"]),
                    ("Side", order["Side"]),
                    ("Quantity", order["Quantity"]),
                    ("Notes", order.get("Notes", "")),
                    ("Delivery Option", order["Delivery Option"]),
                    ("Delivery Address 1", order["Delivery Address 1"]),
                    ("Delivery Address 2", order["Delivery Address 2"]),
                    ("City", order["City"]),
                    ("State", order["State"]),
                    ("Zip", order["Zip"]),
                    ("Marked Ordered Date", order["Marked Ordered Date"]),
                    ("Marked Delivered Date", order["Marked Delivered Date"])
                ]
                
                # Loop through each field, and add it to the order details
                for field_name, field_value in fields:
                    order_details += f"{field_name}: {field_value}\n"
                
                # Display the final order details in a message box
                messagebox.showinfo(
                    title="Examine Order Details",
                    message=order_details
                )
                break
