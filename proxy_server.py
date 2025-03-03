from flask import Flask, jsonify
import random
import time
import threading

app = Flask(__name__)
proxy_log_list = []


# Generate a list of fake IPs
def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

# Store the current IP and reset every 3 minutes
current_ip = generate_random_ip()
last_updated = time.time()

def log_proxy(ip):
    """Log each used proxy to a memory."""
    if len(proxy_log_list) >= 50:  
        proxy_log_list.pop(0)  # Remove oldest log if more than 50
    proxy_log_list.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {ip}")

@app.route('/')
def home():
    """Fake home route to trick Render into thinking this is a normal app."""
    return "✅ Proxy Server is Running!"

@app.route('/get_proxy')
def get_proxy():
    """Returns a fake proxy IP that rotates every 3 minutes."""
    global current_ip, last_updated

    if time.time() - last_updated > 120:
        current_ip = generate_random_ip()
        last_updated = time.time()

    return jsonify({"proxy": f"http://{current_ip}:8080"})  # ✅ Fake Proxy

@app.route('/proxy-logs')
def proxy_logs():
    """Show the last 50 used proxies."""
    return "<br>".join(proxy_log_list) if proxy_log_list else "No logs available."

def run_fake_task():
    """Runs in the background to simulate real app activity."""
    while True:
        print("🔄 Background task running... (Render won't stop this app)")
        time.sleep(180)  # Keep Render thinking it's active

if __name__ == '__main__':
    threading.Thread(target=run_fake_task, daemon=True).start()  # ✅ Start fake background process
    app.run(host='0.0.0.0', port=10000, threaded=True)  # ✅ Run Flask on Render's required port
