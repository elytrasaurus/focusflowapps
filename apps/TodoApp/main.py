import os
import json
import customtkinter as ctk

class AppFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#1a1a1a", corner_radius=12)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.json_path = os.path.join(self.current_dir, "todo_data.json")
        self.task_widgets = []

        self.create_header()
        self.create_content()
        self.load_tasks_from_json()

    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=30, pady=(25, 10), sticky="ew")

        title = ctk.CTkLabel(header_frame, text="Task Matrix", font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"), text_color="#60CDFF")
        title.grid(row=0, column=0, sticky="w")

        subtitle = ctk.CTkLabel(header_frame, text="Organize tasks and track your daily priorities", font=ctk.CTkFont(family="Segoe UI", size=12), text_color="#8c8c8c")
        subtitle.grid(row=1, column=0, sticky="w")

    def create_content(self):
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, padx=30, pady=(10, 30), sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)

        # Input Row
        input_frame = ctk.CTkFrame(content_frame, fg_color="#242424", corner_radius=12, height=70)
        input_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        input_frame.grid_propagate(False)
        input_frame.grid_columnconfigure(0, weight=1)

        self.task_entry = ctk.CTkEntry(input_frame, placeholder_text="Add a new goal or action item...", fg_color="#1a1a1a", border_width=1, border_color="#333333", height=38, corner_radius=6)
        self.task_entry.grid(row=0, column=0, padx=(20, 10), pady=16, sticky="ew")

        add_btn = ctk.CTkButton(input_frame, text="Add Task", fg_color="#0078d4", hover_color="#106ebe", text_color="#ffffff", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), width=100, height=38, corner_radius=6, command=self.add_task_item)
        add_btn.grid(row=0, column=1, padx=(0, 20), pady=16)

        # List Area
        self.list_box = ctk.CTkScrollableFrame(content_frame, fg_color="#242424", corner_radius=12)
        self.list_box.grid(row=1, column=0, sticky="nsew")

    def add_task_item(self):
        text = self.task_entry.get().strip()
        if text:
            self.save_task_to_json(text)
            self.task_entry.delete(0, "end")

    def render_task_element(self, text, index):
        item_frame = ctk.CTkFrame(self.list_box, fg_color="#1a1a1a", corner_radius=8, height=44)
        item_frame.pack(fill="x", pady=6, padx=10)
        item_frame.pack_propagate(False)

        lbl = ctk.CTkLabel(item_frame, text=f"   🔹   {text}", font=ctk.CTkFont(family="Segoe UI", size=13), text_color="#ffffff")
        lbl.pack(side="left", padx=5)

        del_btn = ctk.CTkButton(item_frame, text="×", font=ctk.CTkFont(size=16, weight="bold"), text_color="#FF5F5F", fg_color="transparent", hover_color="#2d2d2d", width=28, height=28, corner_radius=6, command=lambda: self.delete_task(index))
        del_btn.pack(side="right", padx=10)

        self.task_widgets.append(item_frame)

    def load_tasks_from_json(self):
        self.clear_rendered_widgets()
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, "r") as f:
                    tasks = json.load(f)
                    for i, task_text in enumerate(tasks):
                        self.render_task_element(task_text, i)
            except:
                pass

    def save_task_to_json(self, text):
        tasks = []
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, "r") as f:
                    tasks = json.load(f)
            except:
                pass

        tasks.append(text)
        try:
            with open(self.json_path, "w") as f:
                json.dump(tasks, f, indent=4)
        except:
            pass
        self.load_tasks_from_json()

    def delete_task(self, target_index):
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, "r") as f:
                    tasks = json.load(f)
                if 0 <= target_index < len(tasks):
                    tasks.pop(target_index)
                with open(self.json_path, "w") as f:
                    json.dump(tasks, f, indent=4)
            except:
                pass
        self.load_tasks_from_json()

    def clear_rendered_widgets(self):
        for widget in self.task_widgets:
            widget.destroy()
        self.task_widgets = []
