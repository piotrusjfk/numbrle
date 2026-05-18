import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import random
import json
import os

class NumbrleDeluxe:
    def __init__(self, root):
        self.root = root
        self.root.title("Numbrle Pro sigmaligma")
        self.root.geometry("1100x850")
        self.root.configure(bg="#1a1a1e")
        
        self.scores_file = "scores.json"
        self.nickname = ""
        self.num_tries = 6
        self.word_len = 5
        
        self.style = {
            "bg": "#1a1a1e", "sidebar_bg": "#252529", "tile_bg": "#333338",
            "green": "#53a653", "yellow": "#d9b326", "grey": "#4a4a4e",
            "text": "#ffffff", "strike": "#ff4d4d", "gold": "#ffd700"
        }

        self.init_game_vars()
        self.show_nickname_screen()

def init_game_vars(self):
        self.target = "".join([str(random.randint(0, 9)) for _ in range(self.word_len)])
        self.current_row = 0
        self.current_col = 0
        self.guesses = [["" for _ in range(self.word_len)] for _ in range(self.num_tries)]
        self.number_statuses = {str(i): 'unused' for i in range(10)}

    def load_scores(self):
        if os.path.exists(self.scores_file):
            try:
                with open(self.scores_file, "r") as f:
                    return json.load(f)
            except: return []
        return []

    def save_score(self, tries):
        scores = self.load_scores()
