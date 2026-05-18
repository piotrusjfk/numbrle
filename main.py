import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import random
import json
import os

class NumbrleDeluxe:
    def __init__(self, root):
        self.root = root
        self.root.title("Numbrle Deluxe - Pro")
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
