import tkinter as tk
import importlib
from tkinter import ttk

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Application")
        self.root.geometry("800x600")  # Initial size, can be resized
        self.root.config(bg="#f0f8ff")

        # Create a canvas
        self.canvas = tk.Canvas(self.root, bg="#f0f8ff")

        # Create a vertical scrollbar
        self.scrollbar_y = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        # Create a horizontal scrollbar
        self.scrollbar_x = ttk.Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set)

        # Create a frame inside the canvas that will hold the actual content
        self.content_frame = tk.Frame(self.canvas, bg="#f0f8ff", width=600, height=400)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        # Initially show the main menu frame
        self.current_frame = None
        self.show_frame('main_menu')

        # Pack the canvas and scrollbars to fill the window
        self.canvas.pack(side="top", fill="both", expand=True)
        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")

        # Bind resizing events
        self.root.bind("<Configure>", self.update_layout)  # Bind to window resize
        self.content_frame.bind("<Configure>", self.update_layout)  # Correctly bind to update layout

        # Bind scrolling to vertical scrollbar
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)  # Enable mouse scroll for the entire app

    def show_frame(self, frame_name):
        """Dynamically load and show the requested frame."""
        if self.current_frame is not None:
            self.current_frame.destroy()

        # Dynamically import the frame script based on the frame_name
        try:
            frame_module = importlib.import_module(frame_name)  # Dynamically load the module
            frame_class = getattr(frame_module, frame_name + '_Frame')  # Ensure correct class name
            self.current_frame = frame_class(self.content_frame, self)  # Create frame instance

            # Ensure the frame fills the entire space of the content_frame
            self.current_frame.pack(fill="both", expand=True)  # Fill all available space

            # After loading the frame, immediately update the layout
            self.update_layout()

        except (ModuleNotFoundError, AttributeError) as e:
            print(f"Error: Could not load frame {frame_name}. {e}")

        # Recalculate layout to center content and update scroll region after the frame is packed
        self.update_layout()  # Ensure content is centered and scroll region updated


    def update_scroll_region(self, event=None):
        """Update the scroll region when the content size changes."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def center_content(self):
        """Center the content frame within the canvas."""
        # Ensure the content_frame is fully updated before getting its size
        self.content_frame.update_idletasks()  # Forces the geometry manager to update the content frame

        # Get the updated size of the content frame
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        content_frame_width = self.content_frame.winfo_width()
        content_frame_height = self.content_frame.winfo_height()

        # Calculate offsets to center the content_frame
        x_offset = max((canvas_width - content_frame_width) // 2, 0)
        y_offset = max((canvas_height - content_frame_height) // 2, 0)

        # Reposition the content frame within the canvas
        self.canvas.coords(self.canvas_window, x_offset, y_offset)

    def update_layout(self, event=None):
        """Update layout (center content and update scroll region)."""
        self.update_scroll_region()
        self.center_content()

    def on_mouse_wheel(self, event):
        """Handle mouse scroll events to scroll vertically and horizontally."""
        if event.state & 0x0001:  # If the control key is pressed (for horizontal scroll)
            self.canvas.xview_scroll(-1 if event.delta > 0 else 1, "units")
        else:
            self.canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
