import sqlite3
import random
import time

# Connect to SQLite database
conn = sqlite3.connect('riddledb.db')
c = conn.cursor()

# Fetch questions by difficulty
def fetch_questions(difficulty):
    c.execute("SELECT * FROM riddles WHERE difficulty = ?", (difficulty,))
    return c.fetchall()

# Fetch additional Medium1 riddles for Time Challenge Mode
def fetch_time_challenge_questions():
    c.execute("SELECT * FROM riddles WHERE difficulty = 'Medium1'")
    return c.fetchall()

# Display a question
def display_question(question):
    print(f"Riddle: {question[1]}")
    print(f"1) {question[2]}")
    print(f"2) {question[3]}")
    print(f"3) {question[4]}")
    print(f"4) {question[5]}")

# Classic Mode Game
def classic_mode():
    print("\nWelcome to Classic Mode!")
    hp = 5  # Player's lives
    difficulties = ["Easy", "Medium", "Hard"]
    required_correct = {"Easy": 7, "Medium": 7, "Hard": 7}
    riddles_data = {"Easy": fetch_questions("Easy"), 
                    "Medium": fetch_questions("Medium"),
                    "Hard": fetch_questions("Hard")}

    for difficulty in difficulties:
        print(f"\n--- {difficulty} Mode ---")
        completed = 0
        questions = random.sample(riddles_data[difficulty], len(riddles_data[difficulty]))  # Shuffle questions

        while completed < required_correct[difficulty] and hp > 0:
            print(f"Progress: {completed}/{required_correct[difficulty]} in {difficulty}")
            question = questions.pop(0)  # Get the next shuffled question
            display_question(question)
            answer = int(input("Your answer (1-4): "))
            
            if answer == question[6]:
                print("Correct!")
                completed += 1
            else:
                print("Incorrect!")
                hp -= 1
                questions.append(question)  # Append incorrect question to the end
                print(f"You have {hp} HP left.")
                
            if hp == 0:
                print("Game Over! You ran out of HP.")
                break
        
        if hp > 0:
            print(f"Completed all {difficulty} riddles!")
        else:
            print(f"You couldn't complete {difficulty} riddles. Try again later.")
            return
    
    print("Congrats! You've completed all the riddles in Classic Mode.")

# Time Challenge Mode
def time_challenge_mode():
    print("\nWelcome to Time Challenge Mode!")
    start_time = time.time()  # Record the start time
    score = 0
    streak = 0
    highest_streak = 0
    correct_answers = 0  # Initialize the counter for correct answers
    remaining_time = 180  # Initialize the remaining time to 3 minutes
    total_deduction = 0  # Initialize the total deduction time
    riddles = random.sample(fetch_time_challenge_questions(), len(fetch_time_challenge_questions()))  # Shuffle questions

    while remaining_time > 0:  # Continue until the remaining time runs out
        question = riddles.pop(0)
        display_question(question)
        answer = int(input("Your answer (1-4): "))
        
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        remaining_time = 180 - int(elapsed_time) - total_deduction  # Adjust remaining time with total deductions
        
        if answer == question[6]:
            score += 1
            streak += 1
            highest_streak = max(streak, highest_streak)
            correct_answers += 1  # Increment the counter for correct answers
            print("Correct!")
        else:
            print("Incorrect!")
            total_deduction += 10  # Increment total deduction by 10 seconds
            remaining_time = max(0, 180 - int(elapsed_time) - total_deduction)  # Ensure remaining time doesn't go negative
            print(f"Time left: {remaining_time}s")
            streak = 0  # Reset streak on wrong answer
            riddles.append(question)  # Re-add the incorrect question to the list
        
        # Break if time is up
        if remaining_time <= 0:
            break
    
    final_score = score * highest_streak
    print(f"\nTime's up! Your final score is {final_score}.")
    print(f"Your highest streak was {highest_streak}.")
    print(f"Your score is multiplied by the highest streak for a total of {final_score} points.")
    print(f"You answered {correct_answers} questions correctly.")

# Main menu function
def main_menu():
    print("Welcome to the Riddle Game! Get ready to challenge your mind with some fun riddles.")
    while True:
        print("\nSelect Game Mode:")
        print("1) Classic Mode")
        print("2) Time Challenge Mode")
        print("3) Exit")
        
        choice = input("Your choice (1-3): ")
        
        if choice == "1":
            classic_mode()
        elif choice == "2":
            time_challenge_mode()
        elif choice == "3":
            print("Exiting game. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid mode (1-3).")

# Start the game
if __name__ == "__main__":
    main_menu()