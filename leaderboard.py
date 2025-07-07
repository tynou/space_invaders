import os

from config import *


class Leaderboard:
    def __init__(self):
        self.entries = {}
        self.file_path = LEADERBOARD_FILE_PATH
    
    def add_entry(self, username, score):
        self.entries[username] = score

    def read(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        with open(self.file_path, "a+") as file:
            for entry in file.readlines():
                username, score = entry.split(":")
                self.add_entry(username, score)

    def write_to_file(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        with open(self.file_path, "w+") as file:
            file.writelines([f"{username}:{score}\n" for username, score in self.entries.items()])
