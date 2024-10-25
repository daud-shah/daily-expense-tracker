from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",       # Your MySQL username
        password="",       # Your MySQL password
        database="daily_expenses_db"  # Your database name
    )
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get data from the form
        user_name = request.form['name']
        date = request.form['date']
        breakfast = float(request.form['breakfast'])
        lunch = float(request.form['lunch'])
        dinner = float(request.form['dinner'])
        extra = float(request.form['extra'])
        travel = float(request.form['travel'])
        total = breakfast + lunch + dinner + extra + travel
        
        # Save to database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (user_name, date, breakfast, lunch, dinner, extra, travel, total)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (user_name, date, breakfast, lunch, dinner, extra, travel, total))
        conn.commit()
        cursor.close()
        conn.close()

        return render_template('index.html', success=True)  # Redirect to the same page with a success message

    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

