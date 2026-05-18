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

        existing_player = next((item for item in scores if item["nick"].lower() == self.nickname.lower()), None)

        if existing_player:
            if tries < existing_player["tries"]:
                existing_player["tries"] = tries
                messagebox.showinfo("nowy rekord", f"Gratulacje {self.nickname}! Twój najlepszy wynik!")
        else:
            scores.append({"nick": self.nickname, "tries": tries})

        scores = sorted(scores, key=lambda x: x['tries'])[:10]
        
        with open(self.scores_file, "w") as f:
            json.dump(scores, f)
        
        self.update_leaderboard_ui()

def show_nickname_screen(self):
        self.clear_window()
        self.login_frame = tk.Frame(self.root, bg=self.style["bg"])
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.login_frame, text="PODAJ SWÓJ NICK", font=("Arial", 24, "bold"), 
                 bg=self.style["bg"], fg=self.style["text"]).pack(pady=20)
        
        self.nick_entry = tk.Entry(self.login_frame, font=("Arial", 18), justify="center", 
                                  bg="#333338", fg="white", insertbackground="white", bd=0)
        self.nick_entry.pack(pady=10, ipady=5)
        self.nick_entry.focus_set()

        btn = tk.Button(self.login_frame, text="ZALOGUJ I GRAJ", font=("Arial", 12, "bold"), 
                        bg=self.style["green"], fg="white", command=self.start_game, 
                        width=20, relief=tk.FLAT, cursor="hand2")
        btn.pack(pady=20)
        self.root.bind('<Return>', lambda e: self.start_game())

    def start_game(self):
        name = self.nick_entry.get().strip()
        if not name:
            messagebox.showwarning("Wpisz swój nick!")
            return
        self.nickname = name
        self.login_frame.destroy()
        self.root.unbind('<Return>')
        self.setup_main_ui()

    def setup_main_ui(self):
        self.clear_window()
        
        self.left_sidebar = tk.Frame(self.root, width=250, bg=self.style["sidebar_bg"], padx=15, pady=20)
        self.left_sidebar.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(self.left_sidebar, text="TOP 10 GRACZY", font=("Arial", 16, "bold"), 
                 bg=self.style["sidebar_bg"], fg=self.style["gold"]).pack(pady=(0,20))
        self.leaderboard_container = tk.Frame(self.left_sidebar, bg=self.style["sidebar_bg"])
        self.leaderboard_container.pack(fill=tk.BOTH)
        self.update_leaderboard_ui()

        self.right_sidebar = tk.Frame(self.root, width=250, bg=self.style["sidebar_bg"], padx=15, pady=20)
        self.right_sidebar.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Label(self.right_sidebar, text="ZASADY", font=("Arial", 16, "bold"), 
                 bg=self.style["sidebar_bg"], fg=self.style["text"]).pack(pady=(0,20))
        
        rules_text = (
            "• Odgadnij 5 cyfr\n"
            "• Masz 6 prób\n\n"
            "KOLORY:\n"
            "● ZIELONY: Trafione!\n"
            "● ŻÓŁTY: Złe miejsce\n"
            "● SZARY: Brak w haśle\n\n"
            "STEROWANIE:\n"
            "ENTER: Zatwierdź\n"
            "BACKSPACE: Usuń"
        )
        tk.Label(self.right_sidebar, text=rules_text, font=("Arial", 11), 
                 bg=self.style["sidebar_bg"], fg="#cccccc", justify="left").pack()
                self.game_container = tk.Frame(self.root, bg=self.style["bg"])
        self.game_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.welcome_lbl = tk.Label(self.game_container, text=f"Witaj, {self.nickname}!", 
                                    font=("Arial", 14), bg=self.style["bg"], fg="#888888")
        self.welcome_lbl.pack(pady=10)
        
        self.grid_canvas = tk.Canvas(self.game_container, width=450, height=520, bg=self.style["bg"], highlightthickness=0)
        self.grid_canvas.pack()
        self.register_rounded_rect(self.grid_canvas)

        self.draw_grid()

        tk.Label(self.game_container, text="TWOJE CYFRY:", font=("Arial", 10, "bold"), 
                 bg=self.style["bg"], fg="#888888").pack(pady=(15,0))
        self.num_canvas = tk.Canvas(self.game_container, width=400, height=140, bg=self.style["bg"], highlightthickness=0)
        self.num_canvas.pack()
        self.register_rounded_rect(self.num_canvas)
        self.update_number_panel_visuals()

        self.end_buttons_frame = tk.Frame(self.game_container, bg=self.style["bg"])
        self.end_buttons_frame.pack(pady=10)

        self.root.bind("<Key>", self.handle_keypress)
