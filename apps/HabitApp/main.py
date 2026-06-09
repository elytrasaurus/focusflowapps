# apps/HabitApp/main.py
import customtkinter as ctk

class AppFrame(ctk.CTkFrame):
    def __init__(self, parent):
        # Initialize the frame to fit inside the dashboard canvas area
        super().__init__(parent, fg_color="#1a1a1a", corner_radius=12)
        
        # Configure layout inside your custom app space
        self.grid_columnconfigure(0, weight=1)
        
        # Add your app widgets here
        title = ctk.CTkLabel(
            self, 
            text="Welcome to your Custom Module Space!", 
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="#60CDFF"
        )
        title.pack(pady=40)
        
        description = ctk.CTkLabel(
            self, 
            text="You can drop any Tkinter or CustomTkinter UI logic right here inside this frame wrapper.", 
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#8c8c8c"
        )
        description.pack(pady=10)
