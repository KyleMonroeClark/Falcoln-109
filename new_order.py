import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime
import csv
import os
import sys

class new_order_Frame(tk.Frame):

    def reset_form(self):
        # Reset combo boxes to their default value (first item or empty string)
        for label, widget in self.variable_widgets:
            if isinstance(widget, ttk.Combobox):
                widget.set('')  # Reset to empty string or default value
        
        # Reset Entry widgets to empty string
        for label, widget in self.variable_widgets:
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)  # Clear the text entry

        # Reset Text widgets to empty text
        for label, widget in self.variable_widgets:
            if isinstance(widget, tk.Text):
                widget.delete(1.0, tk.END)  # Clear the text box

        # Reset the boolean checkbox to False
        self.home_delivery_var.set(False)  # Reset checkbox to unchecked

        # Reset the date fields to the default empty value (you can set a default date if needed)
        self.order_date.set_date(datetime.datetime.now().date())
        self.month_var.set("Month")
        self.date_var.set("Date")
        self.year_var.set("Year")

        # Reset other individual widgets like labels, comboboxes, etc., if needed
        # Reset insurance, supplier, provider, etc. to empty or default value
        self.patient_first_name.delete(0, tk.END)
        self.patient_last_name.delete(0, tk.END)
        self.provider.set('')
        self.insurance.set('')
        self.supplier.set('')
        self.model.delete(0, tk.END)

        # Reset garment type to empty or default value
        self.garment_type.set('')
        
        # Reset birthdate fields
        self.month_var.set("Month")
        self.date_var.set("Date")
        self.year_var.set("Year")


    def update_variable_widgets(self, event=None):
        # Hide all widgets and labels initially
        self.bg_color = self.controller.root.cget('bg')
        for label, widget in self.variable_widgets:

            # Reset the value of each widget
            if isinstance(widget, ttk.Combobox):
                widget.set("")
            elif isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)  # Clear the entry widget
            elif isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)  # Clear the text widget
            elif isinstance(widget, tk.Checkbutton):
                widget.deselect()  # Deselect the checkbutton
            elif isinstance(widget, tk.Spinbox):
                widget.delete(0, tk.END)  # Clear the spinbox widget
                widget.insert(0, "0")  # Reset to default value (if applicable)

            label.grid_forget()
            widget.grid_forget()

        # Get the selected garment type from the combobox
        selected_garment_type = self.garment_type.get()

        # Check if the selected garment type exists in the dictionary
        if selected_garment_type in self.garment_type_widgets:
            # Get the widget list for the selected garment type (using the widget names from the dictionary)
            widget_names = self.garment_type_widgets[selected_garment_type]
            self.variable_widgets = []

            # Create and display the widgets based on the selected garment type
            row = 11
            for widget_name in widget_names:
                label_text = widget_name.replace("_", " ").capitalize()

                # Create the label for the widget
                label = tk.Label(self.form_frame, text=label_text, bg=self.bg_color)
                label.grid(row=row, column=0, sticky="e", padx=10, pady=5)

                # Get the widget reference from self (e.g., self.body_location, self.compression_level)
                widget = getattr(self, widget_name)
                widget.grid(row=row, column=1, sticky="ew", pady=10, padx=10)

                # Add the label and widget to the list for future reference
                self.variable_widgets.append((label, widget))

                # Increment row for the next widget
                row += 1

    def update_scroll_region(self, event=None):
        """Update the scroll region to match the size of the content inside the canvas."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def __init__(self, parent, controller):
        # Setup
        bg_color = controller.root.cget('bg')  # Get the background color of the main window
        super().__init__(parent, bg=bg_color)  # Set the frame background to match the main window's background
        self.controller = controller
        self.pack(fill="both", expand=True)  # Make the frame fill the entire window
        self.variable_widgets = []

        # Create a frame for the form (still uses dynamic background color)
        self.form_frame = tk.Frame(self, bg=bg_color)
        self.form_frame.pack(fill="both", expand=True, padx=20, pady=20)

        def toggle_address_fields():

            if self.home_delivery_var.get() is True:

                self.address1_label.grid(row=94, column=0, sticky="ew",padx=10,pady=5)
                self.address1.grid(row=94, column=1, sticky="ew",padx=10,pady=10)

                self.address2_label.grid(row=95, column=0, sticky="ew",padx=10,pady=5)
                self.address2.grid(row=95, column=1, sticky="ew",padx=10,pady=10)

                self.city_label.grid(row=96, column=0, sticky="ew",padx=10,pady=5)
                self.city.grid(row=96, column=1, sticky="ew",padx=10,pady=10)

                self.state_label.grid(row=97, column=0, sticky="ew",padx=10,pady=5)
                self.state.grid(row=97, column=1, sticky="ew",padx=10,pady=10)    

                self.zip_label.grid(row=98, column=0, sticky="ew",padx=10,pady=5)
                self.zip.grid(row=98, column=1, sticky="ew",padx=10,pady=10)

            else:

                self.address1_label.grid_forget()
                self.address1.delete(0, tk.END)
                self.address1.grid_forget()

                self.address2_label.grid_forget()
                self.address2.delete(0, tk.END)
                self.address2.grid_forget()

                self.city_label.grid_forget()
                self.city.delete(0, tk.END)
                self.city.grid_forget()

                self.state_label.grid_forget()
                self.state.delete(0, tk.END)
                self.state.grid_forget()

                self.zip_label.grid_forget()
                self.zip.delete(0, tk.END)
                self.zip.grid_forget() 

        # Here's a modularized version of my widget definitions
        PROVIDERS = ["Jamie Cinotto", "Kristin Shepard", "Hashim Jaderanni", "Kyle Clark"]
        INSURANCES = ["Medicare", "Self-Pay", "Aetna", "Anthem Blue Cross", "Blue Shield", "Cencal", "CCPN", "Physician's Choice", "Insurance in Notes"]
        SUPPLIERS = ["Medi", "Juzo", "Jobst", "Sigvaris", "L&R", "Prairiewear", "No Preference"]
        COMPRESSION_LEVELS = ["15-20 mg", "20-30 mg", "30-40 mg", "40-50 mg", "Compression N/A"]
        LENGTH_OPTIONS = ["Standard", "Long", "Petite", "Length in Notes"]
        TOE_OPTIONS = ["Open Toe", "Closed Toe", "No Toe Prefrence"]
        SIDE_OPTIONS = ["No Side", "Right", "Left", "Pair"]
        QUANTITY_OPTIONS = ["1 Pair", "2 Pair", "3 Pair", "4 Pair", "5 Pair", "1 Single", "2 Single", "3 Single", "4 Single", "5 Single"]
        COLORS = ["Black", "Beige", "Sand","White", "Color in Notes"]
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

        self.garment_type_widgets = {
            "": [],
            "Knee High Stocking": [
                "compression_level", "size", "length", "toe", "color", "side", "quantity", "notes"
            ],
            "Thigh High Stocking": [
                "compression_level", "size", "length", "toe", "color", "side", "quantity", "notes"
            ],
            "Waist High Stocking": [
                "compression_level", "size", "length", "toe", "color", "quantity", "notes"
            ],
            "Waist Length - Chaps": [
                "compression_level", "size", "length", "toe", "color", "side", "quantity", "notes"
            ],
            "Shorts": [
                "compression_level", "size", "length", "color", "quantity", "notes"
            ],
            "Arm Sleeve": [
                "compression_level", "size", "length", "strap", "color", "side", "quantity", "notes"
            ],
            "Arm Sleeve Gauntlet Combo": [
                "compression_level", "size", "length", "strap", "color", "side", "quantity", "notes"
            ],
            "Glove - Fingers": [
                "compression_level", "size", "length", "color", "side", "quantity", "notes"
            ],
            "Gauntlet - No Fingers": [
                "compression_level", "size", "length", "color", "side", "quantity", "notes"
            ],
            "Bra / Chest": [
                "size", "color", "quantity", "notes"
            ],
            "Head / Neck": [
                "size", "color", "quantity", "notes"
            ],
            "Toe": [
                "quantity", "notes"
            ],
            "Adjustable Wrap": [
                "body_location", "size", "length", "color", "quantity", "notes"
            ],
            "Nightime": [
                "quantity", "notes"
            ],
            "Custom": [
                "quantity", "notes"
            ]
        }

        # Title
        tk.Label(self.form_frame, text="New Order", font=("Helvetica", 16, "bold"), bg=bg_color).grid(row=0, column=0, columnspan=2, pady=10)

        # Order Date
        tk.Label(self.form_frame, text="Order Date:", bg=bg_color).grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.order_date = DateEntry(self.form_frame, date_pattern='yyyy-mm-dd', width=12)
        self.order_date.grid(row=1, column=1, pady=5)

        # Home Delivery Checkbox
        self.home_delivery_var = tk.BooleanVar(value=False)  # Default to unchecked
        tk.Checkbutton(
            self.form_frame,
            text="Home Delivery?",
            variable=self.home_delivery_var,
            bg=bg_color,
            command=lambda: toggle_address_fields()
        ).grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # Provider (Dropdown)
        tk.Label(self.form_frame, text="Provider", bg=bg_color).grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.provider = ttk.Combobox(self.form_frame, values=PROVIDERS, state="readonly")
        self.provider.grid(row=3, column=1, sticky="ew", pady=10, padx=10)

        # Patient First Name
        tk.Label(self.form_frame, text="Patient First Name", bg=bg_color).grid(row=4, column=0, sticky="e", padx=10, pady=5)
        self.patient_first_name = tk.Entry(self.form_frame)
        self.patient_first_name.grid(row=4, column=1, sticky="ew", pady=10, padx=10)

        # Patient Last Name
        tk.Label(self.form_frame, text="Patient Last Name", bg=bg_color).grid(row=5, column=0, sticky="e", padx=10, pady=5)
        self.patient_last_name = tk.Entry(self.form_frame)
        self.patient_last_name.grid(row=5, column=1, sticky="ew", pady=10, padx=10)

        # Date of Birth
        tk.Label(self.form_frame, text="Date of Birth", bg=bg_color).grid(row=6, column=0, sticky="e", padx=10, pady=5)
        self.birthdate_frame = tk.Frame(self.form_frame, bg=bg_color)
        self.birthdate_frame.grid(row=6, column=1, sticky="ew", pady=10, padx=10)

        # Configure the birthdate_frame to expand all three columns equally
        self.birthdate_frame.grid_columnconfigure(0, weight=1)  # Month column expands
        self.birthdate_frame.grid_columnconfigure(1, weight=1)  # Date column expands
        self.birthdate_frame.grid_columnconfigure(2, weight=1)  # Year column expands

        # Month dropdown
        self.month_var = tk.StringVar(value="Month")
        month_dropdown = ttk.Combobox(self.birthdate_frame, textvariable=self.month_var, values=months, state="readonly", width=10)
        month_dropdown.grid(row=0, column=0, sticky="ew", padx=5)

        # Date dropdown
        dates = [str(i) for i in range(1, 32)]
        self.date_var = tk.StringVar(value="Date")
        date_dropdown = ttk.Combobox(self.birthdate_frame, textvariable=self.date_var, values=dates, state="readonly", width=5)
        date_dropdown.grid(row=0, column=1, sticky="ew", padx=5)

        # Year dropdown
        current_year = datetime.datetime.now().year
        years = [str(i) for i in range(1900, current_year + 1)]
        self.year_var = tk.StringVar(value="Year")
        year_dropdown = ttk.Combobox(self.birthdate_frame, textvariable=self.year_var, values=years, state="readonly", width=8)
        year_dropdown.grid(row=0, column=2, sticky="ew", padx=5)

        # Insurance (Dropdown)
        tk.Label(self.form_frame, text="Insurance", bg=bg_color).grid(row=7, column=0, sticky="e", padx=10, pady=5)
        self.insurance = ttk.Combobox(self.form_frame, values=INSURANCES, state="readonly")
        self.insurance.grid(row=7, column=1, sticky="ew", pady=10, padx=10)

        # Supplier (Dropdown)
        tk.Label(self.form_frame, text="Supplier", bg=bg_color).grid(row=8, column=0, sticky="e", padx=10, pady=5)
        self.supplier = ttk.Combobox(self.form_frame, values=SUPPLIERS, state="readonly")
        self.supplier.grid(row=8, column=1, sticky="ew", pady=10, padx=10)

        # Model (Text Box)
        tk.Label(self.form_frame, text="Model", bg=bg_color).grid(row=9, column=0, sticky="e", padx=10, pady=5)
        self.model = tk.Entry(self.form_frame)
        self.model.grid(row=9, column=1, sticky="ew", pady=10, padx=10)

        # Garment Type (Dropdown)
        tk.Label(self.form_frame, text="Garment Type", bg=bg_color).grid(row=10, column=0, sticky="e", padx=10, pady=5)
        self.garment_type = ttk.Combobox(self.form_frame, 
                                        values=list(self.garment_type_widgets.keys()), 
                                        state="readonly")
        self.garment_type.grid(row=10, column=1, sticky="ew", pady=10, padx=10)
        # Define the event handler that calls both the update_variable_widgets and clear_widgets
        def on_garment_type_selected(event):
            clear_widgets(self.variable_widgets)  # Clear widgets before updating
            self.update_variable_widgets(event)  # Update the variable widgets

        # bind the event handler
        self.garment_type.bind("<<ComboboxSelected>>", on_garment_type_selected)

        # Address fields
        self.address1_label = tk.Label(self.form_frame, text="Delivery Address 1", bg=bg_color)
        self.address1 = tk.Entry(self.form_frame)

        self.address2_label = tk.Label(self.form_frame, text="Delivery Address 2", bg=bg_color)
        self.address2 = tk.Entry(self.form_frame)

        self.city_label = tk.Label(self.form_frame, text="City", bg=bg_color)
        self.city = tk.Entry(self.form_frame)

        self.state_label = tk.Label(self.form_frame, text="State", bg=bg_color)
        self.state = tk.Entry(self.form_frame)

        self.zip_label = tk.Label(self.form_frame, text="Zip Code", bg=bg_color)
        self.zip = tk.Entry(self.form_frame)

        toggle_address_fields()          


        def clear_widgets(variable_widgets):
            for label, widget in variable_widgets:
                    # Reset the value of each widget
                if isinstance(widget, ttk.Combobox):
                    widget.set(value="")
                elif isinstance(widget, tk.Entry):
                    widget.delete(0, tk.END)  # Clear the entry widget
                elif isinstance(widget, tk.Text):
                    widget.delete("1.0", tk.END)  # Clear the text widget
                elif isinstance(widget, tk.Checkbutton):
                    widget.deselect()  # Deselect the checkbutton
                elif isinstance(widget, tk.Spinbox):
                    widget.delete(0, tk.END)  # Clear the spinbox widget
                    widget.insert(0, "0")  # Reset to default value (if applicable)

        self.variable_widgets = []

        # BODY LOCATION - COMBO BOX
        self.body_location_label = tk.Label(self.form_frame, text="Body Location", bg=bg_color)
        self.body_location = ttk.Combobox(self.form_frame, values=["Toes", "Foot", "Calf", "Knee", "Thigh", "Arm", "Glove", "Head & Neck"], state="readonly")
        self.variable_widgets.append((self.body_location_label, self.body_location))

        # COMPRESSION LEVEL - COMBO BOX
        self.compression_level_label = tk.Label(self.form_frame, text="Compression Level", bg=bg_color)
        self.compression_level = ttk.Combobox(self.form_frame, values=COMPRESSION_LEVELS, state="readonly")
        self.variable_widgets.append((self.compression_level_label, self.compression_level))

        # SIZE - TEXT BOX
        self.size_label = tk.Label(self.form_frame, text="Size", bg=bg_color)
        self.size = tk.Entry(self.form_frame)
        self.variable_widgets.append((self.size_label, self.size))

        # LENGTH - COMBO BOX
        self.length_label = tk.Label(self.form_frame, text="Length", bg=bg_color)
        self.length = ttk.Combobox(self.form_frame, values=LENGTH_OPTIONS, state="readonly")
        self.variable_widgets.append((self.length_label, self.length))

        # STRAP / NO STRAP - COMBO BOX
        self.strap_label = tk.Label(self.form_frame, text="Strap / No Strap", bg=bg_color)
        self.strap = ttk.Combobox(self.form_frame, values=["No Strap", "Strap"], state="readonly")
        self.variable_widgets.append((self.strap_label, self.strap))

        # TOE - COMBO BOX
        self.toe_label = tk.Label(self.form_frame, text="Toe", bg=bg_color)
        self.toe = ttk.Combobox(self.form_frame, values=TOE_OPTIONS, state="readonly")
        self.variable_widgets.append((self.toe_label, self.toe))

        # COLOR - COMBO BOX
        self.color_label = tk.Label(self.form_frame, text="Color", bg=bg_color)
        self.color = ttk.Combobox(self.form_frame, values=COLORS, state="readonly")
        self.variable_widgets.append((self.color_label, self.color))

        # SIDE - COMBO BOX
        self.side_label = tk.Label(self.form_frame, text="Side", bg=bg_color)
        self.side = ttk.Combobox(self.form_frame, values=SIDE_OPTIONS, state="readonly")
        self.variable_widgets.append((self.side_label, self.side))

        # QUANTITY - COMBO BOX
        self.quantity_label = tk.Label(self.form_frame, text="Quantity", bg=bg_color)
        self.quantity = ttk.Combobox(self.form_frame, values=QUANTITY_OPTIONS, state="readonly")
        self.variable_widgets.append((self.quantity_label, self.quantity))

        # NOTES - LARGE TEXT BOX
        self.notes_label = tk.Label(self.form_frame, text="Notes", bg=bg_color)
        self.notes = tk.Text(self.form_frame, height=4, width=50)  # Adjust the size as needed
        self.variable_widgets.append((self.notes_label, self.notes))


        def clear_action():
            self.reset_form()
            self.update_variable_widgets()
            toggle_address_fields() 

        #clear button
        clear_button = tk.Button(self.form_frame, text="Clear Form", command=clear_action)
        clear_button.grid(row=99, column=0, columnspan=1, pady=20)

        #submit button
        submit_button = tk.Button(self.form_frame, text="Submit Order", command=self.submit_order)
        submit_button.grid(row=99, column=1, columnspan=1, pady=20)

        # Back button to return to the main menu
        back_button = tk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame("main_menu"))
        back_button.pack(pady=10)

    def submit_order(self):
        # File path for the orders CSV file
        if getattr(sys, 'frozen', False):
            # Running as an executable (PyInstaller bundles the file into the temporary folder)
            file_path = os.path.join(sys._MEIPASS, "orders.csv")
        else:
            # Running as a regular script (during development)
            file_path = os.path.join(os.path.dirname(__file__), "orders.csv")

        # Check if the CSV file exists
        if not os.path.exists(file_path):
            # If not, create the file and write the header row
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                header = ['Order Number', 'Order Date', 'Provider', 'Patient First Name', 'Patient Last Name', 'Date of Birth', 
                        'Insurance', 'Supplier', 'Model', 'Garment Type', 'Body Location', 'Compression Level', 'Size', 'Length', 
                        'Strap', 'Toe', 'Color', 'Side', 'Quantity', 'Notes', 'Delivery Option', 'Delivery Address 1', 'Delivery Address 2', 
                        'City', 'State', 'Zip', 'Is Ordered', 'Marked Ordered Date', 'Is Delivered', 'Marked Delivered Date', 'Deleted']
                writer.writerow(header)

        # Read the existing orders to find the last order number
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)
            last_order_number = 0
            if len(rows) > 1:  # Skip header row
                last_order_number = int(rows[-1][0])  # Get the last order number from the last row
            order_number = last_order_number + 1  # Increment for the new order

        # Getting data from the form fields
        order_date_value = self.order_date.get_date().strftime('%Y-%m-%d')
        provider_value = self.provider.get()
        patient_first_name = self.patient_first_name.get()
        patient_last_name = self.patient_last_name.get()

        # Map months to their numeric values (01, 02, ..., 12)
        month_map = {
            "January": "01", "February": "02", "March": "03", "April": "04",
            "May": "05", "June": "06", "July": "07", "August": "08",
            "September": "09", "October": "10", "November": "11", "December": "12"
        }

        # Get selected values from the dropdowns
        dob_month_name = self.month_var.get()  # Month name (e.g., "January")
        dob_date = self.date_var.get()  # Day of the month (e.g., "01")
        dob_year = self.year_var.get()  # Year (e.g., "1990")

        # Convert the month name to the corresponding numeric value
        dob_month = month_map.get(dob_month_name, "00")  # Default to "00" if invalid month

        # Handle case where day is still set to "Day"
        if dob_date == "Day":
            dob_date = "00"  # Default to "00" if no valid day is selected
        else:
            dob_date = dob_date.zfill(2)  # Pad day with a leading zero if necessary

        # Handle case where year is still set to "Year"
        if dob_year == "Year":
            dob_year = "00"  # Default to "00" if no valid year is selected

        # Create the formatted dob_value in 'YYYY-MM-DD' format
        dob_value = f"{dob_year}-{dob_month}-{dob_date}"

        insurance_value = self.insurance.get()
        supplier_value = self.supplier.get()
        model_value = self.model.get()
        garment_type_value = self.garment_type.get()
        body_location_value = self.body_location.get()
        compression_level_value = self.compression_level.get()
        size_value = self.size.get()
        length_value = self.length.get()
        strap_value = self.strap.get()
        toe_value = self.toe.get()
        color_value = self.color.get()
        side_value = self.side.get()
        quantity_value = self.quantity.get()
        notes_value = self.notes.get("1.0", "end-1c")
        if self.home_delivery_var.get():
            delivery_option = "Drop Shipping"
        else:
            delivery_option = "Office Pickup"
        delivery_address_1_value = self.address1.get()
        delivery_address_2_value = self.address2.get()
        city_value = self.city.get()
        state_value = self.state.get()
        zip_value = self.zip.get()
        is_ordered = False
        marked_ordered_date = ""
        is_delivered = False
        marked_delivered_date = ""
        deleted = False

        # Prepare the order data
        order_data = [order_number, order_date_value, provider_value, patient_first_name, patient_last_name, dob_value, insurance_value,
                    supplier_value, model_value, garment_type_value, body_location_value, compression_level_value, size_value,
                    length_value, strap_value, toe_value, color_value, side_value, quantity_value, notes_value, delivery_option,
                    delivery_address_1_value, delivery_address_2_value, city_value, state_value, zip_value, is_ordered, 
                    marked_ordered_date, is_delivered, marked_delivered_date, deleted]

        # Write the new order to the CSV file
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(order_data)

        # Show a success message
        response = messagebox.askyesno(
            "Order Saved",
            f"Order {order_number} has been saved successfully.\nWould you like to submit another order?"
        )

        if response:  # User wants to submit another order
            self.controller.show_frame("new_order")
        else:
            self.controller.show_frame("main_menu")