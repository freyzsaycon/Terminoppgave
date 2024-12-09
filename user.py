from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors, re, hashlib
import mysql.connector

app = Flask(__name__)

app.secret_key = 'secret'

mydb = mysql.connector.connect(
  host="10.2.3.79",
  user="frendon",
  password="MariaJa81",
  database="loginsystem"
)

print("Connection sucessful")


@app.route('/')
def Home():
    return render_template ('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode()).hexdigest()

        cursor = mydb.cursor(dictionary=True)
        cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (email, hash))
        
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['name'] = account['name']
            session['email'] = account['email']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect email/password!'

    return render_template('login.html', msg=msg)

@app.route('/login/logout')
def logout():

   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)

   return redirect(url_for('login'))
 

@app.route('/login/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
      
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

       
       
        print(f"Name: '{name}', Email: '{email}', Password: '{password}'")

    
        if not name or not password or not email:
            msg = 'Please fill out the form!'  
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'Username must contain only characters and numbers!'
        else:
            hash = password + app.secret_key
            hash = hashlib.sha1(hash.encode()).hexdigest()
            
            cursor = mydb.cursor(dictionary=True)
            try:
                cursor.execute('INSERT INTO accounts (email, password, name) VALUES (%s, %s, %s)', (email, hash, name))
                mydb.commit()
                msg = 'You have successfully registered!'
            except mysql.connector.Error as err:
                if err.errno == 1062: 
                    msg = 'An account with that email already exists!'
                else:
                    msg = f"An error occurred: {err}"

    return render_template('register.html', msg=msg)
 
@app.route('/login/home')
def home():
    if 'loggedin' in session:
        return render_template ('index_loggedin.html', name=session['name'])
    return redirect(url_for('login'))


@app.route('/login/profile')
def profile():
    if 'loggedin' in session:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)   