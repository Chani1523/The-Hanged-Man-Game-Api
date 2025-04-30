
import requests
from datetime import datetime, timedelta
from UserManager import UserManager
# יצירת סשן בקשות
session = requests.session()
# כתובת בסיס של ה-API
basic_url = "http://127.0.0.1:5000"
# ניהול המשתמשים (טעינה ועדכון של פרטי המשתמשים)
user_manager = UserManager()

logo = r"""	    _    _
       | |  | |
       | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
       |  __  |/ _' | '_ \ / _' | '_ ' _ \ / _' | '_ \
       | |  | | (_| | | | | (_| | | | | | | (_| | | | |
       |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                            __/ |
                           |___/
"""

# הגדרת זמן התחברות
time = datetime.utcnow()
#     # הוספת שעתיים
time_connected = datetime.utcnow() + timedelta(hours=2)

# דקורטור שנבדוק אם המשתמש מחובר לפני ביצוע פעולה מסוימת
def decorator(func):
    def wrapper(*args, **kwargs):
        timenow = datetime.utcnow() + timedelta(hours=2)

        try:
            # בדיקה אם העוגיה תקפה
            response = session.get(f"{basic_url}/get_cookie")
            if response.status_code == 200:
                # אם העוגיה תקפה, נמשיך להפעיל את הפונקציה
                time_elapsed = timenow - time_connected
                print(f"משתמש מחובר: זמן ההתחברות: {time_connected}")
                print(f"זמן שעבר מאז ההתחברות שלך: {time_elapsed}")
                return func(*args, **kwargs)
            else:
                print("עליך להתחבר מחדש.")
                login_or_register()
        except requests.RequestException as e:
            print(f"שגיאה בבדיקה של עוגיות: {e}")
            return login_or_register()
    return wrapper

# פונקציה המנהלת את ההתחברות או הרישום של המשתמש
def login_or_register():
    print(logo)
    print("ברוך הבא למשחק איש תלוי")
    while True:
        action = input("האם אתה רוצה להתחבר (הקלד 'התחבר') או להירשם (הקלד 'הרשם')? ").strip().lower()

        if action == 'התחבר':
            user_id = input("הכנס מספר מזהה: ").strip()
            password = input("הכנס סיסמה: ").strip()

            try:
                # ניסיון להתחבר עם מזהה וסיסמה
                response = session.post(f"{basic_url}/login", json={"user_id": user_id, "password": password})
                if response.status_code == 200:
                    user_data = response.json()
                    if "user_id" in user_data:
                        user = user_manager.load_users().get(user_data["user_id"])
                        if user:
                            print(f"שלום {user.name}, ברוך הבא למשחק!")
                            return user
                        else:
                            print("המשתמש לא נמצא במערכת.")
                    else:
                        print(f"תגובה לא צפויה מהשרת: {user_data}")
                else:
                    print("המשתמש או הסיסמה שגויים. נסה שוב.")
            except Exception as e:
                print(f"שגיאה במהלך התחברות: {e}")

        elif action == 'הרשם':
            name = input("הכנס את שמך: ").strip()
            user_id = input("הכנס מספר מזהה: ").strip()
            password = input("הכנס סיסמה: ").strip()

            try:
                # ניסיון לרשום משתמש חדש
                response = session.post(f"{basic_url}/register",
                                        json={"name": name, "user_id": user_id, "password": password})
                if response.status_code == 200:
                    user_data = response.json()
                    user = user_manager.load_users().get(user_data["user_id"])
                    if user:
                        print(f"שלום {user.name}, נרשמת בהצלחה!")
                        return user
                elif response.status_code == 409:
                    print("לא ניתן לרשום את המשתמש, המזהה קיים כבר.")
                else:
                    print(f"שגיאה ברישום: {response.text}")
            except Exception as e:
                print(f"שגיאה במהלך רישום: {e}")
        else:
            print("בחירה לא תקינה. נסה שוב.")

