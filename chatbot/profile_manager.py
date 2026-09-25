import json
from pathlib import Path
 

class ProfileManager:

    def __init__(self):
        self.file_path = Path("data/profile.json")
        self.profile = {}

        self.load_profile()

    def load_profile(self):
        """
        Load the profile from disk.
        If the file doesn't exist or contains invalid JSON,
        start with an empty profile.
        """

        if not self.file_path.exists():
            self.profile = {}
            self.save_profile()
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                self.profile = json.load(file)

        except json.JSONDecodeError:
            self.profile = {}
            self.save_profile()

    def save_profile(self):
        """
        Save the current profile to disk.
        """

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                self.profile,
                file,
                indent=4,
                ensure_ascii=False
            )

    def get_profile(self):
        """
        Return the complete profile.
        """

        return self.profile.copy()

    def get(self, key, default=None):
        """
        Get a single value from the profile.
        """

        return self.profile.get(key, default)

    def update(self, key, value):
        """
        Add or update a profile field.
        """

        self.profile[key] = value
        self.save_profile()

    def remove(self, key):
        """
        Remove a field if it exists.
        """

        if key in self.profile:
            del self.profile[key]
            self.save_profile()

    def exists(self, key):
        """
        Check whether a key exists.
        """

        return key in self.profile

    def clear(self):
        """
        Remove all stored profile data.
        """

        self.profile = {}
        self.save_profile()