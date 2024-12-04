import sqlite3
import random
import time
import tkinter as tk
import re
import hashlib

# Connect to SQLite database
conn = sqlite3.connect('riddledb.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS playerinfo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    classic_completion TEXT NOT NULL DEFAULT 'not_completed',
    best_score INTEGER NOT NULL DEFAULT 0
)
''')
conn.commit()

def is_valid_username(username):
    """Validate username: alphanumeric, max 16 characters, no spaces or special characters."""
    return re.fullmatch(r'[A-Za-z0-9]{1,16}', username) is not None

def hash_password(password):
    """Hash the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def sign_up(username, password):
    """Sign up a new player with a password."""
    if not is_valid_username(username):
        return {"success": False, "message": "Invalid username. Please use only alphanumeric characters (max 16)."}

    if len(password) < 6:
        return {"success": False, "message": "Password must be at least 6 characters long."}

    # Hash the password before storing it in the database
    password_hash = hash_password(password)

    try:
        c.execute("INSERT INTO playerinfo (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        return {"success": True, "message": f"Sign-up successful! Welcome, {username}!"}
    except sqlite3.IntegrityError:
        return {"success": False, "message": "Username already exists. Please choose a different one."}

def login(username, password):
    """Login an existing player with a password."""
    c.execute("SELECT password_hash FROM playerinfo WHERE username = ?", (username,))
    user = c.fetchone()

    if user and user[0] == hash_password(password):
        return {"success": True, "message": f"Login successful! Welcome back, {username}!"}
    else:
        return {"success": False, "message": "Invalid username or password. Please try again."}

def continue_as_guest():
    """Handles creating a guest account and inserting it into the database."""
    guest_username = f"player_{random.randint(1000, 9999)}"
    
    c.execute("SELECT COUNT(*) FROM playerinfo WHERE username = ?", (guest_username,))
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO playerinfo (username, password_hash) VALUES (?, ?)", (guest_username, hash_password("guest")))
        conn.commit()
        return guest_username
    else:
        return continue_as_guest()

# Fetch questions by difficulty
def fetch_questions(difficulty):
    c.execute("SELECT * FROM riddles WHERE difficulty = ?", (difficulty,))
    questions = c.fetchall()
    print(f"Fetched {len(questions)} questions for {difficulty} difficulty.")
    return questions

# Fetch additional Medium1 riddles for Time Challenge Mode
def fetch_time_challenge_questions():
    print("Fetching questions for Time Challenge Mode...")
    c.execute("SELECT * FROM riddles WHERE difficulty = 'Medium1'")
    questions = c.fetchall()
    print(f"Fetched {len(questions)} questions for Time Challenge Mode.")
    return questions

# Main GUI class
class RiddleGameGUI:
    def __init__(self, root, conn):
        self.root = root
        self.conn = conn
        self.root.title("Riddle Game")
        self.root.geometry("1000x500")
        self.mode = None
        self.hp = 5
        self.progress = 0
        self.questions_classic = []
        self.questions_time_challenge = []
        self.current_question_classic = None
        self.current_question_time_challenge = None
        self.score = 0
        self.current_streak = 0
        self.highest_streak = 0
        self.start_time = None
        self.pause_time = None
        self.remaining_time = 180
        self.total_deduction = 0
        self.feedback_label = None
        self.stats_label = None
        self.difficulties = ["Easy", "Medium", "Hard"]
        self.required_correct = {"Easy": 7, "Medium": 7, "Hard": 7}
        self.current_difficulty = 0 
        self.questions_data = {difficulty: fetch_questions(difficulty) for difficulty in self.difficulties}
        self.player = None
        self.resume_available = {"Classic": False, "Time Challenge": False}
        
        self.login_screen()

    def set_feedback(self, message):
        """Displays feedback to the user."""
        light_red_color = "#f44336" 

        if not self.feedback_label or not self.feedback_label.winfo_exists():
            self.feedback_label = tk.Label(self.root, font=("Helvetica", 14), fg=light_red_color, bg="#001f3d")
            self.feedback_label.pack(pady=10)
        self.feedback_label.config(text=message, fg=light_red_color)

    def login_screen(self):
        """Displays the login screen."""
        self.clear_frame()
        self.root.config(bg="#001f3d")

        tk.Label(self.root, text="Welcome to the Riddle Solving Game!", font=("Helvetica", 18), fg="white", bg="#001f3d").pack(pady=20)

        button_color = "#2b5c8a" 

        tk.Button(self.root, text="Sign Up", command=self.sign_up_menu, font=("Helvetica", 14), bg=button_color, fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").pack(pady=(50, 10))
        tk.Button(self.root, text="Login", command=self.login_menu, font=("Helvetica", 14), bg=button_color, fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").pack(pady=10)
        tk.Button(self.root, text="Continue as Guest", command=self.continue_as_guest_menu, font=("Helvetica", 14), bg=button_color, fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit, font=("Helvetica", 14), bg="#f44336", fg="white", bd=2, relief="solid", activebackground="#f44336", activeforeground="white").pack(pady=10) 
        print("Welcome to the Riddle Solving Game!")
    
    def sign_up_menu(self):
        """Displays the sign-up menu."""
        self.clear_frame()
        self.root.config(bg="#001f3d") 

        tk.Label(self.root, text="Sign Up Page", font=("Helvetica", 18), fg="white", bg="#001f3d").pack(pady=20)
        tk.Label(self.root, text="Username:", font=("Helvetica", 14), fg="white", bg="#001f3d").pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.username_entry.pack(pady=5)
        tk.Label(self.root, text="Password:", font=("Helvetica", 14), fg="white", bg="#001f3d").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", font=("Helvetica", 14))
        self.password_entry.pack(pady=5)
      
        button_color = "#2b5c8a"
        tk.Button(self.root, text="Sign Up", command=self.process_sign_up, font=("Helvetica", 14), bg=button_color, fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").pack(pady=10)
        tk.Button(self.root, text="Back", command=self.login_screen, font=("Helvetica", 14), bg=button_color, fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").pack(pady=10)
        print("Sign Up Page")

    def process_sign_up(self):
        """Handles the sign-up process."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        result = sign_up(username, password)

        self.set_feedback(result["message"])

        if result["success"]:
            self.player = username
            self.main_menu_sign_up()
            print("Sign-up successful. Welcome, {}!".format(username))
        else:
            print("Sign-up failed. Please try again.")

    def login_menu(self):
        """Displays the login menu."""
        self.clear_frame()
        self.root.config(bg="#001f3d")

        tk.Label(self.root, text="Login Page", font=("Helvetica", 18), fg="white", bg="#001f3d").pack(pady=20)
        tk.Label(self.root, text="Username:", font=("Helvetica", 14), fg="white", bg="#001f3d").pack(pady=5)
        
        self.username_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:", font=("Helvetica", 14), fg="white", bg="#001f3d").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", font=("Helvetica", 14))
        self.password_entry.pack(pady=5)
        
        button_color = "#2b5c8a"

        tk.Button(self.root, text="Login", command=self.process_login, font=("Helvetica", 14), bg=button_color, fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").pack(pady=10)
        tk.Button(self.root, text="Back", command=self.login_screen, font=("Helvetica", 14), bg=button_color, fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").pack(pady=10)
        print("Login Page")
    
    def process_login(self):
        """Handles the login process."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        result = login(username, password)

        self.set_feedback(result["message"])

        if result["success"]:
            self.player = username
            self.main_menu_login()
            print("Login successful. Welcome, {}!".format(username))
        else:  
            print("Login failed. Please try again.")

    def continue_as_guest_menu(self):
        """Handles continue as guest functionality."""
        guest_username = continue_as_guest()
        self.player = guest_username
        self.set_feedback(f"Guest account created: {guest_username}. Welcome!")
        self.main_menu_guest()
        print("Guest account created. Welcome, {}!".format(guest_username))

    def main_menu(self):
        """Displays the main menu."""
        self.clear_frame()
        self.root.unbind_all("<MouseWheel>") 
        self.root.unbind_all("<Button-4>")
        self.root.unbind_all("<Button-5>")

        self.root.config(bg="#001f3d")

        tk.Label(self.root, text="Riddle Solving Game", font=("Helvetica", 18), fg="white", bg="#001f3d").pack(pady=20)
        tk.Label(self.root, text=f"Currently playing as: {self.player}", font=("Helvetica", 14), fg="#66cc66", bg="#001f3d").pack(pady=10)
        tk.Label(self.root, text="Select a Gameplay Mode:", font=("Helvetica", 14), fg="white", bg="#001f3d").pack(pady=20)

        mode_button_color = "#2b5c8a"

        if self.resume_available["Classic"]:
            tk.Button(self.root, text="Resume Classic Mode", command=self.resume_classic_mode, font=("Helvetica", 14), bg=mode_button_color, fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").pack(pady=10)
        else:
            tk.Button(self.root, text="Classic Mode", command=self.classic_mode, font=("Helvetica", 14), bg=mode_button_color, fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").pack(pady=10)

        if self.resume_available["Time Challenge"]:
            tk.Button(self.root, text="Resume Time Challenge Mode", command=self.resume_time_challenge_mode, font=("Helvetica", 14), bg=mode_button_color, fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").pack(pady=10)
        else:
            tk.Button(self.root, text="Time Challenge Mode", command=self.time_challenge_mode, font=("Helvetica", 14), bg=mode_button_color, fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").pack(pady=10)

        tk.Button(self.root, text="Exit", command=self.root.quit, font=("Helvetica", 14), bg="#f44336", fg="white", bd=2, relief="solid", activebackground="#f44336", activeforeground="white").pack(pady=10)

        tk.Button(self.root, text="Leaderboard", command=self.leaderboard, font=("Helvetica", 12), bg="#2b5c8a", fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").place(x=10, y=10)

        canvas = tk.Canvas(self.root, width=35, height=35, bg="#001f3d", highlightthickness=0)
        canvas.place(x=955, y=5)
        canvas.create_oval(5, 5, 30, 30, fill="#001f3d", outline="white", width=2)
        canvas.create_text(17.5, 17.5, text="!", font=("Helvetica", 14, "bold"), fill="white") 
        canvas.bind("<Button-1>", self.game_instruction)

        tk.Button(self.root, text="Leaderboard", command=self.leaderboard, font=("Helvetica", 12), bg="#2b5c8a", fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").place(x=10, y=10)
        print("Main Menu")

    def main_menu_sign_up(self):
        """Displays the main menu."""
        self.clear_frame()
        self.root.config(bg="#001f3d")

        tk.Label(self.root, text="Riddle Solving Game", font=("Helvetica", 18), fg="white", bg="#001f3d").pack(pady=20)
        tk.Label(self.root, text=f"Welcome, {self.player}!", font=("Helvetica", 14), fg="#66cc66", bg="#001f3d").pack(pady=10)
        tk.Label(self.root, text="Select a Gameplay Mode:", font=("Helvetica", 14), fg="white", bg="#001f3d").pack(pady=20)

        mode_button_color = "#2b5c8a"
        tk.Button(self.root, text="Classic Mode", command=self.classic_mode, font=("Helvetica", 14), bg=mode_button_color, fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").pack(pady=10)
        tk.Button(self.root, text="Time Challenge Mode", command=self.time_challenge_mode, font=("Helvetica", 14), bg=mode_button_color, fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit, font=("Helvetica", 14), bg="#f44336", fg="white", bd=2, relief="solid", activebackground="#f44336", activeforeground="white").pack(pady=10)

        tk.Label(self.root, text="Successfully signed up!", font=("Helvetica", 14), fg="#66cc66", bg="#001f3d").pack(pady=10)

        canvas = tk.Canvas(self.root, width=35, height=35, bg="#001f3d", highlightthickness=0)
        canvas.place(x=955, y=5)
        canvas.create_oval(5, 5, 30, 30, fill="#001f3d", outline="white", width=2)
        canvas.create_text(17.5, 17.5, text="!", font=("Helvetica", 14, "bold"), fill="white")
        canvas.bind("<Button-1>", self.game_instruction)

        tk.Button(self.root, text="Leaderboard", command=self.leaderboard, font=("Helvetica", 12), bg=mode_button_color, fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").place(x=10, y=10)
        print("Main Menu")

    def main_menu_login(self):
        """Displays the main menu."""
        self.clear_frame()
        self.root.config(bg="#001f3d")  # Set background color for the window to a very dark blue

        tk.Label(self.root, text="Riddle Solving Game", font=("Helvetica", 18), fg="white", bg="#001f3d").pack(pady=20)
        tk.Label(self.root, text=f"Welcome back, {self.player}!", font=("Helvetica", 14), fg="#66cc66", bg="#001f3d").pack(pady=10)
        tk.Label(self.root, text="Select a Gameplay Mode:", font=("Helvetica", 14), fg="white", bg="#001f3d").pack(pady=20)

        # Buttons with custom colors
        mode_button_color = "#2b5c8a"  # Darker blue color for buttons
        tk.Button(self.root, text="Classic Mode", command=self.classic_mode, font=("Helvetica", 14), bg=mode_button_color, fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").pack(pady=10)
        tk.Button(self.root, text="Time Challenge Mode", command=self.time_challenge_mode, font=("Helvetica", 14), bg=mode_button_color, fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit, font=("Helvetica", 14), bg="#f44336", fg="white", bd=2, relief="solid", activebackground="#f44336", activeforeground="white").pack(pady=10)

        tk.Label(self.root, text="Successfully logged in!", font=("Helvetica", 14), fg="#66cc66", bg="#001f3d").pack(pady=10)

        canvas = tk.Canvas(self.root, width=35, height=35, bg="#001f3d", highlightthickness=0)
        canvas.place(x=955, y=5)
        canvas.create_oval(5, 5, 30, 30, fill="#001f3d", outline="white", width=2)
        canvas.create_text(17.5, 17.5, text="!", font=("Helvetica", 14, "bold"), fill="white")
        canvas.bind("<Button-1>", self.game_instruction)

        tk.Button(self.root, text="Leaderboard", command=self.leaderboard, font=("Helvetica", 12), bg=mode_button_color, fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").place(x=10, y=10)

    def main_menu_guest(self):
        """Displays the main menu."""
        self.clear_frame()
        self.root.config(bg="#001f3d")

        tk.Label(self.root, text="Riddle Solving Game", font=("Helvetica", 18), fg="white", bg="#001f3d").pack(pady=20)
        tk.Label(self.root, text=f"Welcome, {self.player}!", font=("Helvetica", 14), fg="#66cc66", bg="#001f3d").pack(pady=10)
        tk.Label(self.root, text="Select a Gameplay Mode:", font=("Helvetica", 14), fg="white", bg="#001f3d").pack(pady=20)

        mode_button_color = "#2b5c8a"
        tk.Button(self.root, text="Classic Mode", command=self.classic_mode, font=("Helvetica", 14), bg=mode_button_color, fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").pack(pady=10)
        tk.Button(self.root, text="Time Challenge Mode", command=self.time_challenge_mode, font=("Helvetica", 14), bg=mode_button_color, fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit, font=("Helvetica", 14), bg="#f44336", fg="white", bd=2, relief="solid", activebackground="#f44336", activeforeground="white").pack(pady=10)

        tk.Label(self.root, text="You are currently playing as a guest.", font=("Helvetica", 14), fg="#66cc66", bg="#001f3d").pack(pady=10)

        canvas = tk.Canvas(self.root, width=35, height=35, bg="#001f3d", highlightthickness=0)
        canvas.place(x=955, y=5)
        canvas.create_oval(5, 5, 30, 30, fill="#001f3d", outline="white", width=2)
        canvas.create_text(17.5, 17.5, text="!", font=("Helvetica", 14, "bold"), fill="white")
        canvas.bind("<Button-1>", self.game_instruction)

        tk.Button(self.root, text="Leaderboard", command=self.leaderboard, font=("Helvetica", 12), bg=mode_button_color, fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").place(x=10, y=10)
        print("Main Menu")

    def game_instruction(self, event=None):
        self.clear_frame()

        # Fetch player data from the database
        classic_mode_status, highest_score = self.fetch_player_data(self.player)
        
        if classic_mode_status is None:
            player_status = "Player not found."
        else:
            # Determine the classic mode status (Completed or Not Completed)
            classic_mode_status = "Completed" if classic_mode_status == "completed" else "Not_Completed"
            player_status = f"Name: {self.player:<30}Classic Mode: {classic_mode_status:<30}Highest Score: {highest_score}"

        tk.Label(self.root, text=player_status, font=("Helvetica", 14), anchor="w", fg="white", bg="#001f3d").place(x=10, y=15)
        tk.Button(self.root, text="Back", command=self.main_menu, font=("Helvetica", 12), bg="#2b5c8a", fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").place(x=940, y=10)

        # Game instructions text
        instructions = """
        Welcome to the Riddle Solving Game!
        
        In this game, you will get to test your brain by solving a series of riddles.
        
        Based on your critical analysis and logical reasoning, you will be able to complete it.
        
        There are 2 modes for you to choose from.
        _______________________________________________________________________________

        - Classic Mode: 
        
        You will have 5 lives to solve 21 riddles. 
        
        This series of riddles is divided into 3 levels of difficulty,
        
        specifically 7 for easy level, 7 for medium level, and 7 for hard level.
        _______________________________________________________________________________

        - Time Challenge Mode:
        
        You will have 3 minutes to solve as many riddles as possible.

        However, this mode is only consisted of 20 riddles.

        1 riddle = 1 score. Try to streak up as many as you can.

        Your final score is your score multiplied by your highest streak.

        
        Good luck and have fun!
        _______________________________________________________________________________

        """

        tk.Label(self.root, text=("_" * 89), font=("Helvetica", 14), fg="white", bg="#001f3d").place(x=10, y=45)
        tk.Label(self.root, text="Game Instructions:", font=("Helvetica", 14, 'bold'), fg="white", bg="#001f3d").place(x=10, y=85)
        tk.Label(self.root, text=("_" * 89), font=("Helvetica", 14), fg="white", bg="#001f3d").place(x=10, y=106)

        # Create a container frame for the scrollable area
        container = tk.Frame(self.root, width=970, height=400, bg="#001f3d")
        container.place(x=0, y=150)  # Place container below the title and heading

        # Create canvas and scrollbar
        canvas = tk.Canvas(container, width=970, height=330, bg="#001f3d", highlightthickness=0, borderwidth=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create a frame inside the canvas to hold the instructions text
        frame = tk.Frame(canvas, bg="#001f3d")
        canvas.create_window((0, 0), window=frame, anchor="nw")

        # Add the instructions text to the frame with word wrapping
        label = tk.Label(frame, text=instructions, font=("Helvetica", 14), justify="left", wraplength=980, fg="white", bg="#001f3d")
        label.pack(padx=20, pady=(0,10))  # Add some padding for better indentation

        # Update the scroll region of the canvas to match the frame size
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        def on_mouse_wheel(event):
            if event.delta:  # Windows/Linux
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            elif event.num == 4:  # macOS (scroll up)
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:  # macOS (scroll down)
                canvas.yview_scroll(1, "units")

        # Bind scrolling events
        canvas.bind_all("<MouseWheel>", on_mouse_wheel)
        canvas.bind_all("<Button-4>", on_mouse_wheel)
        canvas.bind_all("<Button-5>", on_mouse_wheel)
        print("Game instructions displayed")

    def fetch_player_data(self, username):
        """Fetch player info from the database based on username."""
        c = self.conn.cursor()
        c.execute("SELECT classic_completion, best_score FROM playerinfo WHERE username = ?", (username,))
        player_data = c.fetchone()
        
        if player_data:
            classic_completion, best_score = player_data
            return classic_completion, best_score
        else:
            return None, None

    def leaderboard(self):
        """Displays the leaderboard."""
        self.clear_frame()
        
        tk.Button(self.root, text="Back", command=self.main_menu, font=("Helvetica", 12), bg="#2b5c8a", fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").place(x=940, y=10)
        tk.Label(self.root, text="Player Leaderboard", font=("Helvetica", 14, "bold"), fg="white", bg="#001f3d", activebackground="#2b5c8a", activeforeground="white").pack(pady=20)

        # Fetch top 20 players with a best_score from the database, ordered by best_score
        cursor = self.conn.cursor()
        cursor.execute(''' 
            SELECT username, classic_completion, best_score 
            FROM playerinfo 
            WHERE best_score IS NOT NULL  -- Exclude players without a best score
            ORDER BY best_score DESC, ROWID DESC, username ASC  -- Order by best score, then by ROWID (newer players first), then by username
            LIMIT 20
        ''')
        leaderboard_data = cursor.fetchall()

        header_frame = tk.Frame(self.root, bg="#001f3d")
        header_frame.pack(pady=5)

        tk.Label(header_frame, text="=" * 84, font=("Helvetica", 14), fg="white", bg="#001f3d", anchor="w").grid(row=0, column=0, columnspan=4)
        tk.Label(header_frame, text="Rank", font=("Helvetica", 14, "bold"), width=10, fg="white", bg="#001f3d", anchor="w").grid(row=1, column=0, padx=10)
        tk.Label(header_frame, text="Name", font=("Helvetica", 14, "bold"), width=25, fg="white", bg="#001f3d", anchor="w").grid(row=1, column=1, padx=10)
        tk.Label(header_frame, text="Classic Completion", font=("Helvetica", 14, "bold"), width=25, fg="white", bg="#001f3d", anchor="w").grid(row=1, column=2, padx=10)
        tk.Label(header_frame, text="Best Score", font=("Helvetica", 14, "bold"), width=10, fg="white", bg="#001f3d", anchor="w").grid(row=1, column=3, padx=10)
        tk.Label(header_frame, text="=" * 84, font=("Helvetica", 14), fg="white", bg="#001f3d", anchor="w").grid(row=2, column=0, columnspan=4)

        # Create a container frame for the scrollable area
        container = tk.Frame(self.root, width=960, height=350, bg="#001f3d")
        container.pack(pady=10, padx=20, fill="both", expand=True)

        # Create canvas and scrollbar
        canvas = tk.Canvas(container, width=940, height=350, bg="#001f3d", highlightthickness=0, borderwidth=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create a frame inside the canvas for leaderboard rows
        frame = tk.Frame(canvas, bg="#001f3d")
        canvas.create_window((0, 0), window=frame, anchor="nw")

        # Populate the leaderboard data
        for rank, (username, classic_completion, best_score) in enumerate(leaderboard_data, start=1):
            tk.Label(frame, text=str(rank), font=("Helvetica", 14), width=10, fg="white", bg="#001f3d", anchor="w").grid(row=rank, column=0, padx=(20, 0), pady=5)
            tk.Label(frame, text=username, font=("Helvetica", 14), width=25, fg="white", bg="#001f3d", anchor="w").grid(row=rank, column=1, padx=(28,0), pady=5)
            tk.Label(frame, text=classic_completion, font=("Helvetica", 14), width=25, fg="white", bg="#001f3d", anchor="w").grid(row=rank, column=2, padx=(48,0), pady=5)
            tk.Label(frame, text=str(best_score), font=("Helvetica", 14), width=10, fg="white", bg="#001f3d", anchor="w").grid(row=rank, column=3, padx=(43, 0), pady=5)

        # Add scrolling for Windows, Linux, and macOS
        def on_mouse_wheel(event):
            """Handles mouse wheel scrolling."""
            if event.delta:  # Windows/Linux
                canvas.yview_scroll(-1 * int(event.delta / 120), "units")
            elif event.num == 4:  # macOS (scroll up)
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:  # macOS (scroll down)
                canvas.yview_scroll(1, "units")

        # Bind scrolling events
        canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # Windows/Linux
        canvas.bind_all("<Button-4>", on_mouse_wheel)   # macOS scroll up
        canvas.bind_all("<Button-5>", on_mouse_wheel)   # macOS scroll down
        print("Leaderboard displayed")

    def classic_mode(self):
        """Starts the Classic Mode."""
        print("Starting Classic Mode...")
        self.mode = "Classic"
        self.hp = 5
        self.progress = 0
        self.questions_classic = random.sample(self.questions_data[self.difficulties[self.current_difficulty]], 
                                    len(self.questions_data[self.difficulties[self.current_difficulty]]))
        self.last_feedback = None
        self.show_question()

    def time_challenge_mode(self):
        """Starts the Time Challenge Mode."""
        print("Starting Time Challenge Mode...")
        self.mode = "Time Challenge"
        self.score = 0
        self.highest_streak = 0
        self.current_streak = 0
        self.start_time = time.time()
        self.remaining_time = 180
        self.total_deduction = 0
        self.last_feedback = None
        self.questions_time_challenge = random.sample(fetch_time_challenge_questions(), len(fetch_time_challenge_questions()))
        self.show_question()
        self.update_time_display()
    
    def update_time_display(self):
        """Update the time display every 1000ms (1 second)."""
        if self.mode == "Time Challenge":
            elapsed_time = int(time.time() - self.start_time)
            self.remaining_time = max(0, 180 - elapsed_time - self.total_deduction)

            # Check if stats_label needs to be created or updated
            if not hasattr(self, 'stats_label') or self.stats_label is None or not self.stats_label.winfo_exists():
                self.stats_label = tk.Label(self.root, text="", font=("Helvetica", 14))
                self.stats_label.pack(pady=10)
            
            # Update the time display in the UI
            stats_text = f"Time Left: {self.remaining_time}s | Score: {self.score} | Current Streak: {self.current_streak} | Highest Streak: {self.highest_streak}"
            self.stats_label.config(text=stats_text)

            # Continue updating every 1 second if the remaining time is more than 0
            if self.remaining_time > 0:
                self.root.after(1000, self.update_time_display)  # Call this function again after 1 second
            else:
                self.complete_time_challenge_mode()

    def show_question(self, resume=False):
        """Displays the current question and options."""
        current_question = None

        if self.mode == "Classic":
            if not resume:
                if not self.questions_classic:
                    self.complete_classic_mode()
                    return
                self.current_question_classic = self.questions_classic.pop(0)
            current_question = self.current_question_classic
        elif self.mode == "Time Challenge":
            if not resume:
                if not self.questions_time_challenge:
                    self.complete_time_challenge_mode()
                    return
                self.current_question_time_challenge = self.questions_time_challenge.pop(0)
            current_question = self.current_question_time_challenge

        self.clear_frame()
        button_color = "#2b5c8a"
        main_bg_color = "#001f3d"

        tk.Button(self.root, text="Back", command=self.return_to_main_menu, font=("Helvetica", 12), bg=button_color, fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").place(x=10, y=10)
        tk.Button(self.root, text="Restart", command=self.restart_mode, font=("Helvetica", 12), bg=button_color, fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").place(x=925, y=10)
        tk.Label(self.root, text=f"Riddle: {current_question[1]}", font=("Helvetica", 16), wraplength=600, fg="white", bg=main_bg_color).pack(pady=20)

        # Display options
        for i in range(2, 6):
            option = current_question[i]
            tk.Button(self.root, text=option, command=lambda i=i-1: self.check_answer(i), font=("Helvetica", 14), wraplength=500, bg=button_color, fg="white", bd=2, relief="solid", activebackground="#2b5c8a", activeforeground="white").pack(pady=5)

        # Feedback and Stats
        if not hasattr(self, 'feedback_label') or not self.feedback_label.winfo_exists():
            self.feedback_label = tk.Label(self.root, text="", font=("Helvetica", 14), fg="blue", bg=main_bg_color)
            self.feedback_label.pack(pady=10)
        else:
            self.feedback_label.config(text="", fg="blue", bg=main_bg_color)

        if self.mode == "Time Challenge":
            stats_text = f"Time Left: {self.remaining_time}s | Score: {self.score} | Current Streak: {self.current_streak} | Highest Streak: {self.highest_streak}"
            if not hasattr(self, 'stats_label') or self.stats_label is None or not self.stats_label.winfo_exists():
                self.stats_label = tk.Label(self.root, text=stats_text, font=("Helvetica", 14), fg="white", bg=main_bg_color)
                self.stats_label.pack(pady=10)
            else:
                self.stats_label.config(text=stats_text, fg="white", bg=main_bg_color)
        else:
            stats_text = f"HP: {self.hp} | {self.difficulties[self.current_difficulty]} Level | Progress: {self.progress}/{self.required_correct[self.difficulties[self.current_difficulty]]}"
            if not hasattr(self, 'stats_label') or self.stats_label is None or not self.stats_label.winfo_exists():
                self.stats_label = tk.Label(self.root, text=stats_text, font=("Helvetica", 14), fg="white", bg=main_bg_color)
                self.stats_label.pack(pady=10)
            else:
                self.stats_label.config(text=stats_text, fg="white", bg=main_bg_color)

        # Display feedback if available
        if hasattr(self, 'last_feedback'):
            self.feedback_label.config(text=self.last_feedback, fg="#66cc66" if self.last_feedback == "Correct!" else "#f44336")
            self.last_feedback = None

    def resume_classic_mode(self):
        """Resumes the classic mode."""
        print("Resuming Classic Mode...")
        self.mode = "Classic"
        self.show_question(resume=True)
    
    def resume_time_challenge_mode(self):
        """Resumes the Time Challenge Mode."""
        print("Resuming Time Challenge Mode...")
        self.mode = "Time Challenge"
        if self.pause_time:
            paused_duration = time.time() - self.pause_time
            self.start_time += paused_duration
            self.pause_time = None
        self.update_time_display()
        self.show_question(resume=True)
   
    def return_to_main_menu(self):
        """Returns to the main menu and allows resume functionality."""
        if self.mode in self.resume_available:
            self.resume_available[self.mode] = True
            if self.mode == "Time Challenge":
                self.pause_time = time.time()

        self.mode = None
        self.main_menu()
        print("Game is paused.")

    def restart_mode(self):
        self.clear_frame()
        if self.mode == "Classic":
            self.current_difficulty = 0
            self.classic_mode()
            print("Restarting Classic Mode...")
        elif self.mode == "Time Challenge":
            self.time_challenge_mode()
            print("Restarting Time Challenge Mode...")
  
    def check_answer(self, choice):
        """Checks the user's answer and updates the game state."""
        correct_answer = None

        if self.mode == "Classic":
            correct_answer = self.current_question_classic[6]
        elif self.mode == "Time Challenge":
            correct_answer = self.current_question_time_challenge[6]

        print(f"User chose: {choice}, Correct answer: {correct_answer}")

        if choice == correct_answer:
            self.last_feedback = "Correct!"

            if self.mode == "Classic":
                self.progress += 1
                if self.progress >= self.required_correct[self.difficulties[self.current_difficulty]]:
                    if self.current_difficulty == 2:
                        self.complete_classic_mode()
                        self.current_difficulty = 0
                        return
                    else:
                        self.complete_difficulty()
                        return
            elif self.mode == "Time Challenge":
                self.current_streak += 1
                if self.current_streak > self.highest_streak:
                    self.highest_streak = self.current_streak
                self.score += 1
                if self.remaining_time <= 0:
                    self.complete_time_challenge_mode()
                    return
        else:
            
            self.last_feedback = "Incorrect!"
            if self.mode == "Classic":
                self.hp -= 1
                if self.hp <= 0:
                    self.end_game("Game Over! You ran out of HP.")
                    self.current_difficulty = 0
                    print("Game Over! You ran out of HP.")
                    return
            elif self.mode == "Time Challenge":
                self.current_streak = 0
                self.total_deduction += 10
                if self.remaining_time <= 0:
                    self.complete_time_challenge_mode()
                    return

        self.show_question()

    def complete_difficulty(self):
        """Handles moving to the next difficulty after completing the current one."""
        if self.current_difficulty < 2:
            self.current_difficulty += 1
            self.progress = 0
            self.questions_classic = random.sample(self.questions_data[self.difficulties[self.current_difficulty]], 
                                           len(self.questions_data[self.difficulties[self.current_difficulty]]))
            self.show_question()
        else:
            self.end_game("Congrats! You completed all difficulties in Classic Mode.")

    def complete_classic_mode(self):
        """Handles completion of Classic Mode."""
        if self.player:
            cursor = self.conn.cursor()

            # Check if the user has already completed Classic Mode
            cursor.execute("""
                SELECT classic_completion FROM playerinfo WHERE username = ?
            """, (self.player,))
            result = cursor.fetchone()

            if result and result[0] != "completed":
                # Update the classic_completion status to 'completed'
                cursor.execute("""
                    UPDATE playerinfo
                    SET classic_completion = 'completed'
                    WHERE username = ?
                """, (self.player,))
                self.conn.commit()
                print(f"Classic Mode completed for {self.player}")
        self.end_game("Congrats! You have completed the Classic Mode.")
        self.stats_label = None

    def complete_time_challenge_mode(self):
        """Called when the time challenge is completed."""
        final_score = self.score * self.highest_streak

        if self.player:
            cursor = self.conn.cursor()

            # Fetch the current best score from the database for the logged-in user
            cursor.execute("""
                SELECT best_score FROM playerinfo WHERE username = ?
            """, (self.player,))
            result = cursor.fetchone()

            # If the player exists and the new score is greater than the current best score
            if result:
                current_best_score = result[0]
                if final_score > current_best_score:
                    # Update the best_score if the new score is higher
                    cursor.execute("""
                        UPDATE playerinfo
                        SET best_score = ?
                        WHERE username = ?
                    """, (final_score, self.player))
                    self.conn.commit()
                    print(f"New highest score: {final_score}")

        # Display the final score and end the game
        self.end_game(f"Time's up! Your Score: {self.score} | Highest Streak: {self.highest_streak}\n\n\nYour Final Score: {self.score * self.highest_streak}")
        self.stats_label = None
        print(f"Time up for {self.player}. Your score is: {self.score}. Your streak is: {self.highest_streak}. Your final score is: {final_score}.")

    def end_game(self, message):
        """Ends the game and returns to the main menu."""
        self.clear_frame()
        button_color = "#2b5c8a"
        main_bg_color = "#001f3d"

        tk.Label(self.root, text=message, font=("Helvetica", 16), fg="white", bg=main_bg_color).pack(pady=20)
        replay_command = self.replay_classic if self.mode == "Classic" else self.replay_time_challenge
        tk.Button(self.root, text="Replay", command=replay_command, font=("Helvetica", 14), bg=button_color, fg="white", bd=2, relief="solid", highlightbackground="black", activebackground="#2b5c8a", activeforeground="white").pack(pady=20)
        tk.Button(self.root, text="Return to Main Menu", command=self.main_menu, font=("Helvetica", 14), bg=button_color, fg="white", bd=2, relief="solid", highlightbackground="black", activebackground="#2b5c8a", activeforeground="white").pack(pady=20)

        if self.mode == "Classic":
            self.resume_available["Classic"] = False
        elif self.mode == "Time Challenge":
            self.resume_available["Time Challenge"] = False

        # Clean up labels
        if hasattr(self, 'feedback_label'):
            self.feedback_label.destroy()
            del self.feedback_label
        if hasattr(self, 'stats_label'):
            self.stats_label.destroy()
            del self.stats_label

        self.mode = None

    def replay_classic(self):
        self.mode = "Classic"
        self.classic_mode()

    def replay_time_challenge(self):
        self.mode = "Time Challenge"
        self.time_challenge_mode()

    def clear_frame(self):
        """Clears the current frame."""
        for widget in self.root.winfo_children():
            widget.destroy()

# Create and run the game
root = tk.Tk()
game = RiddleGameGUI(root, conn)
root.mainloop()
print("Game closed.")