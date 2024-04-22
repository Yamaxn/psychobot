from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector 
import requests, rasa


# Define the Rasa server URL
RASA_SERVER_URL = 'http://0.0.0.0:5005/webhooks/rest/webhook'

app = Flask(__name__)
app.secret_key = 'cheesecakefactory'  # Change this to a random string for security

# Define routes
@app.route('/')

def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.json['message']
    # Send the user's message to the Rasa server
    response = send_message_to_rasa(message)
    # Extract the chatbot response from the Rasa server response
    if response:
        bot_response = response[0].get('text')
    else:
        bot_response = 'Error: No response from Rasa server'
 
    # Save the message to the database
    user_id = session.get('user_id') # Assuming user is logged in and user_id is stored in session
    save_to_database(user_id, message)
 
    # Return the chatbot response to the frontend
    return jsonify({'response': bot_response})

def send_message_to_rasa(message):
    # Prepare the request data
    data = {'message': message}
    # Send the request to the Rasa server
    try:
        rasa_response = requests.post(RASA_SERVER_URL, json=data)
        rasa_response.raise_for_status()
        return rasa_response.json()
    except requests.exceptions.RequestException as e:
        print('Error sending message to Rasa server:', e)
        return None

def save_to_database(user_id, message):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO chat_logs (user_id, message) VALUES (%s, %s)", (user_id, message))
        connection.commit()
        cursor.close()
        connection.close()
        print("Message saved to database successfully")
    except mysql.connector.Error as err:
        print("Error saving message to database:", err)
        
@app.route('/Professionals')
def professionals():
    return render_template('professionals.html')

@app.route('/Articles')
def articles():
    return render_template('articles.html')

@app.route('/Login')
def login_page():
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


# Route to handle the signup form submission
@app.route('/signup', methods=['POST'])
def handle_signup():
    # Connect to the database
    db_connection = connect_to_database()

    # Retrieve form data
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    # Validation (you can add more validation as needed)
    if password != confirm_password:
        # Passwords don't match, render signup form with error message
        return render_template('signup.html', error="Passwords do not match")

    # Insert user data into the database
    cursor = db_connection.cursor()
    try:
        cursor.execute("INSERT INTO user_details (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        db_connection.commit()
        print("User registered successfully")
        # Redirect to the login page
        return redirect(url_for('login'))
    except mysql.connector.Error as err:
        print("Error inserting user data:", err)
        # Render signup form with error message
        return render_template('signup.html', error="An error occurred. Please try again later.")

@app.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']
        
        # Connect to the database
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor(dictionary=True)
            
            # Query the database for the user
            query = "SELECT * FROM user_details WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            
            # Verify user credentials
            if user and user['password'] == password:
                # Set session variables
                session['user_id'] = user['user_id']
                session['username'] = user['username']
                
                # Redirect to the home page or any other page
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid username or password. Please try again.'
                return render_template('login.html', error=error)
        else:
            error = 'Database connection error. Please try again later.'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')
    
# Route to handle the logout
@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    # Redirect the user to the login page
    return redirect(url_for('login'))

# Secure dashboard route
@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'user_id' in session:
        username = session['username']
        return render_template('dashboard.html', username=username)
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('login'))
    
# Run the app
if __name__ == '__main__':
    # Connect to the database
    db_connection = connect_to_database()
    app.run(debug=True)