from flask import Flask, render_template

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

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
