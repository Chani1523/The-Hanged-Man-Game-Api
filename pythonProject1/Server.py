from flask import Flask, request, jsonify, abort, make_response
from flask_cors import CORS
import random
from UserManager import UserManager
app = Flask(__name__)  # יצירת מופע מהשרת

CORS(app, supports_credentials=True)


# יצירת מופע של UserManager
user_manager = UserManager('users.json')

# תקלה כללית
@app.errorhandler(Exception)
def handle_exception(e):
    """
      טיפול בתקלות כלליות בשרת.
      :param e: שגיאה.
      """
    response = {
        "error": str(e),
        "description": "תקלה כללית בשרת, נסה מאוחר יותר."
    }
    return jsonify(response), 500


# API להתחברות
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user_id = data.get('user_id')
    password = data.get('password')

    if not user_id or not password:
        return jsonify({"error": "שם משתמש וסיסמה נדרשים."}), 400

    user = user_manager.users.get(user_id)
    if not user or user.password != password:
        return jsonify({"error": "שם משתמש או סיסמה שגויים."}), 401

    response = make_response(jsonify({"message": "התחברות הצליחה!", "name": user.name, "user_id": user.user_id}), 200)
    # יצירת עוגייה למשתמש
    response.set_cookie(
        "user",
        user.user_id,
        max_age=120,  # תקף ל-10 דקות
        httponly=True,
        secure=False,
        samesite='Lax'
    )

    return response


# API לרישום
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user_id = data.get('user_id')
    password = data.get('password')
    name = data.get('name')

    if not user_id or not password or not name:
        return jsonify({"error": "כל השדות נדרשים."}), 400

    # בדיקה אם המשתמש קיים
    user = user_manager.users.get(user_id)
    if user:
        return jsonify({"error": "משתמש כבר קיים."}), 409

    # יצירת משתמש חדש ושמירה בקובץ
    user = user_manager.register_user(name, user_id, password)

    # טוען את המשתמשים מחדש אחרי השמירה
    user_manager.load_users()

    if user:
        response = make_response(jsonify({"message": "הרשמה הצליחה!", "user_id": user_id}), 200)
        # יצירת עוגייה למשתמש החדש
        response.set_cookie(
            "user",
            user.user_id,
            max_age=600,
            httponly=True,
            secure=False,
            samesite='Lax'
        )

        return response
    else:
        return jsonify({"error": "לא ניתן להירשם."}), 500

# הגרלת  מילה

with open('the text.txt', 'r', encoding='utf-8') as file:
    words = file.read().splitlines()
    random.shuffle(words)


@app.route('/get_word/<int:num>', methods=['GET'])
def get_word(num):
    if not words:
        return jsonify({"error": "קובץ המילים ריק או לא נטען כראוי"}), 500

    # שליפה מעגלית של מילה לפי המספר שהוזן
    c_index = num % len(words)
    selected_word = words[c_index]
    return jsonify({"selected_word": selected_word})





# בדיקת עוגיה
@app.route('/get_cookie', methods=['GET'])
def get_cookie_func():
    user_name = request.cookies.get('user')
    if user_name:
        return jsonify({"message": f"משתמש מחובר: {user_name}"}), 200
    return jsonify({"error": "עוגיה לא נמצאה או פגה."}), 401






# API להוספת נתוני המשחק לאחר המשחק
@app.route('/update_game_data', methods=['POST'])
def update_game_data():
    data = request.json
    user_id = data.get('user_id')
    word = data.get('word')
    won = data.get('won')

    if not user_id or word is None or won is None:
        return jsonify({"error": "נדרשים פרטי משתמש, מילה ותוצאה."}), 400

    user = user_manager.users.get(user_id)
    if not user:
        return jsonify({"error": "משתמש לא נמצא."}), 404

    # עדכון נתוני המשחק

    user.increment_games_played()
    if won:
        user.increment_wins()  # אם ניצח, עדכון מספר הנצחונות
        user.words_played.add(word)
    # שמירה בקובץ
    user_manager.save_users()

    return jsonify({
        "message": "נתוני המשחק עודכנו בהצלחה!",
        "games_played": user.games_played,
        "wins": user.wins,
        "words_played": list(user.words_played)
    }), 200

# היסטורית משחקים
@app.route('/get_game_history', methods=['POST'])
def get_game_history():
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "מזהה משתמש נדרש."}), 400

    user = user_manager.users.get(user_id)
    if user:
        # יצירת היסטוריית משחקים על בסיס words_played
        history = [{"word": word, "won": True} for word in user.words_played]

        # אם יש פחות משחקים ממה שכתוב ב-games_played, נוסיף משחקים ללא מילים
        while len(history) < user.games_played:
            history.append({"word": None, "won": False})

        return jsonify({"game_history": history}), 200

    return jsonify({"error": "משתמש לא נמצא."}), 404


if __name__ == "__main__":
    app.run(debug=True)
