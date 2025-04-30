# פרויקט המן תלוי

זהו פרויקט של משחק **המן תלוי** מבוסס תקשורת בין צד שרת וצד לקוח, עם דגש על ניהול זמן משחק, שמירת תוצאות, ועבודה עם Cookies.

## 🧱 מבנה הפרויקט

- **צד שרת**:
  - מספק API למשחק (שליפת מילה, ניחוש אות, שמירת תוצאה).
  - מגביל את משך המשחק באמצעות עוגייה (Cookie) שנשלחת ללקוח.
  - שומר נתונים (כגון תוצאות משתמשים) בקובץ JSON.

- **צד לקוח**:
  - סקריפט פשוט ששולח בקשות HTTP לשרת (באמצעות `requests` בפייתון ).
  - שומר את העוגייה שקיבל מהשרת כדי לעקוב אחרי זמן המשחק.
  - מציג את התגובה שהתקבלה מהשרת בצורה טקסטואלית.

## 🛠 טכנולוגיות

- צד שרת: Python + Flask
- צד לקוח: Python (`requests`) 
- אחסון נתונים: קובץ `users.json`

## 📦 התקנה והרצה

```bash
# שלב 1 - שכפול הריפו
git clone https://github.com/your-username/hangman-project.git
cd hangman-project

# שלב 2 - הרצת צד השרת
cd server
pip install -r requirements.txt
python server.py

# שלב 3 - הרצת צד הלקוח

python game.py
