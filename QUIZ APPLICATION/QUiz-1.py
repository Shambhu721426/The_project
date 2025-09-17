import pandas as pd
import os
import json
import time
import threading
import sys
import shutil
import time
#hi i am shambhu
#------------------- title part -----------------
def print_app_title():
    title = " QUIZ APPLICATION "
    border = "═" * (len(title) + 4)
    
    # get terminal width
    term_width = shutil.get_terminal_size().columns
    
    # build lines
    top = f"╔{border}╗"
    mid = f"║  {title}  ║"
    bottom = f"╚{border}╝"    
    
    # calculate padding for center
    def center_line(line):
        return line.center(term_width)
    
    print("\n" * 1)   # some top spacing
    print(center_line(top))
    print(center_line(mid))
    print(center_line(bottom))
    print("\n")


# ---------------- PASSWORD SET FUNCTION ----------------
def set_password(min_length=6):    # default len is 6 
    while True:
        pwd = input("Enter a password: ")

        has_upper = False
        has_lower = False
        has_digit = False
        has_special = False
        has_space = " " in pwd   # 🔹 check for space

        special_chars = "!@#$%^&*()-_=+[{]}\|;:'\",<.>/?"

        for ch in pwd:
            if ch.isupper():
                has_upper = True
            elif ch.islower():
                has_lower = True
            elif ch.isdigit():
                has_digit = True
            elif ch in special_chars:
                has_special = True

        pass_length = len(pwd) >= min_length

        if pass_length and has_upper and has_lower and has_digit and has_special and not has_space:
            print("🎉 Password successfully.")
            return pwd   # exit loop when password is correct
        else:
            print("❌ Password is NOT valid.")
            print("   📌 Password must contain:")
            if not pass_length:
                print("    - At least 8 characters")
            if not has_upper:
                print("    - At least one uppercase letter")
            if not has_lower:
                print("    - At least one lowercase letter")
            if not has_digit:
                print("    - At least one digit")
            if not has_special:
                print("    - At least one special character (!@#$ etc.)")
            if has_space:
                print("    - No spaces allowed in the password")
            print("\n⚠ Please try again.\n")


# ---------------- USER HANDLING ----------------
def load_users():
    if os.path.exists("dataBase.json"):
        with open("dataBase.json", "r") as f:
            return json.load(f)
    return []


def save_users(users):
    with open("dataBase.json", "w") as f:
        json.dump(users, f, indent=4)

#  ------------REGISTER PART-----------------
def register_user():
    users = load_users()

    while True:   # keep asking until unique username
        username = input("Enter username: ")

        # check if username already exists
        if any(user["username"] == username for user in users):
            print("❌ This username already exists. Try another one.\n")
        else:
            break   # ✅ unique username found

    password = set_password()   # ✅ this will return the password

    # Add new user
    user_data = {"username": username, "password": password}
    users.append(user_data)
    save_users(users)
    print(user_data)
    print(f"✅ User '{username}' registered successfully!")


#  ------------LOGIN PART-------------------
def login_user():
    print("\n--- Login your account ---")
    users = load_users()
    username = input("Enter username: ")
    password = input("Enter password: ")

    for user in users:
        if user["username"] == username and user["password"] == password:
            print("🎉 Login successful! \n")
            time.sleep(1)
            return True   # ✅ login success
    print("❌ Invalid username or password.")
    return False   # ❌ login failed

# ---------------- CLEAR FUNCTION ----------------
def clear_ter():
    os.system('cls' if os.name == 'nt' else 'clear')  # this is for clear terminal


# ---------------- INPUT WITH TIMEOUT ----------------
def input_with_timeout(prompt, timeout=30):
    user_input = [None]

    def get_input():
        try:
            user_input[0] = input(prompt)
        except EOFError:
            pass

    thread = threading.Thread(target=get_input)
    thread.daemon = True
    thread.start()
    thread.join(timeout)

    if thread.is_alive():  # time expired
        print("\n⏰ Time's up! No answer given.")
        return None
    return user_input[0]


# ---------------- MAIN MENU ----------------
def main_menu():
    while True:
        print_app_title()
        print("\n--- MENU ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose option (1/2/3): ")

        if choice == "1":
            register_user()
        elif choice == "2":
            if login_user():      # ✅ only start quiz if login successful
                start_quiz()
            else:
                continue
        elif choice == "3":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice, try again.")


# ---------------- QUIZ SYSTEM ----------------
bolly = "Bollywood.xlsx"
histry = "HISTORY.xlsx"
tech = "Technology.xlsx"
science = "Science.xlsx"
sport = "SPORTS.xlsx"