# פונקציה המתחילה משחק חדש עבור המשתמש
@decorator
def start_game(user):
    print("\nמתחילים משחק חדש...")
    num = int(input("הכנס מספר: "))

    def get_unique_word(user, num):
        tried_indices = set()
        while True:
            # בקשת מילה ייחודית מהשרת
            response = session.get(f"{basic_url}/get_word/{num}")
            if response.status_code != 200:
                print(f"שגיאה בקבלת מילה: {response.json().get('error')}")
                return None

            word = response.json().get("selected_word", "")
            if word not in tried_indices:
                tried_indices.add(num)
            if word and word not in user.words_played:  # אם המילה לא קיימת כבר
                return word
            num += 1
            if len(tried_indices) >= len(user.words_played):  # כל המילים כבר שוחקו
                print("כל המילים האפשריות כבר שוחקו.")
                return None
    word = get_unique_word(user, num)
    if not word:
        print("לא ניתן להמשיך במשחק.")
        return

    try:
        # קריאת תוכן של "הציורים"
        with open('the drawings', 'r') as file:
            content = file.read()
        sections = content.split('\n\n')
    except Exception as e:
        raise IOError(f"שגיאה בקריאת הקובץ: {e}")

    def creating_stripes(word):
        words = word.split(" ")
        dashes = ["-" * len(w) for w in words]
        return " ".join(dashes[::-1])

    def remove_spaces(s):
        return s.replace(" ", "")

    result = creating_stripes(word)
    print(result)

    numerr = 0
    new_word = result[::-1]
    err = False

    while numerr < 7 and remove_spaces(new_word) != remove_spaces(word):
        print(f" נתרו לך {7-numerr}  פסילות ")
        letter = input("הכנס אות: ")
        err = False
        # עיבוד התשובות של המשתמש
        for i, char in enumerate(word):
            if char == letter:
                new_word = new_word[:i] + letter + new_word[i + 1:]
                err = True

        if not err:
            numerr += 1
            print(sections[numerr - 1])
        else:
            print(new_word)

    if remove_spaces(new_word) == remove_spaces(word):
        print("המילה הושלמה! כל הכבוד ניצחתה!!!")
        response = session.post(f"{basic_url}/update_game_data", json={"user_id": user.user_id, "word": word, "won": True})
        if response.status_code == 200:
            updated_data = response.json()  # קבל נתונים מעודכנים מהשרת
            user.games_played = updated_data.get('games_played', user.games_played)
            user.wins = updated_data.get('wins', user.wins)
            user.words_played.update(updated_data.get('words_played', []))
        else:
            print(f"שגיאה בעדכון נתוני המשתמש: {response.json().get('error')}")

    else:
        print("עברתה את מספר השגיאות המותר.. אופס נפסלתה.")
        response = session.post(f"{basic_url}/update_game_data", json={"user_id": user.user_id, "word": word, "won": False})
        if response.status_code != 200:
            print(f"שגיאה בעדכון נתוני המשתמש: {response.json().get('error')}")
        if response.status_code == 200:
            updated_data = response.json()  # קבל נתונים מעודכנים מהשרת
            user.games_played = updated_data.get('games_played', user.games_played)
            user.wins = updated_data.get('wins', user.wins)
            user.words_played.update(updated_data.get('words_played', []))


@decorator
def view_history(user):
    response = session.post(f"{basic_url}/get_game_history", json={"user_id": user.user_id})
    if response.status_code == 200:
        # שליפת ההיסטוריה מתגובת ה-API
        history = response.json().get("game_history", [])

        # חישוב המשחקים והנצחונות מבוסס על ההיסטוריה שהתקבלה
        user.games_played = len(history)  # עדכון מספר המשחקים
        user.wins = sum(1 for game in history if game['won'])  # עדכון מספר הנצחונות

        if history:
            print("\nהיסטוריית המשחקים שלך:")
            for game in history:
                print(f"משחק: {game['word']} | ניצחון: {'כן' if game['won'] else 'לא'}")
            print(f"סך הכל משחקים: {user.games_played}")
            print(f"נצחונות: {user.wins}")
        else:
            print("אין היסטוריה לשחקן הזה.")
    else:
        print(f"שגיאה בהבאת ההיסטוריה: {response.json().get('error')}")


# תפריט המשתמש הראשי המאפשר בחירה בין פונקציות
@decorator
def user_menu(user):
    while True:
        user_message = """
          שלום! אנא הכנס בחירה:
          1. התחל משחק חדש
          2. צפה בהיסטורית משחקים
          3. התנתקות
          4. יציאה מהתוכנית
          """
        try:
            choice = int(input(user_message))
        except ValueError:
            print("בחירה לא תקינה, אנא הכנס מספר בין 1 ל-4.")
            continue

        if not 1 <= choice <= 4:
            print("בחירה לא תקינה, אנא נסה שוב.")
            continue

        if choice == 3:
            print("התנתקות... נתראה בפעם הבאה!")
            user = None  # איפוס המשתמש כדי לחזור למסך ההתחברות
            break
        elif choice == 4:
            print("יציאה מהתוכנית... להתראות!")
            exit()

        try:
            # מיפוי בחירות לפונקציות
            functions = [start_game, view_history]
            func = functions[choice - 1]
            func(user)
        except IndexError:
            print("שגיאה במיפוי הפונקציות. נסה שוב.")

# פונקציה ראשית להפעלת התוכנית
def main():
    user = None

    while True:
        if not user:
            user = login_or_register()
        else:
            user = user_menu(user)


if __name__ == "__main__":
    main()
