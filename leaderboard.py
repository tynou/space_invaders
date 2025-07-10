import os

from config import *


class Leaderboard:
    def __init__(self):
        self.entries = {}
        self.file_path = LEADERBOARD_FILE_PATH

        self.read()
    
    def add_entry(self, username, score):
        self.entries[username] = max(self.entries[username], score) if username in self.entries else score

    def read(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        with open(self.file_path, "a+") as file:
            file.seek(0)
            for entry in file.readlines():
                username, score = entry.strip().split(":")
                self.add_entry(username, int(score))

    def write_to_file(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        with open(self.file_path, "w+") as file:
            file.writelines([f"{username}:{score}\n" for username, score in self.entries.items()])