def get_question(data):
    row = data.sample().iloc[0]
    return row  # pick one random row


def print_question(row):
    print("\n❓ Question:", row["Question"])
    print(f"A. {row['Option A']}\nB. {row['Option B']}\nC. {row['Option C']}\nD. {row['Option D']}")


def check_answer(row, user_answer):
    correct = str(row["Answer"]).strip().upper()
    user = user_answer.strip().upper()
    if user == correct:
        print("✅ Correct!")
    else:
        option_text = row.get(f"Option {correct}", "Unknown")
        print(f"❌ Wrong! The correct answer is: {correct}. {option_text}")


def load_excel(path: str):
    if not os.path.exists(path):
        print(f"Quiz file not found: {path}")
        return None
    try:
        df = pd.read_excel(path)
    except Exception as e:
        print("Error loading quiz file:", e)
        return None

    required_cols = {"Question", "Option A", "Option B", "Option C", "Option D", "Answer"}
    if not required_cols.issubset(df.columns):
        print("Excel file must contain columns:", required_cols)
        return None

    df = df.dropna(subset=list(required_cols))
    if df.empty:
        print("No valid questions found in the quiz file.")
        return None
    return df


# ---------------- CHECK ANSWER ----------------
def check_answer(row, user_answer):
    correct = str(row["Answer"]).strip().upper()
    user = user_answer.strip().upper()
    if user == correct:
        print("✅ Correct!")
        return True
    else:
        option_text = row.get(f"Option {correct}", "Unknown")
        print(f"❌ Wrong! The correct answer is: {correct}. {option_text}")
        return False


# ---------------- QUIZ FUNCTION ----------------
def start_quiz():
    clear_ter()         # clear reg and login part 
    print_app_title()
    print("START YOUR QUIZ , 𝐵𝑒𝓈𝓉 𝑜𝒻 𝓁𝓊𝒸𝓀")
    print("Choose a quiz category:")
    print("1. Bollywood")
    print("2. History")
    print("3. Technology")
    print("4. Science")
    print("5. Sports")
    choice = input("Enter 1, 2, 3, 4, or 5: ").strip()

    category_name = ""  
    if choice == "1":
        df = load_excel(bolly)
        category_name = "🎬 Bollywood Questions"
    elif choice == "2":
        df = load_excel(histry)
        category_name = "📜 History Questions"
    elif choice == "3":
        df = load_excel(tech)
        category_name = "💻 Technology Questions"
    elif choice == "4":
        df = load_excel(science)
        category_name = "🔬 Science Questions"
    elif choice == "5":
        df = load_excel(sport)
        category_name = "⚽ Sports Questions"
    else:
        print("Invalid choice.")
        return

    if df is None:
        return

    # ---------------- Loop until user says NO ----------------
    while True:
        # ---------------- Choose number of questions ----------------
        while True:
            try:
                total_qs = int(input("How many questions do you want to practice (e.g., 10, 20, 30): "))
                if total_qs > 0:
                    break
                else:
                    print("Please enter a positive number.")
            except ValueError:
                print("❌ Invalid input. Please enter a number.")

        print(f"\n📌 You chose to practice {total_qs} questions.\n")
        time.sleep(1)

        # ---------------- Run the quiz ----------------
        asked = 0
        score = 0
        while asked < total_qs:
            que = get_question(df)
            clear_ter()
            print_app_title()
            print(category_name)
            print(f"Question {asked+1} of {total_qs}")

            # 🔹 Show timer message before question
            print("\n⏳ Your time is starting... 10 sec!\n")

            # print the question
            print_question(que)

            # ⏳ timer input (10 sec)
            user_answer = input_with_timeout("Your answer (A/B/C/D or Q to quit): ", timeout=10)

            if user_answer is None:   # timeout
                print("❌ You missed the question.")
                print("-" * 40)
                time.sleep(3)
                asked += 1
                continue

            user_answer = user_answer.strip()
            if user_answer.lower() == "q":
                print("Thank you for playing!")
                return   # exit completely

            if check_answer(que, user_answer):   # ✅ now returns True/False
                score += 1

            print("-" * 40)
            time.sleep(3)
            asked += 1

        # ---------------- Final score ----------------
        print(f"\n🏆 You got {score} out of {total_qs} correct!\n")   # ✅ now works

        # ---------------- Ask play again ----------------
        play_again = input("Do you want to play again? (Y/N): ").strip().lower()
        if play_again != "y":
            print("\n👋 Thank you for playing! Goodbye!\n")
            break




# ---------------- RUN PROGRAM ----------------
if __name__ == "__main__":
    main_menu()
