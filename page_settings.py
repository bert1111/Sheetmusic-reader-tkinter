import json
import os

class PageSettings:
    def __init__(self, filename='page_settings.json'):
        self.filename = filename
        self.settings = {}
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.settings = json.load(f)
            except Exception as e:
                print(f"Fout bij laden instellingen: {e}")
                self.settings = {}
        else:
            self.settings = {}

    def save(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Fout bij opslaan instellingen: {e}")

    def get(self, filepath, page_number):
        return self.settings.get(filepath, {}).get(str(page_number), {"zoom": 1.0, "rotation": 0, "annotations": []})

    def set(self, filepath, page_number, zoom, rotation, annotations=None):
        if filepath not in self.settings:
            self.settings[filepath] = {}
        existing = self.settings[filepath].get(str(page_number), {})
        existing.update({
            "zoom": zoom,
            "rotation": rotation,
        })
        if annotations is not None:
            existing["annotations"] = annotations
        self.settings[filepath][str(page_number)] = existing
