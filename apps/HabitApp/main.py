import os
import json
import customtkinter as ctk
from datetime import datetime, date, timedelta

class AppFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#111111", corner_radius=0)
        
        # Paths for localized data persistence - Safe for module loaders
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_file = os.path.join(self.base_dir, "habits.json")
        
        # Configure layout distributions
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Load habits dataset from disk storage
        self.habits_dataset = self.load_habits_from_disk()
        
        # Run an initial check to auto-reset broken streaks on startup safely
        self.verify_and_reset_broken_streaks()

        # 1. Header Layout Block
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=40, pady=(20, 15), sticky="ew")
        
        ctk.CTkLabel(
            header_frame, 
            text="Habit Routine Tracker", 
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color="#ffffff"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header_frame, 
            text="Build your consistency loops and secure active daily streaks.", 
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#8c8c8c"
        ).pack(anchor="w", pady=(2, 0))

        # 2. Input Control Field Bar (Create Custom Habits)
        input_frame = ctk.CTkFrame(self, fg_color="#1a1a1a", height=70, corner_radius=10)
        input_frame.grid(row=1, column=0, padx=40, pady=(0, 15), sticky="ew")
        input_frame.pack_propagate(False)

        self.habit_entry = ctk.CTkEntry(
            input_frame, 
            placeholder_text="Type a new routine tracker habit here...",
            fg_color="#111111",
            border_color="#2b2b2b",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            height=38
        )
        self.habit_entry.pack(side="left", fill="x", expand=True, padx=(20, 12), pady=16)

        add_btn = ctk.CTkButton(
            input_frame,
            text="Add Habit",
            fg_color="#0078d4",
            hover_color="#106ebe",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            height=38,
            width=110,
            corner_radius=6,
            command=self.add_custom_habit
        )
        add_btn.pack(side="right", padx=(0, 20), pady=16)

        # Bind Enter key to instantly append text entry strings
        self.habit_entry.bind("<Return>", lambda event: self.add_custom_habit())

        # 3. Main Scrollable Tracking Workspace Canvas
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.grid(row=2, column=0, padx=40, pady=(0, 20), sticky="nsew")
        
        self.render_habit_cards()

    def load_habits_from_disk(self):
        """Loads data entries directly from local json snapshot targets safely."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                print("ERROR loading habits mapping targets:", e)
        return []

    def save_habits_to_disk(self):
        """Commits memory storage state parameters directly down to local systems."""
        try:
            with open(self.data_file, "w") as f:
                json.dump(self.habits_dataset, f, indent=4)
        except Exception as e:
            print("ERROR writing habits configurations down to disk storage:", e)

    def verify_and_reset_broken_streaks(self):
        """Resets streaks to 0 if a user completely skipped the previous calendar day."""
        today = date.today()
        updated = False
        
        for habit in self.habits_dataset:
            last_completed_str = habit.get("last_completed", "").strip()
            if last_completed_str:
                try:
                    last_date = datetime.strptime(last_completed_str, "%Y-%m-%d").date()
                    days_since = (today - last_date).days
                    # If it's been 2 or more days since completion, the streak died
                    if days_since > 1:
                        habit["streak"] = 0
                        updated = True
                except ValueError:
                    # Guard against malformed json data entries corruption
                    habit["last_completed"] = ""
                    updated = True
                    
        if updated:
            self.save_habits_to_disk()

    def add_custom_habit(self):
        habit_text = self.habit_entry.get().strip()
        if not habit_text:
            return

        new_habit = {
            "name": habit_text,
            "streak": 0,
            "last_completed": ""  
        }
        self.habits_dataset.append(new_habit)
        self.save_habits_to_disk()
        
        self.habit_entry.delete(0, "end")
        self.render_habit_cards()

    def remove_habit_item(self, index):
        """Deletes habit entries and resets layouts instantly."""
        if 0 <= index < len(self.habits_dataset):
            self.habits_dataset.pop(index)
            self.save_habits_to_disk()
            self.render_habit_cards()

    def toggle_habit_state(self, index):
        """Alters target completion state based on real-world elapsed dates."""
        habit = self.habits_dataset[index]
        today_str = str(date.today())
        
        # Scenario A: Already completed today -> Clicking it acts as an "Undo" operation
        if habit["last_completed"] == today_str:
            # Revert to yesterday to preserve the timeline check logic if needed
            yesterday_str = str(date.today() - timedelta(days=1))
            habit["last_completed"] = yesterday_str 
            habit["streak"] = max(0, habit["streak"] - 1)
            
        # Scenario B: Not completed today yet -> Complete it
        else:
            last_completed_str = habit["last_completed"].strip()
            if last_completed_str:
                try:
                    last_date = datetime.strptime(last_completed_str, "%Y-%m-%d").date()
                    days_since = (date.today() - last_date).days
                    # If they missed a day in between, drop the streak back down
                    if days_since > 1:
                        habit["streak"] = 0
                except ValueError:
                    habit["streak"] = 0
            
            habit["last_completed"] = today_str
            habit["streak"] += 1
            
        self.save_habits_to_disk()
        self.render_habit_cards()

    def render_habit_cards(self):
        for widget in self.scroll_container.winfo_children():
            widget.destroy()

        if not self.habits_dataset:
            empty_lbl = ctk.CTkLabel(
                self.scroll_container,
                text="No habits created yet. Type something above to begin your routine mapping!",
                font=ctk.CTkFont(family="Segoe UI", size=13),
                text_color="#555555"
            )
            empty_lbl.pack(pady=40)
            return

        today_str = str(date.today())

        for idx, habit in enumerate(self.habits_dataset):
            is_done_today = (habit.get("last_completed") == today_str)

            card = ctk.CTkFrame(self.scroll_container, fg_color="#1a1a1a", height=85, corner_radius=10)
            card.pack(fill="x", pady=6, padx=5)
            card.pack_propagate(False)
            
            card.grid_columnconfigure(0, weight=1)
            card.grid_columnconfigure(1, weight=0)

            # Left text layout blocks
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.grid(row=0, column=0, padx=20, pady=15, sticky="w")

            title_color = "#60CDFF" if is_done_today else "#ffffff"
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

            # Right actions panel layout
            actions_panel = ctk.CTkFrame(card, fg_color="transparent")
            actions_panel.grid(row=0, column=1, padx=20, pady=24, sticky="e")

            action_btn = ctk.CTkButton(
                actions_panel,
                text="Undo Done" if is_done_today else "Complete",
                fg_color="#1c3322" if is_done_today else "#1f1f1f",
                hover_color="#25452e" if is_done_today else "#2b2b2b",
                text_color="#63E286" if is_done_today else "#ffffff",
                border_width=1,
                border_color="#25452e" if is_done_today else "#3c3c3c",
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                width=100,
                height=32,
                corner_radius=6,
                command=lambda i=idx: self.toggle_habit_state(i)
            )
            action_btn.pack(side="left", padx=5)

            delete_btn = ctk.CTkButton(
                actions_panel,
                text="✕",
                fg_color="transparent",
                hover_color="#2a1818",
                text_color="#ff5f5f",
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                width=32,
                height=32,
                corner_radius=6,
                command=lambda i=idx: self.remove_habit_item(i)
            )
            delete_btn.pack(side="left", padx=5)

# Runtime loader entry point configurations 
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Habit Routine App Workspace")
    root.geometry("620x540")
    root.minsize(520, 420)

    app_frame = AppFrame(root)
    app_frame.pack(fill="both", expand=True)

    root.mainloop()
