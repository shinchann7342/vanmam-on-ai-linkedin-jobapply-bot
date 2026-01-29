import time
import requests
import subprocess
import sys
import os

# --- 1. Load Configuration ---
try:
    with open("user_config.txt", "r") as f:
        lines = f.readlines()
        
    TELEGRAM_TOKEN = lines[8].split('\t:')[-1].strip()
    CHAT_ID        = lines[9].split('\t:')[-1].strip()
except Exception as e:
    print(f"Config Error: {e}")
    TELEGRAM_TOKEN = None
    CHAT_ID = None

# --- 2. Helper Functions ---

def send_message(message):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except:
        pass

def start_bot():
    """Starts the job_apply.py script as a separate subprocess."""
    # using sys.executable ensures we use the same python interpreter
    return subprocess.Popen([sys.executable, "job_apply.py"])

# --- 3. Main Supervisor Loop ---

def main():
    print("==================================================")
    print("                 BOT STARTED                      ")
    print("==================================================")

    # If Telegram is not configured, just run the bot normally and exit the manager
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print(">> No Telegram Token found. Running in passthrough mode.")
        subprocess.call([sys.executable, "job_apply.py"])
        return

    # Start the worker bot
    bot_process = start_bot()
    print(">> Job Bot Launched.")
    send_message("🤖 Manager: Bot started. Send 'End' to stop or 'Restart' to reboot.")

    last_update_id = None
    startup_time = time.time()

    # Loop to monitor Telegram commands
    while True:
        try:
            # Check if the child process (Job Bot) has crashed or finished
            if bot_process.poll() is not None:
                print(">> Job Bot has stopped unexpectedly or finished.")
                send_message("⚠️ Alert: The Job Bot process has stopped.")
                # We exit the manager so run.bat can handle the error/pause
                sys.exit(bot_process.returncode)

            # Poll Telegram for updates
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
            params = {'timeout': 5} # Short polling timeout
            if last_update_id:
                params['offset'] = last_update_id + 1
            
            resp = requests.get(url, params=params)
            data = resp.json()
            
            if 'result' in data:
                for update in data['result']:
                    last_update_id = update['update_id']
                    
                    if 'message' in update and 'text' in update['message']:
                        # Ignore old messages
                        if update['message'].get('date', 0) < startup_time:
                            continue

                        text = update['message']['text'].strip().lower()
                        uid = str(update['message']['chat']['id'])

                        # Security Check
                        if uid == CHAT_ID:
                            if text == "end":
                                print(">> Received END command.")
                                send_message("🛑 Manager: Halting execution. Goodbye.")
                                bot_process.terminate() # Kill the worker
                                sys.exit(0) # Exit the manager
                                
                            elif text == "restart":
                                print(">> Received RESTART command.")
                                send_message("🔄 Manager: Restarting Job Bot...")
                                bot_process.terminate() # Kill the worker
                                bot_process.wait()      # Ensure it's dead
                                bot_process = start_bot() # Start a new one
                                send_message("✅ Manager: Job Bot Rebooted.")

            time.sleep(2)

        except KeyboardInterrupt:
            bot_process.terminate()
            break
        except Exception as e:
            print(f"Manager Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()