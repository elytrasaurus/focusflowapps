import os
import json
import customtkinter as ctk

class AppFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#1e1e1e", corner_radius=12)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.timer_running = False
        self.default_time = 1500
        self.time_left = self.default_time

        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.json_path = os.path.join(self.current_dir, "history.json")

        self.create_header()
        self.create_content()
        self.load_history_from_json()

    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=30, pady=(25, 10), sticky="ew")

        title = ctk.CTkLabel(header_frame, text="Focus Timer", font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"), text_color="#ffffff")
        title.grid(row=0, column=0, sticky="w")

        subtitle = ctk.CTkLabel(header_frame, text="Deep work session & activity logging", font=ctk.CTkFont(family="Segoe UI", size=12), text_color="#858585")
        subtitle.grid(row=1, column=0, sticky="w")

    def create_content(self):
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, padx=30, pady=(10, 30), sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=4)
        content_frame.grid_columnconfigure(1, weight=5)
        content_frame.grid_rowconfigure(0, weight=1)

        timer_card = ctk.CTkFrame(content_frame, fg_color="#2d2d2d", corner_radius=12)
        timer_card.grid(row=0, column=0, padx=(0, 15), sticky="nsew")
        timer_card.grid_columnconfigure(0, weight=1)

        self.time_display = ctk.CTkLabel(timer_card, text="25:00", font=ctk.CTkFont(family="Segoe UI", size=54, weight="bold"), text_color="#60CDFF")
        self.time_display.grid(row=0, column=0, pady=(50, 20))

        btn_frame = ctk.CTkFrame(timer_card, fg_color="transparent")
        btn_frame.grid(row=1, column=0, pady=(0, 40))

        self.action_btn = ctk.CTkButton(btn_frame, text="Start Session", fg_color="#0078d4", hover_color="#106ebe", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), width=110, height=36, command=self.toggle_timer)
        self.action_btn.grid(row=0, column=0, padx=5)

        reset_btn = ctk.CTkButton(btn_frame, text="Reset", fg_color="#3a3a3a", hover_color="#4a4a4a", text_color="#ffffff", font=ctk.CTkFont(family="Segoe UI", size=13), width=80, height=36, command=self.reset_timer)
        reset_btn.grid(row=0, column=1, padx=5)

        log_card = ctk.CTkFrame(content_frame, fg_color="#2d2d2d", corner_radius=12)
        log_card.grid(row=0, column=1, padx=(15, 0), sticky="nsew")
        log_card.grid_columnconfigure(0, weight=1)
        log_card.grid_rowconfigure(2, weight=1)

        log_title = ctk.CTkLabel(log_card, text="Activity Log", font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"), text_color="#ffffff")
        log_title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        input_frame = ctk.CTkFrame(log_card, fg_color="transparent")
        input_frame.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)

        self.log_entry = ctk.CTkEntry(input_frame, placeholder_text="What are you working on?", fg_color="#1e1e1e", border_width=1, border_color="#3a3a3a", height=36)
        self.log_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        add_btn = ctk.CTkButton(input_frame, text="Log", fg_color="#00CA4E", hover_color="#00b545", text_color="#ffffff", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), width=60, height=36, command=self.add_log_item)
        add_btn.grid(row=0, column=1)

        self.log_box = ctk.CTkScrollableFrame(log_card, fg_color="#1e1e1e", corner_radius=8)
        self.log_box.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")

    def toggle_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.action_btn.configure(text="Start Session", fg_color="#0078d4", hover_color="#106ebe")
        else:
            self.timer_running = True
            self.action_btn.configure(text="Pause", fg_color="#d83b01", hover_color="#b83201")
            self.run_timer_loop()

    def run_timer_loop(self):
        if self.timer_running:
            if self.time_left > 0:
                self.time_left -= 1
                mins, secs = divmod(self.time_left, 60)
                self.time_display.configure(text=f"{mins:02d}:{secs:02d}")
                self.after(1000, self.run_timer_loop)
            else:
                self.timer_running = False
                self.action_btn.configure(text="Start Session", fg_color="#0078d4")
                self.time_left = self.default_time
                self.time_display.configure(text="25:00")
                self.append_log_to_json("⏱️ Focus session completed!", is_system=True)

    def reset_timer(self):
        self.timer_running = False
        self.time_left = self.default_time
        self.time_display.configure(text="25:00")
        self.action_btn.configure(text="Start Session", fg_color="#0078d4", hover_color="#106ebe")

    def add_log_item(self):
        text = self.log_entry.get().strip()
        if text:
            self.append_log_to_json(text, is_system=False)
            self.log_entry.delete(0, "end")

    def render_log_element(self, text, is_system=False):
        bg = "#143622" if is_system else "#2d2d2d"
        fg = "#00CA4E" if is_system else "#ffffff"
        weight = "bold" if is_system else "normal"
        prefix = "" if is_system else "• "

        item_frame = ctk.CTkFrame(self.log_box, fg_color=bg, corner_radius=6, height=34)
        item_frame.pack(fill="x", pady=4, padx=5)
        item_frame.pack_propagate(False)
        
        lbl = ctk.CTkLabel(item_frame, text=f"{prefix}{text}", font=ctk.CTkFont(family="Segoe UI", size=13, weight=weight), text_color=fg)
        lbl.pack(side="left", padx=10)

    def load_history_from_json(self):
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, "r") as f:
                    logs = json.load(f)
                    for log in logs:
                        self.render_log_element(log["text"], log["is_system"])
            except:
                pass

    def append_log_to_json(self, text, is_system=False):
        logs = []
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, "r") as f:
                    logs = json.load(f)
            except:
                logs = []

        logs.append({"text": text, "is_system": is_system})

        try:
            with open(self.json_path, "w") as f:
                json.dump(logs, f, indent=4)
        except:
            pass

        self.render_log_element(text, is_system)
