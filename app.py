from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Professionals')
def professionals():
    return render_template('professionals.html')

@app.route('/Articles')
def articles():
    return render_template('articles.html')

@app.route('/Login')
def login():
    return render_template('login.html')

@app.route('/Signup')
def signup():
    return render_template('signup.html')

@app.route('/Terms-conditions')
def terms():
    return render_template('terms.html')


# Connect to the MySQL database
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="0207",
            database="psychobot"
        )
        print("Connected to MySQL database successfully")
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to MySQL database:", err)

# Run the app
if __name__ == '__main__':
    # Connect to the database
    db_connection = connect_to_database()
    app.run(debug=True)