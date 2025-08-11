from flask import Flask, render_template, request, redirect, url_for, session
from simulator import run_simulation, stop_simulation
import threading, os, json

app = Flask(__name__)
app.secret_key = '9fa82d7a9bcb4dc1ae6b48f9ae12b394'

@app.route("/")
def homepage():
    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        gmail = request.form.get('gmail')
        password = request.form.get('password')

        if gmail == 'admin@gmail.com' and password == '1234':
            session['user'] = gmail
            # start simulator in background (10 entries)
            threading.Thread(target=run_simulation, kwargs={'entry_limit': 100}, daemon=True).start()
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Access form data (currently no persistent store)
        gmail = request.form.get('gmail')
        password = request.form.get('password')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/temperature')
def get_latest_temperature():
    try:
        if not os.path.exists("data.json"):
            return {"temperature": "--", "status": "safe", "safe_temperature": 85, "run_time": 0.0, "max_run_time": 4}

        with open("data.json", "r") as f:
            lines = f.readlines()
            if not lines:
                return {"temperature": "--", "status": "safe", "safe_temperature": 85, "run_time": 0.0, "max_run_time": 4}

            last_entry = json.loads(lines[-1])
            temp = last_entry.get("temperature", "--")
            status = last_entry.get("status", "safe")
            run_time = len(lines) * 5 / 3600  # approximate hours for demo

            return {
                "temperature": temp,
                "status": status,
                "safe_temperature": 85,
                "run_time": run_time,
                "max_run_time": 4
            }

    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    stop_simulation()
    session.pop('user', None)
    return redirect(url_for('homepage'))

if __name__ == '__main__':
    app.run(debug=True)
