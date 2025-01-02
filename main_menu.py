import tkinter as tk

class main_menu_Frame(tk.Frame):
    def __init__(self, parent, controller):
        # Get the background color of the main window
        bg_color = controller.root.cget('bg')
        super().__init__(parent, bg=bg_color)
        self.controller = controller

        self.create_menu()

    def create_menu(self):
        """Create the main menu layout."""
        tk.Label(self, text="Main Menu", font=("Helvetica", 16, "bold"), bg=self['bg']).pack(pady=20)

        # Button to navigate to New Order
        tk.Button(self, text="New Order", width=20, height=2,
                  command=lambda: self.controller.show_frame("new_order")).pack(pady=10)

        # Button to navigate to Order List
        tk.Button(self, text="To Order", width=20, height=2,
                  command=lambda: self.controller.show_frame("order_list")).pack(pady=10)

        # Button to navigate to Delivery List
        tk.Button(self, text="Mark Delivered", width=20, height=2,
                  command=lambda: self.controller.show_frame("delivery_list")).pack(pady=10)
        
        # Button to navigate to Delivery List
        tk.Button(self, text="Check Orders", width=20, height=2,
                  command=lambda: self.controller.show_frame("check_orders")).pack(pady=10)

        # Exit button
        tk.Button(self, text="Exit", width=20, height=2,
                  command=self.controller.root.quit).pack(pady=10)
