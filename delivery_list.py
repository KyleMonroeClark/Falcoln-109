import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import date
import sys

class delivery_list_Frame(tk.Frame):
    def get_file_path(self, csv_file):
        """ Determine the correct file path whether running as a script or executable """
        if getattr(sys, 'frozen', False):
            # Running as an executable (PyInstaller)
            return os.path.join(sys._MEIPASS, csv_file)
        else:
            # Running as a regular script (development mode)
            return os.path.join(os.path.dirname(__file__), csv_file)
        
    def __init__(self, parent, controller, csv_file="orders.csv"):
        super().__init__(parent)
        self.controller = controller
        self.csv_file = self.get_file_path(csv_file)
        self.orders = self.load_orders()

        # Title
        tk.Label(self, text="Delivery List", font=("Arial", 16)).pack(pady=10)

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

    def create_treeview(self):
        # Define the columns to be displayed
        columns = (
            "Order Number", "Marked Ordered", "Provider", "Patient Name",
            "Supplier", "Model", "Garment Type", "Side", "Quantity", "Other"
        )

        # Create a frame to hold both the Treeview and the Scrollbars
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True)

        # Create the Treeview widget
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        
        # Configure the columns and headings
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.W)
            self.tree.column(col, anchor=tk.W, width=120)

        # Add a vertical scrollbar for the Treeview
        tree_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        tree_scrollbar.pack(side="right", fill="y")

        # Pack the Treeview inside the tree_frame
        self.tree.pack(pady=10, expand=True, fill="both")

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

        # Filter orders based on selected filters and "Is Ordered" status
        filtered_orders = self.orders

        # Apply filter for "Is Ordered" status (only show orders that are not marked as ordered)
        filtered_orders = [
            order for order in filtered_orders 
            if not (order.get("Is Delivered") == True or str(order.get("Is Delivered", "")).lower() == "true") 
            and (order.get("Is Ordered") == True or str(order.get("Is Ordered", "")).lower() == "true") 
            and not (order.get("Deleted") is True or str(order.get("Deleted", "")).lower() == "true")
        ]


        if selected_supplier != "All":
            filtered_orders = [order for order in filtered_orders if order["Supplier"] == selected_supplier]

        if selected_delivery != "All":
            filtered_orders = [order for order in filtered_orders if order["Delivery Option"] == selected_delivery]

        if selected_provider != "All":
            filtered_orders = [order for order in filtered_orders if order["Provider"] == selected_provider]

        # Delete all existing rows from the treeview
        self.tree.delete(*self.tree.get_children())

        # Loop through all filtered orders and insert them into the treeview
        for order in filtered_orders:
            patient_name = f"{order['Patient First Name']} {order['Patient Last Name']}"
            if order['Size'] != "" and order['Length'] != "":
                size_length = f"{order['Size']}, {order['Length']}"
            elif order['Size'] != "" or order['Length'] != "":
                size_length = f"{order['Size']}{order['Length']}"
            else:
                size_length = "N/A"
            # Prepare the row values
            row_values = (
                order["Order Number"],
                order["Marked Ordered Date"],
                order["Provider"],
                patient_name,
                order["Supplier"],
                order["Model"],
                order["Garment Type"],
                order["Side"],
                order["Quantity"]
            )

            # Prepare the "Other" column (optional additional details)
            other_values = []
            if not size_length == "N/A":
                other_values.append(f"Size/ Legnth: {size_length}")
            if order["Body Location"]:
                other_values.append(f"Body Location: {order['Body Location']}")
            if not order["Color"] == "Color in Notes":
                other_values.append(f"Color: {order['Color']}")
            if order["Length"]:
                other_values.append(f"Length: {order['Length']}")
            if order["Strap"]:
                other_values.append(f"Strap: {order['Strap']}")
            if order["Toe"]:
                other_values.append(f"Toe: {order['Toe']}")
            if order["Notes"]:
                other_values.append(f"Notes: {order['Notes']}")

            # Join all the non-empty other values into a single string, separated by commas
            other_column_value = ", ".join(other_values) if other_values else ""

            # Add the "Other" column value to the row values
            row_values += (other_column_value,)

            # Insert the row into the treeview
            item = self.tree.insert("", tk.END, values=row_values)

            # If "Delivery Option" is "Drop Shipping", change the row text color to red
            if order["Delivery Option"] == "Drop Shipping":
                self.tree.item(item, tags=("drop_shipping",))

        # Apply tags for styling
        self.tree.tag_configure("drop_shipping", foreground="red")


    def create_buttons(self):
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Mark Delivered", command=self.mark_delivered, bg="green", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Examine Order", command=self.examine_order, bg="blue", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Back", command=lambda: self.controller.show_frame('main_menu'), bg="red", fg="white").pack(side=tk.LEFT, padx=5)

    def mark_delivered(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        selected_values = self.tree.item(selected_item, "values")
        order_number = selected_values[0]

        for order in self.orders:
            if order["Order Number"] == order_number:
                order["Is Delivered"] = "True"
                order["Marked Delivered Date"] = date.today().strftime("%Y-%m-%d")
                break

        self.save_orders()
        self.refresh_treeview()

    def examine_order(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        selected_values = self.tree.item(selected_item, "values")
        order_number = selected_values[0]
        patient_name = f"{selected_values[2]} {selected_values[3]}"

        # Find the order corresponding to the selected order number
        for order in self.orders:
            if order["Order Number"] == order_number:
                notes = order.get("Notes", "No notes available.")
                
                # Build the order details string, skipping blank values
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
                    ("Notes", notes),  # Include the Notes field as well
                    ("Delivery Option", order["Delivery Option"]),
                    ("Delivery Address 1", order["Delivery Address 1"]),
                    ("Delivery Address 2", order["Delivery Address 2"]),
                    ("City", order["City"]),
                    ("State", order["State"]),
                    ("Zip", order["Zip"])
                ]
                
                # Loop through each field, and add it to the order details if it's not blank
                for field_name, field_value in fields:
                    if field_value and field_value.strip():  # Skip empty values
                        order_details += f"{field_name}: {field_value}\n"
                
                # Display the final order details in a message box
                messagebox.showinfo(
                    title="Examine Order Details",
                    message=order_details
                )
                break
