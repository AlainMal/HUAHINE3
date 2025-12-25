from flask import Flask
import subprocess
import sys
import os

app = Flask(__name__)

@app.route("/launch-huahine")
def launch_huahine():
    script_path = os.path.join(os.getcwd(), "HUAHINE.py")
    subprocess.Popen([sys.executable, script_path])
    return "HUAHINE launched"

if __name__ == "__main__":
    app.run(port=5002)
