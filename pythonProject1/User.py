class User:
    def __init__(self, name, user_id, password, games_played=0, words_played=None, wins=0):
        """
                אתחול אובייקט משתמש.
                """
        self.name = name
        self.user_id = user_id
        self.password = password
        self.games_played = games_played
        # self.words_played = words_played if words_played is not None else set()
        self.words_played = set(words_played) if words_played else set()
        self.wins = wins



    def increment_games_played(self):
        """הגדלת מספר המשחקים ב-1"""
        self.games_played += 1

    def add_word_played(self, word):
        """הוספת מילה למשחקים הקודמים אם היא לא כבר ברשימה"""
        self.words_played.add(word)

    def increment_wins(self):
        """הגדלת מספר הניצחונות ב-1"""
        self.wins += 1


    def to_dict(self):
        """הפיכת אובייקט המשתמש לדיקשנרי שניתן לשמור ב-JSON"""
        return {
            "name": self.name,
            "user_id": self.user_id,
            "password": self.password,
            "games_played": self.games_played,
            "words_played": list(self.words_played),
            "wins": self.wins
        }

    def update_history(self, game_history):
        """עדכון היסטוריית המשחקים מהשרת"""
        self.history = game_history