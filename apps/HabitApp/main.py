import customtkinter as ctk

class AppFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#111111", corner_radius=0)
        
        # Configure grid distribution
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 1. Header Layout Block
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=40, pady=(20, 20), sticky="ew")
        
        ctk.CTkLabel(
            header_frame, 
            text="Habit Routine Tracker", 
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color="#ffffff"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header_frame, 
            text="Maintain your consistency loops and secure active daily streaks.", 
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#8c8c8c"
        ).pack(anchor="w", pady=(2, 0))

        # 2. Main Scrollable Tracking Workspace
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.grid(row=1, column=0, padx=40, pady=(0, 20), sticky="nsew")
        
        # In-memory default habits state database mock
        self.habits_dataset = [
            {"name": "Deep Work Session", "streak": 5, "done": True},
            {"name": "Read 10 Pages", "streak": 12, "done": True},
            {"name": "Physical Exercise Routine", "streak": 0, "done": False},
            {"name": "Hydration Target (3L)", "streak": 3, "done": False},
        ]

        self.render_habit_cards()

    def render_habit_cards(self):
        # Clear out existing widgets in the scroll frame to redraw cleanly
        for widget in self.scroll_container.winfo_children():
            widget.destroy()

        for idx, habit in enumerate(self.habits_dataset):
            card = ctk.CTkFrame(self.scroll_container, fg_color="#1a1a1a", height=85, corner_radius=10)
            card.pack(fill="x", pady=6, padx=5)
            card.pack_propagate(False)
            
            card.grid_columnconfigure(0, weight=1)
            card.grid_columnconfigure(1, weight=0)

            # Left block text metadata elements
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.grid(row=0, column=0, padx=20, pady=15, sticky="w")

            title_color = "#60CDFF" if habit["done"] else "#ffffff"
            title_lbl = ctk.CTkLabel(
                info_frame, 
                text=habit["name"], 
                font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                text_color=title_color
            )
            title_lbl.pack(anchor="w")

            streak_text = f"🔥 {habit['streak']} Day Streak" if habit["streak"] > 0 else "💀 No active streak"
            streak_lbl = ctk.CTkLabel(
                info_frame, 
                text=streak_text, 
                font=ctk.CTkFont(family="Segoe UI", size=12),
                text_color="#8c8c8c"
            )
            streak_lbl.pack(anchor="w", pady=(2, 0))

            # Right action interactive checkbox mapping layout 
            action_btn = ctk.CTkButton(
                card,
                text="Complete" if not habit["done"] else "Undo Done",
                fg_color="#1f1f1f" if not habit["done"] else "#1c3322",
                hover_color="#2b2b2b" if not habit["done"] else "#25452e",
                text_color="#ffffff" if not habit["done"] else "#63E286",
                border_width=1,
                border_color="#3c3c3c" if not habit["done"] else "#25452e",
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                width=100,
                height=32,
                corner_radius=6,
                command=lambda i=idx: self.toggle_habit_state(i)
            )
            action_btn.grid(row=0, column=1, padx=20, pady=26, sticky="e")

    def toggle_habit_state(self, index):
        """Alters target completion state loops and increments streaks dynamically."""
        habit = self.habits_dataset[index]
        if not habit["done"]:
            habit["done"] = True
            habit["streak"] += 1
        else:
            habit["done"] = False
            habit["streak"] = max(0, habit["streak"] - 1)
            
        self.render_habit_cards()
