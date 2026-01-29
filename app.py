from flask import Flask, render_template, request
import subprocess
import sys
import webbrowser
import os  
from threading import Timer

app = Flask(__name__)

# File constants
DATA_FILE = "user_config.txt"
BOT_SCRIPT = "telegram_manager.py"

def open_browser():
    """Opens the default web browser to the correct URL"""
    webbrowser.open_new("http://127.0.0.1:5000")

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit_data():
    if request.method == 'POST':
        try:
            lines = [
                f"{'API_KEY':<25}\t: {request.form['api_key']}",
                f"{'USER_ID':<25}\t: {request.form['user_id']}",
                f"{'PASSWORD':<25}\t: {request.form['password']}",
                f"{'ROLES':<25}\t: {request.form['roles']}",
                f"{'INPUT_RESUME_PATH':<25}\t: {request.form['resume_path']}",
                f"{'YEARS':<25}\t: {request.form['years']}",
                f"{'MONTHS':<25}\t: {request.form['months']}",
                f"{'LINKS':<25}\t: {request.form['links']}",
                f"{'TELEGRAM_TOKEN':<25}\t: {request.form['telegram_token']}",
                f"{'CHAT_ID':<25}\t: {request.form['chat_id']}",
            ]
            
            file_content = "\n".join(lines)

            with open(DATA_FILE, "w") as file:
                file.write(file_content)
            
            subprocess.Popen([sys.executable, BOT_SCRIPT])

            return f"""
            <div style="font-family: sans-serif; text-align: center; margin-top: 50px;">
                <h1>✅ Configuration Saved!</h1>
                <p>Data written to <strong>{DATA_FILE}</strong> with all required keys.</p>
                <p>Bot is running in the background.</p>
                <a href='/'>Go back</a>
            </div>
            """
        
        except Exception as e:
            return f"<h1>Error: {e}</h1>"

if __name__ == '__main__':
    # This check prevents the browser from opening twice
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        Timer(1, open_browser).start()
        
    app.run(debug=True)