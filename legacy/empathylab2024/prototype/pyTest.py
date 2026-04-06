from flask import Flask, render_template, request
from pyCode import runThis
from summerCode import chatgpt_characterModified as ai

app = Flask(__name__)

@app.route('/')
def index():
    runThis()
    return render_template("htmlTest.html")

@app.route('/run_script', methods=['POST'])
def run_script():
    print("hello world")
    return render_template("htmlTest2.html")

@app.route('/test_ai', methods=['POST'])
def run_ai():
    ai.run()
    return render_template("htmlTest2.html")

if __name__ == "__main__":
    app.run(debug=True)
