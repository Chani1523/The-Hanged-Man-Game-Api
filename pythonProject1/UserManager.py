import json
from User import User
DEFAULT_USER_FILE = "users.json"

class UserManager:
    def __init__(self, filename=DEFAULT_USER_FILE):
        """
               אתחול מחלקת מנהל משתמשים.
               :param filename: שם הקובץ שבו נשמרים הנתונים.
               """
        self.filename = filename
        self.users = self.load_users()

    def load_users(self):
        #  טוען את המשתמשים מהקובץ JSON.
        #         :return: מילון של משתמשים.
        try:
            with open(DEFAULT_USER_FILE, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return {
                    user_data["user_id"]: User(
                        name=user_data["name"],
                        user_id=user_data["user_id"],
                        password=user_data["password"],
                        games_played=user_data.get("games_played", 0),
                        # words_played=user_data.get("words_played", set()),
                        words_played=set(user_data.get("words_played", [])),
                        wins=user_data.get("wins", 0)
                    ) for user_data in data.values()
                }
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            print("שגיאה: קובץ המשתמשים אינו בפורמט JSON תקין.")
            return {}
    def save_users(self):
        #  שומר את נתוני המשתמשים לקובץ JSON.

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump({user.user_id: user.to_dict() for user in self.users.values()}, file, ensure_ascii=False,
                      indent=4)

    def register_user(self, name, user_id, password):
        # רושם משתמש חדש אם המזהה לא קיים
        if user_id in self.users:
            print("מספר משתמש קיים בחר אחר")
            return None
        user = User(name, user_id, password)
        self.users[user_id] = user
        self.save_users()  # שמירה אחרי רישום
        return user

    def update_user_after_game(self, user, word, won):
    #עדכון נתוני המשתמש לאחר משחק
        user.add_word_played(word)  # הוספת המילה לרשימה
        user.increment_games_played()  # עדכון מספר המשחקים
        if won:  # אם המשתמש ניצח
            user.increment_wins()
        self.save_users()  # שמירת הנתונים המעודכנים
