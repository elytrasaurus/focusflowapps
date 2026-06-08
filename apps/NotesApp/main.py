import os
import json
import customtkinter as ctk

class AppFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#1a1a1a", corner_radius=12)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.json_path = os.path.join(self.current_dir, "notebook_data.json")

        self.create_header()
        self.create_content()
        self.load_note_from_json()

    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=30, pady=(25, 10), sticky="ew")

        title = ctk.CTkLabel(header_frame, text="Quick Scratchpad", font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"), text_color="#60CDFF")
        title.grid(row=0, column=0, sticky="w")

        subtitle = ctk.CTkLabel(header_frame, text="Distraction-free thoughts and active clipboard cache", font=ctk.CTkFont(family="Segoe UI", size=12), text_color="#8c8c8c")
        subtitle.grid(row=1, column=0, sticky="w")

    def create_content(self):
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, padx=30, pady=(10, 30), sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        # Main Rich Text Area Textbox
        self.textbox = ctk.CTkTextbox(content_frame, fg_color="#242424", border_width=1, border_color="#333333", corner_radius=12, font=ctk.CTkFont(family="Consolas", size=14), text_color="#f0f0f0", wrap="word")
        self.textbox.grid(row=0, column=0, sticky="nsew")
        
        # Capture raw keyboard release strings automatically to drop saves on key up
        self.textbox.bind("<KeyRelease>", self.auto_save_note)

    def load_note_from_json(self):
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, "r") as f:
                    data = json.load(f)
                    saved_text = data.get("content", "")
                    self.textbox.delete("1.0", "end")
                    self.textbox.insert("1.0", saved_text)
            except:
                pass

    def auto_save_note(self, event=None):
        current_text = self.textbox.get("1.0", "end-1c")
        data = {"content": current_text}
        try:
            with open(self.json_path, "w") as f:
                json.dump(data, f, indent=4)
        except:
            pass
