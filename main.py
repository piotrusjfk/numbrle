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

def draw_grid(self):
        self.tile_data = []
        self.grid_canvas.delete("all")
        for r in range(self.num_tries):
            row_tiles = []
            for c in range(self.word_len):
                x, y = c * 85 + 25, r * 85
                tids = self.draw_rounded_tile(self.grid_canvas, x, y, 75, "", self.style["tile_bg"], "white")
                row_tiles.append(tids)
            self.tile_data.append(row_tiles)

    def show_end_options(self, message, win=True):
        for widget in self.end_buttons_frame.winfo_children():
            widget.destroy()

        msg_lbl = tk.Label(self.end_buttons_frame, text=message, font=("Arial", 12, "bold"), 
                           bg=self.style["bg"], fg=self.style["green"] if win else self.style["strike"])
        msg_lbl.pack(pady=10)

        btn_frame = tk.Frame(self.end_buttons_frame, bg=self.style["bg"])
        btn_frame.pack()

        tk.Button(btn_frame, text="KONTYNUUJ JAKO TEN SAM GRACZ", font=("Arial", 10, "bold"),
                  bg=self.style["green"], fg="white", relief=tk.FLAT, padx=10, pady=5,
                  command=self.continue_same_player, cursor="hand2").pack(side=tk.LEFT, padx=10)

        tk.Button(btn_frame, text="ZACZNIJ JAKO INNY GRACZ", font=("Arial", 10, "bold"),
                  bg=self.style["grey"], fg="white", relief=tk.FLAT, padx=10, pady=5,
                  command=self.show_nickname_screen, cursor="hand2").pack(side=tk.LEFT, padx=10)
    def continue_same_player(self):
        self.init_game_vars()
        for widget in self.end_buttons_frame.winfo_children():
            widget.destroy()
        self.draw_grid()
        self.update_number_panel_visuals()
        self.root.bind("<Key>", self.handle_keypress)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def update_leaderboard_ui(self):
        for widget in self.leaderboard_container.winfo_children():
            widget.destroy()
        
        scores = self.load_scores()
        for i, entry in enumerate(scores):
            color = self.style["gold"] if i == 0 else "white"
            txt = f"{i+1}. {entry['nick']} — {entry['tries']} prób"
            tk.Label(self.leaderboard_container, text=txt, font=("Arial", 11), 
                     bg=self.style["sidebar_bg"], fg=color, anchor="w").pack(fill=tk.X, pady=2)

    def register_rounded_rect(self, canvas):
        def _rect(x, y, x2, y2, r, **kwargs):
            points = (x+r, y, x2-r, y, x2, y, x2, y+r, x2, y2-r, x2, y2, x2-r, y2, x+r, y2, x, y2, x, y2-r, x, y+r, x, y)
            return canvas.create_polygon(points, **kwargs, smooth=True)
        canvas.create_rounded_rect = _rect

    def draw_rounded_tile(self, canvas, x, y, size, text, bg, fg, strike=False):
        t_id = canvas.create_rounded_rect(x, y, x+size, y+size, 12, fill=bg, outline="#4a4a4e")
        txt_id = canvas.create_text(x+size/2, y+size/2, text=text, fill=fg, font=("Arial", 24, "bold"))
        if strike:
            canvas.create_line(x+10, y+10, x+size-10, y+size-10, fill=self.style["strike"], width=3)
        return t_id, txt_id

    def handle_keypress(self, event):
        if self.current_row >= self.num_tries: return
        if event.keysym == "BackSpace":
            if self.current_col > 0:
                self.current_col -= 1
                self.guesses[self.current_row][self.current_col] = ""
                self.update_grid()
        elif event.keysym == "Return":
            if self.current_col == self.word_len: self.check_guess()
        elif event.char.isdigit():
            if self.current_col < self.word_len:
                self.guesses[self.current_row][self.current_col] = event.char
                self.current_col += 1
                self.update_grid()

def update_grid(self):
        for c in range(self.word_len):
            txt = self.guesses[self.current_row][c]
            self.grid_canvas.itemconfig(self.tile_data[self.current_row][c][1], text=txt)

    def check_guess(self):
        guess = "".join(self.guesses[self.current_row])
        colors = [""] * 5
        target_list = list(self.target)

        for i in range(5):
            if guess[i] == self.target[i]:
                colors[i] = "green"
                target_list[i] = None

        for i in range(5):
            if colors[i] == "":
                if guess[i] in target_list:
                    colors[i] = "yellow"
                    target_list[target_list.index(guess[i])] = None
                else:
                    colors[i] = "grey"

        for i, col in enumerate(colors):
            self.grid_canvas.itemconfig(self.tile_data[self.current_row][i][0], fill=self.style[col], outline=self.style[col])
            self.update_status(guess[i], col)

        self.update_number_panel_visuals()

        if guess == self.target:
            self.save_score(self.current_row + 1)
            self.root.unbind("<Key>")
            self.show_end_options(f"Kongratulejszions odgadłeś w {self.current_row+1} prób(ie).", True)
            self.current_row = 10
        elif self.current_row == self.num_tries - 1:
            self.root.unbind("<Key>")
            self.show_end_options(f"KONIEC PRÓB   Hasło to: {self.target}", False)
            self.current_row = 10
        else:
            self.current_row += 1
            self.current_col = 0
